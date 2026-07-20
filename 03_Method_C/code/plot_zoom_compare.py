"""
매칭 지역(시청, 차이 거의 0) vs 편차 최대 지역(도봉산) — v2/v3 동일 스케일 확대 비교
2x2 그리드: 행=지역(시청/도봉산), 열=버전(v2/v3). 네 패널 모두 동일 vmin/vmax, 동일 지리적 범위(2km x 2km).
"""
import os
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

CROP_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/compare_v2_v3_seoul_5m/zoom_crops'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_v2_v3_seoul_5m'
os.makedirs(OUT_DIR, exist_ok=True)

SITES = [('cityhall', '시청 (매칭 지역)'), ('dobongsan', '도봉산 (편차 최대 지역)')]
HALF_M = 1000  # 2km x 2km 표시 범위(고정)


def load(site, var):
    with rasterio.open(os.path.join(CROP_DIR, f'{site}_{var}.tif')) as src:
        arr = src.read(1)
        bounds = src.bounds
        cx = (bounds.left + bounds.right) / 2
        cy = (bounds.bottom + bounds.top) / 2
    return arr, bounds, cx, cy


# ── Tmrt 2x2 ─────────────────────────────────────────────────────────────
arrs = {}
for site, _ in SITES:
    for ver in ['v2', 'v3']:
        arrs[(site, ver)] = load(site, f'Tmrt_{ver}')

vmin_t = min(np.nanmin(a[0]) for a in arrs.values())
vmax_t = max(np.nanmax(a[0]) for a in arrs.values())

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
for i, (site, site_label) in enumerate(SITES):
    _, _, cx, cy = arrs[(site, 'v2')]
    for j, ver in enumerate(['v2', 'v3']):
        arr, bounds, _, _ = arrs[(site, ver)]
        ax = axes[i, j]
        im = ax.imshow(arr, cmap='YlOrRd', vmin=vmin_t, vmax=vmax_t,
                        extent=(bounds.left, bounds.right, bounds.bottom, bounds.top))
        # 동일 지도 축척 강제: 중심 기준 ±HALF_M 고정
        ax.set_xlim(cx - HALF_M, cx + HALF_M)
        ax.set_ylim(cy - HALF_M, cy + HALF_M)
        ax.set_aspect('equal')
        ax.set_title(f'{site_label} — {"v2(30m 소스)" if ver=="v2" else "v3(1m 소스)"}', fontsize=12)
        ax.set_xticks([]); ax.set_yticks([])
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.03, pad=0.03, label='Tmrt 평균 (degC)')
fig.suptitle('동일 스케일(2km x 2km) 확대 비교 — Tmrt 평균', fontsize=16)
p1 = os.path.join(OUT_DIR, '2026-07-20_zoom_compare_Tmrt.png')
fig.savefig(p1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p1}")

# ── UTCI 2x2 (Bröde 카테고리) ─────────────────────────────────────────────
BOUNDS = [26, 32, 38, 46]
LABELS = ['Moderate heat stress (26-32)', 'Strong heat stress (32-38)',
          'Very strong heat stress (38-46)']
COLORS = ['#FED976', '#FD8D3C', '#BD0026']
cmap_cat = ListedColormap(COLORS)
norm_cat = BoundaryNorm(BOUNDS, cmap_cat.N)
legend_handles = [Patch(facecolor=c, label=l) for c, l in zip(COLORS, LABELS)]

arrs_u = {}
for site, _ in SITES:
    for ver in ['v2', 'v3']:
        arrs_u[(site, ver)] = load(site, f'UTCI_{ver}')

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
for i, (site, site_label) in enumerate(SITES):
    _, _, cx, cy = arrs_u[(site, 'v2')]
    for j, ver in enumerate(['v2', 'v3']):
        arr, bounds, _, _ = arrs_u[(site, ver)]
        ax = axes[i, j]
        ax.imshow(arr, cmap=cmap_cat, norm=norm_cat,
                  extent=(bounds.left, bounds.right, bounds.bottom, bounds.top))
        ax.set_xlim(cx - HALF_M, cx + HALF_M)
        ax.set_ylim(cy - HALF_M, cy + HALF_M)
        ax.set_aspect('equal')
        ax.set_title(f'{site_label} — {"v2(30m 소스)" if ver=="v2" else "v3(1m 소스)"}', fontsize=12)
        ax.set_xticks([]); ax.set_yticks([])
fig.legend(handles=legend_handles, loc='lower center', ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.02), fontsize=11)
fig.suptitle('동일 스케일(2km x 2km) 확대 비교 — UTCI 열스트레스 급간', fontsize=16)
p2 = os.path.join(OUT_DIR, '2026-07-20_zoom_compare_UTCI.png')
fig.savefig(p2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {p2}")
