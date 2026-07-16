"""
[파일럿/미확정] 서울 전체 — UTCI 하드컷 임계값 x 시간대 민감도 분석
================================================================
임계값(28~46도)과 시간대(06~19시)를 함께 바꿔가며 "임계값 이상 링크 비율"이
어떻게 변하는지 확인 — 균형점(약 50%)이 시간대마다 다른 온도에 위치함을 시각화.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
CSV_PATH = os.path.join(PROJ, '03_Method_C', 'results', '2026-07-16_link_utci_seoul_5m_PILOT.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'figures', 'seoul_5m_utci_PILOT')
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
hours = list(range(6, 20))
thresholds = np.arange(28, 47, 1)

# ── 임계값 x 시간대 매트릭스 ────────────────────────────────────────────────
matrix = np.zeros((len(hours), len(thresholds)))
for i, h in enumerate(hours):
    col = f'UTCI_{h:02d}'
    for j, t in enumerate(thresholds):
        matrix[i, j] = (df[col] >= t).mean() * 100

# ── 1. 히트맵 ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
im = ax.imshow(matrix, aspect='auto', cmap='RdYlBu_r', vmin=0, vmax=100)
ax.set_xticks(range(len(thresholds)))
ax.set_xticklabels(thresholds)
ax.set_yticks(range(len(hours)))
ax.set_yticklabels([f'{h:02d}시' for h in hours])
ax.set_xlabel('UTCI 임계값 (°C)')
ax.set_ylabel('시간대')
ax.set_title('[파일럿/미확정] 임계값 x 시간대 — 임계값 이상 링크 비율(%)', color='darkred')
# 50% 등고선 표시(균형점)
cs = ax.contour(range(len(thresholds)), range(len(hours)), matrix, levels=[50],
                 colors='black', linewidths=2)
ax.clabel(cs, fmt='균형점(50%%)', fontsize=10)
fig.colorbar(im, ax=ax, label='임계값 이상 링크 비율 (%)')
path1 = os.path.join(OUT_DIR, '2026-07-16_UTCI_sensitivity_heatmap_seoul_5m_PILOT.png')
fig.savefig(path1, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path1}")

# ── 2. 대표 시간대 라인 플롯 ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
cmap = mpl.colormaps['YlOrRd']
for h in hours:
    i = hours.index(h)
    color = cmap((h - 6) / (19 - 6))
    ax.plot(thresholds, matrix[i], color=color, linewidth=1.5, alpha=0.8, label=f'{h:02d}시')
ax.axhline(50, color='black', linestyle='--', linewidth=1, label='균형점(50%)')
ax.set_xlabel('UTCI 임계값 (°C)')
ax.set_ylabel('임계값 이상 링크 비율 (%)')
ax.set_title('[파일럿/미확정] 시간대별 임계값 민감도 곡선', color='darkred')
ax.legend(ncol=2, fontsize=8, frameon=False, loc='center left', bbox_to_anchor=(1.0, 0.5))
ax.spines[['top', 'right']].set_visible(False)
path2 = os.path.join(OUT_DIR, '2026-07-16_UTCI_sensitivity_curves_seoul_5m_PILOT.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path2}")

# ── 3. 시간대별 균형점(50%에 가장 가까운 임계값) 표 ────────────────────────
print("\n시간대별 균형점(50%에 가장 가까운 임계값):")
for i, h in enumerate(hours):
    idx = np.argmin(np.abs(matrix[i] - 50))
    print(f"  {h:02d}시: {thresholds[idx]}도 (그때 비율 {matrix[i, idx]:.1f}%)")
