"""
건물높이 3D 압출 — 성동구 + 서울 전체 (분석 파이프라인과 동일한 높이값 사용)
================================================================
15_build_dsm_cdsm_seoul_5m.py와 동일한 4단계 하이브리드 건물높이 로직
(F_FAC_BUILDING 실측 > 자체층수 > TL 교차보완 > 기본값) 재사용.
렌더링은 57_3d_maps.py의 make_ax()/Poly3DCollection 압출 기법 재사용.
"""
import os
import sys
import numpy as np
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
JBG_PATH = '/Users/jin/석사논문/통계지역경계/집계구.shp'
NET_PATH = os.path.join(PROJ, 'data', 'network', '2026-08-02_seoul_walk_api_network.gpkg')
FAC_PATH = os.path.join(PROJ, 'data', 'F_FAC_BUILDING_서울', 'F_FAC_BUILDING_11_202606.shp')
TL_PATH = '/Users/jin/석사논문/TAVI/03_건물데이터/(도로명주소)건물_서울/TL_SPBD_BULD_11_202603.shp'
OUT_DIR = os.path.join(PROJ, 'figures', '발표용_20260805', '3d')

TARGET_CRS = 'EPSG:5186'
DEFAULT_HEIGHT = 3.0
ELEV, AZIM = 35, -65
FIGSIZE, DPI = (12, 12), 150
Z_EXAG = 10

TARGET = sys.argv[1] if len(sys.argv) > 1 else 'seongdong'  # 'seongdong' | 'seoul'
SIMPLIFY_TOL = 3 if TARGET == 'seongdong' else 15
MIN_HEIGHT = 0 if TARGET == 'seongdong' else 6.0  # 서울 전체: 1~2층 건물 제외(스카이라인 기여 적음, face 수 절감)

# ── 집계구 경계 ─────────────────────────────────────────────────────────
print("집계구 로드...")
jbg = gpd.read_file(JBG_PATH)
if jbg.crs is None:
    jbg = jbg.set_crs('EPSG:5179', allow_override=True)
jbg = jbg.to_crs(TARGET_CRS)

if TARGET == 'seongdong':
    area = jbg[jbg['TOT_REG_CD'].astype(str).str.startswith('11040')]
else:
    area = jbg.dissolve()

xmin, ymin, xmax, ymax = area.total_bounds
cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2

# ── 건물 높이 (4단계 하이브리드, 15_build_dsm_cdsm_seoul_5m.py와 동일 로직) ──
print("건물 로드 및 높이 계산...")
fac = gpd.read_file(FAC_PATH, encoding='cp949')
fac['geometry'] = fac.geometry.buffer(0)
fac = gpd.clip(fac, area)
print(f"  건물 {len(fac):,}동")

tl = gpd.read_file(TL_PATH, encoding='cp949')
tl['geometry'] = tl.geometry.buffer(0)
tl = gpd.clip(tl, area.to_crs(tl.crs)).to_crs(TARGET_CRS)
tl_height_lookup = (tl[tl['GRO_FLO_CO'].notna() & (tl['GRO_FLO_CO'] > 0)]
                     .set_index('BD_MGT_SN')['GRO_FLO_CO'] * DEFAULT_HEIGHT).to_dict()

fac['HEIGHT_FINAL'] = np.nan
valid = (fac['HEIGHT'] > 0) & (fac['HEIGHT'] < 200)
fac.loc[valid, 'HEIGHT_FINAL'] = fac.loc[valid, 'HEIGHT']
need2 = fac['HEIGHT_FINAL'].isna() & (fac['GRND_FLR'] > 0)
fac.loc[need2, 'HEIGHT_FINAL'] = fac.loc[need2, 'GRND_FLR'] * DEFAULT_HEIGHT
need3 = fac['HEIGHT_FINAL'].isna() & fac['BD_MGT_SN'].isin(tl_height_lookup)
fac.loc[need3, 'HEIGHT_FINAL'] = fac.loc[need3, 'BD_MGT_SN'].map(tl_height_lookup)
fac['HEIGHT_FINAL'] = fac['HEIGHT_FINAL'].fillna(DEFAULT_HEIGHT)
print(f"  실측 {valid.sum():,} | 자체층수 {need2.sum():,} | "
      f"교차보완 {need3.sum():,} | 기본값 {(len(fac)-valid.sum()-need2.sum()-need3.sum()):,}")

