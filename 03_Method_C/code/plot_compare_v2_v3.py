"""
서울 전체 v2(30m DEM 소스) vs v3(1m DEM 소스) 비교 시각화
- 평균 Tmrt/UTCI 나란히 비교, 산점도, Hard Cut(38도) 분류 불일치 지도
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

GPKG_PATH = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-20_link_compare_v2_v3_seoul_5m.gpkg'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_v2_v3_seoul_5m'
os.makedirs(OUT_DIR, exist_ok=True)

gdf = gpd.read_file(GPKG_PATH)

BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap_cat = ListedColormap(COLORS)
norm_cat = BoundaryNorm(BOUNDS, cmap_cat.N)
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

# ── 3. 평균 Tmrt 나란히(v2|v3) ────────────────────────────────────────────
vmin_t = min(gdf['Tmrt_avg_v2'].min(), gdf['Tmrt_avg_v3'].min())
vmax_t = max(gdf['Tmrt_avg_v2'].max(), gdf['Tmrt_avg_v3'].max())
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
gdf.plot(column='Tmrt_avg_v2', cmap='YlOrRd', vmin=vmin_t, vmax=vmax_t, linewidth=0.15, ax=axes[0])
axes[0].set_title('v2 (30m DEM 소스)', fontsize=14)
gdf.plot(column='Tmrt_avg_v3', cmap='YlOrRd', vmin=vmin_t, vmax=vmax_t, linewidth=0.15, ax=axes[1])
axes[1].set_title('v3 (1m DEM 소스)', fontsize=14)
for ax in axes:
    ax.axis('off')
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=mpl.colors.Normalize(vmin=vmin_t, vmax=vmax_t))
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.04, pad=0.03, label='Tmrt 평균 (degC)')
fig.suptitle('서울 전체 링크 평균 Tmrt — v2(30m) vs v3(1m) 소스 비교 (5m)', fontsize=16)
p5 = os.path.join(OUT_DIR, '2026-07-20_compare_Tmrt_avg_v2_v3.png')
fig.savefig(p5, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p5}")

# ── 4. 평균 UTCI 나란히(v2|v3, Bröde 카테고리) ────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
gdf.plot(column='UTCI_avg_v2', cmap=cmap_cat, norm=norm_cat, linewidth=0.15, ax=axes[0])
axes[0].set_title('v2 (30m DEM 소스)', fontsize=14)
gdf.plot(column='UTCI_avg_v3', cmap=cmap_cat, norm=norm_cat, linewidth=0.15, ax=axes[1])
axes[1].set_title('v3 (1m DEM 소스)', fontsize=14)
for ax in axes:
    ax.axis('off')
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.02), fontsize=11)
fig.suptitle('서울 전체 링크 평균 UTCI 급간 — v2(30m) vs v3(1m) 소스 비교 (5m)', fontsize=16)
p6 = os.path.join(OUT_DIR, '2026-07-20_compare_UTCI_avg_v2_v3.png')
fig.savefig(p6, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p6}")

# ── 5. 차이 지도 (발산형 컬러맵) ───────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
for ax, col, title in zip(axes, ['Tmrt_diff_v3_v2', 'UTCI_diff_v3_v2'],
                          ['Tmrt 차이 (v3-v2)', 'UTCI 차이 (v3-v2)']):
    vabs = max(abs(gdf[col].min()), abs(gdf[col].max()))
    gdf.plot(column=col, cmap='RdBu_r', vmin=-vabs, vmax=vabs, linewidth=0.2, ax=ax,
             legend=True, legend_kwds={'label': title, 'shrink': 0.6})
    ax.set_title(title, fontsize=14)
    ax.axis('off')
fig.suptitle('서울 전체 링크 Tmrt/UTCI 평균 차이 지도 (v3 - v2, 5m)', fontsize=16)
p7 = os.path.join(OUT_DIR, '2026-07-20_compare_diff_map_v3minusv2.png')
fig.savefig(p7, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p7}")

# ── 6. 산점도 ──────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 6))
for ax, (c2, c3, name) in zip(axes, [('Tmrt_avg_v2', 'Tmrt_avg_v3', 'Tmrt'),
                                       ('UTCI_avg_v2', 'UTCI_avg_v3', 'UTCI')]):
    x, y = gdf[c2].values, gdf[c3].values
    ax.scatter(x, y, s=1, alpha=0.05, color='steelblue', rasterized=True)
    lims = [min(x.min(), y.min()), max(x.max(), y.max())]
    ax.plot(lims, lims, 'r--', linewidth=1, label='1:1')
    r = np.corrcoef(x, y)[0, 1]
    mae = np.abs(y - x).mean()
    ax.text(0.05, 0.92, f'r={r:.4f}\nMAE={mae:.3f}°C', transform=ax.transAxes,
            fontsize=12, va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.set_xlabel(f'{name} v2 (30m 소스)')
    ax.set_ylabel(f'{name} v3 (1m 소스)')
    ax.set_title(f'{name} 평균 — 링크 469,010개')
    ax.legend(loc='lower right')
fig.suptitle('v2 vs v3 링크 평균 산점도', fontsize=15)
p8 = os.path.join(OUT_DIR, '2026-07-20_compare_scatter_v2_v3.png')
fig.savefig(p8, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p8}")

# ── 7. Hard Cut(38도) 분류 불일치 지도 ────────────────────────────────────
agree = gdf[gdf['hardcut38_agree']]
disagree = gdf[~gdf['hardcut38_agree']]
fig, ax = plt.subplots(figsize=(10, 10))
agree.plot(ax=ax, color='#cccccc', linewidth=0.15)
disagree.plot(ax=ax, color='#e41a1c', linewidth=2.0)
ax.axis('off')
ax.set_title(f'Hard Cut(UTCI≥38°C) 분류 불일치 링크 — {len(disagree):,}개 / {len(gdf):,}개 '
             f'({len(disagree)/len(gdf)*100:.2f}%)', fontsize=14)
handles = [Patch(facecolor='#cccccc', label='일치'), Patch(facecolor='#e41a1c', label='불일치')]
ax.legend(handles=handles, loc='lower left', frameon=True)
p9 = os.path.join(OUT_DIR, '2026-07-20_compare_hardcut38_disagreement.png')
fig.savefig(p9, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p9}")
