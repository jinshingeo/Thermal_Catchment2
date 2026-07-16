"""
[파일럿/미확정] 서울 전체 — UTCI 열스트레스 급간 지도 (래스터, Bröde et al. 2012 Table 3)
================================================================
연속 컬러스케일이 아니라 공식 열스트레스 분류를 범주형 색상으로 시각화.
성동구 파일럿(09/10번 스크립트, 링크 버전)과 동일한 구간·색상 사용.
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
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/seoul_5m_utci_PILOT'
os.makedirs(OUT_DIR, exist_ok=True)

# Bröde et al.(2012) Table 3(p.489) — 데이터 범위(30~46도)에 해당하는 구간만
BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap = ListedColormap(COLORS)
norm = BoundaryNorm(BOUNDS, cmap.N)

files = sorted(glob.glob(os.path.join(BASE, 'UTCI_seoul_5m_PILOT_*.tif')))
files = [f for f in files if 'average' not in f]
hours = [int(os.path.basename(f).split('_')[-1].replace('.tif', '')) for f in files]

data = {}
for f, h in zip(files, hours):
    with rasterio.open(f) as src:
        data[h] = src.read(1).astype(float)

hours_sorted = sorted(data.keys())
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

# ── 1. 시간대별 14장 그리드 ────────────────────────────────────────────────
fig, axes = plt.subplots(4, 4, figsize=(16, 15))
for ax, h in zip(axes.flat, hours_sorted):
    ax.imshow(data[h], cmap=cmap, norm=norm)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(hours_sorted):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.0), fontsize=11)
fig.suptitle('[파일럿/미확정] 서울 전체 — UTCI 열스트레스 급간(Bröde et al. 2012) 시간대별',
             fontsize=16, color='darkred')
path1 = os.path.join(OUT_DIR, '2026-07-16_UTCI_category_hourly_seoul_5m_PILOT.png')
fig.savefig(path1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path1}")

# ── 2. Colaninno 3구간 ─────────────────────────────────────────────────────
morning = np.nanmean([data[h] for h in [6, 7, 8, 9]], axis=0)
midday = np.nanmean([data[h] for h in [10, 11, 12, 13, 14]], axis=0)
evening = np.nanmean([data[h] for h in [15, 16, 17, 18, 19]], axis=0)
periods = {'아침(06-09시)': morning, '낮(10-14시)': midday, '저녁(15-19시)': evening}

fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))
for ax, (label, arr) in zip(axes, periods.items()):
    ax.imshow(arr, cmap=cmap, norm=norm)
    ax.set_title(label, fontsize=14)
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.05), fontsize=11)
fig.suptitle('[파일럿/미확정] 서울 전체 — UTCI 열스트레스 급간 Colaninno 3구간', fontsize=15, color='darkred')
path2 = os.path.join(OUT_DIR, '2026-07-16_UTCI_category_3period_seoul_5m_PILOT.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path2}")

# ── 3. 구간별 픽셀 비율 요약 ───────────────────────────────────────────────
print("\n구간별 픽셀 비율:")
for label, arr in periods.items():
    valid = arr[~np.isnan(arr)]
    print(f"\n[{label}]")
    total = valid.size
    below = (valid < BOUNDS[0]).sum() / total * 100
    m1 = ((valid >= BOUNDS[0]) & (valid < BOUNDS[1])).sum() / total * 100
    m2 = ((valid >= BOUNDS[1]) & (valid < BOUNDS[2])).sum() / total * 100
    m3 = ((valid >= BOUNDS[2]) & (valid < BOUNDS[3])).sum() / total * 100
    above = (valid >= BOUNDS[3]).sum() / total * 100
    print(f"  26 미만: {below:.1f}% | {LABELS[0]}: {m1:.1f}% | {LABELS[1]}: {m2:.1f}% | "
          f"{LABELS[2]}: {m3:.1f}% | 46 이상: {above:.1f}%")
