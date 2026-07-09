"""
성동구 파일럿 — 링크별 Tmrt 값 분포(KDE) 시각화
================================================================
3구간(Colaninno)별, 그리고 06~19시 시간대별 분포를 정규분포 곡선
형태(커널밀도추정, KDE)로 그림.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import gaussian_kde

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

CSV_PATH = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-09_link_tmrt_approach1_30m.csv'
OUT_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures'
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
hours = list(range(6, 20))

df['아침(06-09시)'] = df[[f'Tmrt_{h:02d}' for h in [6, 7, 8, 9]]].mean(axis=1)
df['낮(10-14시)'] = df[[f'Tmrt_{h:02d}' for h in [10, 11, 12, 13, 14]]].mean(axis=1)
df['저녁(15-19시)'] = df[[f'Tmrt_{h:02d}' for h in [15, 16, 17, 18, 19]]].mean(axis=1)


def kde_curve(values, n=300):
    values = values.dropna().values
    kde = gaussian_kde(values)
    x = np.linspace(values.min() - 2, values.max() + 2, n)
    return x, kde(x), values


# ── 1. 3구간 KDE 오버레이 ──────────────────────────────────────────────────
period_cols = ['아침(06-09시)', '낮(10-14시)', '저녁(15-19시)']
period_colors = ['#4C72B0', '#C44E52', '#DD8452']  # 파랑(아침)-빨강(낮)-주황(저녁)

fig, ax = plt.subplots(figsize=(9, 6))
for col, color in zip(period_cols, period_colors):
    x, y, vals = kde_curve(df[col])
    ax.plot(x, y, color=color, linewidth=2, label=f'{col} (평균 {vals.mean():.1f}°C)')
    ax.fill_between(x, y, color=color, alpha=0.15)
ax.set_xlabel('Tmrt (°C)')
ax.set_ylabel('밀도(density)')
ax.set_title('성동구 링크별 Tmrt 분포 — Colaninno 3구간 비교 (접근1, 30m)')
ax.legend(frameon=False)
ax.spines[['top', 'right']].set_visible(False)
path1 = os.path.join(OUT_DIR, '2026-07-09_TmrtDist_3period_approach1_30m.png')
fig.savefig(path1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path1}")

# ── 2. 시간대별(06~19시) 능선그래프(ridgeline) — 시간마다 분산 차이가 커서
#      한 y축에 겹치면 06시처럼 뾰족한 분포가 다른 시간대를 다 눌러버림.
#      각 시간대를 세로로 쌓고, 곡선별로 최고점을 1로 정규화해서 모양만 비교.
cmap = mpl.colormaps['YlOrRd']
fig, ax = plt.subplots(figsize=(9, 8))
OFFSET = 1.1
label_x = df[[f'Tmrt_{h:02d}' for h in hours]].max().max() + 2
for i, h in enumerate(hours):
    color = cmap((h - 6) / (19 - 6))
    x, y, vals = kde_curve(df[f'Tmrt_{h:02d}'])
    y_norm = y / y.max()  # 곡선별 최고점 1로 정규화 (모양 비교용)
    base = i * OFFSET
    ax.plot(x, y_norm + base, color=color, linewidth=1.3)
    ax.fill_between(x, base, y_norm + base, color=color, alpha=0.6)
    ax.text(label_x, base + 0.3, f'{h:02d}시 (평균 {vals.mean():.1f}°C)',
            fontsize=9, va='center')
ax.set_yticks([])
ax.set_xlabel('Tmrt (°C)')
ax.set_title('성동구 링크별 Tmrt 분포 — 시간대별(06~19시) 능선그래프 (접근1, 30m)')
ax.spines[['top', 'right', 'left']].set_visible(False)
path2 = os.path.join(OUT_DIR, '2026-07-09_TmrtDist_hourly_approach1_30m.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path2}")

# ── 3. 시간대별 개별 소형 다중패널 (분포 모양 개별 확인용) ──────────────────
fig, axes = plt.subplots(4, 4, figsize=(16, 14), sharex=True, sharey=False)
all_vals_flat = df[[f'Tmrt_{h:02d}' for h in hours]].values.flatten()
xmin, xmax = np.nanmin(all_vals_flat), np.nanmax(all_vals_flat)
for ax, h in zip(axes.flat, hours):
    color = cmap((h - 6) / (19 - 6))
    x, y, vals = kde_curve(df[f'Tmrt_{h:02d}'])
    ax.plot(x, y, color=color, linewidth=2)
    ax.fill_between(x, y, color=color, alpha=0.2)
    ax.axvline(vals.mean(), color='black', linestyle='--', linewidth=0.8)
    ax.set_title(f'{h:02d}시 (평균 {vals.mean():.1f}°C, 표준편차 {vals.std():.1f})', fontsize=10)
    ax.set_xlim(xmin - 2, xmax + 2)
for ax in axes.flat[len(hours):]:
    ax.axis('off')
fig.suptitle('성동구 링크별 Tmrt 분포 — 시간대별 개별 (접근1, 30m)', fontsize=16)
fig.supxlabel('Tmrt (°C)')
path3 = os.path.join(OUT_DIR, '2026-07-09_TmrtDist_hourly_grid_approach1_30m.png')
fig.savefig(path3, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path3}")
