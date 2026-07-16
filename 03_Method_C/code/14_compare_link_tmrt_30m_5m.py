"""
성동구 파일럿 — 링크별 Tmrt 30m(접근1) vs 5m(접근2) 비교 시각화
================================================================
05_plot_link_tmrt_maps.py, 06_plot_tmrt_distributions.py와 동일한
컬러맵(YlOrRd)·레이아웃 스타일로, 두 해상도를 공통 컬러스케일로 비교.
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

GPKG_30M = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-09_link_tmrt_approach1_30m.gpkg'
GPKG_5M = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/seongdong_compare_30m_5m'
os.makedirs(OUT_DIR, exist_ok=True)

CMAP = 'YlOrRd'
HOURS = list(range(6, 20))
HOUR_COLS = [f'Tmrt_{h:02d}' for h in HOURS]


def add_periods(gdf):
    gdf['아침(06-09시)'] = gdf[[f'Tmrt_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
    gdf['낮(10-14시)'] = gdf[[f'Tmrt_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
    gdf['저녁(15-19시)'] = gdf[[f'Tmrt_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)
    return gdf


gdf30 = add_periods(gpd.read_file(GPKG_30M))
gdf5 = add_periods(gpd.read_file(GPKG_5M))
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']

# ── 공통 컬러스케일 (30m + 5m 전체 시간대 값 기준) ──────────────────────────
all_vals = np.concatenate([gdf30[HOUR_COLS].values.flatten(), gdf5[HOUR_COLS].values.flatten()])
VMIN, VMAX = np.nanmin(all_vals), np.nanmax(all_vals)
print(f"공통 컬러스케일(30m+5m): {VMIN:.1f} ~ {VMAX:.1f} degC")
sm = plt.cm.ScalarMappable(cmap=CMAP, norm=mpl.colors.Normalize(vmin=VMIN, vmax=VMAX))

# ── 1. 3구간 비교 (2행 x 3열: 위 30m, 아래 5m) ─────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
for ax, col in zip(axes[0], period_cols):
    gdf30.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.4, ax=ax)
    ax.set_title(f'{col}\n(접근1, 30m)', fontsize=13)
    ax.axis('off')
for ax, col in zip(axes[1], period_cols):
    gdf5.plot(column=col, cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.4, ax=ax)
    ax.set_title(f'{col}\n(접근2, 5m)', fontsize=13)
    ax.axis('off')
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.03, pad=0.03, label='Tmrt (degC)')
fig.suptitle('성동구 파일럿 — 링크별 Tmrt 해상도 비교: 30m(위) vs 5m(아래), 공통 컬러스케일', fontsize=17)
path = os.path.join(OUT_DIR, '2026-07-12_LinkTmrt_3period_compare_30m_5m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")

# ── 2. 시간대별 14장 비교 (2행: 위 30m, 아래 5m) ────────────────────────────
fig, axes = plt.subplots(2, 14, figsize=(30, 5.5))
for ax, h in zip(axes[0], HOURS):
    gdf30.plot(column=f'Tmrt_{h:02d}', cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.3, ax=ax)
    ax.set_title(f'{h:02d}시', fontsize=10)
    ax.axis('off')
for ax, h in zip(axes[1], HOURS):
    gdf5.plot(column=f'Tmrt_{h:02d}', cmap=CMAP, vmin=VMIN, vmax=VMAX, linewidth=0.3, ax=ax)
    ax.axis('off')
fig.colorbar(sm, ax=axes, orientation='horizontal', fraction=0.02, pad=0.04, label='Tmrt (degC)')
fig.suptitle('성동구 파일럿 — 링크별 시간대별 Tmrt: 30m(위) vs 5m(아래), 공통 컬러스케일', fontsize=17)
path = os.path.join(OUT_DIR, '2026-07-12_LinkTmrt_hourly_compare_30m_5m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")


# ── 3. 링크값 분포(KDE) 비교 ────────────────────────────────────────────────
def kde_curve(values, n=300):
    values = values.dropna().values
    kde = gaussian_kde(values)
    x = np.linspace(VMIN - 2, VMAX + 2, n)
    return x, kde(x), values


period_colors = ['#4C72B0', '#C44E52', '#DD8452']
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharex=True, sharey=True)
for ax, gdf, label in zip(axes, [gdf30, gdf5], ['접근1 (30m)', '접근2 (5m)']):
    for col, color in zip(period_cols, period_colors):
        x, y, vals = kde_curve(gdf[col])
        ax.plot(x, y, color=color, linewidth=2, label=f'{col} (평균 {vals.mean():.1f}°C)')
        ax.fill_between(x, y, color=color, alpha=0.15)
    ax.set_xlabel('Tmrt (°C)')
    ax.set_title(f'{label} — 링크 단위 분포')
    ax.legend(frameon=False, fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
axes[0].set_ylabel('밀도(density)')
fig.suptitle('성동구 파일럿 — 링크별 Tmrt 분포 비교: 30m vs 5m (Colaninno 3구간)', fontsize=15)
path = os.path.join(OUT_DIR, '2026-07-12_LinkTmrtDist_3period_compare_30m_5m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")

# ── 4. 통계 요약 ────────────────────────────────────────────────────────────
print("\n=== 링크 단위 3구간 평균/표준편차 비교 ===")
for col in period_cols:
    m30, s30 = gdf30[col].mean(), gdf30[col].std()
    m5, s5 = gdf5[col].mean(), gdf5[col].std()
    print(f"{col}: 30m 평균 {m30:.2f}±{s30:.2f} | 5m 평균 {m5:.2f}±{s5:.2f} | 차이 {m5-m30:+.2f}")

# 링크별 30m-5m 차이 통계 (동일 링크 순서 가정: 같은 네트워크 클립이라 u,v,osmid 동일해야 함)
if len(gdf30) == len(gdf5):
    diffs = gdf5[HOUR_COLS].values - gdf30[HOUR_COLS].values
    print(f"\n=== 링크x시간 단위 30m-5m 차이 통계 (n={diffs.size}) ===")
    print(f"평균 차이: {np.nanmean(diffs):+.3f}°C, 표준편차: {np.nanstd(diffs):.3f}, "
          f"절대차 평균: {np.nanmean(np.abs(diffs)):.3f}, 최대절대차: {np.nanmax(np.abs(diffs)):.3f}")
else:
    print(f"\n⚠️ 링크 개수 불일치(30m={len(gdf30)}, 5m={len(gdf5)}) — 링크 단위 차이 통계 생략")
