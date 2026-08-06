"""
UTCI 기존(단일값) vs 신규(KMA 격자기상) 비교 — 06~19시 전체, 서울+성동구, 동일 범례
================================================================
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
OLD_GPKG = os.path.join(PROJ, '03_Method_C', 'results', '2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg')
NEW_GPKG = os.path.join(PROJ, '03_Method_C', 'results', '2026-08-06_link_utci_seoul_5m_KMA격자기상.gpkg')
JBG_PATH = '/Users/jin/석사논문/통계지역경계/집계구.shp'
OUT_DIR = os.path.join(PROJ, 'figures', '발표용_20260805')
os.makedirs(os.path.join(OUT_DIR, '2d', 'utci_compare'), exist_ok=True)

HOURS = list(range(6, 20))
FIGSIZE, DPI = (12, 12), 150
CMAP = 'Reds'

utci_cols = [f'UTCI_{h:02d}' for h in HOURS]
print("데이터 로드...")
old = gpd.read_file(OLD_GPKG, columns=['geometry'] + utci_cols)
new = gpd.read_file(NEW_GPKG, columns=['geometry'] + utci_cols)

print("전역 범례 범위 계산...")
all_vals = np.concatenate([old[utci_cols].values.ravel(), new[utci_cols].values.ravel()])
all_vals = all_vals[~np.isnan(all_vals)]
vmin, vmax = np.percentile(all_vals, [2, 98])
print(f"  범위: {vmin:.1f} ~ {vmax:.1f}")
norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
cmap = cm.get_cmap(CMAP)

print("성동구 경계 로드...")
jbg = gpd.read_file(JBG_PATH)
if jbg.crs is None:
    jbg = jbg.set_crs('EPSG:5179', allow_override=True)
jbg = jbg.to_crs('EPSG:5186')
seongdong = jbg[jbg['TOT_REG_CD'].astype(str).str.startswith('11040')]
sd_bounds = seongdong.total_bounds

print("성동구 클립 인덱스 계산...")
sd_mask_old = old.geometry.intersects(seongdong.union_all())


def render(gdf_subset, col, out_path, bounds):
    vals = gdf_subset[col].values
    segments, colors = [], []
    for geom, v in zip(gdf_subset.geometry, vals):
        if geom is None or geom.is_empty or np.isnan(v):
            continue
        xs, ys = geom.xy
        segments.append(np.column_stack([xs, ys]))
        colors.append(cmap(norm(v)))
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_alpha(0)
    lc = LineCollection(segments, colors=colors, linewidths=0.5)
    ax.add_collection(lc)
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])
    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)


seoul_bounds = old.total_bounds
sd_old = old[sd_mask_old]
sd_new = new[sd_mask_old]

for h in HOURS:
    col = f'UTCI_{h:02d}'
    render(old, col, os.path.join(OUT_DIR, '2d', 'utci_compare', f'utci_old_seoul_{h:02d}h.png'), seoul_bounds)
    render(new, col, os.path.join(OUT_DIR, '2d', 'utci_compare', f'utci_new_seoul_{h:02d}h.png'), seoul_bounds)
    render(sd_old, col, os.path.join(OUT_DIR, '2d', 'utci_compare', f'utci_old_seongdong_{h:02d}h.png'), sd_bounds)
    render(sd_new, col, os.path.join(OUT_DIR, '2d', 'utci_compare', f'utci_new_seongdong_{h:02d}h.png'), sd_bounds)
    print(f"{h:02d}시 완료", flush=True)

# 범례
fig, ax = plt.subplots(figsize=(1.2, 4), dpi=DPI)
fig.patch.set_alpha(0)
cb = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='vertical')
cb.set_label('UTCI (°C) — 06~19시 전체 공통 범례', fontsize=10)
plt.savefig(os.path.join(OUT_DIR, 'legends', 'legend_utci_allhours_compare.png'),
            dpi=DPI, bbox_inches='tight', transparent=True)
print("완료")
