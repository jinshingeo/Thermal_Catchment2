"""
서울 전체 — MRT 하드컷 임계값 x 시간대 민감도 분석
================================================================
25번(UTCI 버전)과 동일한 분석을 MRT 기준으로 수행 — 임계값(24~70도)과
시간대(06~19시)를 함께 바꿔가며 "임계값 이상 링크 비율"을 확인.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
CSV_PATH = os.path.join(PROJ, '03_Method_C', 'results', '2026-07-16_link_tmrt_seoul_5m.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'figures', 'seoul_5m_mrt')
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
hours = list(range(6, 20))
thresholds = np.arange(24, 71, 2)

matrix = np.zeros((len(hours), len(thresholds)))
for i, h in enumerate(hours):
    col = f'Tmrt_{h:02d}'
    for j, t in enumerate(thresholds):
        matrix[i, j] = (df[col] >= t).mean() * 100

# ── 1. 히트맵 ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))
im = ax.imshow(matrix, aspect='auto', cmap='RdYlBu_r', vmin=0, vmax=100)
ax.set_xticks(range(len(thresholds)))
ax.set_xticklabels(thresholds)
ax.set_yticks(range(len(hours)))
ax.set_yticklabels([f'{h:02d}시' for h in hours])
ax.set_xlabel('MRT 임계값 (°C)')
ax.set_ylabel('시간대')
ax.set_title('서울 전체 — MRT 임계값 x 시간대 (임계값 이상 링크 비율, %)')
cs = ax.contour(range(len(thresholds)), range(len(hours)), matrix, levels=[50],
                 colors='black', linewidths=2)
ax.clabel(cs, fmt='균형점(50%%)', fontsize=10)
fig.colorbar(im, ax=ax, label='임계값 이상 링크 비율 (%)')
path1 = os.path.join(OUT_DIR, '2026-07-16_MRT_sensitivity_heatmap_seoul_5m.png')
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
ax.set_xlabel('MRT 임계값 (°C)')
ax.set_ylabel('임계값 이상 링크 비율 (%)')
ax.set_title('서울 전체 — 시간대별 MRT 임계값 민감도 곡선')
ax.legend(ncol=2, fontsize=8, frameon=False, loc='center left', bbox_to_anchor=(1.0, 0.5))
ax.spines[['top', 'right']].set_visible(False)
path2 = os.path.join(OUT_DIR, '2026-07-16_MRT_sensitivity_curves_seoul_5m.png')
fig.savefig(path2, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f"저장: {path2}")

print("\n시간대별 균형점(50%에 가장 가까운 임계값):")
for i, h in enumerate(hours):
    idx = np.argmin(np.abs(matrix[i] - 50))
    print(f"  {h:02d}시: {thresholds[idx]}도 (그때 비율 {matrix[i, idx]:.1f}%)")

# ── 3. 전환구간 폭 비교 (90%->10% 되는 데 걸리는 임계값 폭) ────────────────
print("\n시간대별 '전환구간 폭'(비율이 90%에서 10%로 떨어지는 임계값 범위):")
for i, h in enumerate(hours):
    row = matrix[i]
    above90 = thresholds[row >= 90]
    below10 = thresholds[row <= 10]
    if len(above90) == 0 or len(below10) == 0:
        print(f"  {h:02d}시: 해당없음(전 구간 90%이상 또는 10%이하)")
        continue
    t90 = above90.max()
    t10 = below10.min()
    print(f"  {h:02d}시: {t90}도(90%) -> {t10}도(10%), 폭 {t10-t90}도")
