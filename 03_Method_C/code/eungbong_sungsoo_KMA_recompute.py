"""
응봉역·성수역 파일럿 — KMA 격자기상 UTCI로 재계산 (마스터초안 IV§3.5 수치 갱신용)
================================================================
기존 §3.5 서술(eungbong_sungsoo_greedy_link_repair.py와 동일 네트워크·조건:
서울시 도보 네트워크 API, 지하철역+버스정류장 기회, WALK_SPEED=4.0km/h,
TIME_BUDGET=15분, THRESHOLD=38°C)을 새 UTCI(2026-08-06_link_utci_seoul_5m_
KMA격자기상.gpkg)로 재계산한다. 기존엔 09시만 계산했으나 §3.5가 09시·19시를
모두 인용하므로 두 시각 다 계산.

1. 반경 1.2km 내 이진적 제거 대상(UTCI≥38°C) 링크 비율 — 09시/19시
2. 기회(지하철역·버스정류장) 기준 접근성 감소율(CA vs TCA) — 09시/19시
(노드 평균 차수 2.50·막다른 골목 28.2%는 네트워크 위상 고유값이라 기상방식과
무관 — 재계산 불필요, 기존값 유지)
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree

WALK_SPEED = 4.0 * 1000 / 3600
TIME_BUDGET = 15 * 60
THRESHOLD = 38.0
HOURS = ['09', '19']
RADIUS_M = 1200
TARGET_CRS = 'EPSG:5186'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
API_NET = f'{PROJ}/data/network/2026-08-02_seoul_walk_api_network.gpkg'
NEW_GPKG = f'{PROJ}/03_Method_C/results/2026-08-06_link_utci_seoul_5m_KMA격자기상.gpkg'
SUBWAY_GPKG = f'{PROJ}/data/facilities/seoul_subway_stations.gpkg'
GTFS_STOPS = '/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt'

print("API 네트워크 로드...")
api = gpd.read_file(API_NET)
api = api[api['LNKG_TYPE_CD'].str.startswith('1')].copy()
api = api.to_crs(TARGET_CRS)
api['LNKG_LEN'] = api['LNKG_LEN'].astype(float)
api = api[api['LNKG_LEN'] > 0].copy()
print(f"  API 보행 링크: {len(api):,}개")

print("UTCI(KMA 격자기상, 신버전) 매칭...")
new_utci = gpd.read_file(NEW_GPKG, columns=[f'UTCI_{h}' for h in HOURS])
api['centroid'] = api.geometry.centroid
api_pts = gpd.GeoDataFrame(api[['LNKG_ID']], geometry=api['centroid'], crs=TARGET_CRS)
joined = gpd.sjoin_nearest(api_pts, new_utci.to_crs(TARGET_CRS), how='left', distance_col='dist_m')
joined = joined.drop_duplicates(subset='LNKG_ID')
print(f"  평균 매칭 거리: {joined['dist_m'].mean():.1f}m")
api = api.merge(joined[['LNKG_ID', 'dist_m'] + [f'UTCI_{h}' for h in HOURS]], on='LNKG_ID', how='left')
api = api.drop(columns='centroid')

print("그래프 구성...")
G = nx.Graph()
node_xy = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    G.add_edge(u, v, travel_time=row['LNKG_LEN'] / WALK_SPEED,
               **{f'UTCI_{h}': row[f'UTCI_{h}'] for h in HOURS})
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]
    node_xy[v] = coords[-1]
print(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}")

node_ids = list(node_xy.keys())
node_xy_arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(node_xy_arr)

print("응봉역·성수역 스냅...")
subway = gpd.read_file(SUBWAY_GPKG)[['name', 'geometry']].to_crs(TARGET_CRS)
targets = {}
for key, name in [('eungbong', '응봉'), ('sungsoo', '성수')]:
    pt = subway[subway['name'] == name].geometry.iloc[0]
    _, i = tree.query([pt.x, pt.y])
    targets[key] = {'node': node_ids[i], 'label': f'{name}역', 'point': pt}

print("기회(지하철역+버스정류장) 스냅...")
bus = pd.read_csv(GTFS_STOPS)
bus['region'] = bus['stop_id'].str.split('_').str[1]
bus = bus[bus['region'] == '1100'].copy()
bus_gdf = gpd.GeoDataFrame(
    bus[['stop_name']], geometry=gpd.points_from_xy(bus['stop_lon'], bus['stop_lat']),
    crs=4326).to_crs(TARGET_CRS)
opp = pd.concat([subway.rename(columns={'name': 'stop_name'}), bus_gdf], ignore_index=True)
opp_xy = np.array([[p.x, p.y] for p in opp.geometry])
_, idx = tree.query(opp_xy)
opp['net_node'] = [node_ids[i] for i in idx]
opportunity_nodes = set(opp['net_node'].unique())

# ---------- 1. 반경 1.2km 내 이진적 제거 대상 링크 비율 ----------
print(f"\n=== 반경 {RADIUS_M}m 내 이진적 제거(UTCI>={THRESHOLD}) 대상 링크 비율 ===")
for key, t in targets.items():
    buf = t['point'].buffer(RADIUS_M)
    sub = api[api.geometry.intersects(buf)]
    for h in HOURS:
        vals = sub[f'UTCI_{h}'].dropna()
        pct = (vals >= THRESHOLD).mean() * 100
        print(f"  {t['label']} {h}시: {pct:.1f}% ({len(vals):,}개 링크)")

# ---------- 2. 기회 기준 CA vs TCA ----------
print(f"\n=== 기회(지하철역·버스정류장) 기준 CA vs TCA (임계값 {THRESHOLD}) ===")


def reachable(graph, origin):
    return set(nx.single_source_dijkstra_path_length(graph, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())


for key, t in targets.items():
    origin = t['node']
    s_classic = reachable(G, origin)
    ca = len(s_classic & opportunity_nodes)
    for h in HOURS:
        col = f'UTCI_{h}'
        hot_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get(col) is not None and d[col] >= THRESHOLD]
        G_th = G.copy()
        G_th.remove_edges_from(hot_edges)
        tca = len(reachable(G_th, origin) & opportunity_nodes)
        reduction = (ca - tca) / max(ca, 1) * 100
        print(f"  {t['label']} {h}시: CA={ca} -> TCA={tca}  감소율={reduction:.1f}%")

print("\n완료")
