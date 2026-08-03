"""
서울 전역 — 병목 링크(link importance) 분석, 09시 x 38°C
================================================================
근거: Jenelius, Petersen & Mattsson (2006), "Importance and exposure in road
      network vulnerability analysis", Transportation Research Part A, 40(7),
      537-560 — 링크를 하나씩 복구(반대: 폐쇄)했을 때 접근성이 얼마나
      회복(감소)되는지로 "링크 중요도"를 정의하는 표준 방법론을 그대로 적용.
방식: 이진적 제거로 손상된 네트워크(G_thermal)에서, 각 출발지의 도달가능
      경계(frontier)에 있는 핫링크를 하나씩 복구해보고, 회복되는 기회
      (지하철역+버스정류장) 개수를 측정 — 출발지 인접 링크만 테스트
      (§3.5에서 확인한 평균 노드차수 2.5 특성 근거로 범위 한정).
시간대: 09시(부분 붕괴 구간 — 완전포화 시간대는 복구 효과가 안 보이므로 제외)
"""
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree

WALK_SPEED = 4.0 * 1000 / 3600
TIME_BUDGET = 15 * 60
THRESHOLD = 38.0
HOUR = '09'
TARGET_CRS = 'EPSG:5186'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
API_NET = f'{PROJ}/data/network/2026-08-02_seoul_walk_api_network.gpkg'
OSM_RESULT = f'{PROJ}/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg'
JIBGYEGU_SHP = f'{PROJ}/data/_tmp_boundary/집계구.shp'
SUBWAY_GPKG = f'{PROJ}/data/facilities/seoul_subway_stations.gpkg'
GTFS_STOPS = '/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt'
OUT_CSV = f'{PROJ}/03_Method_C/results/2026-08-03_seoul_link_importance_09h38.csv'

t0 = time.time()
def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)

log("API 네트워크 로드...")
api = gpd.read_file(API_NET)
api = api[api['LNKG_TYPE_CD'].str.startswith('1')].copy()
api = api.to_crs(TARGET_CRS)
api['LNKG_LEN'] = api['LNKG_LEN'].astype(float)
api = api[api['LNKG_LEN'] > 0].copy()
log(f"  보행 링크: {len(api):,}개")

log("OSM 링크 UTCI 결과 로드 및 최근접 매칭...")
osm = gpd.read_file(OSM_RESULT)
col = f'UTCI_{HOUR}'
api['centroid'] = api.geometry.centroid
api_pts = gpd.GeoDataFrame(api[['LNKG_ID']], geometry=api['centroid'], crs=TARGET_CRS)
joined = gpd.sjoin_nearest(api_pts, osm[[col, 'geometry']], how='left', distance_col='dist_m')
joined = joined.drop_duplicates(subset='LNKG_ID')
api = api.merge(joined[['LNKG_ID', col]], on='LNKG_ID', how='left')
api = api.drop(columns='centroid')
log(f"  매칭 완료, 평균거리 {joined['dist_m'].mean():.1f}m")

log("그래프 구성...")
G = nx.Graph()
node_xy = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    G.add_edge(u, v, travel_time=row['LNKG_LEN'] / WALK_SPEED, utci=row[col], hot=(row[col] is not None and row[col] >= THRESHOLD))
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]
    node_xy[v] = coords[-1]
log(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}")

node_ids = list(node_xy.keys())
node_xy_arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(node_xy_arr)

log("집계구 출발지 스냅...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True).to_crs(TARGET_CRS)
c_xy = np.array([[p.x, p.y] for p in jbg.geometry.centroid])
_, idx = tree.query(c_xy)
jbg['net_node'] = [node_ids[i] for i in idx]
origins = jbg.drop_duplicates(subset='net_node')[['TOT_REG_CD', 'ADM_NM', 'net_node']].reset_index(drop=True)
log(f"  출발지 {len(origins)}개")

log("기회(지하철역+버스정류장) 스냅...")
subway = gpd.read_file(SUBWAY_GPKG)[['name', 'geometry']].to_crs(TARGET_CRS)
bus = pd.read_csv(GTFS_STOPS)
bus['region'] = bus['stop_id'].str.split('_').str[1]
bus = bus[bus['region'] == '1100'].copy()
bus_gdf = gpd.GeoDataFrame(bus[['stop_name']], geometry=gpd.points_from_xy(bus['stop_lon'], bus['stop_lat']), crs=4326).to_crs(TARGET_CRS)
opp = pd.concat([subway.rename(columns={'name': 'stop_name'}), bus_gdf], ignore_index=True)
opp_xy = np.array([[p.x, p.y] for p in opp.geometry])
_, idx = tree.query(opp_xy)
opp['net_node'] = [node_ids[i] for i in idx]
opportunity_nodes = set(opp['net_node'].unique())
log(f"  기회 노드 {len(opportunity_nodes)}개")

G_thermal = G.copy()
hot_edges_all = [(u, v) for u, v, d in G.edges(data=True) if d['hot']]
G_thermal.remove_edges_from(hot_edges_all)
log(f"  전체 핫링크 {len(hot_edges_all):,}개 제거(09시 38도 기준)")

def reachable(graph, origin):
    return set(nx.single_source_dijkstra_path_length(graph, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

rows = []
t_loop = time.time()
for i, row in origins.iterrows():
    origin = row['net_node']
    if origin not in G_thermal:
        continue
    s_thermal = reachable(G_thermal, origin)
    tca = len(s_thermal & opportunity_nodes)
    if origin not in G:
        continue
    s_classic = reachable(G, origin)
    ca = len(s_classic & opportunity_nodes)
    if ca == 0 or ca == tca:
        continue  # 손실 없는 출발지는 스킵

    # 출발지 인접 핫링크(원본 그래프 기준)만 후보로 테스트
    # 성능: 그래프 전체를 복사하지 않고, 엣지 하나만 추가 -> 테스트 -> 제거
    candidates = [(origin, nb) for nb in G.neighbors(origin) if G[origin][nb]['hot']]
    for u, v in candidates:
        G_thermal.add_edge(u, v, **G[u][v])
        s_test = reachable(G_thermal, origin)
        G_thermal.remove_edge(u, v)
        recovered = len(s_test & opportunity_nodes) - tca
        if recovered > 0:
            rows.append({
                'TOT_REG_CD': row['TOT_REG_CD'], 'ADM_NM': row['ADM_NM'],
                'net_node': origin, 'candidate_edge': f'{u}-{v}',
                'ca': ca, 'tca_before': tca, 'opp_recovered': recovered,
                'recovery_pct_of_loss': round(recovered / max(ca - tca, 1) * 100, 1),
            })
    if i % 2000 == 0:
        log(f"  진행 {i}/{len(origins)} ({time.time()-t_loop:.0f}s)")

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False, encoding='utf-8-sig')
log(f"저장: {OUT_CSV} ({len(df)} rows, 영향 있는 후보 링크만)")
if len(df):
    top = df.sort_values('opp_recovered', ascending=False).head(20)
    log("상위 20개 병목 링크:\n" + top[['ADM_NM', 'candidate_edge', 'opp_recovered', 'recovery_pct_of_loss']].to_string())
