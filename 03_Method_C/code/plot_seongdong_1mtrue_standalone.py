"""성동구 1mtrue(진짜 1m DEM, 9타일) 단독 시각화 — 서울 5m 시각화 포맷과 동일 구조
(16/19/23/27_plot_*_seoul_5m*.py 템플릿 참고)
"""
import os
import glob
import numpy as np
import geopandas as gpd
import rasterio
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TMRT_DIR = os.path.join(BASE, '03_Method_C/results/solweig_seongdong_1mtrue_mosaic_local')
UTCI_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_1mtrue_local')
LINK_GPKG = os.path.join(BASE, '03_Method_C/results/compare_5m_1mtrue_seongdong/2026-07-28_link_compare_5m_1mtrue_seongdong.gpkg')
OUT_DIR = os.path.join(BASE, '03_Method_C/results/figures/seongdong_1mtrue_standalone')
os.makedirs(OUT_DIR, exist_ok=True)
TODAY = '2026-07-28'

HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}

# ---------- 데이터 로드 ----------
tmrt = {}
utci_d = {}
for h in HOURS:
    with rasterio.open(os.path.join(TMRT_DIR, f'Tmrt_seongdong_1mtrue_{HCODE[h]}.tif')) as src:
        arr = src.read(1).astype(np.float32)
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        tmrt[h] = arr
    with rasterio.open(os.path.join(UTCI_DIR, f'UTCI_seongdong_1mtrue_{h:02d}.tif')) as src:
        arr = src.read(1).astype(np.float32)
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        utci_d[h] = arr

tmrt_avg = np.nanmean(list(tmrt.values()), axis=0)
utci_avg = np.nanmean(list(utci_d.values()), axis=0)

morning_t = np.nanmean([tmrt[h] for h in [6, 7, 8, 9]], axis=0)
midday_t = np.nanmean([tmrt[h] for h in [10, 11, 12, 13, 14]], axis=0)
evening_t = np.nanmean([tmrt[h] for h in [15, 16, 17, 18, 19]], axis=0)
periods_t = {'아침(06-09시)': morning_t, '낮(10-14시)': midday_t, '저녁(15-19시)': evening_t}

morning_u = np.nanmean([utci_d[h] for h in [6, 7, 8, 9]], axis=0)
midday_u = np.nanmean([utci_d[h] for h in [10, 11, 12, 13, 14]], axis=0)
evening_u = np.nanmean([utci_d[h] for h in [15, 16, 17, 18, 19]], axis=0)
periods_u = {'아침(06-09시)': morning_u, '낮(10-14시)': midday_u, '저녁(15-19시)': evening_u}

# ---------- 1. Tmrt 시간대별 14패널 ----------
fig, axes = plt.subplots(4, 4, figsize=(16, 15))
vmin, vmax = np.nanpercentile(tmrt_avg, 2), np.nanpercentile([np.nanmax(v) for v in tmrt.values()], 80)
for ax, h in zip(axes.flat, HOURS):
    im = ax.imshow(tmrt[h], cmap='inferno', vmin=vmin, vmax=vmax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(HOURS):]:
    ax.axis('off')
fig.colorbar(im, ax=axes, shrink=0.6, label='Tmrt (°C)')
fig.suptitle('성동구 1mtrue — Tmrt 시간대별', fontsize=16)
fig.savefig(os.path.join(OUT_DIR, f'{TODAY}_Tmrt_hourly_seongdong_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장: Tmrt_hourly')

# ---------- 2. Tmrt 3구간 ----------
fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))
for ax, (label, arr) in zip(axes, periods_t.items()):
    im = ax.imshow(arr, cmap='inferno', vmin=vmin, vmax=vmax)
    ax.set_title(label, fontsize=14)
    ax.axis('off')
