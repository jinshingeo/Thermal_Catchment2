"""
성동구 집계구별 — 병목 링크 복구 효율(50% 회복까지 필요한 누적 m) 배치
================================================================
근거: 응봉역·성수역 2개 지점에서 확인한 탐욕적 복구(Nemhauser, Fisher &
      Wolsey, 1978) 방식을 성동구 전체 집계구(570개)로 확장. 지점마다
      "CA 대비 50% 회복"에 도달하는 순간 조기 종료(계산량 절감) —
      "조금만 고쳐도 크게 좋아지는 동 vs 많이 고쳐야 하는 동"을 지도로
      보여주기 위한 단일 요약 지표.
시간대: 09시, 임계값 UTCI 38°C. 결과는 매 지점마다 즉시 CSV에 append
      (중간에 끊겨도 그때까지 결과는 보존).
"""
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from scipy.spatial import cKDTree
import os

WALK_SPEED = 4.0*1000/3600
TIME_BUDGET = 15*60
TARGET_CRS = 'EPSG:5186'
PROJ_DIR = '/Users/jin/석사논문/Thermal_Catchment'
JIBGYEGU_SHP = f'{PROJ_DIR}/data/_tmp_boundary/집계구.shp'
OUT_CSV = f'{PROJ_DIR}/03_Method_C/results/2026-08-04_seongdong_jibgyegu_repair_efficiency.csv'
TARGET_PCT = 0.5
MAX_STEPS = 300

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
log(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}")

node_ids = list(node_xy.keys())
arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(arr)

log("기회(지하철역+버스정류장) 스냅...")
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
log(f"  핫링크 {len(all_hot):,}개 제거 완료(09시 38도 기준)")

log("성동구 집계구 출발지 스냅...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True).to_crs(TARGET_CRS)
jbg = jbg[jbg['TOT_REG_CD'].str[:5] == '11040'].copy().reset_index(drop=True)
c_xy = np.array([[p.x, p.y] for p in jbg.geometry.centroid])
_, idx = tree.query(c_xy)
jbg['net_node'] = [node_ids[i] for i in idx]
jbg = jbg.drop_duplicates(subset='net_node').reset_index(drop=True)
log(f"  성동구 집계구 {len(jbg)}개")

def reachable(graph, origin):
    return set(nx.single_source_dijkstra_path_length(graph, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

def hop_distance_from_origin(graph, origin):
    return nx.single_source_shortest_path_length(graph, origin)

if not os.path.exists(OUT_CSV):
    pd.DataFrame(columns=['TOT_REG_CD', 'ADM_NM', 'net_node', 'ca', 'tca0_opp', 'tca0_pct',
                           'reached_50pct', 'len_to_50pct_m', 'steps_to_50pct',
                           'max_pct_reached', 'total_steps_run', 'elapsed_s']).to_csv(
        OUT_CSV, index=False, encoding='utf-8-sig')
done_nodes = set(pd.read_csv(OUT_CSV)['net_node'].astype(str)) if os.path.getsize(OUT_CSV) > 0 else set()

for i, row in jbg.iterrows():
    origin = row['net_node']
    if str(origin) in done_nodes:
        continue
    t_origin = time.time()

    s_classic = reachable(G, origin)
    ca = len(s_classic & opportunity_nodes)

    if ca == 0:
        rec = {'TOT_REG_CD': row['TOT_REG_CD'], 'ADM_NM': row['ADM_NM'], 'net_node': origin,
               'ca': 0, 'tca0_opp': 0, 'tca0_pct': 0.0, 'reached_50pct': False,
               'len_to_50pct_m': np.nan, 'steps_to_50pct': np.nan, 'max_pct_reached': 0.0,
               'total_steps_run': 0, 'elapsed_s': round(time.time()-t_origin, 2)}
        pd.DataFrame([rec]).to_csv(OUT_CSV, mode='a', header=False, index=False, encoding='utf-8-sig')
        continue

    hop_dist = hop_distance_from_origin(G, origin)
    G_work = G_th_base.copy()
    s_current = reachable(G_work, origin)
    tca_now = len(s_current & opportunity_nodes)
    tca0_opp = tca_now
    tca0_pct = round(tca_now/ca*100, 1)

    target_opp = ca * TARGET_PCT
    cum_len = 0.0
    reached = tca_now >= target_opp
    len_to_50 = 0.0 if reached else np.nan
    steps_to_50 = 0 if reached else np.nan
    max_pct = tca0_pct
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
        pct_now = tca_now/ca*100
        max_pct = max(max_pct, pct_now)
        if tca_now >= target_opp:
            reached = True
            len_to_50 = round(cum_len, 1)
            steps_to_50 = step

    rec = {'TOT_REG_CD': row['TOT_REG_CD'], 'ADM_NM': row['ADM_NM'], 'net_node': origin,
           'ca': ca, 'tca0_opp': tca0_opp,
           'tca0_pct': tca0_pct, 'reached_50pct': reached,
           'len_to_50pct_m': len_to_50, 'steps_to_50pct': steps_to_50,
           'max_pct_reached': round(max_pct, 1), 'total_steps_run': step,
           'elapsed_s': round(time.time()-t_origin, 2)}
    pd.DataFrame([rec]).to_csv(OUT_CSV, mode='a', header=False, index=False, encoding='utf-8-sig')

    if i % 10 == 0 or i == len(jbg)-1:
        log(f"  [{i+1}/{len(jbg)}] {row['ADM_NM']} CA={ca} 50%도달={reached} "
            f"({len_to_50}m, {steps_to_50}단계) elapsed={time.time()-t_origin:.1f}s")

log("완료")
