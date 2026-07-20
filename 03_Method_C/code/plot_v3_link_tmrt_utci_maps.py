"""
서울 전체 v3(1m DEM 소스) — 링크별 Tmrt 연속값 + UTCI 급간(Bröde 2012) 지도
20_plot_link_tmrt_maps_seoul_5m.py / 24_plot_utci_category_links_seoul_5m_PILOT.py와
동일 스타일로 v3에 재현.
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

GPKG_PATH = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_v2_v3_seoul_5m'
os.makedirs(OUT_DIR, exist_ok=True)

gdf = gpd.read_file(GPKG_PATH)
hours = list(range(6, 20))

# ── 1. Tmrt 연속값 (YlOrRd) ──────────────────────────────────────────────
CMAP = 'YlOrRd'
hour_cols = [f'Tmrt_{h:02d}' for h in hours]
all_vals = gdf[hour_cols].values.flatten()
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, hours):
    gdf.plot(column=f'Tmrt_{h:02d}', cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.15, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
sm = plt.cm.ScalarMappable(cmap=CMAP, norm=mpl.colors.Normalize(vmin=VMIN, vmax=VMAX))
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02, label='Tmrt (degC)')
fig.suptitle('서울 전체 v3(1m DEM 소스) — 링크별 시간대별 Tmrt (5m)', fontsize=17)
p1 = os.path.join(OUT_DIR, '2026-07-20_v3_LinkTmrt_hourly_seoul_5m.png')
fig.savefig(p1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p1}")

gdf['아침(06-09시)'] = gdf[[f'Tmrt_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'Tmrt_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'Tmrt_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col in zip(axes, period_cols):
    gdf.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.2, ax=ax)
    ax.set_title(col, fontsize=14)
    ax.axis('off')
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05, label='Tmrt (degC)')
fig.suptitle('서울 전체 v3(1m DEM 소스) — 링크별 Colaninno 3구간 평균 Tmrt (5m)', fontsize=16)
p2 = os.path.join(OUT_DIR, '2026-07-20_v3_LinkTmrt_3period_seoul_5m.png')
fig.savefig(p2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p2}")

# ── 2. UTCI 급간(Bröde 2012) ──────────────────────────────────────────────
BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap_cat = ListedColormap(COLORS)
norm_cat = BoundaryNorm(BOUNDS, cmap_cat.N)
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, hours):
    gdf.plot(column=f'UTCI_{h:02d}', cmap=cmap_cat, norm=norm_cat, linewidth=0.15, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, 0.05), fontsize=11)
fig.suptitle('서울 전체 v3(1m DEM 소스) — 링크별 UTCI 열스트레스 급간 시간대별 (5m)', fontsize=17)
p3 = os.path.join(OUT_DIR, '2026-07-20_v3_LinkUTCI_category_hourly_seoul_5m.png')
fig.savefig(p3, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p3}")

gdf['UTCI_아침(06-09시)'] = gdf[[f'UTCI_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['UTCI_낮(10-14시)'] = gdf[[f'UTCI_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['UTCI_저녁(15-19시)'] = gdf[[f'UTCI_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
utci_period_cols = ['UTCI_아침(06-09시)', 'UTCI_낮(10-14시)', 'UTCI_저녁(15-19시)']

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col in zip(axes, utci_period_cols):
    gdf.plot(column=col, cmap=cmap_cat, norm=norm_cat, linewidth=0.2, ax=ax)
    ax.set_title(col.replace('UTCI_', ''), fontsize=14)
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.05), fontsize=11)
fig.suptitle('서울 전체 v3(1m DEM 소스) — 링크별 UTCI 열스트레스 급간 Colaninno 3구간 (5m)', fontsize=16)
p4 = os.path.join(OUT_DIR, '2026-07-20_v3_LinkUTCI_category_3period_seoul_5m.png')
fig.savefig(p4, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p4}")
