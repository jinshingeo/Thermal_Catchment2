"""
서울 전역 — 서울시 도보 네트워크 API(TbTraficWlkNet) 기반 컨투어 메저 (CA vs TCA)
================================================================
seoul_wide_jibgyegu_contour.py(OSM 기반)와 동일한 출발지/기회/파라미터를
API 네트워크로 재현. Tmrt/UTCI는 재계산하지 않고, API 링크마다 최근접
OSM 링크(2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg)에서 값을 상속.
성동구 파일럿(pilot_seongdong_api_network_catchment.py)에서 방법 검증 완료.

출발지: 서울 집계구 중심점 / 기회: 지하철역 + 버스정류장(GTFS, 서울)
시간대: 06~19시 / 임계값: 38.0 / 42.4
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
API_NET = f'{PROJ}/data/network/2026-08-02_seoul_walk_api_network.gpkg'
OSM_RESULT = f'{PROJ}/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg'
JIBGYEGU_SHP = f'{PROJ}/data/_tmp_boundary/집계구.shp'
SUBWAY_GPKG = f'{PROJ}/data/facilities/seoul_subway_stations.gpkg'
GTFS_STOPS = '/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt'
OUT_CSV = f'{PROJ}/03_Method_C/results/2026-08-02_seoul_wide_api_network_contour_CA_vs_TCA_allhours.csv'

t0 = time.time()


def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)


# ── 1. API 네트워크 — 서울 전체 보행 링크 ───────────────────────────────────
log("API 네트워크 로드...")
api = gpd.read_file(API_NET)
api = api[api['LNKG_TYPE_CD'].str.startswith('1')].copy()
api = api.to_crs(TARGET_CRS)
api['LNKG_LEN'] = api['LNKG_LEN'].astype(float)
api = api[api['LNKG_LEN'] > 0].copy()
log(f"  보행 링크: {len(api):,}개")

# ── 2. OSM 기반 Tmrt/UTCI 결과 — 최근접 매칭으로 값 상속 ────────────────────
log("OSM 링크 Tmrt/UTCI 결과 로드...")
osm = gpd.read_file(OSM_RESULT)
value_cols = [c for c in osm.columns if c.startswith('Tmrt_') or c.startswith('UTCI_')]
log(f"  OSM 링크: {len(osm):,}개, 값 컬럼 {len(value_cols)}개")

log("최근접 매칭(전체 서울, 시간 소요 예상)...")
api['centroid'] = api.geometry.centroid
api_pts = gpd.GeoDataFrame(api[['LNKG_ID']], geometry=api['centroid'], crs=TARGET_CRS)
joined = gpd.sjoin_nearest(api_pts, osm[value_cols + ['geometry']], how='left', distance_col='dist_m')
joined = joined.drop_duplicates(subset='LNKG_ID')
log(f"  매칭 완료. 평균거리 {joined['dist_m'].mean():.1f}m / 최대 {joined['dist_m'].max():.1f}m")

api = api.merge(joined[['LNKG_ID', 'dist_m'] + value_cols], on='LNKG_ID', how='left')
api = api.drop(columns='centroid')

# ── 3. 그래프 구성 ───────────────────────────────────────────────────────────
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

# ── 4. 출발지(집계구 중심점) 스냅 ────────────────────────────────────────────
log("집계구 로드 및 중심점 스냅...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True).to_crs(TARGET_CRS)
c_xy = np.array([[p.x, p.y] for p in jbg.geometry.centroid])
_, idx = tree.query(c_xy)
jbg['net_node'] = [node_ids[i] for i in idx]
origins = jbg.drop_duplicates(subset='net_node')[['TOT_REG_CD', 'ADM_NM', 'net_node']].reset_index(drop=True)
log(f"  집계구 {len(jbg)}개 -> 중복제거 후 출발지 {len(origins)}개")

# ── 5. 기회(지하철역+버스정류장) 스냅 ────────────────────────────────────────
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

# ── 6. CA(무보정) ────────────────────────────────────────────────────────────
log("CA(무보정) 계산 중...")
ca_results = {}
for origin in origins['net_node']:
    lengths = nx.single_source_dijkstra_path_length(
        G, origin, cutoff=TIME_BUDGET, weight='travel_time')
    reachable = set(lengths.keys())
    ca_results[origin] = len(reachable & opportunity_nodes)
log("  CA 완료")

# ── 7. TCA(시간대 x 임계값) ──────────────────────────────────────────────────
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
            n_tca = len(reachable & opportunity_nodes)
            n_ca = ca_results[origin]
            rows.append({
                'TOT_REG_CD': row['TOT_REG_CD'], 'ADM_NM': row['ADM_NM'],
                'net_node': origin, 'hour': hour, 'threshold': thr,
                'opp_CA': n_ca, 'opp_TCA': n_tca,
                'reduction_pct': round((n_ca - n_tca) / max(n_ca, 1) * 100, 2),
            })
        log(f"  {hour:02d}시 x {thr}도 완료 ({time.time()-t2:.1f}s)")

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
log(f"저장: {OUT_CSV} ({len(df)} rows)")
