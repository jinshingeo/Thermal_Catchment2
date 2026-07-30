"""
서울 전역 집계구 기반 컨투어 메저 (CA vs TCA)
================================================
출발지: 서울 집계구 19,153개 중심점
기회(opportunity): 지하철역 367개 + 버스정류장(GTFS, 서울) 10,916개
시간대: 08시(출근) / 18시(퇴근)
임계값: 38.0 / 42.7
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
JIBGYEGU_SHP = "/Users/jin/석사논문/Thermal_Catchment/data/_tmp_boundary/집계구.shp"
SUBWAY_GPKG = "/Users/jin/석사논문/Thermal_Catchment/data/facilities/seoul_subway_stations.gpkg"
GTFS_STOPS = "/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt"
OUT_CSV = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-30_seoul_jibgyegu_contour_CA_vs_TCA_allhours.csv"

t0 = time.time()
print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
for u, v, k, d in G.edges(keys=True, data=True):
    d['travel_time'] = float(d.get('length', 0)) / WALK_SPEED
print(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}  ({time.time()-t0:.1f}s)")

node_ids = list(G.nodes())
node_xy = np.array([[float(G.nodes[n]['x']), float(G.nodes[n]['y'])] for n in node_ids])
tree = cKDTree(node_xy)

print("집계구 로드 및 중심점 스냅...")
jbg = gpd.read_file(JIBGYEGU_SHP)
jbg = jbg.set_crs(5179, allow_override=True)
centroid_5179 = jbg.geometry.centroid
jbg = jbg.to_crs(4326)
jbg['centroid'] = centroid_5179.to_crs(4326)
c_xy = np.array([[p.x, p.y] for p in jbg['centroid']])
_, idx = tree.query(c_xy)
jbg['net_node'] = [node_ids[i] for i in idx]
origins = jbg.drop_duplicates(subset='net_node')[['TOT_REG_CD', 'ADM_NM', 'net_node']].reset_index(drop=True)
print(f"  집계구 {len(jbg)}개 -> 중복제거 후 출발지 {len(origins)}개  ({time.time()-t0:.1f}s)")

print("기회(지하철역+버스정류장) 로드 및 스냅...")
subway = gpd.read_file(SUBWAY_GPKG)[['name', 'geometry']]
subway['type'] = 'subway'

bus = pd.read_csv(GTFS_STOPS)
bus['region'] = bus['stop_id'].str.split('_').str[1]
bus = bus[bus['region'] == '1100'].copy()
bus_gdf = gpd.GeoDataFrame(
    bus[['stop_name']].rename(columns={'stop_name': 'name'}),
    geometry=gpd.points_from_xy(bus['stop_lon'], bus['stop_lat']), crs=4326)
bus_gdf['type'] = 'bus'

opp = pd.concat([subway, bus_gdf], ignore_index=True)
opp_xy = np.array([[p.x, p.y] for p in opp.geometry])
_, idx = tree.query(opp_xy)
opp['net_node'] = [node_ids[i] for i in idx]
opportunity_nodes = set(opp['net_node'].unique())
print(f"  지하철역 {len(subway)} + 버스정류장 {len(bus_gdf)} -> 스냅된 기회 노드 {len(opportunity_nodes)}개  ({time.time()-t0:.1f}s)")

print("UTCI 링크 데이터 로드...")
utci_gdf = gpd.read_file(UTCI_GPKG)
utci_gdf['u'] = utci_gdf['u'].astype(str)
utci_gdf['v'] = utci_gdf['v'].astype(str)
print(f"  ({time.time()-t0:.1f}s)")

# ---------- 1. CA (Hard Cut 없음, 1회) ----------
print("\nCA(무보정) 계산 중...")
ca_results = {}
t1 = time.time()
for origin in origins['net_node']:
    lengths = nx.single_source_dijkstra_path_length(
        G, origin, cutoff=TIME_BUDGET, weight='travel_time')
    reachable = set(lengths.keys())
    ca_results[origin] = len(reachable & opportunity_nodes)
print(f"  완료 ({time.time()-t1:.1f}s, 누적 {time.time()-t0:.1f}s)")

# ---------- 2. TCA (시간대 x 임계값) ----------
rows = []
for hour in HOURS:
    col = f'UTCI_{hour:02d}'
    utci_lookup = {}
    for _, r in utci_gdf.dropna(subset=[col]).iterrows():
        u, v, val = r['u'], r['v'], r[col]
        utci_lookup[(u, v)] = val
        utci_lookup[(v, u)] = val

    for thr in THRESHOLDS:
        def weight(u, v, d, _lookup=utci_lookup, _thr=thr):
            best = None
            val = _lookup.get((u, v))
            for _, attrs in d.items():
                if val is not None and val >= _thr:
                    continue
                w = attrs['travel_time']
                if best is None or w < best:
                    best = w
            return best

        t2 = time.time()
        for _, row in origins.iterrows():
            origin = row['net_node']
            lengths = nx.single_source_dijkstra_path_length(
                G, origin, cutoff=TIME_BUDGET, weight=weight)
            reachable = set(lengths.keys())
            n_tca = len(reachable & opportunity_nodes)
            n_ca = ca_results[origin]
            rows.append({
                'TOT_REG_CD': row['TOT_REG_CD'], 'ADM_NM': row['ADM_NM'],
                'net_node': origin, 'hour': hour, 'threshold': thr,
                'opp_CA': n_ca, 'opp_TCA': n_tca,
                'reduction_pct': round((n_ca - n_tca) / max(n_ca, 1) * 100, 2),
            })
        print(f"  {hour:02d}시 x {thr}도 완료 ({time.time()-t2:.1f}s, 누적 {time.time()-t0:.1f}s)")

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
print(f"\n저장: {OUT_CSV} ({len(df)} rows)")
