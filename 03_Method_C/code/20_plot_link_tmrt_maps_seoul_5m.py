"""
서울 전체 — 링크별 Tmrt 지도 시각화 (시간대별 14장 + Colaninno 3구간)
================================================================
성동구 파일럿(05_plot_link_tmrt_maps.py)과 동일 스타일/범례 규칙.
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

GPKG_PATH = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-16_link_tmrt_seoul_5m.gpkg'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/seoul_5m_mrt'
os.makedirs(OUT_DIR, exist_ok=True)

CMAP = 'YlOrRd'

gdf = gpd.read_file(GPKG_PATH)
hours = list(range(6, 20))
hour_cols = [f'Tmrt_{h:02d}' for h in hours]

gdf['아침(06-09시)'] = gdf[[f'Tmrt_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'Tmrt_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'Tmrt_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

all_vals = gdf[hour_cols].values.flatten()
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)
print(f"공통 컬러스케일: {VMIN:.1f} ~ {VMAX:.1f} degC")

fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, hours):
    col = f'Tmrt_{h:02d}'
    gdf.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.15, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
sm = plt.cm.ScalarMappable(cmap=CMAP, norm=mpl.colors.Normalize(vmin=VMIN, vmax=VMAX))
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02,
             label='Tmrt (degC)')
fig.suptitle('서울 전체 — 링크별 시간대별 Tmrt (5m, Method C)', fontsize=17)
hourly_path = os.path.join(OUT_DIR, '2026-07-16_LinkTmrt_hourly_seoul_5m.png')
fig.savefig(hourly_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {hourly_path}")

fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, col in zip(axes, period_cols):
    gdf.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.2, ax=ax)
    ax.set_title(col, fontsize=14)
    ax.axis('off')
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05,
             label='Tmrt (degC)')
fig.suptitle('서울 전체 — 링크별 Colaninno 3구간 평균 Tmrt (5m, Method C)', fontsize=16)
period_path = os.path.join(OUT_DIR, '2026-07-16_LinkTmrt_3period_seoul_5m.png')
fig.savefig(period_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {period_path}")
