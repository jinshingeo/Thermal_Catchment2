"""
서울 전체 5m — Tmrt 지도 시각화 (시간대별 14장 + Colaninno 3구간)
================================================================
성동구 파일럿(03_plot_tmrt_maps.py)과 동일한 스타일/범례 규칙 적용:
범례(컬러스케일)는 전체 시간대 공통 최소~최대값으로 고정.
"""
import os
import glob
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/solweig_seoul_5m_v2_mosaic'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures'
os.makedirs(OUT_DIR, exist_ok=True)

CMAP = 'YlOrRd'  # 성동구와 동일 (순차형 단일색상)

# ── 1. 시간대별 파일 로드 ──────────────────────────────────────────────────
files = sorted(glob.glob(os.path.join(BASE, 'Tmrt_seoul_5m_*.tif')))
files = [f for f in files if 'average' not in f]
hours = [int(os.path.basename(f).split('_')[-1][:2]) for f in files]

data = {}
for f, h in zip(files, hours):
    with rasterio.open(f) as src:
        d = src.read(1).astype(float)
        d[(d <= -100) | (d >= 200)] = np.nan
        data[h] = d

# ── 2. 전체 공통 컬러스케일 (min/max 고정) ─────────────────────────────────
all_vals = np.concatenate([d[~np.isnan(d)] for d in data.values()])
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)
print(f"공통 컬러스케일: {VMIN:.1f} ~ {VMAX:.1f} degC")

# ── 3. Colaninno 3구간 평균 ────────────────────────────────────────────────
morning = np.nanmean([data[h] for h in [6, 7, 8, 9]], axis=0)
midday = np.nanmean([data[h] for h in [10, 11, 12, 13, 14]], axis=0)
evening = np.nanmean([data[h] for h in [15, 16, 17, 18, 19]], axis=0)
periods = {'아침(06-09시)': morning, '낮(10-14시)': midday, '저녁(15-19시)': evening}

# ── 4. 시간대별 14장 그리드 ────────────────────────────────────────────────
hours_sorted = sorted(data.keys())
fig, axes = plt.subplots(4, 4, figsize=(16, 14))
for ax, h in zip(axes.flat, hours_sorted):
    im = ax.imshow(data[h], cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(f'{h:02d}시', fontsize=12)
    ax.axis('off')
for ax in axes.flat[len(hours_sorted):]:
    ax.axis('off')
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02,
             label='Tmrt (degC)')
fig.suptitle('서울 전체 — 시간대별 Tmrt (5m, Method C)', fontsize=16)
hourly_path = os.path.join(OUT_DIR, '2026-07-16_Tmrt_hourly_seoul_5m.png')
fig.savefig(hourly_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {hourly_path}")

# ── 5. Colaninno 3구간 ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, (label, arr) in zip(axes, periods.items()):
    im = ax.imshow(arr, cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(label, fontsize=13)
    ax.axis('off')
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05,
             label='Tmrt (degC)')
fig.suptitle('서울 전체 — Colaninno 3구간 평균 Tmrt (5m, Method C)', fontsize=15)
period_path = os.path.join(OUT_DIR, '2026-07-16_Tmrt_3period_seoul_5m.png')
fig.savefig(period_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {period_path}")

# ── 6. 전체 평균 단일 지도 ─────────────────────────────────────────────────
with rasterio.open(os.path.join(BASE, 'Tmrt_seoul_5m_average.tif')) as src:
    avg = src.read(1).astype(float)
    avg[(avg <= -100) | (avg >= 200)] = np.nan
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(avg, cmap=CMAP, vmin=VMIN, vmax=VMAX)
ax.axis('off')
fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.04, pad=0.02, label='Tmrt (degC)')
ax.set_title('서울 전체 — 06~19시 평균 Tmrt (5m, Method C)', fontsize=14)
avg_path = os.path.join(OUT_DIR, '2026-07-16_Tmrt_average_seoul_5m.png')
fig.savefig(avg_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {avg_path}")
