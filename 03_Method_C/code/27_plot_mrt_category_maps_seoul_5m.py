"""
[방법론 탐색] 서울 전체 — MRT 환산 열스트레스 급간 지도 (래스터)
================================================================
Bröde et al.(2012) Table 3의 UTCI 경계(26/32/38/46)를, 그 시간대 실제
기상값(Ta/RH/wind)을 이용해 "그 경계 UTCI가 나오는 MRT 값"으로 시간대별로
역산해서 경계로 사용 — 23번(UTCI 버전)과 동일한 3색 구간·틀.
"""
import os
import glob
import numpy as np
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
from pythermalcomfort.models import utci
from scipy.optimize import brentq

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
BASE = os.path.join(PROJ, '03_Method_C/results/solweig_seoul_5m_v2_mosaic')
MET_CSV = os.path.join(PROJ, '04_MeteoComparison/results/seoul_met_profile_06_19h.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C/results/figures/seoul_5m_mrt')
os.makedirs(OUT_DIR, exist_ok=True)

UTCI_BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate 상당 (26-32)', 'Strong 상당 (32-38)', 'Very strong 상당 (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap = ListedColormap(COLORS)

met = pd.read_csv(MET_CSV).set_index('hour')


def solve_mrt_for_utci(target, ta, rh, wind):
    # Bröde et al.(2012) 회귀식 유효범위: Tr-Ta in [-30, 70]도
    lo, hi = ta - 30.0, ta + 70.0
    f = lambda tr: float(utci(tdb=ta, tr=tr, v=wind, rh=rh).utci) - target
    flo, fhi = f(lo), f(hi)
    if flo > 0:      # 유효범위 하한(Tr=Ta-30)에서도 이미 target 초과 -> 도달 불가(하한 취급)
        return -274.0
    if fhi < 0:      # 유효범위 상한(Tr=Ta+70)에서도 target 미달 -> 도달 불가(상한 취급)
        return 999.0
    return brentq(f, lo, hi)


def mrt_bounds_for_hour(h):
    row = met.loc[h]
    return [solve_mrt_for_utci(b, row['Ta'], row['RH'], row['wind']) for b in UTCI_BOUNDS]


files = sorted(glob.glob(os.path.join(BASE, 'Tmrt_seoul_5m_*.tif')))
files = [f for f in files if 'average' not in f]
hours = sorted(int(os.path.basename(f).split('_')[-1][:2]) for f in files)

data = {}
for f in files:
    h = int(os.path.basename(f).split('_')[-1][:2])
    with rasterio.open(f) as src:
        data[h] = src.read(1).astype(float)

bounds_by_hour = {h: mrt_bounds_for_hour(h) for h in hours}
print("시간대별 MRT 환산 경계(26/32/38/46 UTCI 상당):")
for h in hours:
    print(f"  {h:02d}시: {[round(b, 1) for b in bounds_by_hour[h]]}")

legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

# ── 1. 시간대별 14장 그리드 (시간마다 경계값이 다름) ────────────────────────
fig, axes = plt.subplots(4, 4, figsize=(16, 15))
for ax, h in zip(axes.flat, hours):
    norm = BoundaryNorm(bounds_by_hour[h], cmap.N)
    ax.imshow(data[h], cmap=cmap, norm=norm)
    b = bounds_by_hour[h]
    ax.set_title(f'{h:02d}시 (경계 {b[0]:.0f}/{b[1]:.0f}/{b[2]:.0f}/{b[3]:.0f})', fontsize=10)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.0), fontsize=11)
fig.suptitle('[방법론 탐색] 서울 전체 — MRT 환산 열스트레스 급간(시간대별 UTCI 26/32/38/46 역산) 시간대별',
             fontsize=15, color='darkblue')
path1 = os.path.join(OUT_DIR, '2026-07-16_MRT_category_hourly_seoul_5m.png')
fig.savefig(path1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path1}")

# ── 2. Colaninno 3구간 (구간 내 시간대 경계 평균을 대표 경계로 사용) ─────────
morning_h, midday_h, evening_h = [6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]
periods = {
    '아침(06-09시)': (np.nanmean([data[h] for h in morning_h], axis=0), morning_h),
    '낮(10-14시)': (np.nanmean([data[h] for h in midday_h], axis=0), midday_h),
    '저녁(15-19시)': (np.nanmean([data[h] for h in evening_h], axis=0), evening_h),
}

fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))
for ax, (label, (arr, hs)) in zip(axes, periods.items()):
    b = np.mean([bounds_by_hour[h] for h in hs], axis=0)
    norm = BoundaryNorm(b, cmap.N)
    ax.imshow(arr, cmap=cmap, norm=norm)
    ax.set_title(f'{label}\n(평균경계 {b[0]:.0f}/{b[1]:.0f}/{b[2]:.0f}/{b[3]:.0f})', fontsize=12)
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.05), fontsize=11)
fig.suptitle('[방법론 탐색] 서울 전체 — MRT 환산 열스트레스 급간 Colaninno 3구간', fontsize=14, color='darkblue')
path2 = os.path.join(OUT_DIR, '2026-07-16_MRT_category_3period_seoul_5m.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path2}")

# ── 3. 구간별 픽셀 비율 요약 ───────────────────────────────────────────────
print("\n구간별 픽셀 비율(3구간 평균경계 기준):")
for label, (arr, hs) in periods.items():
    b = np.mean([bounds_by_hour[h] for h in hs], axis=0)
    valid = arr[~np.isnan(arr)]
    total = valid.size
    below = (valid < b[0]).sum() / total * 100
    m1 = ((valid >= b[0]) & (valid < b[1])).sum() / total * 100
    m2 = ((valid >= b[1]) & (valid < b[2])).sum() / total * 100
    m3 = ((valid >= b[2]) & (valid < b[3])).sum() / total * 100
    above = (valid >= b[3]).sum() / total * 100
    print(f"\n[{label}]")
    print(f"  하한 미만: {below:.1f}% | {LABELS[0]}: {m1:.1f}% | {LABELS[1]}: {m2:.1f}% | "
          f"{LABELS[2]}: {m3:.1f}% | 상한 이상: {above:.1f}%")
