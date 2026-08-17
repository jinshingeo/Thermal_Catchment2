"""
서울 전역 — API 네트워크 네이티브 컨투어 메저 (CA vs SEAR), 픽셀 우선계산·
버퍼 없음 최종판
================================================================
21_api_network_native_contour.py와 동일 구조(그래프를 API 링크
BGNG_LNKG_ID/END_LNKG_ID로 직접 구성)이나, UTCI 소스를
2026-08-18_link_utci_seoul_5m_api_network_nobuffer.gpkg(32번 스크립트,
픽셀 단위 KMA 격자기상 반영·버퍼 없음)로 교체. 임계값은 38.0만 계산.

2026-08-18 확인: 이게 진짜 메인 분석(서울시 도보 네트워크 API 기준)이며,
2026-08-17에 돌린 OSM 기반 결과(seoul_wide_jibgyegu_contour_KMA_v2_nobuffer.py)는
OSM 네트워크를 잘못 메인으로 쓴 것이었음 — 이제 그 OSM 결과는 §3.3 강건성
비교(메인 API vs 검증용 OSM)에 재활용한다.
"""
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree

WALK_SPEED = 4.0 * 1000 / 3600  # Brode et al.(2012) p.483
TIME_BUDGET = 15 * 60
THRESHOLD = 38.0
HOURS = list(range(6, 20))
TARGET_CRS = 'EPSG:5186'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
LINK_UTCI_GPKG = f'{PROJ}/03_Method_C/results/2026-08-18_link_utci_seoul_5m_api_network_nobuffer.gpkg'
JIBGYEGU_SHP = f'{PROJ}/data/_tmp_boundary/집계구.shp'
SUBWAY_GPKG = f'{PROJ}/data/facilities/seoul_subway_stations.gpkg'
GTFS_STOPS = '/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt'
OUT_CSV = f'{PROJ}/03_Method_C/results/2026-08-18_seoul_jibgyegu_contour_CA_vs_SEAR_api_network_nobuffer.csv'

t0 = time.time()


def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)


log("API 링크 UTCI(픽셀 우선계산·버퍼 없음) 로드...")
api = gpd.read_file(LINK_UTCI_GPKG)
value_cols = [c for c in api.columns if c.startswith('UTCI_')]
log(f"  API 링크: {len(api):,}개, UTCI 컬럼 {len(value_cols)}개")

log("그래프 구성...")
G = nx.Graph()
node_xy = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    try:
        lnkg_len = float(row['LNKG_LEN'])
    except (TypeError, ValueError):
        lnkg_len = 0.0
    length = lnkg_len if lnkg_len > 0 else row.geometry.length
    G.add_edge(u, v, travel_time=length / WALK_SPEED,
               **{c: row[c] for c in value_cols})
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]
    node_xy[v] = coords[-1]
log(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}")

node_ids = list(node_xy.keys())
node_xy_arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(node_xy_arr)

log("집계구 로드 및 중심점 스냅...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True).to_crs(TARGET_CRS)
c_xy = np.array([[p.x, p.y] for p in jbg.geometry.centroid])
_, idx = tree.query(c_xy)
jbg['net_node'] = [node_ids[i] for i in idx]
origins = jbg.drop_duplicates(subset='net_node')[['TOT_REG_CD', 'ADM_NM', 'net_node']].reset_index(drop=True)
log(f"  집계구 {len(jbg)}개 -> 중복제거 후 출발지 {len(origins)}개")

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

log("CA(무보정) 계산 중...")
ca_results = {}
for origin in origins['net_node']:
    lengths = nx.single_source_dijkstra_path_length(
        G, origin, cutoff=TIME_BUDGET, weight='travel_time')
    reachable = set(lengths.keys())
    ca_results[origin] = len(reachable & opportunity_nodes)
log("  CA 완료")

rows = []
for hour in HOURS:
    col = f'UTCI_{hour:02d}'

    def weight(u, v, d, _col=col):
        val = d.get(_col)
        if val is not None and not (isinstance(val, float) and np.isnan(val)) and val >= THRESHOLD:
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
            'net_node': origin, 'hour': hour, 'threshold': THRESHOLD,
            'opp_CA': n_ca, 'opp_SEAR': n_sear,
            'reduction_pct': round((n_ca - n_sear) / max(n_ca, 1) * 100, 2),
        })
    log(f"  {hour:02d}시 완료 ({time.time()-t2:.1f}s)")

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
log(f"저장: {OUT_CSV} ({len(df)} rows)")
log(f"총 소요시간: {(time.time()-t0)/60:.1f}분")
