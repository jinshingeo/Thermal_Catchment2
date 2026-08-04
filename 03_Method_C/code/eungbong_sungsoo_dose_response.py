"""
응봉역·성수역 — 병목 링크 K개 누적 개선 시 접근성 회복 (용량-반응 곡선)
================================================================
탐욕적(하나씩, 즉시 이득만) 방식의 한계(응봉역처럼 여러 겹으로 막힌
경우 첫 단계에서 회복 효과 0이라 조기 종료)를 넘어서기 위해, 출발지에서
BFS(너비우선)로 가까운 순서대로 핫링크를 K개씩 누적 복구하며 회복되는
기회(지하철역·버스정류장) 개수를 측정. 즉시 이득이 없어도 계속 진행.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from collections import deque

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

WALK_SPEED = 4.0*1000/3600
TIME_BUDGET = 15*60
TARGET_CRS = 'EPSG:5186'
PROJ = '/Users/jin/석사논문/Thermal_Catchment'

api = gpd.read_file(f'{PROJ}/data/network/2026-08-02_seoul_walk_api_network.gpkg')
api = api[api['LNKG_TYPE_CD'].str.startswith('1')].copy()
api = api.to_crs(TARGET_CRS)
api['LNKG_LEN'] = api['LNKG_LEN'].astype(float)
api = api[api['LNKG_LEN'] > 0].copy()

osm = gpd.read_file(f'{PROJ}/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg')
api['centroid'] = api.geometry.centroid
api_pts = gpd.GeoDataFrame(api[['LNKG_ID']], geometry=api['centroid'], crs=TARGET_CRS)
joined = gpd.sjoin_nearest(api_pts, osm[['UTCI_09', 'geometry']], how='left', distance_col='dist_m')
joined = joined.drop_duplicates(subset='LNKG_ID')
api = api.merge(joined[['LNKG_ID', 'UTCI_09']], on='LNKG_ID', how='left')

G = nx.Graph()
node_xy = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    hot = row['UTCI_09'] is not None and row['UTCI_09'] >= 38.0
    G.add_edge(u, v, travel_time=row['LNKG_LEN']/WALK_SPEED, hot=hot)
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]; node_xy[v] = coords[-1]

node_ids = list(node_xy.keys())
arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(arr)

subway = gpd.read_file(f'{PROJ}/data/facilities/seoul_subway_stations.gpkg')[['name', 'geometry']].to_crs(TARGET_CRS)
bus = pd.read_csv('/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt')
bus['region'] = bus['stop_id'].str.split('_').str[1]
bus = bus[bus['region'] == '1100'].copy()
bus_gdf = gpd.GeoDataFrame(bus[['stop_name']], geometry=gpd.points_from_xy(bus['stop_lon'], bus['stop_lat']), crs=4326).to_crs(TARGET_CRS)
opp = pd.concat([subway.rename(columns={'name': 'stop_name'}), bus_gdf], ignore_index=True)
opp_xy = np.array([[p.x, p.y] for p in opp.geometry])
_, idx = tree.query(opp_xy)
opp['net_node'] = [node_ids[i] for i in idx]
opportunity_nodes = set(opp['net_node'].unique())

def reachable(graph, origin):
    return set(nx.single_source_dijkstra_path_length(graph, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

def bfs_hot_edges_order(G, origin, max_edges=500):
    """origin에서 너비우선으로 탐색하며 만나는 핫링크를 순서대로 수집(전체 그래프 기준, 열 여부 무관하게 탐색)"""
    visited = {origin}
    order = []
    q = deque([origin])
    while q and len(order) < max_edges:
        n = q.popleft()
        for nb in G.neighbors(n):
            if G[n][nb]['hot']:
                order.append((n, nb))
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    return order

results = {}
for key, name in [('eungbong', '응봉'), ('sungsoo', '성수')]:
    pt = subway[subway['name'] == name].geometry.iloc[0]
    _, i = tree.query([pt.x, pt.y])
    origin = node_ids[i]

    s_classic = reachable(G, origin)
    ca = len(s_classic & opportunity_nodes)

    hot_order = bfs_hot_edges_order(G, origin, max_edges=300)
    print(f'{name}역: CA={ca}, BFS로 찾은 핫링크 후보 {len(hot_order)}개')

    K_list = [0, 1, 2, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300]
    K_list = [k for k in K_list if k <= len(hot_order)]

    G_th_base = G.copy()
    all_hot = [(u, v) for u, v, d in G.edges(data=True) if d['hot']]
    G_th_base.remove_edges_from(all_hot)

    rows = []
    for K in K_list:
        G_test = G_th_base.copy()
        for (u, v) in hot_order[:K]:
            G_test.add_edge(u, v, **G[u][v])
        s = reachable(G_test, origin)
        tca = len(s & opportunity_nodes)
        rows.append({'K_links_fixed': K, 'opp_reachable': tca, 'pct_of_ca': round(tca/max(ca,1)*100, 1)})
        print(f'  K={K:3d}개 고치면 -> 기회 {tca}/{ca}개 도달 ({tca/max(ca,1)*100:.1f}%)')

    df = pd.DataFrame(rows)
    df['ca'] = ca
    out_csv = f'{PROJ}/03_Method_C/results/2026-08-04_{key}_dose_response.csv'
    df.to_csv(out_csv, index=False, encoding='utf-8-sig')
    results[key] = {'df': df, 'ca': ca, 'label': f'{name}역'}

fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=150)
colors = {'eungbong': '#C3450F', 'sungsoo': '#1C5C82'}
for key, r in results.items():
    ax.plot(r['df']['K_links_fixed'], r['df']['opp_reachable'], marker='o', markersize=4,
            color=colors[key], label=f"{r['label']} (CA={r['ca']})")
ax.set_xlabel('복구한 핫링크 개수 K (BFS 근접 순, 즉시이득 조건 없이 누적)')
ax.set_ylabel('도달 가능한 기회(지하철역·버스정류장) 개수')
ax.set_title('응봉역·성수역 — 병목 링크 K개 누적 개선에 따른 접근성 회복\n(용량-반응 곡선, 09시·UTCI 38°C)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
out_png = f'{PROJ}/03_Method_C/results/figures/2026-08-04_eungbong_sungsoo_dose_response_curve.png'
plt.savefig(out_png, dpi=150, facecolor='white')
print('저장:', out_png)
