"""
서울 전역 — API 네트워크 "네이티브" 컨투어 메저 (CA vs SEAR)
================================================================
seoul_wide_api_network_contour.py는 OSM 링크 UTCI를 최근접매칭으로 상속했다.
이 스크립트는 20_api_network_native_tmrt_utci.py가 API 링크 지오메트리에
직접 zonal 집계·계산한 Tmrt/UTCI(상속 아님)를 사용해 동일한 컨투어 메저를
다시 계산한다. 출발지/기회/파라미터는 seoul_wide_api_network_contour.py와
완전히 동일 — 비교 목적.
"""
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree

WALK_SPEED = 4.0 * 1000 / 3600  # Brode et al.(2012) p.483
TIME_BUDGET = 15 * 60
THRESHOLDS = [38.0, 42.4]
HOURS = list(range(6, 20))
TARGET_CRS = 'EPSG:5186'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
NATIVE_GPKG = f'{PROJ}/03_Method_C/results/2026-08-11_link_tmrt_utci_seoul_5m_api_network_native.gpkg'
JIBGYEGU_SHP = f'{PROJ}/data/_tmp_boundary/집계구.shp'
SUBWAY_GPKG = f'{PROJ}/data/facilities/seoul_subway_stations.gpkg'
GTFS_STOPS = '/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt'
OUT_CSV = f'{PROJ}/03_Method_C/results/2026-08-11_seoul_wide_api_network_native_contour_CA_vs_SEAR_allhours.csv'

t0 = time.time()


def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)


# ── 1. API 네트워크(네이티브 Tmrt/UTCI 포함) 로드 ────────────────────────────
log("네이티브 API 링크 Tmrt/UTCI 로드...")
api = gpd.read_file(NATIVE_GPKG)
value_cols = [c for c in api.columns if c.startswith('UTCI_')]
log(f"  API 링크: {len(api):,}개, UTCI 컬럼 {len(value_cols)}개")

# ── 2. 그래프 구성 ────────────────────────────────────────────────────────
log("그래프 구성...")
G = nx.Graph()
node_xy = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    G.add_edge(u, v, travel_time=row['LNKG_LEN'] / WALK_SPEED,
               **{c: row[c] for c in value_cols})
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]
    node_xy[v] = coords[-1]
log(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}")

node_ids = list(node_xy.keys())
node_xy_arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(node_xy_arr)

# ── 3. 출발지(집계구 중심점) 스냅 ─────────────────────────────────────────
log("집계구 로드 및 중심점 스냅...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True).to_crs(TARGET_CRS)
c_xy = np.array([[p.x, p.y] for p in jbg.geometry.centroid])
_, idx = tree.query(c_xy)
jbg['net_node'] = [node_ids[i] for i in idx]
origins = jbg.drop_duplicates(subset='net_node')[['TOT_REG_CD', 'ADM_NM', 'net_node']].reset_index(drop=True)
log(f"  집계구 {len(jbg)}개 -> 중복제거 후 출발지 {len(origins)}개")

# ── 4. 기회(지하철역+버스정류장) 스냅 ─────────────────────────────────────
log("기회(지하철역+버스정류장) 로드 및 스냅...")
subway = gpd.read_file(SUBWAY_GPKG)[['name', 'geometry']].to_crs(TARGET_CRS)
subway['type'] = 'subway'

bus = pd.read_csv(GTFS_STOPS)
bus['region'] = bus['stop_id'].str.split('_').str[1]
bus = bus[bus['region'] == '1100'].copy()
bus_gdf = gpd.GeoDataFrame(
    bus[['stop_name']].rename(columns={'stop_name': 'name'}),
    geometry=gpd.points_from_xy(bus['stop_lon'], bus['stop_lat']), crs=4326).to_crs(TARGET_CRS)
bus_gdf['type'] = 'bus'

opp = pd.concat([subway, bus_gdf], ignore_index=True)
opp_xy = np.array([[p.x, p.y] for p in opp.geometry])
_, idx = tree.query(opp_xy)
opp['net_node'] = [node_ids[i] for i in idx]
opportunity_nodes = set(opp['net_node'].unique())
log(f"  지하철역 {len(subway)} + 버스정류장 {len(bus_gdf)} -> 스냅된 기회 노드 {len(opportunity_nodes)}개")

# ── 5. CA(무보정) ─────────────────────────────────────────────────────────
log("CA(무보정) 계산 중...")
ca_results = {}
for origin in origins['net_node']:
    lengths = nx.single_source_dijkstra_path_length(
        G, origin, cutoff=TIME_BUDGET, weight='travel_time')
    reachable = set(lengths.keys())
    ca_results[origin] = len(reachable & opportunity_nodes)
log("  CA 완료")

# ── 6. SEAR(시간대 x 임계값) ─────────────────────────────────────────────
rows = []
for hour in HOURS:
    col = f'UTCI_{hour:02d}'
    for thr in THRESHOLDS:
        def weight(u, v, d, _col=col, _thr=thr):
            val = d.get(_col)
            if val is not None and not (isinstance(val, float) and np.isnan(val)) and val >= _thr:
                return None
            return d['travel_time']

        t2 = time.time()
        for _, row in origins.iterrows():
            origin = row['net_node']
            lengths = nx.single_source_dijkstra_path_length(
                G, origin, cutoff=TIME_BUDGET, weight=weight)
            reachable = set(lengths.keys())
            n_sear = len(reachable & opportunity_nodes)
            n_ca = ca_results[origin]
            rows.append({
                'TOT_REG_CD': row['TOT_REG_CD'], 'ADM_NM': row['ADM_NM'],
                'net_node': origin, 'hour': hour, 'threshold': thr,
                'opp_CA': n_ca, 'opp_SEAR': n_sear,
                'reduction_pct': round((n_ca - n_sear) / max(n_ca, 1) * 100, 2),
            })
        log(f"  {hour:02d}시 x {thr}도 완료 ({time.time()-t2:.1f}s)")

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
log(f"저장: {OUT_CSV} ({len(df)} rows)")
log(f"총 소요시간: {(time.time()-t0)/60:.1f}분")