if MIN_HEIGHT > 0:
    before = len(fac)
    fac = fac[fac['HEIGHT_FINAL'] >= MIN_HEIGHT].copy()
    print(f"  {MIN_HEIGHT}m 미만 제외: {before:,} -> {len(fac):,}동")

fac['geometry'] = fac.geometry.simplify(SIMPLIFY_TOL)
fac = fac[fac.geometry.is_valid & ~fac.geometry.is_empty].copy()

# ── 네트워크 ────────────────────────────────────────────────────────────
print("네트워크 로드...")
edges = gpd.read_file(NET_PATH).to_crs(TARGET_CRS)
edges = edges[edges['LNKG_TYPE_CD'].astype(str).str.startswith('1')].copy()
edges = gpd.clip(edges, area)

# ── 렌더 ────────────────────────────────────────────────────────────────
X_RANGE, Y_RANGE = xmax - xmin, ymax - ymin
Z_MAX = int(fac['HEIGHT_FINAL'].quantile(0.99)) * Z_EXAG + 200

fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor='none')
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(xmin - cx, xmax - cx)
ax.set_ylim(ymin - cy, ymax - cy)
ax.set_zlim(0, Z_MAX)
ax.set_box_aspect([X_RANGE, Y_RANGE, Z_MAX * 0.7])
ax.view_init(elev=ELEV, azim=AZIM)
ax.set_axis_off()
for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor('none')
ax.grid(False)

print("경계/네트워크 드로잉...")
for geom in area.geometry:
    polys = [geom] if geom.geom_type == 'Polygon' else list(geom.geoms)
    for poly in polys:
        xs, ys = poly.exterior.xy
        ax.plot(np.array(xs) - cx, np.array(ys) - cy, 0,
                 color='#DDDDDD', linewidth=0.5, zorder=1)
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
                 color='#AAAAAA', linewidth=0.4, alpha=0.6, zorder=2)

print("건물 압출 face 생성...", flush=True)
MAX_H = fac['HEIGHT_FINAL'].quantile(0.99)
cmap = plt.cm.Greys
faces, facecolors, edgecolors = [], [], []
t0_faces = __import__('time').time()

for i_row, (height, geom) in enumerate(zip(fac['HEIGHT_FINAL'].values, fac.geometry.values)):
    h = height * Z_EXAG
    t = min(height / MAX_H, 1.0)
    roof_c = mcolors.to_rgba(cmap(0.35 + t * 0.55), alpha=0.97)
    wall_c = mcolors.to_rgba(cmap(0.25 + t * 0.45), alpha=0.90)

    polys = [geom] if geom.geom_type == 'Polygon' else (
        list(geom.geoms) if geom.geom_type == 'MultiPolygon' else [])
    for poly in polys:
        if poly.is_empty or not poly.is_valid:
            continue
        ext = list(poly.exterior.coords)
        xs = [p[0] - cx for p in ext]
        ys = [p[1] - cy for p in ext]
        faces.append(list(zip(xs, ys, [h] * len(ext))))
        facecolors.append(roof_c)
        edgecolors.append((0, 0, 0, 0.06))
        for i in range(len(ext) - 1):
            wall = [(xs[i], ys[i], 0), (xs[i+1], ys[i+1], 0),
                    (xs[i+1], ys[i+1], h), (xs[i], ys[i], h)]
            faces.append(wall)
            facecolors.append(wall_c)
            edgecolors.append((0, 0, 0, 0.03))
    if i_row % 100000 == 0 and i_row > 0:
        print(f"  {i_row:,}동 처리, face {len(faces):,}개 "
              f"({__import__('time').time()-t0_faces:.0f}초 경과)", flush=True)

print(f"  face 수: {len(faces):,} ({__import__('time').time()-t0_faces:.0f}초)", flush=True)
print("Poly3DCollection 생성/렌더 중...", flush=True)
col = Poly3DCollection(faces, zsort='average')
col.set_facecolors(facecolors)
col.set_edgecolors(edgecolors)
col.set_linewidth(0.0)
ax.add_collection3d(col)

out_path = os.path.join(OUT_DIR, f'buildings_{TARGET}_3d.png')
plt.savefig(out_path, dpi=DPI, bbox_inches='tight', transparent=True)
plt.close(fig)
print(f"저장: {out_path}")
