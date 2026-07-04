"""
작성일: 2026-07-03
버전: v2.0
목적: Method C (SOLWEIG 30m DSM) Classic vs Thermal Catchment 비교 지도
      응봉역 / 성수역 — 파일럿 지도학회 발표와 동일 대상 + 시각화 스타일
근거: 파일럿 65_catchment_contrast_map.py 스타일 준용
변경(v2): ox.load_graphml → nx.read_graphml + geopandas 직접 처리
"""
import os, warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer
from shapely.geometry import LineString, Point
warnings.filterwarnings('ignore')

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

SCRATCH    = "/private/tmp/claude-501/-Users-jin------TAVI/11a7aa5d-485a-4d32-8032-faf31923985e/scratchpad"
OUT_DIR    = SCRATCH + "/link_mrt_seongdong"
FIG_DIR    = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results"
NET_PATH   = "/Users/jin/석사논문/성동구_STP연구/01_네트워크/seongdong_walk_network.graphml"
MRT_CSV    = OUT_DIR + "/link_mrt_method_c.csv"
os.makedirs(FIG_DIR, exist_ok=True)

WALK_SPEED    = 4.5 * 1000 / 3600
TIME_BUDGET   = 15 * 60
MRT_THRESHOLD = 56.0

TARGETS = {
    'eungbong': {
        'net_node': '7838649561',
        'label':    '응봉역 인근',
        'out':      '2026-07-03_catchment_contrast_eungbong_methodC.png',
    },
    'sungsoo': {
        'net_node': '436855717',
        'label':    '성수역 인근',
        'out':      '2026-07-03_catchment_contrast_sungsoo_methodC.png',
    },
}

# ── 네트워크 로드
print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
wgs2wm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

for u, v, d in G.edges(data=True):
    d['travel_time'] = float(d.get('length', 0)) / WALK_SPEED

# ── MRT CSV 로드 → hot_edges
print("Method C MRT 로드...")
mrt_df = pd.read_csv(MRT_CSV)
hot_edges = set()
for _, row in mrt_df.dropna(subset=['mrt']).iterrows():
    if row['mrt'] >= MRT_THRESHOLD:
        hot_edges.add((str(int(float(row['u']))), str(int(float(row['v'])))))
        hot_edges.add((str(int(float(row['v']))), str(int(float(row['u'])))))
print(f"  Hard Cut 링크: {len(hot_edges)//2:,}개")

# ── GeoDataFrame 빌드 (EPSG:3857)
print("GeoDataFrame 빌드...")
edge_rows = []
for u, v, d in G.edges(data=True):
    un, vn = G.nodes[u], G.nodes[v]
    ux, uy = wgs2wm.transform(float(un['x']), float(un['y']))
    vx, vy = wgs2wm.transform(float(vn['x']), float(vn['y']))
    edge_rows.append({'u': u, 'v': v, 'geometry': LineString([(ux, uy), (vx, vy)])})
edges_gdf = gpd.GeoDataFrame(edge_rows, crs="EPSG:3857")

node_rows = []
for nid, attrs in G.nodes(data=True):
    nx_, ny_ = wgs2wm.transform(float(attrs['x']), float(attrs['y']))
    node_rows.append({'nid': nid, 'geometry': Point(nx_, ny_)})
nodes_gdf = gpd.GeoDataFrame(node_rows, crs="EPSG:3857").set_index('nid')

# ── Catchment 계산
def compute_catchment(origin_node):
    classic = set(nx.single_source_dijkstra_path_length(
        G, origin_node, cutoff=TIME_BUDGET, weight='travel_time'
    ).keys())
    G_th = G.copy()
    remove = [(u, v) for u, v in G_th.edges()
              if (str(u), str(v)) in hot_edges]
    G_th.remove_edges_from(remove)
    for u, v, d in G_th.edges(data=True):
        d['travel_time'] = float(d.get('length', 0)) / WALK_SPEED
    thermal = set(nx.single_source_dijkstra_path_length(
        G_th, origin_node, cutoff=TIME_BUDGET, weight='travel_time'
    ).keys())
    return classic, thermal

# ── 지도 생성
def make_map(target_key):
    cfg = TARGETS[target_key]
    origin = cfg['net_node']
    print(f"\n[{cfg['label']}]")

    classic, thermal = compute_catchment(origin)
    lost = classic - thermal
    reduction = len(lost) / max(len(classic), 1) * 100
    print(f"  Classic: {len(classic):,} / Thermal: {len(thermal):,} / 감소율: {reduction:.1f}%")

    def classify(row):
        u, v = str(row['u']), str(row['v'])
        in_cl = (u in classic)  and (v in classic)
        in_th = (u in thermal)  and (v in thermal)
        if in_th:   return 'thermal'
        elif in_cl: return 'lost'
        else:       return 'outside'

    edges_gdf['etype'] = edges_gdf.apply(classify, axis=1)

    ox_node = nodes_gdf.loc[origin]
    cx, cy  = ox_node.geometry.x, ox_node.geometry.y
    PAD     = 1600
    xlim = (cx - PAD, cx + PAD)
    ylim = (cy - PAD, cy + PAD)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    try:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=15, alpha=0.65)
    except Exception as e:
        print(f"  베이스맵 오류 (무시): {e}")

    e_lost    = edges_gdf[edges_gdf['etype'] == 'lost']
    e_thermal = edges_gdf[edges_gdf['etype'] == 'thermal']
    if not e_lost.empty:
        e_lost.plot(ax=ax, color='#E53935', linewidth=1.6, alpha=0.9, zorder=4)
    if not e_thermal.empty:
        e_thermal.plot(ax=ax, color='#43A047', linewidth=1.6, alpha=0.9, zorder=3)

    ax.scatter([cx], [cy], c='#212121', s=80, zorder=6)
    ax.annotate(
        f"{cfg['label']}\nClassic: {len(classic):,} nodes\n"
        f"Thermal: {len(thermal):,} nodes\n감소율: {reduction:.1f}%",
        xy=(0.03, 0.97), xycoords='axes fraction',
        va='top', ha='left', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.85), zorder=7
    )
    ax.set_axis_off()
    plt.tight_layout(pad=0)
    out_path = os.path.join(FIG_DIR, cfg['out'])
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  저장: {out_path}")
    return {
        'station': cfg['label'], 'method': 'Method_C_SOLWEIG30m',
        'classic_nodes': len(classic), 'thermal_nodes': len(thermal),
        'lost_nodes': len(lost), 'reduction_pct': round(reduction, 1),
    }

results = [make_map(k) for k in TARGETS]

pd.DataFrame(results).to_csv(
    FIG_DIR + '/2026-07-03_catchment_summary_method_c.csv', index=False
)
print("\n=== 완료 ===")
for r in results:
    print(f"  {r['station']}: {r['classic_nodes']:,} → {r['thermal_nodes']:,} "
          f"(감소율 {r['reduction_pct']}%)")
