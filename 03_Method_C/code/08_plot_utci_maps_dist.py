"""
성동구 파일럿 — 링크별 UTCI 지도 + 분포 시각화 (시간대별 14장 + Colaninno 3구간)
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import gaussian_kde

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

GPKG_PATH = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-09_link_utci_approach1_30m.gpkg'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures'
os.makedirs(OUT_DIR, exist_ok=True)
CMAP = 'YlOrRd'

gdf = gpd.read_file(GPKG_PATH)
hours = list(range(6, 20))
gdf['아침(06-09시)'] = gdf[[f'UTCI_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
gdf['낮(10-14시)'] = gdf[[f'UTCI_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
gdf['저녁(15-19시)'] = gdf[[f'UTCI_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

all_vals = gdf[[f'UTCI_{h:02d}' for h in hours]].values.flatten()
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)
print(f"공통 컬러스케일: {VMIN:.1f} ~ {VMAX:.1f} degC")

# ── 1. 시간대별 지도 ────────────────────────────────────────────────────
fig, axes = plt.subplots(4, 4, figsize=(18, 18))
for ax, h in zip(axes.flat, hours):
    gdf.plot(column=f'UTCI_{h:02d}', cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.3, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=13)
    ax.axis('off')
for ax in axes.flat[len(hours):]:
    ax.axis('off')
sm = plt.cm.ScalarMappable(cmap=CMAP, norm=mpl.colors.Normalize(vmin=VMIN, vmax=VMAX))
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.02, label='UTCI (degC)')
fig.suptitle('성동구 파일럿 — 링크별 시간대별 UTCI (접근1, 30m, IDW Ta/RH)', fontsize=17)
p = os.path.join(OUT_DIR, '2026-07-09_LinkUTCI_hourly_approach1_30m.png')
fig.savefig(p, dpi=150, bbox_inches='tight'); plt.close(fig); print(f"저장: {p}")

# ── 2. Colaninno 3구간 ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, col in zip(axes, period_cols):
    gdf.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.4, ax=ax)
    ax.set_title(col, fontsize=14)
    ax.axis('off')
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05, label='UTCI (degC)')
fig.suptitle('성동구 파일럿 — 링크별 Colaninno 3구간 평균 UTCI (접근1, 30m)', fontsize=16)
p = os.path.join(OUT_DIR, '2026-07-09_LinkUTCI_3period_approach1_30m.png')
fig.savefig(p, dpi=150, bbox_inches='tight'); plt.close(fig); print(f"저장: {p}")


# ── 3. 분포(KDE) ────────────────────────────────────────────────────────
def kde_curve(values, n=300):
    values = values.dropna().values
    kde = gaussian_kde(values)
    x = np.linspace(values.min() - 2, values.max() + 2, n)
    return x, kde(x), values


df = pd.DataFrame(gdf.drop(columns='geometry'))
period_colors = ['#4C72B0', '#C44E52', '#DD8452']
fig, ax = plt.subplots(figsize=(9, 6))
for col, color in zip(period_cols, period_colors):
    x, y, vals = kde_curve(df[col])
    ax.plot(x, y, color=color, linewidth=2, label=f'{col} (평균 {vals.mean():.1f}°C)')
    ax.fill_between(x, y, color=color, alpha=0.15)
ax.axvline(38, color='gray', linestyle=':', linewidth=1)
ax.text(38.2, ax.get_ylim()[1]*0.5, 'UTCI 38°C', fontsize=9, ha='left', color='gray',
        rotation=90, va='center')
ax.set_xlabel('UTCI (°C)'); ax.set_ylabel('밀도(density)')
ax.set_title('성동구 링크별 UTCI 분포 — Colaninno 3구간 비교 (접근1, 30m)')
ax.legend(frameon=False); ax.spines[['top', 'right']].set_visible(False)
p = os.path.join(OUT_DIR, '2026-07-09_UTCIDist_3period_approach1_30m.png')
fig.savefig(p, dpi=150, bbox_inches='tight'); plt.close(fig); print(f"저장: {p}")

cmap = mpl.colormaps['YlOrRd']
fig, ax = plt.subplots(figsize=(9, 8))
label_x = df[[f'UTCI_{h:02d}' for h in hours]].max().max() + 2
for i, h in enumerate(hours):
    color = cmap((h - 6) / (19 - 6))
    x, y, vals = kde_curve(df[f'UTCI_{h:02d}'])
    y_norm = y / y.max()
    base = i * 1.1
    ax.plot(x, y_norm + base, color=color, linewidth=1.3)
    ax.fill_between(x, base, y_norm + base, color=color, alpha=0.6)
    ax.text(label_x, base + 0.3, f'{h:02d}시 (평균 {vals.mean():.1f}°C)', fontsize=9, va='center')
ax.set_yticks([]); ax.set_xlabel('UTCI (°C)')
ax.set_title('성동구 링크별 UTCI 분포 — 시간대별(06~19시) 능선그래프 (접근1, 30m)')
ax.spines[['top', 'right', 'left']].set_visible(False)
p = os.path.join(OUT_DIR, '2026-07-09_UTCIDist_hourly_approach1_30m.png')
fig.savefig(p, dpi=150, bbox_inches='tight'); plt.close(fig); print(f"저장: {p}")
