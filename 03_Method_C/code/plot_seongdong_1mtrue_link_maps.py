"""성동구 1mtrue — 링크(도로망) 단위 시각화 (20/24_..._seoul_5m*.py 템플릿과 동일 포맷)
1. 링크에 1mtrue Tmrt/UTCI(시간대별) 할당(Colaninno et al. 2024 방식, 5m 버퍼+zonal mean)
2. Link Tmrt 시간대별 14패널 + 3구간
3. Link UTCI 열스트레스 급간(Bröde et al. 2012 Table 3) 시간대별 14패널 + 3구간
MRT(Tmrt) 급간 지도(28번 템플릿)는 재현하지 않음 — 그 템플릿은 폐기된 "UTCI->MRT 역산"
방식을 쓰고 있어 현재의 UTCI 직접 채택 방법론과 맞지 않음(2026-07-28 판단).
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.warp import reproject, Resampling
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
from rasterstats import zonal_stats

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TODAY = '2026-07-28'

TMRT1_DIR = os.path.join(BASE, '03_Method_C/results/solweig_seongdong_1mtrue_mosaic_local')
UTCI1_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_1mtrue_local')
LINK_SRC = os.path.join(BASE, '03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg')
OUT_GPKG = os.path.join(BASE, '03_Method_C/results/2026-07-28_link_tmrt_utci_seongdong_1mtrue.gpkg')
OUT_DIR = os.path.join(BASE, '03_Method_C/results/figures/seongdong_1mtrue_standalone')
os.makedirs(OUT_DIR, exist_ok=True)

HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}

# ---------- 1. 링크에 1mtrue Tmrt/UTCI 할당 ----------
# 참고 5m 격자(정합 리샘플 기준) — approach2_5m Tmrt 파일 아무거나 사용
with rasterio.open(os.path.join(BASE, '03_Method_C/results/solweig_approach2_5m/Tmrt_2025_209_1300D.tif')) as ref:
    ref_tr, ref_crs, ref_w, ref_h = ref.transform, ref.crs, ref.width, ref.height

links = gpd.read_file(LINK_SRC)[['u', 'v', 'osmid', 'highway_1', 'width_final', 'length', 'geometry']].copy()
links_buf = links.buffer(5.0)

print('링크에 1mtrue Tmrt/UTCI 시간대별 할당 중...', flush=True)
for h in HOURS:
    hc = HCODE[h]
    with rasterio.open(os.path.join(TMRT1_DIR, f'Tmrt_seongdong_1mtrue_{hc}.tif')) as src:
        arr = src.read(1).astype(np.float32)
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        dst = np.full((ref_h, ref_w), np.nan, dtype=np.float32)
        reproject(source=arr, destination=dst, src_transform=src.transform, src_crs=src.crs,
                  dst_transform=ref_tr, dst_crs=ref_crs, resampling=Resampling.average,
                  src_nodata=np.nan, dst_nodata=np.nan)
    st = zonal_stats(links_buf, dst, affine=ref_tr, stats=['mean'], nodata=np.nan)
    links[f'Tmrt_{h:02d}'] = [s['mean'] for s in st]

    with rasterio.open(os.path.join(UTCI1_DIR, f'UTCI_seongdong_1mtrue_{h:02d}.tif')) as src:
        arr = src.read(1).astype(np.float32)
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        dstu = np.full((ref_h, ref_w), np.nan, dtype=np.float32)
        reproject(source=arr, destination=dstu, src_transform=src.transform, src_crs=src.crs,
                  dst_transform=ref_tr, dst_crs=ref_crs, resampling=Resampling.average,
                  src_nodata=np.nan, dst_nodata=np.nan)
    stu = zonal_stats(links_buf, dstu, affine=ref_tr, stats=['mean'], nodata=np.nan)
    links[f'UTCI_{h:02d}'] = [s['mean'] for s in stu]
    print(f'  {h:02d}시 완료', flush=True)

links.to_file(OUT_GPKG, driver='GPKG')
print(f'저장: {OUT_GPKG}', flush=True)

gdf = links.dropna(subset=[f'Tmrt_{h:02d}' for h in HOURS])
hour_cols = [f'Tmrt_{h:02d}' for h in HOURS]

# ---------- 2. Link Tmrt 시간대별 + 3구간 ----------
CMAP = 'YlOrRd'
all_vals = gdf[hour_cols].values.flatten()
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, HOURS):
    gdf.plot(column=f'Tmrt_{h:02d}', cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.3, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(HOURS):]:
    ax.axis('off')
sm = plt.cm.ScalarMappable(cmap=CMAP, norm=mpl.colors.Normalize(vmin=VMIN, vmax=VMAX))
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02, label='Tmrt (°C)')
fig.suptitle('성동구 1mtrue — 링크별 시간대별 Tmrt', fontsize=17)
p1 = os.path.join(OUT_DIR, f'{TODAY}_LinkTmrt_hourly_seongdong_1mtrue.png')
fig.savefig(p1, dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장:', p1)

gdf['아침(06-09시)'] = gdf[[f'Tmrt_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'Tmrt_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'Tmrt_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col in zip(axes, period_cols):
    gdf.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.4, ax=ax)
    ax.set_title(col, fontsize=14)
    ax.axis('off')
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05, label='Tmrt (°C)')
fig.suptitle('성동구 1mtrue — 링크별 3구간 평균 Tmrt', fontsize=16)
p2 = os.path.join(OUT_DIR, f'{TODAY}_LinkTmrt_3period_seongdong_1mtrue.png')
fig.savefig(p2, dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장:', p2)

# ---------- 3. Link UTCI 급간(Bröde 2012) 시간대별 + 3구간 ----------
BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap_cat = ListedColormap(COLORS)
norm_cat = BoundaryNorm(BOUNDS, cmap_cat.N)
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, HOURS):
    gdf.plot(column=f'UTCI_{h:02d}', cmap=cmap_cat, norm=norm_cat, linewidth=0.3, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(HOURS):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.05), fontsize=11)
fig.suptitle('성동구 1mtrue — 링크별 UTCI 열스트레스 급간(Bröde et al. 2012) 시간대별', fontsize=17)
p3 = os.path.join(OUT_DIR, f'{TODAY}_LinkUTCI_category_hourly_seongdong_1mtrue.png')
fig.savefig(p3, dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장:', p3)

gdf['UTCI_아침'] = gdf[[f'UTCI_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['UTCI_낮'] = gdf[[f'UTCI_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['UTCI_저녁'] = gdf[[f'UTCI_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
utci_period_cols = ['UTCI_아침', 'UTCI_낮', 'UTCI_저녁']
period_labels = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col, lab in zip(axes, utci_period_cols, period_labels):
    gdf.plot(column=col, cmap=cmap_cat, norm=norm_cat, linewidth=0.4, ax=ax)
    ax.set_title(lab, fontsize=14)
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.02), fontsize=11)
fig.suptitle('성동구 1mtrue — 링크별 UTCI 열스트레스 급간 3구간', fontsize=16)
p4 = os.path.join(OUT_DIR, f'{TODAY}_LinkUTCI_category_3period_seongdong_1mtrue.png')
fig.savefig(p4, dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장:', p4)

# Hard Cut(38도) 링크 비율 요약
print('\nHard Cut(UTCI>=38) 링크 비율(3구간):')
for lab, col in zip(period_labels, utci_period_cols):
    pct = (gdf[col] >= 38).mean() * 100
    print(f'  {lab}: {pct:.1f}%')

print('\n링크 단위 단독 시각화 전부 완료.', flush=True)
