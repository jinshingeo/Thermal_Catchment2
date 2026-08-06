"""
KMA 500m 격자 기상 입력값(기온·습도·풍속) 시각화 — 06~19시, 서울+성동구
변수별 공통 범례(06~19시 전체 공통)
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
IDX_CSV = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache', 'link_to_kma_grid_index.csv')
MET_CSV = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache', 'kma_grid_met_12day_avg.csv')
JBG_PATH = '/Users/jin/석사논문/통계지역경계/집계구.shp'
OUT_DIR = os.path.join(PROJ, 'figures', '발표용_20260805')
os.makedirs(os.path.join(OUT_DIR, '2d', 'kma_weather'), exist_ok=True)

HOURS = list(range(6, 20))
FIGSIZE, DPI = (10, 10), 150
VARS = {'ta': ('기온', 'Oranges'), 'hm': ('습도', 'Blues'), 'ws_10m': ('풍속', 'Greens')}

print("격자 좌표 로드...")
idx = pd.read_csv(IDX_CSV)
cells = idx[['grid_row', 'grid_col', 'grid_lon', 'grid_lat']].drop_duplicates(
    subset=['grid_row', 'grid_col']).reset_index(drop=True)

tr = Transformer.from_crs('EPSG:4326', 'EPSG:5186', always_xy=True)
x5186, y5186 = tr.transform(cells['grid_lon'].values, cells['grid_lat'].values)
cells['x'], cells['y'] = x5186, y5186

met = pd.read_csv(MET_CSV)
met = met.merge(cells, on=['grid_row', 'grid_col'], how='left')

print("성동구 경계 로드...")
jbg = gpd.read_file(JBG_PATH)
if jbg.crs is None:
    jbg = jbg.set_crs('EPSG:5179', allow_override=True)
jbg = jbg.to_crs('EPSG:5186')
seongdong = jbg[jbg['TOT_REG_CD'].astype(str).str.startswith('11040')]
sd_poly = seongdong.union_all()
sd_bounds = seongdong.total_bounds
seoul_bounds = [cells['x'].min(), cells['y'].min(), cells['x'].max(), cells['y'].max()]

pts = gpd.GeoSeries([Point(x, y) for x, y in zip(cells['x'], cells['y'])], crs='EPSG:5186')
sd_cell_mask = pts.intersects(sd_poly)
sd_cells = set(cells.loc[sd_cell_mask, ['grid_row', 'grid_col']].apply(tuple, axis=1))
met['in_sd'] = met.apply(lambda r: (r['grid_row'], r['grid_col']) in sd_cells, axis=1)


def render(df, x, y, val, cmap, norm, out_path, bounds, s):
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_alpha(0)
    ax.scatter(x, y, c=val, cmap=cmap, norm=norm, s=s, edgecolors='none')
    ax.set_xlim(bounds[0], bounds[1] if False else bounds[2])
    ax.set_ylim(bounds[1], bounds[3])
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)


for var, (label, cmap_name) in VARS.items():
    cmap = cm.get_cmap(cmap_name)
    vmin, vmax = np.nanpercentile(met[var].values, [2, 98])
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    print(f"[{var}] 범위 {vmin:.1f}~{vmax:.1f}")

    for h in HOURS:
        hdf = met[met['hour'] == h]
        render(hdf, hdf['x'], hdf['y'], hdf[var], cmap, norm,
               os.path.join(OUT_DIR, '2d', 'kma_weather', f'{var}_seoul_{h:02d}h.png'),
               seoul_bounds, s=40)
        sdf = hdf[hdf['in_sd']]
        render(sdf, sdf['x'], sdf['y'], sdf[var], cmap, norm,
               os.path.join(OUT_DIR, '2d', 'kma_weather', f'{var}_seongdong_{h:02d}h.png'),
               sd_bounds, s=200)
    print(f"[{var}] 06~19시 완료", flush=True)

    fig, ax = plt.subplots(figsize=(1.2, 4), dpi=DPI)
    fig.patch.set_alpha(0)
    cb = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='vertical')
    cb.set_label(f'{label} — 06~19시 공통 범례', fontsize=10)
    plt.savefig(os.path.join(OUT_DIR, 'legends', f'legend_{var}_allhours.png'),
                dpi=DPI, bbox_inches='tight', transparent=True)
    plt.close(fig)

print("완료")
