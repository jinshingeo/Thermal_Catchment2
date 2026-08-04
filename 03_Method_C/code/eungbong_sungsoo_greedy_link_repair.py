"""
응봉역·성수역 파일럿 — 탐욕적 병목 링크 순차 복구 (Greedy Link Repair)
================================================================
근거: Jenelius, Petersen & Mattsson(2006)의 링크 중요도 개념을, 이전 시도
      (출발지 1홉 이내로 한정)의 한계를 넘어 확장 적용 — 매 단계마다 현재
      도달가능 경계(frontier)에 닿은 핫링크를 전부 후보로 검토하고, 가장
      회복 효과가 큰 링크 하나를 골라 복구, 그 다음 새로 열린 경계에서
      다시 반복(탐욕적/greedy). 응봉역·성수역 2개 지점으로 범위를 좁혀
      전체 서울 대신 가볍게 실행.
시간대: 09시, 임계값 38°C (기존 §5.3.2·§5.4.3과 동일 조건)
"""
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

WALK_SPEED = 4.0 * 1000 / 3600
TIME_BUDGET = 15 * 60
THRESHOLD = 38.0
HOUR = '09'
TARGET_CRS = 'EPSG:5186'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
API_NET = f'{PROJ}/data/network/2026-08-02_seoul_walk_api_network.gpkg'
OSM_RESULT = f'{PROJ}/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg'
SUBWAY_GPKG = f'{PROJ}/data/facilities/seoul_subway_stations.gpkg'
GTFS_STOPS = '/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/gtfs_KTDB/stops.txt'
OUT_DIR = f'{PROJ}/03_Method_C/results'

t0 = time.time()
def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)

log("네트워크 로드 및 09시 UTCI 매칭...")
api = gpd.read_file(API_NET)
api = api[api['LNKG_TYPE_CD'].str.startswith('1')].copy()
api = api.to_crs(TARGET_CRS)
api['LNKG_LEN'] = api['LNKG_LEN'].astype(float)
api = api[api['LNKG_LEN'] > 0].copy()

osm = gpd.read_file(OSM_RESULT)
col = f'UTCI_{HOUR}'
api['centroid'] = api.geometry.centroid
api_pts = gpd.GeoDataFrame(api[['LNKG_ID']], geometry=api['centroid'], crs=TARGET_CRS)
joined = gpd.sjoin_nearest(api_pts, osm[[col, 'geometry']], how='left', distance_col='dist_m')
joined = joined.drop_duplicates(subset='LNKG_ID')
api = api.merge(joined[['LNKG_ID', col]], on='LNKG_ID', how='left')
api = api.drop(columns='centroid')

log("그래프 구성...")
G = nx.Graph()
node_xy = {}
edge_geom = {}
for _, row in api.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    hot = row[col] is not None and row[col] >= THRESHOLD
    G.add_edge(u, v, travel_time=row['LNKG_LEN'] / WALK_SPEED, utci=row[col], hot=hot)
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]
    node_xy[v] = coords[-1]
    edge_geom[(u, v)] = row.geometry
    edge_geom[(v, u)] = row.geometry
log(f"  노드 {G.number_of_nodes():,} / 엣지 {G.number_of_edges():,}")

node_ids = list(node_xy.keys())
node_xy_arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(node_xy_arr)

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

G_thermal_base = G.copy()
hot_edges_all = [(u, v) for u, v, d in G.edges(data=True) if d['hot']]
G_thermal_base.remove_edges_from(hot_edges_all)
log(f"  핫링크 {len(hot_edges_all):,}개 제거 완료(09시 38도 기준)")

