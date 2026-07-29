"""
시간대별(06~19시) 링크별 UTCI 실측값 지도 — 1도 단위 구간 색상
행: 응봉역(위) / 성수역(아래)   열: 06시~19시
"""
import os
import warnings
import numpy as np
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.colors import BoundaryNorm
from matplotlib.cm import ScalarMappable
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

HOURS = [(h, f'{h:02d}시') for h in range(6, 20)]
TARGETS = {
    'eungbong': {'net_node': '7838649561', 'label': '응봉역 인근'},
    'sungsoo': {'net_node': '436855717', 'label': '성수역 인근'},
}

print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
wgs2wm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

node_rows = []
for nid, attrs in G.nodes(data=True):
    nx_, ny_ = wgs2wm.transform(float(attrs['x']), float(attrs['y']))
    node_rows.append({'nid': nid, 'geometry': Point(nx_, ny_)})
nodes_gdf = gpd.GeoDataFrame(node_rows, crs="EPSG:3857").set_index('nid')

edge_rows = []
for u, v, d in G.edges(data=True):
    geom_wkt = d.get('geometry')
    geom = None
    if geom_wkt:
        try:
            line_wgs = wkt.loads(geom_wkt)
            coords_wm = [wgs2wm.transform(x, y) for x, y in line_wgs.coords]
            geom = LineString(coords_wm)
        except Exception:
            geom = None
    if geom is None:
        un, vn = G.nodes[u], G.nodes[v]
        ux, uy = wgs2wm.transform(float(un['x']), float(un['y']))
        vx, vy = wgs2wm.transform(float(vn['x']), float(vn['y']))
        geom = LineString([(ux, uy), (vx, vy)])
    edge_rows.append({'u': u, 'v': v, 'geometry': geom})
edges_gdf = gpd.GeoDataFrame(edge_rows, crs="EPSG:3857")

print("UTCI 링크 데이터 로드...")
utci_gdf = gpd.read_file(UTCI_GPKG)
utci_gdf['u'] = utci_gdf['u'].astype(str)
utci_gdf['v'] = utci_gdf['v'].astype(str)

# 1도 단위 구간 (전체 시간대 실측 범위 기준: 30~46도)
BINS = np.arange(30, 47, 1)
cmap = matplotlib.colormaps['RdYlBu_r'].resampled(len(BINS) - 1)
norm = BoundaryNorm(BINS, cmap.N)
BG_COLOR = '#D0D0D0'

n_cols = len(HOURS)
n_rows = len(TARGETS)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(3.2 * n_cols, 3.4 * n_rows), dpi=150)

for row_idx, (key, cfg) in enumerate(TARGETS.items()):
    origin = cfg['net_node']
    ox_node = nodes_gdf.loc[origin]
    cx, cy = ox_node.geometry.x, ox_node.geometry.y
    PAD = 1600

    for col_idx, (hour, hour_label) in enumerate(HOURS):
        ax = axes[row_idx, col_idx]
        col = f'UTCI_{hour:02d}'
        utci_lookup = {}
        for _, row in utci_gdf.dropna(subset=[col]).iterrows():
            u, v, val = row['u'], row['v'], row[col]
            utci_lookup[(u, v)] = val
            utci_lookup[(v, u)] = val

        edges_gdf['utci_val'] = edges_gdf.apply(
            lambda r: utci_lookup.get((r['u'], r['v']), np.nan), axis=1)

        ax.set_xlim(cx - PAD, cx + PAD)
        ax.set_ylim(cy - PAD, cy + PAD)
        try:
            ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=15, alpha=0.5)
        except Exception:
            pass

        e_bg = edges_gdf[edges_gdf['utci_val'].isna()]
        if not e_bg.empty:
            e_bg.plot(ax=ax, color=BG_COLOR, linewidth=0.6, alpha=0.6, zorder=2)
        e_val = edges_gdf[edges_gdf['utci_val'].notna()]
        if not e_val.empty:
            e_val.plot(ax=ax, column='utci_val', cmap=cmap, norm=norm, linewidth=1.6, zorder=3)

        ax.scatter([cx], [cy], c='#212121', s=40, zorder=6)
        ax.set_axis_off()
        if row_idx == 0:
            ax.set_title(hour_label, fontsize=12)
        if col_idx == 0:
            ax.text(-0.05, 0.5, cfg['label'], transform=ax.transAxes,
                     rotation=90, va='center', ha='center', fontsize=11)

sm = ScalarMappable(norm=norm, cmap=cmap)
cbar_ax = fig.add_axes([0.15, 0.03, 0.7, 0.015])
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal', ticks=BINS)
cbar.set_label('UTCI (°C, 1도 단위 구간)')

fig.suptitle("응봉역·성수역 — 시간대별 링크 UTCI 실측값 (06~19시)", fontsize=14)
plt.tight_layout(rect=[0.02, 0.06, 1, 0.96])
plt.subplots_adjust(hspace=0.25)
out_path = os.path.join(FIG_DIR, '2026-07-29_utci_links_grid_allhours.png')
plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"저장: {out_path}")
