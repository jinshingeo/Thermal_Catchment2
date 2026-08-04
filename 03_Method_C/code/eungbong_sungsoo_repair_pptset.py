"""
응봉역·성수역 — 탐욕적(값 우선, 동점시 거리) 병목 링크 복구 시각화, PPT 조합용
================================================================
근거: Nemhauser, Fisher & Wolsey(1978) 탐욕적 알고리즘. X축은 "누적 길이(m)"
(Jenelius et al. 2006 등의 "일반화된 비용" 관행에 맞춤).

eungbong_sungsoo_greedy_tca_snapshots.py 와 동일한 탐욕적 복구 로직을 사용하되,
출력을 하나의 합성 그림이 아니라 지도 낱장 + 효용곡선 + 범례로 분리해서 저장
(사용자가 PPT에서 직접 조합할 예정).

지도 레이어(아래→위): CA(연회색, 출발지 15분 전체 도달권) → 현재 TCA(검정) →
잔여 핫링크(빨강) → 이번에 복구된 링크(파랑) → 출발지(별)
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.spatial import cKDTree
import contextily as ctx
import pyproj

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

WALK_SPEED = 4.0*1000/3600
TIME_BUDGET = 15*60
TARGET_CRS = 'EPSG:5186'
PROJ_DIR = '/Users/jin/석사논문/Thermal_Catchment'
OUT_DIR = f'{PROJ_DIR}/03_Method_C/results/figures/2026-08-04_bottleneck_repair_pptset'

COL_CA = '#c9c9c9'
COL_TCA = '#1a1a1a'
COL_HOT = '#d62728'
COL_FIXED = '#1f5fd6'

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

curve_rows = []

for key, name in [('eungbong', '응봉'), ('sungsoo', '성수')]:
    pt = subway[subway['name'] == name].geometry.iloc[0]
    _, i = tree.query([pt.x, pt.y])
    origin = node_ids[i]
    s_classic = reachable(G, origin)
    ca = len(s_classic & opportunity_nodes)

    hop_dist = hop_distance_from_origin(G, origin)

    G_th_base = G.copy()
    all_hot = [(u, v) for u, v, d in G.edges(data=True) if d['hot']]
    G_th_base.remove_edges_from(all_hot)

    # CA 범위 내 핫링크(양끝 노드가 모두 classic 도달권 안) — 지도에 표시할 "잔여 핫링크" 전체 후보
    hot_in_ca = [(u, v) for (u, v) in all_hot if u in s_classic and v in s_classic]

    G_work = G_th_base.copy()
    s_current = reachable(G_work, origin)
    tca_now = len(s_current & opportunity_nodes)

    repair_order = []
    MAX_STEPS = 400
    for step in range(MAX_STEPS):
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
        repair_order.append((u, v, G[u][v]['length'], gain))

    cum_len = np.cumsum([e[2] for e in repair_order]) if repair_order else np.array([])
    total_len = cum_len[-1] if len(cum_len) else 0
    print(f'{name}역: CA={ca}, 탐욕적 복구 {len(repair_order)}단계, 총 길이 {total_len:.0f}m')

    # 효용곡선용: 매 단계 기록(부드러운 곡선)
    tca_track = [tca_now]
    G_track = G_th_base.copy()
    tca_running = len(reachable(G_track, origin) & opportunity_nodes)
    step_tca = [tca_running]
    for (u, v, ln, g) in repair_order:
        G_track.add_edge(u, v, **G[u][v])
        step_tca.append(step_tca[-1] + g)
    for K in range(len(repair_order) + 1):
        length_done = cum_len[K-1] if K > 0 else 0.0
        curve_rows.append({'station': name, 'K_links': K, 'cum_length_m': round(float(length_done), 1),
                            'opp_reachable': step_tca[K], 'pct_of_ca': round(step_tca[K]/max(ca,1)*100, 1), 'ca': ca})

    # 스냅샷: 0 / 25% / 50% / 75% / 100% 길이 지점
    targets_pct = [0, 0.25, 0.5, 0.75, 1.0]
    snap_idxs = []
    for p in targets_pct:
        target = total_len * p
        idx_ = int(np.searchsorted(cum_len, target)) if len(cum_len) else 0
        snap_idxs.append(min(idx_, len(repair_order)))

    ox_, oy_ = node_xy[origin]
    cx, cy = transformer.transform(ox_, oy_)

    # CA 지오메트리(베이스 레이어): 양끝 노드가 모두 classic 도달권 안인 엣지
    ca_pairs = [(u, v) for u, v in G.edges() if u in s_classic and v in s_classic]

    for panel_i, K in enumerate(snap_idxs):
        G_test = G_th_base.copy()
        for (u, v, ln, g) in repair_order[:K]:
            G_test.add_edge(u, v, **G[u][v])
        s_tca = reachable(G_test, origin)
        tca = len(s_tca & opportunity_nodes)
        len_done = cum_len[K-1] if K > 0 else 0
        pct = round(tca/max(ca,1)*100, 1)

        repaired_set = set(repair_order[j][:2] for j in range(K)) | set((v, u) for u, v, l, g in repair_order[:K])

        fig, ax = plt.subplots(figsize=(7, 7), dpi=150)
        PAD = 900
        ax.set_xlim(cx - PAD, cx + PAD)
        ax.set_ylim(cy - PAD, cy + PAD)
        try:
            ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=16, alpha=0.6)
        except Exception:
            pass

        # 1) CA 베이스 레이어(연회색)
        for u, v in ca_pairs:
            geom = edge_geom.get((u, v))
            if geom is None:
                continue
            xs, ys = geom.xy
            xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
            ax.plot(xs3857, ys3857, color=COL_CA, linewidth=0.7, zorder=2)

        # 2) 잔여 핫링크(빨강) — 아직 복구 안 된 것만
        for u, v in hot_in_ca:
            if (u, v) in repaired_set:
                continue
            geom = edge_geom.get((u, v))
            if geom is None:
                continue
            xs, ys = geom.xy
            xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
            ax.plot(xs3857, ys3857, color=COL_HOT, linewidth=1.3, alpha=0.9, zorder=3)

        # 3) 현재 TCA(검정) — 도달가능 서브그래프
        for u, v in G_test.edges():
            if u in s_tca and v in s_tca:
                geom = edge_geom.get((u, v))
                if geom is None:
                    continue
                xs, ys = geom.xy
                xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
                ax.plot(xs3857, ys3857, color=COL_TCA, linewidth=1.8, zorder=4)

        # 4) 이번에 복구된 링크(파랑) — 검정 위에 강조
        for j in range(K):
            u, v, ln, g = repair_order[j]
            geom = edge_geom.get((u, v))
            if geom is None:
                continue
            xs, ys = geom.xy
            xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
            ax.plot(xs3857, ys3857, color=COL_FIXED, linewidth=2.2, zorder=5)

        ax.scatter([cx], [cy], c='black', s=130, zorder=7, marker='*', edgecolor='white', linewidth=1.2)
        ax.set_axis_off()
        ax.annotate(f'{len_done:,.0f}m 복구 / 기회 {tca}/{ca} ({pct}%)',
                    xy=(0.03, 0.03), xycoords='axes fraction', fontsize=11, fontweight='bold',
                    va='bottom', ha='left', bbox=dict(boxstyle='round,pad=0.35', fc='white', alpha=0.85), zorder=8)

        plt.tight_layout(pad=0.2)
        out_map = f'{OUT_DIR}/{key}_map_{panel_i}_{int(targets_pct[panel_i]*100)}pct.png'
        plt.savefig(out_map, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        print('저장:', out_map)

df_curve = pd.DataFrame(curve_rows)
df_curve.to_csv(f'{OUT_DIR}/dose_response_data.csv', index=False, encoding='utf-8-sig')

# ── 효용곡선(따로) ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
colors = {'응봉': '#C3450F', '성수': '#1C5C82'}
for name, g in df_curve.groupby('station'):
    ax.plot(g['cum_length_m'], g['pct_of_ca'], color=colors[name], linewidth=2, label=f'{name}역 (CA={g["ca"].iloc[0]})')
ax.set_xlabel('누적 복구 길이 (m)')
ax.set_ylabel('Classic Catchment 대비 회복 비율 (%)')
ax.set_title('응봉역·성수역 — 병목 링크 복구에 따른 접근성 회복 곡선\n(09시, UTCI 38°C 기준, 탐욕적 순서)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
out_curve = f'{OUT_DIR}/dose_response_curve.png'
plt.savefig(out_curve, dpi=150, facecolor='white')
plt.close()
print('저장:', out_curve)

# ── 범례(따로) ───────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(4.5, 2.3), dpi=150)
ax.set_axis_off()
handles = [
    Line2D([0], [0], color=COL_CA, linewidth=3, label='CA (출발지 15분 전체 도달권)'),
    Line2D([0], [0], color=COL_TCA, linewidth=3, label='TCA (현재 도달가능 구간)'),
    Line2D([0], [0], color=COL_HOT, linewidth=3, label='잔여 핫링크 (UTCI ≥38°C)'),
    Line2D([0], [0], color=COL_FIXED, linewidth=3, label='복구된 링크'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='black', markeredgecolor='white', markersize=14, label='출발지(역)'),
]
ax.legend(handles=handles, loc='center', frameon=False, fontsize=11)
plt.tight_layout()
out_legend = f'{OUT_DIR}/legend.png'
plt.savefig(out_legend, dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
print('저장:', out_legend)
print('완료')