def reachable(graph, origin):
    return set(nx.single_source_dijkstra_path_length(graph, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

targets = {}
for key, name in [('eungbong', '응봉'), ('sungsoo', '성수')]:
    pt = subway[subway['name'] == name].geometry.iloc[0]
    _, i = tree.query([pt.x, pt.y])
    targets[key] = {'node': node_ids[i], 'label': f'{name}역'}

results_all = {}
for key, cfg in targets.items():
    origin = cfg['node']
    log(f"[{cfg['label']}] 탐욕적 복구 시작...")
    s_classic = reachable(G, origin)
    ca = len(s_classic & opportunity_nodes)

    G_work = G_thermal_base.copy()
    s_current = reachable(G_work, origin)
    tca0 = len(s_current & opportunity_nodes)

    steps = [{'step': 0, 'link': None, 'cum_opp': tca0, 'cum_pct_of_ca': round(tca0 / max(ca, 1) * 100, 1)}]
    repaired_edges = []

    for step in range(1, 31):  # 최대 30단계
        # 현재 도달가능 경계에 닿은 핫링크 후보 전부 탐색
        frontier = set()
        for n in s_current:
            for nb in G.neighbors(n):
                if G[n][nb]['hot'] and not G_work.has_edge(n, nb):
                    frontier.add((n, nb))
        if not frontier:
            break
        best = None
        best_gain = 0
        for (u, v) in frontier:
            G_work.add_edge(u, v, **G[u][v])
            s_test = reachable(G_work, origin)
            gain = len(s_test & opportunity_nodes) - len(s_current & opportunity_nodes)
            G_work.remove_edge(u, v)
            if gain > best_gain:
                best_gain = gain
                best = (u, v)
        if best is None or best_gain <= 0:
            break
        G_work.add_edge(*best, **G[best[0]][best[1]])
        s_current = reachable(G_work, origin)
        cum_opp = len(s_current & opportunity_nodes)
        repaired_edges.append(best)
        steps.append({'step': step, 'link': f'{best[0]}-{best[1]}', 'opp_gain_this_step': best_gain,
                       'cum_opp': cum_opp, 'cum_pct_of_ca': round(cum_opp / max(ca, 1) * 100, 1)})
        log(f"  step {step}: 링크 {best} 복구 -> +{best_gain} (누적 {cum_opp}/{ca}, {cum_opp/max(ca,1)*100:.1f}%)")

    df = pd.DataFrame(steps)
    df['ca'] = ca
    out_csv = f'{OUT_DIR}/2026-08-04_{key}_greedy_link_repair.csv'
    df.to_csv(out_csv, index=False, encoding='utf-8-sig')
    log(f"  저장: {out_csv} (CA={ca}, 초기 TCA={tca0}, {len(repaired_edges)}단계 후 {cum_opp if steps[-1]['step']>0 else tca0})")
    results_all[key] = {'df': df, 'ca': ca, 'label': cfg['label'], 'repaired_edges': repaired_edges}

# ── 시각화: 두 지점 회복 곡선 비교 ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
colors = {'eungbong': '#C3450F', 'sungsoo': '#1C5C82'}
for key, r in results_all.items():
    ax.plot(r['df']['step'], r['df']['cum_pct_of_ca'], marker='o', markersize=3,
            color=colors[key], label=f"{r['label']} (CA={r['ca']})")
ax.set_xlabel('복구한 병목 링크 수 (탐욕적 순서)')
ax.set_ylabel('Classic Catchment 대비 회복 비율 (%)')
ax.set_title('응봉역·성수역 — 탐욕적 병목 링크 복구에 따른 접근성 회복\n(09시, UTCI 38°C 기준)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
out_png = f'{OUT_DIR}/figures/2026-08-04_eungbong_sungsoo_greedy_repair_curve.png'
plt.savefig(out_png, dpi=150, facecolor='white')
log(f"저장: {out_png}")

# ── 시각화: 지도 — 복구 순서대로 링크 강조 ──────────────────────────────────
import contextily as ctx
import pyproj
transformer = pyproj.Transformer.from_crs(TARGET_CRS, 3857, always_xy=True)

for key, r in results_all.items():
    origin = targets[key]['node']
    ox_, oy_ = node_xy[origin]
    cx, cy = transformer.transform(ox_, oy_)
    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    PAD = 1200
    ax.set_xlim(cx - PAD, cx + PAD)
    ax.set_ylim(cy - PAD, cy + PAD)
    try:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=16, alpha=0.7)
    except Exception as e:
        log(f"  베이스맵 오류(무시): {e}")

    n_repaired = len(r['repaired_edges'])
    cmap = plt.cm.autumn_r
    for i, (u, v) in enumerate(r['repaired_edges']):
        geom = edge_geom.get((u, v))
        if geom is None:
            continue
        xs, ys = geom.xy
        xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
        color = cmap((i + 1) / max(n_repaired, 1))
        ax.plot(xs3857, ys3857, color=color, linewidth=3, zorder=5)
        mx, my = transformer.transform(*geom.centroid.coords[0])
        ax.annotate(str(i + 1), (mx, my), fontsize=8, fontweight='bold', zorder=6,
                    bbox=dict(boxstyle='circle,pad=0.15', fc='white', ec='none', alpha=0.8))

    ax.scatter([cx], [cy], c='#212121', s=100, zorder=7, edgecolor='white')
    ax.annotate(f"{r['label']}\nCA={r['ca']}, {n_repaired}개 링크로\n{r['df'].iloc[-1]['cum_pct_of_ca']:.1f}% 회복",
                xy=(0.03, 0.97), xycoords='axes fraction', va='top', ha='left', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.85), zorder=8)
    ax.set_axis_off()
    plt.tight_layout(pad=0)
    out_map = f'{OUT_DIR}/figures/2026-08-04_{key}_greedy_repair_map.png'
    plt.savefig(out_map, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    log(f"저장: {out_map}")

log("완료")
