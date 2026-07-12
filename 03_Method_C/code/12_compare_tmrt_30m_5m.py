"""
성동구 파일럿 — Tmrt 30m(접근1) vs 5m(접근2) 비교 시각화
================================================================
30m 시각화(03_plot_tmrt_maps.py, 06_plot_tmrt_distributions.py)와
동일한 컬러맵(YlOrRd)·레이아웃 스타일을 쓰되, 두 해상도를 같은
컬러스케일(vmin/vmax 공통)로 그려서 직접 비교 가능하게 함.
※ 5m은 아직 링크 단위 할당 전이라, 분포 비교는 래스터 픽셀값 기준.
"""
import os
import glob
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import gaussian_kde

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

DIR_30M = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/dsm_cdsm_seongdong/solweig_approach1_30m'
DIR_5M = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/solweig_approach2_5m'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures'
os.makedirs(OUT_DIR, exist_ok=True)

CMAP = 'YlOrRd'
HOURS = list(range(6, 20))


def load_hourly(base_dir):
    files = sorted(glob.glob(os.path.join(base_dir, 'Tmrt_2025_209_*.tif')))
    data = {}
    for f in files:
        h = int(os.path.basename(f).split('_')[3][:2])
        with rasterio.open(f) as src:
            d = src.read(1).astype(float)
            d[(d <= -100) | (d >= 200)] = np.nan
            data[h] = d
    return data


data30 = load_hourly(DIR_30M)
data5 = load_hourly(DIR_5M)

# ── 공통 컬러스케일 (30m + 5m 전체값 기준) ──────────────────────────────────
all_vals = np.concatenate(
    [d[~np.isnan(d)] for d in data30.values()] + [d[~np.isnan(d)] for d in data5.values()]
)
VMIN, VMAX = all_vals.min(), all_vals.max()
print(f"공통 컬러스케일(30m+5m): {VMIN:.1f} ~ {VMAX:.1f} degC")


def period_means(data):
    morning = np.nanmean([data[h] for h in [6, 7, 8, 9]], axis=0)
    midday = np.nanmean([data[h] for h in [10, 11, 12, 13, 14]], axis=0)
    evening = np.nanmean([data[h] for h in [15, 16, 17, 18, 19]], axis=0)
    return {'아침(06-09시)': morning, '낮(10-14시)': midday, '저녁(15-19시)': evening}


periods30 = period_means(data30)
periods5 = period_means(data5)

# ── 1. 3구간 비교 (2행 x 3열: 위 30m, 아래 5m) ─────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
for ax, (label, arr) in zip(axes[0], periods30.items()):
    im = ax.imshow(arr, cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(f'{label}\n(접근1, 30m)', fontsize=12)
    ax.axis('off')
for ax, (label, arr) in zip(axes[1], periods5.items()):
    im = ax.imshow(arr, cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(f'{label}\n(접근2, 5m)', fontsize=12)
    ax.axis('off')
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.03, pad=0.03, label='Tmrt (degC)')
fig.suptitle('성동구 파일럿 — Tmrt 해상도 비교: 30m(위) vs 5m(아래), 공통 컬러스케일', fontsize=16)
path = os.path.join(OUT_DIR, '2026-07-12_Tmrt_3period_compare_30m_5m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")

# ── 2. 시간대별 14장 비교 (2행: 위 30m, 아래 5m, 공통 컬러스케일) ───────────
fig, axes = plt.subplots(2, 14, figsize=(28, 5))
for ax, h in zip(axes[0], HOURS):
    im = ax.imshow(data30[h], cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.set_title(f'{h:02d}시', fontsize=10)
    ax.axis('off')
for ax, h in zip(axes[1], HOURS):
    im = ax.imshow(data5[h], cmap=CMAP, vmin=VMIN, vmax=VMAX)
    ax.axis('off')
axes[0, 0].set_ylabel('30m', fontsize=12)
axes[1, 0].set_ylabel('5m', fontsize=12)
fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.02, pad=0.04, label='Tmrt (degC)')
fig.suptitle('성동구 파일럿 — 시간대별 Tmrt: 30m(위) vs 5m(아래), 공통 컬러스케일', fontsize=16)
path = os.path.join(OUT_DIR, '2026-07-12_Tmrt_hourly_compare_30m_5m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")


# ── 3. 분포(KDE) 비교 — 래스터 픽셀값 기준 (5m은 링크할당 전이라 픽셀 기준 통일) ──
def kde_curve(values, n=300):
    values = values[~np.isnan(values)]
    kde = gaussian_kde(values)
    x = np.linspace(VMIN - 2, VMAX + 2, n)
    return x, kde(x), values


period_colors = ['#4C72B0', '#C44E52', '#DD8452']
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharex=True, sharey=True)
for ax, periods, label in zip(axes, [periods30, periods5], ['접근1 (30m)', '접근2 (5m)']):
    for (pname, arr), color in zip(periods.items(), period_colors):
        x, y, vals = kde_curve(arr.flatten())
        ax.plot(x, y, color=color, linewidth=2, label=f'{pname} (평균 {np.nanmean(vals):.1f}°C)')
        ax.fill_between(x, y, color=color, alpha=0.15)
    ax.set_xlabel('Tmrt (°C)')
    ax.set_title(f'{label} — 픽셀 단위 분포')
    ax.legend(frameon=False, fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
axes[0].set_ylabel('밀도(density)')
fig.suptitle('성동구 파일럿 — Tmrt 픽셀값 분포 비교: 30m vs 5m (Colaninno 3구간)', fontsize=15)
path = os.path.join(OUT_DIR, '2026-07-12_TmrtDist_3period_compare_30m_5m.png')
fig.savefig(path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path}")

# ── 4. 통계 요약 출력 ───────────────────────────────────────────────────────
print("\n=== 3구간 평균/표준편차 비교 ===")
for pname in periods30:
    m30, s30 = np.nanmean(periods30[pname]), np.nanstd(periods30[pname])
    m5, s5 = np.nanmean(periods5[pname]), np.nanstd(periods5[pname])
    print(f"{pname}: 30m 평균 {m30:.2f}±{s30:.2f} | 5m 평균 {m5:.2f}±{s5:.2f} | 차이 {m5-m30:+.2f}")
