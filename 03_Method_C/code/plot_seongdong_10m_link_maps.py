"""성동구 10m(clean) — 링크 단위 시각화(1mtrue와 동일 포맷)
1. 링크에 10m Tmrt/UTCI(시간대별) 할당(Colaninno 방식, 5m 버퍼+zonal mean, 10m 격자 직접 사용)
2. Link Tmrt 시간대별+3구간, Link UTCI 급간(Bröde 2012) 시간대별+3구간
"""
import os
import numpy as np
import geopandas as gpd
import rasterio
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
from rasterstats import zonal_stats

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TODAY = '2026-07-29'
TMRT_DIR = os.path.join(BASE, '03_Method_C/results/solweig_seongdong_10m_clean_local')
UTCI_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_10m_clean_local')
LINK_SRC = os.path.join(BASE, '03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg')
OUT_GPKG = os.path.join(BASE, '03_Method_C/results/2026-07-29_link_tmrt_utci_seongdong_10m.gpkg')
OUT_DIR = os.path.join(BASE, '03_Method_C/results/figures/seongdong_10m_standalone')
os.makedirs(OUT_DIR, exist_ok=True)

HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}

links = gpd.read_file(LINK_SRC)[['u', 'v', 'osmid', 'highway_1', 'width_final', 'length', 'geometry']].copy()
links_buf = links.buffer(5.0)

print('링크에 10m Tmrt/UTCI 할당 중...', flush=True)
for h in HOURS:
    hc = HCODE[h]
    with rasterio.open(os.path.join(TMRT_DIR, f'Tmrt_2025_209_{hc}.tif')) as src:
        arr = src.read(1).astype(np.float32)
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        tr = src.transform
    st = zonal_stats(links_buf, arr, affine=tr, stats=['mean'], nodata=np.nan)
    links[f'Tmrt_{h:02d}'] = [s['mean'] for s in st]

    with rasterio.open(os.path.join(UTCI_DIR, f'UTCI_seongdong_10m_clean_{h:02d}.tif')) as src:
        arru = src.read(1).astype(np.float32)
        arru[(arru <= -100) | (arru >= 200)] = np.nan
        tru = src.transform
    stu = zonal_stats(links_buf, arru, affine=tru, stats=['mean'], nodata=np.nan)
    links[f'UTCI_{h:02d}'] = [s['mean'] for s in stu]
    print(f'  {h:02d}시 완료', flush=True)

links.to_file(OUT_GPKG, driver='GPKG')
print(f'저장: {OUT_GPKG}', flush=True)

gdf = links.dropna(subset=[f'Tmrt_{h:02d}' for h in HOURS])
hour_cols = [f'Tmrt_{h:02d}' for h in HOURS]

CMAP = 'YlOrRd'
all_vals = gdf[hour_cols].values.flatten()
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, HOURS):
    gdf.plot(column=f'Tmrt_{h:02d}', cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.3, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13); ax.axis('off')
for ax in axes.flat[len(HOURS):]:
    ax.axis('off')
sm = plt.cm.ScalarMappable(cmap=CMAP, norm=mpl.colors.Normalize(vmin=VMIN, vmax=VMAX))
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02, label='Tmrt (°C)')
fig.suptitle('성동구 10m(clean) — 링크별 시간대별 Tmrt', fontsize=17)
p1 = os.path.join(OUT_DIR, f'{TODAY}_LinkTmrt_hourly_seongdong_10m.png')
fig.savefig(p1, dpi=150, bbox_inches='tight'); plt.close(fig); print('저장:', p1)

gdf['아침(06-09시)'] = gdf[[f'Tmrt_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'Tmrt_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'Tmrt_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col in zip(axes, period_cols):
    gdf.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.4, ax=ax)
    ax.set_title(col, fontsize=14); ax.axis('off')
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05, label='Tmrt (°C)')
fig.suptitle('성동구 10m(clean) — 링크별 3구간 평균 Tmrt', fontsize=16)
p2 = os.path.join(OUT_DIR, f'{TODAY}_LinkTmrt_3period_seongdong_10m.png')
fig.savefig(p2, dpi=150, bbox_inches='tight'); plt.close(fig); print('저장:', p2)

BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)', 'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap_cat = ListedColormap(COLORS); norm_cat = BoundaryNorm(BOUNDS, cmap_cat.N)
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, HOURS):
    gdf.plot(column=f'UTCI_{h:02d}', cmap=cmap_cat, norm=norm_cat, linewidth=0.3, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13); ax.axis('off')
for ax in axes.flat[len(HOURS):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.05), fontsize=11)
fig.suptitle('성동구 10m(clean) — 링크별 UTCI 열스트레스 급간(Bröde et al. 2012) 시간대별', fontsize=17)
p3 = os.path.join(OUT_DIR, f'{TODAY}_LinkUTCI_category_hourly_seongdong_10m.png')
fig.savefig(p3, dpi=150, bbox_inches='tight'); plt.close(fig); print('저장:', p3)

gdf['UTCI_아침'] = gdf[[f'UTCI_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['UTCI_낮'] = gdf[[f'UTCI_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['UTCI_저녁'] = gdf[[f'UTCI_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
utci_period_cols = ['UTCI_아침', 'UTCI_낮', 'UTCI_저녁']

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col, lab in zip(axes, utci_period_cols, period_cols):
    gdf.plot(column=col, cmap=cmap_cat, norm=norm_cat, linewidth=0.4, ax=ax)
    ax.set_title(lab, fontsize=14); ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.02), fontsize=11)
fig.suptitle('성동구 10m(clean) — 링크별 UTCI 열스트레스 급간 3구간', fontsize=16)
p4 = os.path.join(OUT_DIR, f'{TODAY}_LinkUTCI_category_3period_seongdong_10m.png')
fig.savefig(p4, dpi=150, bbox_inches='tight'); plt.close(fig); print('저장:', p4)

print('\n10m 링크 단위 시각화 완료.', flush=True)
