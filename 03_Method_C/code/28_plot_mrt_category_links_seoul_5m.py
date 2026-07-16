"""
[방법론 탐색] 서울 전체 — 링크별 MRT 환산 열스트레스 급간 지도
================================================================
27번(래스터 버전)과 동일한 시간대별 MRT 환산 경계(UTCI 26/32/38/46 역산)를
링크(Colaninno 버퍼 zonal mean) MRT 값에 적용 — 24번(UTCI 버전)과 동일한 틀.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch
from pythermalcomfort.models import utci
from scipy.optimize import brentq

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
GPKG_PATH = os.path.join(PROJ, '03_Method_C/results/2026-07-16_link_tmrt_seoul_5m.gpkg')
MET_CSV = os.path.join(PROJ, '04_MeteoComparison/results/seoul_met_profile_06_19h.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C/results/figures/seoul_5m_mrt')
os.makedirs(OUT_DIR, exist_ok=True)

UTCI_BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate 상당 (26-32)', 'Strong 상당 (32-38)', 'Very strong 상당 (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap = ListedColormap(COLORS)

met = pd.read_csv(MET_CSV).set_index('hour')


def solve_mrt_for_utci(target, ta, rh, wind):
    lo, hi = ta - 30.0, ta + 70.0
    f = lambda tr: float(utci(tdb=ta, tr=tr, v=wind, rh=rh).utci) - target
    flo, fhi = f(lo), f(hi)
    if flo > 0:
        return -274.0
    if fhi < 0:
        return 999.0
    return brentq(f, lo, hi)


def mrt_bounds_for_hour(h):
    row = met.loc[h]
    return [solve_mrt_for_utci(b, row['Ta'], row['RH'], row['wind']) for b in UTCI_BOUNDS]


gdf = gpd.read_file(GPKG_PATH)
hours = list(range(6, 20))
bounds_by_hour = {h: mrt_bounds_for_hour(h) for h in hours}
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

# ── 1. 시간대별 14장 그리드 ────────────────────────────────────────────────
fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, hours):
    b = bounds_by_hour[h]
    norm = BoundaryNorm(b, cmap.N)
    gdf.plot(column=f'Tmrt_{h:02d}', cmap=cmap, norm=norm, linewidth=0.15, ax=ax)
    ax.set_title(f'{h:02d}시 (경계 {b[0]:.0f}/{b[1]:.0f}/{b[2]:.0f}/{b[3]:.0f})', fontsize=11)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.05), fontsize=11)
fig.suptitle('[방법론 탐색] 서울 전체 — 링크별 MRT 환산 열스트레스 급간 시간대별 (5m)',
             fontsize=17, color='darkblue')
path1 = os.path.join(OUT_DIR, '2026-07-16_LinkMRT_category_hourly_seoul_5m.png')
fig.savefig(path1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path1}")

# ── 2. Colaninno 3구간 ─────────────────────────────────────────────────────
morning_h, midday_h, evening_h = [6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]
gdf['아침(06-09시)'] = gdf[[f'Tmrt_{h:02d}' for h in morning_h]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'Tmrt_{h:02d}' for h in midday_h]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'Tmrt_{h:02d}' for h in evening_h]].mean(axis=1)
period_cols = {'아침(06-09시)': morning_h, '낮(10-14시)': midday_h, '저녁(15-19시)': evening_h}

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, (col, hs) in zip(axes, period_cols.items()):
    b = np.mean([bounds_by_hour[h] for h in hs], axis=0)
    norm = BoundaryNorm(b, cmap.N)
    gdf.plot(column=col, cmap=cmap, norm=norm, linewidth=0.2, ax=ax)
    ax.set_title(f'{col}\n(평균경계 {b[0]:.0f}/{b[1]:.0f}/{b[2]:.0f}/{b[3]:.0f})', fontsize=13)
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.05), fontsize=11)
fig.suptitle('[방법론 탐색] 서울 전체 — 링크별 MRT 환산 열스트레스 급간 Colaninno 3구간 (5m)',
             fontsize=16, color='darkblue')
path2 = os.path.join(OUT_DIR, '2026-07-16_LinkMRT_category_3period_seoul_5m.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path2}")

# ── 3. 구간별 링크 비율 요약 ───────────────────────────────────────────────
print("\n구간별 링크 비율(3구간 평균경계 기준):")
for col, hs in period_cols.items():
    b = np.mean([bounds_by_hour[h] for h in hs], axis=0)
    print(f"\n[{col}]")
    cats = pd.cut(gdf[col], bins=[-999] + list(b) + [9999], labels=['하한미만'] + LABELS + ['상한이상'])
    print(cats.value_counts(normalize=True).mul(100).round(1))
