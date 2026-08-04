"""
응봉역·성수역 — 탐욕적(값 우선, 동점시 거리) 병목 링크 복구 + 지도 시각화
================================================================
근거: Nemhauser, Fisher & Wolsey(1978) 탐욕적 알고리즘(매 단계 한계이득이
가장 큰 것을 선택) — 값이 동점(대부분 0)인 구간은 출발지로부터의 거리로
tiebreak(구현 디테일). X축은 "링크 개수" 대신 "누적 길이(m)" 사용
(Jenelius et al. 2006 등 확립된 문헌의 "일반화된 비용" 관행에 맞춤).

지도: 전체 도보망(연회색) + 현재 TCA(검정) + 이미 복구된 핫링크(단색
빨강, 순서는 패널 진행 자체로 표현 — 그라데이션 불필요) + 미복구 핫링크
(연분홍).
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from shapely.geometry import box
import contextily as ctx
import pyproj

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

WALK_SPEED = 4.0*1000/3600
TIME_BUDGET = 15*60
TARGET_CRS = 'EPSG:5186'
PROJ_DIR = '/Users/jin/석사논문/Thermal_Catchment'

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

G = nx.Graph()
edge_geom = {}
node_xy = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    hot = row['UTCI_09'] is not None and row['UTCI_09'] >= 38.0
    G.add_edge(u, v, travel_time=row['LNKG_LEN']/WALK_SPEED, length=row['LNKG_LEN'], hot=hot)
    edge_geom[(u, v)] = row.geometry
    edge_geom[(v, u)] = row.geometry
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

def reachable(graph, origin):
    return set(nx.single_source_dijkstra_path_length(graph, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

def hop_distance_from_origin(G, origin):
    return nx.single_source_shortest_path_length(G, origin)

transformer = pyproj.Transformer.from_crs(TARGET_CRS, 3857, always_xy=True)

for key, name in [('eungbong', '응봉'), ('sungsoo', '성수')]:
    pt = subway[subway['name'] == name].geometry.iloc[0]
    _, i = tree.query([pt.x, pt.y])
    origin = node_ids[i]
    s_classic = reachable(G, origin)
    ca = len(s_classic & opportunity_nodes)

    hop_dist = hop_distance_from_origin(G, origin)  # tiebreak용(전체 그래프 기준 홉 거리)

    G_th_base = G.copy()
    all_hot = [(u, v) for u, v, d in G.edges(data=True) if d['hot']]
    G_th_base.remove_edges_from(all_hot)

    G_work = G_th_base.copy()
    s_current = reachable(G_work, origin)
    tca_now = len(s_current & opportunity_nodes)

    repair_order = []  # (u, v, length, gain_at_selection)
    MAX_STEPS = 400
    for step in range(MAX_STEPS):
        frontier = set()
        for n in s_current:
            for nb in G.neighbors(n):
                if G[n][nb]['hot'] and not G_work.has_edge(n, nb):
                    frontier.add((n, nb))
        if not frontier:
            break
        # 값(이득) 우선, 동점이면 거리(홉) 가까운 순
        best = None
        best_key = None
        for (u, v) in frontier:
            G_work.add_edge(u, v, **G[u][v])
            s_test = reachable(G_work, origin)
            gain = len(s_test & opportunity_nodes) - tca_now
            G_work.remove_edge(u, v)
            dist = min(hop_dist.get(u, 1e9), hop_dist.get(v, 1e9))
            k = (-gain, dist)  # 이득 큰 것 우선(음수로 오름차순 정렬), 동점시 거리 가까운 것 우선
            if best_key is None or k < best_key:
                best_key = k
                best = (u, v, gain)
        u, v, gain = best
        G_work.add_edge(u, v, **G[u][v])
        s_current = reachable(G_work, origin)
        tca_now = len(s_current & opportunity_nodes)
        repair_order.append((u, v, G[u][v]['length'], gain))

    cum_len = np.cumsum([e[2] for e in repair_order]) if repair_order else np.array([])
    total_len = cum_len[-1] if len(cum_len) else 0
    print(f'{name}역: CA={ca}, 탐욕적 복구 {len(repair_order)}단계, 총 길이 {total_len:.0f}m')

    # 스냅샷: 0 / 25% / 50% / 75% / 100% 길이 지점
    targets_pct = [0, 0.25, 0.5, 0.75, 1.0]
    snap_idxs = []
    for p in targets_pct:
        target = total_len * p
        idx_ = int(np.searchsorted(cum_len, target)) if len(cum_len) else 0
        snap_idxs.append(min(idx_, len(repair_order)))

    ox_, oy_ = node_xy[origin]
    cx, cy = transformer.transform(ox_, oy_)
    pad_5186 = 1400
    bbox_5186 = box(ox_ - pad_5186, oy_ - pad_5186, ox_ + pad_5186, oy_ + pad_5186)
    local_edges = api[api.geometry.intersects(bbox_5186)].to_crs(3857)

    rows = []
    fig, axes = plt.subplots(1, len(snap_idxs), figsize=(6*len(snap_idxs), 6.5), dpi=140)
    PAD = 900

    for panel_i, K in enumerate(snap_idxs):
        G_test = G_th_base.copy()
        for (u, v, ln, g) in repair_order[:K]:
            G_test.add_edge(u, v, **G[u][v])
        s_tca = reachable(G_test, origin)
        tca = len(s_tca & opportunity_nodes)
        len_done = cum_len[K-1] if K > 0 else 0
        rows.append({'K_links': K, 'cum_length_m': round(float(len_done), 1),
                      'opp_reachable': tca, 'pct_of_ca': round(tca/max(ca,1)*100, 1)})

        ax = axes[panel_i]
        ax.set_xlim(cx - PAD, cx + PAD)
        ax.set_ylim(cy - PAD, cy + PAD)
        try:
            ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=16, alpha=0.6)
        except Exception:
            pass

        local_edges.plot(ax=ax, color='#d9d9d9', linewidth=0.6, zorder=2)

        tca_edges = [(u, v) for u, v in G_test.edges() if u in s_tca and v in s_tca]
        for u, v in tca_edges:
            geom = edge_geom.get((u, v))
            if geom is None:
                continue
            xs, ys = geom.xy
            xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
            ax.plot(xs3857, ys3857, color='#1a1a1a', linewidth=2.0, zorder=4)

        for rank, (u, v, ln, g) in enumerate(repair_order):
            geom = edge_geom.get((u, v))
            if geom is None:
                continue
            xs, ys = geom.xy
            xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
            if rank < K:
                ax.plot(xs3857, ys3857, color='#d62728', linewidth=2.2, alpha=0.95, zorder=5)
            else:
                ax.plot(xs3857, ys3857, color='#f4a6a6', linewidth=0.8, alpha=0.5, zorder=3)

        ax.scatter([cx], [cy], c='black', s=110, zorder=7, marker='*', edgecolor='white', linewidth=1.2)
        ax.set_axis_off()
        ax.set_title(f'{len_done:.0f}m 개선\n기회 {tca}/{ca} ({tca/max(ca,1)*100:.1f}%)', fontsize=11)

    fig.suptitle(f'{name}역 — 탐욕적(값우선·동점시거리) 병목 링크 복구에 따른 TCA 변화 (09시, UTCI 38°C)\n'
                 f'회색=전체 도보망 / 검정=현재 TCA / 진빨강=복구완료 / 연분홍=미복구 핫링크',
                 fontsize=12)
    plt.tight_layout()
    out_png = f'{PROJ_DIR}/03_Method_C/results/figures/2026-08-04_{key}_greedy_tca_snapshots.png'
    plt.savefig(out_png, dpi=140, bbox_inches='tight', facecolor='white')
    plt.close()
    print('저장:', out_png)

    df = pd.DataFrame(rows)
    df['ca'] = ca
    out_csv = f'{PROJ_DIR}/03_Method_C/results/2026-08-04_{key}_greedy_dose_response.csv'
    df.to_csv(out_csv, index=False, encoding='utf-8-sig')
    print(df.to_string())
