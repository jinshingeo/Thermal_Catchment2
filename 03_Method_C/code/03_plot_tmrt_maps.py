"""
성동구 파일럿 — Tmrt 지도 시각화 (시간대별 14장 + Colaninno 3구간)
================================================================
범례(컬러스케일)는 전체 시간대 공통 최소~최대값으로 고정 —
그래야 시간대 간 상대적인 더위 차이가 비교 가능함.
"""
import os
import glob
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/dsm_cdsm_seongdong/solweig_approach1_30m'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures'
os.makedirs(OUT_DIR, exist_ok=True)

CMAP = 'YlOrRd'  # 순차형(sequential) 단일색상, 온도 크기 표현에 적합

# ── 1. 시간대별 파일 로드 ──────────────────────────────────────────────────
files = sorted(glob.glob(os.path.join(BASE, 'Tmrt_2025_209_*.tif')))
hours = [int(os.path.basename(f).split('_')[3][:2]) for f in files]

data = {}
for f, h in zip(files, hours):
    with rasterio.open(f) as src:
        d = src.read(1).astype(float)
        d[(d <= -100) | (d >= 200)] = np.nan
        data[h] = d

# ── 2. 전체 공통 컬러스케일 (min/max 고정) ─────────────────────────────────
all_vals = np.concatenate([d[~np.isnan(d)] for d in data.values()])
VMIN, VMAX = all_vals.min(), all_vals.max()
print(f"공통 컬러스케일: {VMIN:.1f} ~ {VMAX:.1f} degC")

# ── 3. Colaninno 3구간 평균 ────────────────────────────────────────────────
morning = np.nanmean([data[h] for h in [6, 7, 8, 9]], axis=0)
midday = np.nanmean([data[h] for h in [10, 11, 12, 13, 14]], axis=0)
evening = np.nanmean([data[h] for h in [15, 16, 17, 18, 19]], axis=0)
periods = {'아침(06-09시)': morning, '낮(10-14시)': midday, '저녁(15-19시)': evening}

# ── 4. 시간대별 14장 그리드 ────────────────────────────────────────────────
fig, axes = plt.subplots(4, 4, figsize=(16, 16))
for ax, h in zip(axes.flat, hours):
    im = ax.imshow(data[h], cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(f'{h:02d}시', fontsize=12)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02,
             label='Tmrt (degC)')
fig.suptitle('성동구 파일럿 — 시간대별 Tmrt (접근1, 30m)', fontsize=16)
hourly_path = os.path.join(OUT_DIR, '2026-07-09_Tmrt_hourly_approach1_30m.png')
fig.savefig(hourly_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {hourly_path}")

# ── 5. Colaninno 3구간 ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (label, arr) in zip(axes, periods.items()):
    im = ax.imshow(arr, cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(label, fontsize=13)
    ax.axis('off')
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05,
             label='Tmrt (degC)')
fig.suptitle('성동구 파일럿 — Colaninno 3구간 평균 Tmrt (접근1, 30m)', fontsize=15)
period_path = os.path.join(OUT_DIR, '2026-07-09_Tmrt_3period_approach1_30m.png')
fig.savefig(period_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {period_path}")
