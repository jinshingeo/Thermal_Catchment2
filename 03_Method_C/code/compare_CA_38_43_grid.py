"""
CA(무보정) vs Hard Cut 42.7°C vs Hard Cut 38°C — 3x3 그리드 비교
================================================================
행: CA(Hard Cut 없음) / 42.7°C TCA / 38°C TCA
열: 아침(09시) / 정오(13시) / 오후(17시)
실제 도로 형상(geometry)을 살려서 그림.
"""
import os
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer
from shapely import wkt
from shapely.geometry import LineString, Point
warnings.filterwarnings('ignore')

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

FIG_DIR = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_hardcut_38_vs_43"
os.makedirs(FIG_DIR, exist_ok=True)
NET_PATH = "/Users/jin/석사논문/성동구_STP연구/01_네트워크/seongdong_walk_network.graphml"
UTCI_GPKG = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg"

WALK_SPEED = 4.5 * 1000 / 3600
TIME_BUDGET = 15 * 60
THR_A = 38.0
THR_B = 42.7
HOURS = [(h, f'{h:02d}시') for h in range(6, 20)]

TARGETS = {
    'eungbong': {'net_node': '7838649561', 'label': '응봉역 인근'},
    'sungsoo': {'net_node': '436855717', 'label': '성수역 인근'},
}

print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
wgs2wm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
for u, v, d in G.edges(data=True):
    d['travel_time'] = float(d.get('length', 0)) / WALK_SPEED

node_rows = []
for nid, attrs in G.nodes(data=True):
    nx_, ny_ = wgs2wm.transform(float(attrs['x']), float(attrs['y']))
    node_rows.append({'nid': nid, 'geometry': Point(nx_, ny_)})
nodes_gdf = gpd.GeoDataFrame(node_rows, crs="EPSG:3857").set_index('nid')

# 실제 도로 형상(geometry) 살려서 엣지 GeoDataFrame 구성
edge_rows = []
for u, v, d in G.edges(data=True):
    geom_wkt = d.get('geometry')
    if geom_wkt:
        try:
            line_wgs = wkt.loads(geom_wkt)
            coords_wm = [wgs2wm.transform(x, y) for x, y in line_wgs.coords]
            geom = LineString(coords_wm)
        except Exception:
            geom = None
    else:
        geom = None
    if geom is None:
        un, vn = G.nodes[u], G.nodes[v]
        ux, uy = wgs2wm.transform(float(un['x']), float(un['y']))
        vx, vy = wgs2wm.transform(float(vn['x']), float(vn['y']))
        geom = LineString([(ux, uy), (vx, vy)])
    edge_rows.append({'u': u, 'v': v, 'geometry': geom})
edges_gdf = gpd.GeoDataFrame(edge_rows, crs="EPSG:3857")
print(f"  엣지 {len(edges_gdf)}개 (geometry 보유: {sum(1 for d in G.edges(data=True) if d[2].get('geometry'))}개)")

print("UTCI 링크 데이터 로드...")
utci_gdf = gpd.read_file(UTCI_GPKG)
utci_gdf['u'] = utci_gdf['u'].astype(str)
utci_gdf['v'] = utci_gdf['v'].astype(str)

REACH_COLOR = '#1565C0'
BG_COLOR = '#D0D0D0'

for key, cfg in TARGETS.items():
    origin = cfg['net_node']
    if origin not in G:
        print(f"[경고] {cfg['label']} 없음 — 스킵")
        continue

    n_cols = len(HOURS)
    fig, axes = plt.subplots(3, n_cols, figsize=(3.2 * n_cols, 10.5), dpi=150)
    row_labels = ['CA (Hard Cut 없음)', 'TCA — Hard Cut 42.7°C', 'TCA — Hard Cut 38°C']

    ox_node = nodes_gdf.loc[origin]
    cx, cy = ox_node.geometry.x, ox_node.geometry.y
    PAD = 1600

    for col_idx, (hour, hour_label) in enumerate(HOURS):
        col = f'UTCI_{hour:02d}'
        utci_lookup = {}
        for _, row in utci_gdf.dropna(subset=[col]).iterrows():
            u, v, val = row['u'], row['v'], row[col]
            utci_lookup[(u, v)] = val
            utci_lookup[(v, u)] = val
        for u, v, d in G.edges(data=True):
            d['utci'] = utci_lookup.get((u, v), np.nan)

        G_ca = G  # Hard Cut 없음(원본)
        G_a = G.copy()
        G_a.remove_edges_from([(u, v) for u, v, d in G_a.edges(data=True)
                                if not np.isnan(d['utci']) and d['utci'] >= THR_B])  # 42.7
        G_b = G.copy()
        G_b.remove_edges_from([(u, v) for u, v, d in G_b.edges(data=True)
                                if not np.isnan(d['utci']) and d['utci'] >= THR_A])  # 38

        graphs = [G_ca, G_a, G_b]

        for row_idx, GG in enumerate(graphs):
            ax = axes[row_idx, col_idx]
            ax.set_xlim(cx - PAD, cx + PAD)
            ax.set_ylim(cy - PAD, cy + PAD)
            try:
                ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=15, alpha=0.5)
            except Exception:
                pass

            edges_gdf.plot(ax=ax, color=BG_COLOR, linewidth=0.8, alpha=0.7, zorder=2)

            reach_nodes = set(nx.single_source_dijkstra_path_length(
                GG, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

            def is_reach(r):
                return (r['u'] in reach_nodes) and (r['v'] in reach_nodes)

            mask = edges_gdf.apply(is_reach, axis=1)
            e_reach = edges_gdf[mask]
            if not e_reach.empty:
                e_reach.plot(ax=ax, color=REACH_COLOR, linewidth=1.8, alpha=0.95, zorder=3)

            ax.scatter([cx], [cy], c='#212121', s=60, zorder=6)
            ax.set_axis_off()
            if row_idx == 0:
                ax.set_title(hour_label, fontsize=12)
            if col_idx == 0:
                ax.text(-0.05, 0.5, row_labels[row_idx], transform=ax.transAxes,
                         rotation=90, va='center', ha='center', fontsize=11)
            ax.annotate(f"{len(reach_nodes):,}", xy=(0.05, 0.05), xycoords='axes fraction',
                        fontsize=8, bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.85))

    from matplotlib.patches import Patch
    legend_elems = [Patch(facecolor=REACH_COLOR, label='도달 가능 영역 (15분 예산)'),
                    Patch(facecolor=BG_COLOR, label='전체 도보망')]
    fig.legend(handles=legend_elems, loc='lower center', ncol=2, fontsize=11, bbox_to_anchor=(0.5, -0.01))
    fig.suptitle(f"{cfg['label']} — CA vs Hard Cut TCA (38°C / 42.7°C) 시간대별 비교", fontsize=14)
    plt.tight_layout(rect=[0.02, 0.02, 1, 0.97])
    out_path = os.path.join(FIG_DIR, f'2026-07-29_{key}_CA_vs_38_vs_42-7_grid_allhours.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"저장: {out_path}")
