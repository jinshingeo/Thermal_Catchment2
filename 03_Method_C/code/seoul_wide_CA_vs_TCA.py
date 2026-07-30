"""
서울 전역 TCA vs CA 산출 (지하철역 367개 기준)
================================================
- CA(Classic Catchment): Hard Cut 없음, 시간대 무관, 1회만 계산
- TCA(Thermal Catchment): Hard Cut 적용, 06~19시 x [38, 42.7]도 임계값 조합
- 그래프 복사 없이 callable weight function으로 처리(성능)
"""
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree

WALK_SPEED = 4.5 * 1000 / 3600
TIME_BUDGET = 15 * 60
THRESHOLDS = [38.0, 42.7]
HOURS = list(range(6, 20))

NET_PATH = "/Users/jin/석사논문/Thermal_Catchment/data/network/seoul_walk_network.graphml"
UTCI_GPKG = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg"
STATIONS_GPKG = "/Users/jin/석사논문/Thermal_Catchment/data/facilities/seoul_subway_stations.gpkg"
OUT_CSV = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-30_seoul_stations_CA_vs_TCA.csv"

t0 = time.time()
print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
for u, v, k, d in G.edges(keys=True, data=True):
    d['travel_time'] = float(d.get('length', 0)) / WALK_SPEED
print(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}  ({time.time()-t0:.1f}s)")

print("역 데이터 로드 및 네트워크 스냅...")
stations = gpd.read_file(STATIONS_GPKG)
node_ids = list(G.nodes())
node_xy = np.array([[float(G.nodes[n]['x']), float(G.nodes[n]['y'])] for n in node_ids])
tree = cKDTree(node_xy)
st_xy = np.array([[geom.x, geom.y] for geom in stations.geometry])
_, idx = tree.query(st_xy)
stations['net_node'] = [node_ids[i] for i in idx]
stations = stations.drop_duplicates(subset='net_node').reset_index(drop=True)
print(f"  역 {len(stations)}개 (중복 스냅 제거 후)")

print("UTCI 링크 데이터 로드...")
utci_gdf = gpd.read_file(UTCI_GPKG)
utci_gdf['u'] = utci_gdf['u'].astype(str)
utci_gdf['v'] = utci_gdf['v'].astype(str)
print(f"  ({time.time()-t0:.1f}s)")

# ---------- 1. CA (Hard Cut 없음, 1회) ----------
print("\nCA(무보정) 계산 중...")
ca_results = {}
for _, row in stations.iterrows():
    origin = row['net_node']
    lengths = nx.single_source_dijkstra_path_length(
        G, origin, cutoff=TIME_BUDGET, weight='travel_time')
    ca_results[origin] = len(lengths)
print(f"  완료 ({time.time()-t0:.1f}s)")

# ---------- 2. TCA (시간대 x 임계값) ----------
rows = []
for hour in HOURS:
    col = f'UTCI_{hour:02d}'
    if col not in utci_gdf.columns:
        continue
    utci_lookup = {}
    for _, r in utci_gdf.dropna(subset=[col]).iterrows():
        u, v, val = r['u'], r['v'], r[col]
        utci_lookup[(u, v)] = val
        utci_lookup[(v, u)] = val

    for thr in THRESHOLDS:
        def weight(u, v, d, _lookup=utci_lookup, _thr=thr):
            # MultiDiGraph: d는 병렬 엣지 {key: attrs} 딕셔너리
            best = None
            val = _lookup.get((u, v))
            for _, attrs in d.items():
                if val is not None and val >= _thr:
                    continue
                w = attrs['travel_time']
                if best is None or w < best:
                    best = w
            return best

        t1 = time.time()
        for _, row in stations.iterrows():
            origin = row['net_node']
            lengths = nx.single_source_dijkstra_path_length(
                G, origin, cutoff=TIME_BUDGET, weight=weight)
            n_tca = len(lengths)
            n_ca = ca_results[origin]
            rows.append({
                'station': row['name'], 'net_node': origin, 'hour': hour,
                'threshold': thr, 'nodes_CA': n_ca, 'nodes_TCA': n_tca,
                'reduction_pct': round((n_ca - n_tca) / max(n_ca, 1) * 100, 2),
            })
        print(f"  {hour:02d}시 x {thr}도 완료 ({time.time()-t1:.1f}s, 누적 {time.time()-t0:.1f}s)")

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
print(f"\n저장: {OUT_CSV} ({len(df)} rows)")
