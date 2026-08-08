"""
도보 네트워크 3D — 서울 전체 + 성동구
================================================================
기존 TAVI/Thermal_Catchment/02_코드/57_3d_maps.py의 make_ax() 기법 재사용
(matplotlib 3D, elev=35/azim=-65, z=0 평면에 지오메트리, 투명배경, 축/범례 없음).
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
NET_PATH = os.path.join(PROJ, 'data', 'network', '2026-08-02_seoul_walk_api_network.gpkg')
JBG_PATH = '/Users/jin/석사논문/통계지역경계/집계구.shp'
OUT_DIR = os.path.join(PROJ, 'figures', '발표용_20260805', '3d')

ELEV, AZIM = 35, -65
FIGSIZE, DPI = (12, 12), 150
LINE_COLOR = '#2C7FB8'  # 단색 (범례 불필요)


def make_ax(xmin, xmax, ymin, ymax, cx, cy):
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor='none')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(xmin - cx, xmax - cx)
    ax.set_ylim(ymin - cy, ymax - cy)
    ax.set_zlim(0, 500)
    ax.set_box_aspect([xmax - xmin, ymax - ymin, 350])
    ax.view_init(elev=ELEV, azim=AZIM)
    ax.set_axis_off()
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('none')
    ax.grid(False)
    return fig, ax


def draw_network(ax, edges, cx, cy, color, lw=0.4, alpha=0.8):
    for geom in edges.geometry:
        if geom is None or geom.is_empty:
            continue
        parts = list(geom.geoms) if geom.geom_type in (
            'MultiLineString', 'GeometryCollection') else [geom]
        for part in parts:
            if part.geom_type != 'LineString':
                continue
            xs, ys = part.xy
            ax.plot(np.array(xs) - cx, np.array(ys) - cy, 0,
                     color=color, linewidth=lw, alpha=alpha, zorder=2)


def render(edges, boundary, out_path, lw=0.4):
    xmin, ymin, xmax, ymax = boundary.total_bounds
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    fig, ax = make_ax(xmin, xmax, ymin, ymax, cx, cy)
    for geom in boundary.geometry:
        polys = [geom] if geom.geom_type == 'Polygon' else list(geom.geoms)
        for poly in polys:
            xs, ys = poly.exterior.xy
            ax.plot(np.array(xs) - cx, np.array(ys) - cy, 0,
                     color='#DDDDDD', linewidth=0.5, zorder=1)
    draw_network(ax, edges, cx, cy, LINE_COLOR, lw=lw)
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', transparent=True)
    plt.close(fig)
    print(f"저장: {out_path}")


print("네트워크 로드...")
edges = gpd.read_file(NET_PATH).to_crs('EPSG:5186')
edges = edges[edges['LNKG_TYPE_CD'].astype(str).str.startswith('1')].copy()

print("집계구 경계 로드...")
jbg = gpd.read_file(JBG_PATH)
if jbg.crs is None:
    jbg = jbg.set_crs('EPSG:5179', allow_override=True)
jbg = jbg.to_crs('EPSG:5186')
seoul_boundary = jbg.dissolve()
seongdong = jbg[jbg['TOT_REG_CD'].astype(str).str.startswith('11040')]

print("[1] 서울 전체 네트워크 3D...")
render(edges, seoul_boundary,
       os.path.join(OUT_DIR, 'network_seoul_3d.png'), lw=0.15)

print("[2] 성동구 네트워크 3D...")
edges_sd = gpd.clip(edges, seongdong)
render(edges_sd, seongdong,
       os.path.join(OUT_DIR, 'network_seongdong_3d.png'), lw=0.5)

print("완료")
