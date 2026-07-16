"""
[파일럿/미확정] 서울 전체 — 링크별 UTCI 열스트레스 급간 지도 (Bröde et al. 2012 Table 3)
================================================================
성동구 파일럿(09/10번 스크립트)과 완전히 동일한 구간·색상.
"""
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

GPKG_PATH = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-16_link_utci_seoul_5m_PILOT.gpkg'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/seoul_5m_utci_PILOT'
os.makedirs(OUT_DIR, exist_ok=True)

BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap = ListedColormap(COLORS)
norm = BoundaryNorm(BOUNDS, cmap.N)

gdf = gpd.read_file(GPKG_PATH)
hours = list(range(6, 20))
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

# ── 1. 시간대별 14장 그리드 ────────────────────────────────────────────────
fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, hours):
    gdf.plot(column=f'UTCI_{h:02d}', cmap=cmap, norm=norm, linewidth=0.15, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.05), fontsize=11)
fig.suptitle('[파일럿/미확정] 서울 전체 — 링크별 UTCI 열스트레스 급간 시간대별 (5m)',
             fontsize=17, color='darkred')
path1 = os.path.join(OUT_DIR, '2026-07-16_LinkUTCI_category_hourly_seoul_5m_PILOT.png')
fig.savefig(path1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path1}")

# ── 2. Colaninno 3구간 ─────────────────────────────────────────────────────
gdf['아침(06-09시)'] = gdf[[f'UTCI_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'UTCI_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'UTCI_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col in zip(axes, period_cols):
    gdf.plot(column=col, cmap=cmap, norm=norm, linewidth=0.2, ax=ax)
    ax.set_title(col, fontsize=14)
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.05), fontsize=11)
fig.suptitle('[파일럿/미확정] 서울 전체 — 링크별 UTCI 열스트레스 급간 Colaninno 3구간 (5m)',
             fontsize=16, color='darkred')
path2 = os.path.join(OUT_DIR, '2026-07-16_LinkUTCI_category_3period_seoul_5m_PILOT.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path2}")

# ── 3. 구간별 링크 비율 요약 ───────────────────────────────────────────────
print("\n구간별 링크 비율:")
for col in period_cols:
    print(f"\n[{col}]")
    cats = pd.cut(gdf[col], bins=[-999] + BOUNDS + [999], labels=['이하'] + LABELS + ['이상'])
    print(cats.value_counts(normalize=True).mul(100).round(1))
