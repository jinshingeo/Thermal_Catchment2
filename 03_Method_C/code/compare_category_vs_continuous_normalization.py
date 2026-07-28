"""
서울 전체 5m — UTCI 급간 분류 지도 vs 연속형(0~1) 정규화 지도 비교
================================================================
Hard Cut(급간/이진 방식)과 Colaninno(2024)식 연속 정규화 방식을 시각적으로
나란히 비교. Colaninno 원래 방법(여러 날 평균+95백분위수)은 저희가 단일
대표일만 계산해뒀기 때문에 재현 불가 — 대신 단순화하여 현재 UTCI 값을
그대로 0~1 min-max 정규화만 적용(단순화한 점 명시).
"""
import os
import glob
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/utci_seoul_5m_PILOT_단일기상값'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_category_vs_continuous'
os.makedirs(OUT_DIR, exist_ok=True)

BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap_cat = ListedColormap(COLORS)
norm_cat = BoundaryNorm(BOUNDS, cmap_cat.N)

files = sorted(glob.glob(os.path.join(BASE, 'UTCI_seoul_5m_PILOT_*.tif')))
files = [f for f in files if 'average' not in f]
hours = [int(os.path.basename(f).split('_')[-1].replace('.tif', '')) for f in files]

data = {}
for f, h in zip(files, hours):
    with rasterio.open(f) as src:
        data[h] = src.read(1).astype(float)

morning = np.nanmean([data[h] for h in [6, 7, 8, 9]], axis=0)
midday = np.nanmean([data[h] for h in [10, 11, 12, 13, 14]], axis=0)
evening = np.nanmean([data[h] for h in [15, 16, 17, 18, 19]], axis=0)
periods = {'아침(06-09시)': morning, '낮(10-14시)': midday, '저녁(15-19시)': evening}

# 전체 3구간 통합 min/max로 정규화(Colaninno 원문처럼 "구간별이 아니라 전체 통합 min/max" 사용)
all_vals = np.concatenate([arr[~np.isnan(arr)].ravel() for arr in periods.values()])
gmin, gmax = np.nanmin(all_vals), np.nanmax(all_vals)
print(f"전체 min={gmin:.2f}, max={gmax:.2f}")

norm_periods = {label: (arr - gmin) / (gmax - gmin) for label, arr in periods.items()}

legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
for ax, (label, arr) in zip(axes[0], periods.items()):
    ax.imshow(arr, cmap=cmap_cat, norm=norm_cat)
    ax.set_title(f'[급간 분류] {label}', fontsize=13)
    ax.axis('off')
for ax, (label, arr) in zip(axes[1], norm_periods.items()):
    im = ax.imshow(arr, cmap='inferno', vmin=0, vmax=1)
    ax.set_title(f'[연속형 0~1 정규화] {label}', fontsize=13)
    ax.axis('off')

fig.legend(handles=legend_handles, loc='upper center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.96), fontsize=11)
cbar_ax = fig.add_axes([0.35, 0.04, 0.3, 0.02])
fig.colorbar(im, cax=cbar_ax, orientation='horizontal', label='정규화된 UTCI (0~1)')

fig.suptitle('서울 전체 5m — UTCI 급간 분류(위) vs 연속형 0~1 정규화(아래) 비교\n'
             '(Colaninno et al. 2024 방식 단순화 적용 — 단일 대표일 기준, 다일 평균 아님)',
             fontsize=15, y=1.02)
path = os.path.join(OUT_DIR, '2026-07-29_category_vs_continuous_3period.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")

# ── 정량 요약: 정규화값 0.8/0.9 이상 비율 ──────────────────────────────────
print("\n구간별 연속형 정규화값 분포 요약:")
for label, arr in norm_periods.items():
    valid = arr[~np.isnan(arr)]
    p80 = (valid >= 0.8).sum() / valid.size * 100
    p90 = (valid >= 0.9).sum() / valid.size * 100
    print(f"[{label}] 0.8 이상: {p80:.1f}% | 0.9 이상: {p90:.1f}% | "
          f"평균: {valid.mean():.3f} | 표준편차: {valid.std():.3f}")
