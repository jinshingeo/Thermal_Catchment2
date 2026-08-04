"""
응봉역·성수역 — 병목 링크 BFS 복구 순서 지도 시각화
================================================================
용량-반응 분석에서 쓴 BFS 순서(출발지에서 가까운 순으로 핫링크 수집)를
지도로 시각화 — 색이 진할수록(=색상값 낮을수록) 먼저 복구되는(가까운)
링크, 밝을수록 늦게(멀리) 복구되는 링크. "벽의 두께"를 시각적으로 표현.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from scipy.spatial import cKDTree
from collections import deque
import contextily as ctx
import pyproj

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

WALK_SPEED = 4.0*1000/3600
TARGET_CRS = 'EPSG:5186'
PROJ_DIR = '/Users/jin/석사논문/Thermal_Catchment'
MAX_K = 300

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
    G.add_edge(u, v, hot=hot)
    edge_geom[(u, v)] = row.geometry
    edge_geom[(v, u)] = row.geometry
    coords = list(row.geometry.coords)
    node_xy[u] = coords[0]; node_xy[v] = coords[-1]

node_ids = list(node_xy.keys())
arr = np.array([node_xy[n] for n in node_ids])
tree = cKDTree(arr)
subway = gpd.read_file(f'{PROJ_DIR}/data/facilities/seoul_subway_stations.gpkg')[['name', 'geometry']].to_crs(TARGET_CRS)
transformer = pyproj.Transformer.from_crs(TARGET_CRS, 3857, always_xy=True)

def bfs_hot_edges_order(G, origin, max_edges=MAX_K):
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

for key, name in [('eungbong', '응봉'), ('sungsoo', '성수')]:
    pt = subway[subway['name'] == name].geometry.iloc[0]
    _, i = tree.query([pt.x, pt.y])
    origin = node_ids[i]
    hot_order = bfs_hot_edges_order(G, origin)

    ox_, oy_ = node_xy[origin]
    cx, cy = transformer.transform(ox_, oy_)

    fig, ax = plt.subplots(figsize=(9, 9), dpi=160)
    PAD = 1000
    ax.set_xlim(cx - PAD, cx + PAD)
    ax.set_ylim(cy - PAD, cy + PAD)
    try:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=16, alpha=0.75)
    except Exception as e:
        print(f'베이스맵 오류(무시): {e}')

    cmap = cm.get_cmap('RdYlBu')
    norm = mcolors.Normalize(vmin=0, vmax=len(hot_order))
    for rank, (u, v) in enumerate(hot_order):
        geom = edge_geom.get((u, v))
        if geom is None:
            continue
        xs, ys = geom.xy
        xs3857, ys3857 = transformer.transform(np.array(xs), np.array(ys))
        ax.plot(xs3857, ys3857, color=cmap(norm(rank)), linewidth=2.2, alpha=0.9, zorder=4)

    ax.scatter([cx], [cy], c='black', s=140, zorder=6, edgecolor='white', linewidth=1.5, marker='*')

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = plt.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
    cbar.set_label('복구 순서 (BFS 거리 — 낮을수록 출발지에서 가까움)', fontsize=9)

    ax.annotate(f"{name}역", xy=(0.03, 0.97), xycoords='axes fraction', va='top', ha='left',
                fontsize=13, fontweight='bold', zorder=8,
                bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.9))
    ax.set_axis_off()
    ax.set_title(f'{name}역 인근 병목 링크 복구 순서 (09시, UTCI 38°C 기준)\n색이 붉을수록 먼저(가까이) 복구, 파랄수록 나중(멀리) 복구',
                 fontsize=11)
    plt.tight_layout()
    out_png = f'{PROJ_DIR}/03_Method_C/results/figures/2026-08-04_{key}_bfs_repair_order_map.png'
    plt.savefig(out_png, dpi=160, bbox_inches='tight', facecolor='white')
    plt.close()
    print('저장:', out_png)