fig.colorbar(im, ax=axes, shrink=0.7, label='Tmrt (°C)')
fig.suptitle('성동구 1mtrue — Tmrt 3구간', fontsize=15)
fig.savefig(os.path.join(OUT_DIR, f'{TODAY}_Tmrt_3period_seongdong_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장: Tmrt_3period')

# ---------- 3. Tmrt 평균 ----------
fig, ax = plt.subplots(figsize=(9, 8))
im = ax.imshow(tmrt_avg, cmap='inferno', vmin=vmin, vmax=vmax)
ax.axis('off')
ax.set_title('성동구 1mtrue — Tmrt 평균(06-19시)', fontsize=14)
fig.colorbar(im, ax=ax, shrink=0.8, label='Tmrt (°C)')
fig.savefig(os.path.join(OUT_DIR, f'{TODAY}_Tmrt_average_seongdong_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장: Tmrt_average')

# ---------- 4. UTCI 시간대별 14패널 (연속) ----------
fig, axes = plt.subplots(4, 4, figsize=(16, 15))
vminu, vmaxu = np.nanpercentile(utci_avg, 2), np.nanpercentile([np.nanmax(v) for v in utci_d.values()], 90)
for ax, h in zip(axes.flat, HOURS):
    imu = ax.imshow(utci_d[h], cmap='inferno', vmin=vminu, vmax=vmaxu)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(HOURS):]:
    ax.axis('off')
fig.colorbar(imu, ax=axes, shrink=0.6, label='UTCI (°C)')
fig.suptitle('성동구 1mtrue — UTCI 시간대별', fontsize=16)
fig.savefig(os.path.join(OUT_DIR, f'{TODAY}_UTCI_hourly_seongdong_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장: UTCI_hourly')

# ---------- 5. UTCI 평균 ----------
fig, ax = plt.subplots(figsize=(9, 8))
imu = ax.imshow(utci_avg, cmap='inferno', vmin=vminu, vmax=vmaxu)
ax.axis('off')
ax.set_title('성동구 1mtrue — UTCI 평균(06-19시)', fontsize=14)
fig.colorbar(imu, ax=ax, shrink=0.8, label='UTCI (°C)')
fig.savefig(os.path.join(OUT_DIR, f'{TODAY}_UTCI_average_seongdong_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장: UTCI_average')

# ---------- 6. UTCI 열스트레스 급간(Bröde 2012 Table 3) ----------
BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap_cat = ListedColormap(COLORS)
norm_cat = BoundaryNorm(BOUNDS, cmap_cat.N)
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

fig, axes = plt.subplots(4, 4, figsize=(16, 15))
for ax, h in zip(axes.flat, HOURS):
    ax.imshow(utci_d[h], cmap=cmap_cat, norm=norm_cat)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(HOURS):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.0), fontsize=11)
fig.suptitle('성동구 1mtrue — UTCI 열스트레스 급간(Bröde et al. 2012) 시간대별', fontsize=16)
fig.savefig(os.path.join(OUT_DIR, f'{TODAY}_UTCI_category_hourly_seongdong_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장: UTCI_category_hourly')

fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))
for ax, (label, arr) in zip(axes, periods_u.items()):
    ax.imshow(arr, cmap=cmap_cat, norm=norm_cat)
    ax.set_title(label, fontsize=14)
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.05), fontsize=11)
fig.suptitle('성동구 1mtrue — UTCI 열스트레스 급간 3구간', fontsize=15)
fig.savefig(os.path.join(OUT_DIR, f'{TODAY}_UTCI_category_3period_seongdong_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print('저장: UTCI_category_3period')

# ---------- 구간별 비율 요약 ----------
print('\n구간별 픽셀 비율(3구간):')
for label, arr in periods_u.items():
    valid = arr[~np.isnan(arr)]
    total = valid.size
    below = (valid < BOUNDS[0]).sum() / total * 100
    m1 = ((valid >= BOUNDS[0]) & (valid < BOUNDS[1])).sum() / total * 100
    m2 = ((valid >= BOUNDS[1]) & (valid < BOUNDS[2])).sum() / total * 100
    m3 = ((valid >= BOUNDS[2]) & (valid < BOUNDS[3])).sum() / total * 100
    above = (valid >= BOUNDS[3]).sum() / total * 100
    print(f'[{label}] 26미만:{below:.1f}% {LABELS[0]}:{m1:.1f}% {LABELS[1]}:{m2:.1f}% '
          f'{LABELS[2]}:{m3:.1f}% 46이상:{above:.1f}%')

print('\n표준 단독 시각화 완료 (링크 버전은 비교 스크립트의 gpkg 결과물을 재사용해 별도 생성)')
