"""
seongdong_jibgyegu_repair_efficiency.py 에서 MAX_STEPS=300 상한에 걸려
50%에 도달하지 못한 33개 집계구만 상한을 늘려(800) 재계산 — 확인 결과
전부 300단계 시점에 이미 40%대까지 도달해 있어(진짜 벽이 아니라 계산
상한 문제), CSV에서 해당 행만 교체.
"""
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree

WALK_SPEED = 4.0*1000/3600
TIME_BUDGET = 15*60
TARGET_CRS = 'EPSG:5186'
PROJ_DIR = '/Users/jin/석사논문/Thermal_Catchment'
JIBGYEGU_SHP = f'{PROJ_DIR}/data/_tmp_boundary/집계구.shp'
OUT_CSV = f'{PROJ_DIR}/03_Method_C/results/2026-08-04_seongdong_jibgyegu_repair_efficiency.csv'
TARGET_PCT = 0.5
MAX_STEPS = 800

t0 = time.time()
def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)

log("네트워크 로드 및 09시 UTCI 매칭...")
api = gpd.read_file(f'{PROJ_DIR}/data/network/2026-08-02_seoul_walk_api_network.gpkg')
api = api[api['LNKG_TYPE_CD'].str.startswith('1')].copy()
api = api.to_crs(TARGET_CRS)
api['LNKG_LEN'] = api['LNKG_LEN'].astype(float)
api = api[api['LNKG_LEN'] > 0].copy()

osm = gpd.read_file(f'{PROJ_DIR}/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg')
api['centroid'] = api.geometry.centroid
api_pts = gpd.GeoDataFrame(api[['LNKG_ID']], geometry=api['centroid'], crs=TARGET_CRS)
joined = gpd.sjoin_nearest(api_pts, osm[['UTCI_09', 'geometry']], how='left', distance_col='dist_m')
joined = joined.drop_duplicates(subset='LNKG_ID')
api = api.merge(joined[['LNKG_ID', 'UTCI_09']], on='LNKG_ID', how='left')

log("그래프 구성...")
G = nx.Graph()
node_xy = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    hot = row['UTCI_09'] is not None and row['UTCI_09'] >= 38.0
    G.add_edge(u, v, travel_time=row['LNKG_LEN']/WALK_SPEED, length=row['LNKG_LEN'], hot=hot)
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]; node_xy[v] = coords[-1]

node_ids = list(node_xy.keys())
arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(arr)

subway = gpd.read_file(f'{PROJ_DIR}/data/facilities/seoul_subway_stations.gpkg')[['name', 'geometry']].to_crs(TARGET_CRS)
bus = pd.read_csv('/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt')
bus['region'] = bus['stop_id'].str.split('_').str[1]
bus = bus[bus['region'] == '1100'].copy()
bus_gdf = gpd.GeoDataFrame(bus[['stop_name']], geometry=gpd.points_from_xy(bus['stop_lon'], bus['stop_lat']), crs=4326).to_crs(TARGET_CRS)
opp = pd.concat([subway.rename(columns={'name': 'stop_name'}), bus_gdf], ignore_index=True)
opp_xy = np.array([[p.x, p.y] for p in opp.geometry])
_, idx = tree.query(opp_xy)
opp['net_node'] = [node_ids[i] for i in idx]
opportunity_nodes = set(opp['net_node'].unique())

G_th_base = G.copy()
all_hot = [(u, v) for u, v, d in G.edges(data=True) if d['hot']]
G_th_base.remove_edges_from(all_hot)
log(f"  핫링크 {len(all_hot):,}개 제거 완료")

def reachable(graph, origin):
    return set(nx.single_source_dijkstra_path_length(graph, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

def hop_distance_from_origin(graph, origin):
    return nx.single_source_shortest_path_length(graph, origin)

df = pd.read_csv(OUT_CSV, dtype={'TOT_REG_CD': str, 'net_node': str})
todo = df[(df['reached_50pct'] == False) & (df['ca'] > 0)].copy()
log(f"재계산 대상: {len(todo)}개")

for i, row in todo.iterrows():
    origin = row['net_node']
    ca = row['ca']
    t_origin = time.time()

    hop_dist = hop_distance_from_origin(G, origin)
    G_work = G_th_base.copy()
    s_current = reachable(G_work, origin)
    tca_now = len(s_current & opportunity_nodes)

    target_opp = ca * TARGET_PCT
    cum_len = 0.0
    reached = tca_now >= target_opp
    len_to_50 = 0.0 if reached else np.nan
    steps_to_50 = 0 if reached else np.nan
    step = 0

    while not reached and step < MAX_STEPS:
        step += 1
        frontier = set()
        for n in s_current:
            for nb in G.neighbors(n):
                if G[n][nb]['hot'] and not G_work.has_edge(n, nb):
                    frontier.add((n, nb))
        if not frontier:
            break
        best = None
        best_key = None
        for (u, v) in frontier:
            G_work.add_edge(u, v, **G[u][v])
            s_test = reachable(G_work, origin)
            gain = len(s_test & opportunity_nodes) - tca_now
            G_work.remove_edge(u, v)
            dist = min(hop_dist.get(u, 1e9), hop_dist.get(v, 1e9))
            k = (-gain, dist)
            if best_key is None or k < best_key:
                best_key = k
                best = (u, v, gain)
        u, v, gain = best
        G_work.add_edge(u, v, **G[u][v])
        s_current = reachable(G_work, origin)
        tca_now = len(s_current & opportunity_nodes)
        cum_len += G[u][v]['length']
        if tca_now >= target_opp:
            reached = True
            len_to_50 = round(cum_len, 1)
            steps_to_50 = step

    df.loc[i, 'reached_50pct'] = reached
    df.loc[i, 'len_to_50pct_m'] = len_to_50
    df.loc[i, 'steps_to_50pct'] = steps_to_50
    df.loc[i, 'max_pct_reached'] = max(row['max_pct_reached'], round(tca_now/ca*100, 1))
    df.loc[i, 'total_steps_run'] = step
    df.loc[i, 'elapsed_s'] = round(time.time()-t_origin, 2)
    log(f"  {row['ADM_NM']} CA={ca} -> 50%도달={reached} ({len_to_50}m, {steps_to_50}단계, {step}회 반복, {time.time()-t_origin:.1f}s)")

df.to_csv(OUT_CSV, index=False, encoding='utf-8-sig')
log(f"완료 — 여전히 미도달: {(~df['reached_50pct'] & (df['ca']>0)).sum()}개")
