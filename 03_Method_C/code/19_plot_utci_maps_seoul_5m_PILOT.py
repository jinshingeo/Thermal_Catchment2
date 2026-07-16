"""
[파일럿 / 미확정 방법론] 서울 전체 5m — UTCI 지도 시각화
================================================================
⚠️ 18_compute_utci_seoul_5m_PILOT.py의 산출물 시각화 — 방법론 미확정
(단일 기상값, URock/공간보간 미적용). 성동구 Tmrt 시각화(03_plot_tmrt_maps.py)
와 동일 스타일 적용하되, Bröde et al.(2012) Table 3 스트레스 등급 경계선을
추가로 표시.
"""
import os
import glob
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/utci_seoul_5m_PILOT_단일기상값'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures'
os.makedirs(OUT_DIR, exist_ok=True)

CMAP = 'YlOrRd'

files = sorted(glob.glob(os.path.join(BASE, 'UTCI_seoul_5m_PILOT_*.tif')))
files = [f for f in files if 'average' not in f]
hours = [int(os.path.basename(f).split('_')[-1].replace('.tif', '')) for f in files]

data = {}
for f, h in zip(files, hours):
    with rasterio.open(f) as src:
        d = src.read(1).astype(float)
        data[h] = d

all_vals = np.concatenate([d[~np.isnan(d)] for d in data.values()])
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)
print(f"공통 컬러스케일: {VMIN:.1f} ~ {VMAX:.1f} degC")

# Bröde et al.(2012) Table 3 하드컷 임계값(38도) 초과 비율 확인
for h in sorted(data.keys()):
    d = data[h]
    valid = ~np.isnan(d)
    pct38 = (d[valid] >= 38).sum() / valid.sum() * 100
    print(f"  {h:02d}시: UTCI>=38도 비율 {pct38:.1f}%")

hours_sorted = sorted(data.keys())
fig, axes = plt.subplots(4, 4, figsize=(16, 14))
for ax, h in zip(axes.flat, hours_sorted):
    im = ax.imshow(data[h], cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(f'{h:02d}시', fontsize=12)
    ax.axis('off')
for ax in axes.flat[len(hours_sorted):]:
    ax.axis('off')
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02,
             label='UTCI (degC)')
fig.suptitle('[파일럿/미확정] 서울 전체 — 시간대별 UTCI (5m, 단일기상값)', fontsize=16, color='darkred')
hourly_path = os.path.join(OUT_DIR, '2026-07-16_UTCI_hourly_seoul_5m_PILOT.png')
fig.savefig(hourly_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {hourly_path}")

with rasterio.open(os.path.join(BASE, 'UTCI_seoul_5m_PILOT_average.tif')) as src:
    avg = src.read(1).astype(float)
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(avg, cmap=CMAP, vmin=VMIN, vmax=VMAX)
ax.axis('off')
fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.04, pad=0.02, label='UTCI (degC)')
ax.set_title('[파일럿/미확정] 서울 전체 — 06~19시 평균 UTCI (5m, 단일기상값)', fontsize=13, color='darkred')
avg_path = os.path.join(OUT_DIR, '2026-07-16_UTCI_average_seoul_5m_PILOT.png')
fig.savefig(avg_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {avg_path}")
