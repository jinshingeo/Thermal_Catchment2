"""
성동구 파일럿 — 링크별 UTCI 시간대별(06~19시) 급간 지도 (Bröde et al. 2012 기준)
"""
import os
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

BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap = ListedColormap(COLORS)
norm = BoundaryNorm(BOUNDS, cmap.N)

gdf = gpd.read_file(GPKG_PATH)
hours = list(range(6, 20))

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, hours):
    gdf.plot(column=f'UTCI_{h:02d}', cmap=cmap, norm=norm, linewidth=0.3, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')

legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.06), fontsize=11)
fig.suptitle('성동구 파일럿 — 링크별 UTCI 열스트레스 급간(Bröde et al. 2012) 시간대별',
             fontsize=17)
path = os.path.join(OUT_DIR, '2026-07-09_LinkUTCI_category_hourly_approach1_30m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")
