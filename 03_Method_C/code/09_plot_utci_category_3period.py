"""
성동구 파일럿 — 링크별 UTCI 3구간 지도 (Bröde et al. 2012 열스트레스 급간 기준)
================================================================
연속 컬러스케일이 아니라 UTCI 공식 열스트레스 분류(Table 3, p.489)를
그대로 범주형 색상으로 시각화.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

GPKG_PATH = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-09_link_utci_approach1_30m.gpkg'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/seongdong_approach1_30m'
os.makedirs(OUT_DIR, exist_ok=True)

# Bröde et al.(2012) Table 3(p.489) UTCI 열스트레스 분류 — 우리 데이터 범위(약 26~46도)에
# 해당하는 구간만 사용 (그 이하/이상 구간은 이번 파일럿 데이터에 없음)
BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress\n(중간 열스트레스, 26-32)',
          'Strong heat stress\n(강한 열스트레스, 32-38)',
          'Very strong heat stress\n(매우강한 열스트레스, 38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']  # 순차형(옅은 주황 -> 진한 빨강), 심각도 순

cmap = ListedColormap(COLORS)
norm = BoundaryNorm(BOUNDS, cmap.N)

gdf = gpd.read_file(GPKG_PATH)
gdf['아침(06-09시)'] = gdf[[f'UTCI_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'UTCI_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'UTCI_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))
for ax, col in zip(axes, period_cols):
    gdf.plot(column=col, cmap=cmap, norm=norm, linewidth=0.4, ax=ax)
    ax.set_title(col, fontsize=14)
    ax.axis('off')

legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.05), fontsize=10)
fig.suptitle('성동구 파일럿 — 링크별 UTCI 열스트레스 급간 (Bröde et al. 2012), Colaninno 3구간',
             fontsize=16)
path = os.path.join(OUT_DIR, '2026-07-09_LinkUTCI_category_3period_approach1_30m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")

# 구간별 링크 비율 요약 출력
print("\n구간별 링크 비율:")
for col in period_cols:
    print(f"\n[{col}]")
    cats = pd.cut(gdf[col], bins=[-999] + BOUNDS + [999], labels=['이하'] + LABELS + ['이상'])
    print(cats.value_counts(normalize=True).mul(100).round(1))
