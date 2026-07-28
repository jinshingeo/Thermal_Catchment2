"""해상도(1/5/10/30m)별 소요시간 vs 정밀도 트레이드오프 그래프
근거논문: 없음(자체 산출 비교). 박진우 교수님 제안 — 5m 채택의 엘보우 포인트 근거 시각화.
"""
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TODAY = '2026-07-29'
STATS_DIR = os.path.join(BASE, '03_Method_C/results/compare_resolution_tradeoff')
FIG_DIR = os.path.join(BASE, '03_Method_C/results/figures')

prec = pd.read_csv(os.path.join(STATS_DIR, f'{TODAY}_precision_vs_1mtrue.csv'))
timing = pd.read_csv(os.path.join(STATS_DIR, f'{TODAY}_timing_summary.csv'))

df = pd.merge(timing, prec, on='resolution', how='outer')
# 1m 행은 기준값(자기 자신과 비교)이므로 정밀도 지표가 비어있음 — 100%/r=1.0으로 채움
precision_cols_100 = ['pixel_HardCut38_agree_pct', 'link_HardCut38_agree_pct']
precision_cols_r1 = ['pixel_Tmrt_r', 'pixel_UTCI_r', 'link_Tmrt_r', 'link_UTCI_r']
is_1m = df['resolution'] == '1m'
for c in precision_cols_100:
    df.loc[is_1m, c] = 100.0
for c in precision_cols_r1:
    df.loc[is_1m, c] = 1.0

df['res_m'] = df['resolution'].str.replace('m', '').astype(float)
df = df.sort_values('res_m')
df.to_csv(os.path.join(STATS_DIR, f'{TODAY}_tradeoff_merged.csv'), index=False)
print(df.to_string(index=False))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.plot(df['res_m'], df['total_seconds'] / 60, 'o-', color='steelblue', markersize=8)
ax1.set_xscale('log'); ax1.set_yscale('log')
ax1.set_xlabel('격자 해상도 (m, 로그스케일)')
ax1.set_ylabel('전체 파이프라인 소요시간 (분, 로그스케일)')
ax1.set_title('해상도별 소요시간')
for _, row in df.iterrows():
    ax1.annotate(row['resolution'], (row['res_m'], row['total_seconds'] / 60),
                 textcoords='offset points', xytext=(5, 5))
ax1.axvline(5, color='red', linestyle='--', alpha=0.5, label='5m(메인 채택)')
ax1.legend()
ax1.grid(True, which='both', alpha=0.3)

ax2.plot(df['res_m'], df['link_HardCut38_agree_pct'], 'o-', color='darkorange', markersize=8,
         label='링크 HardCut38 일치율')
ax2.plot(df['res_m'], df['link_UTCI_r'] * 100, 's--', color='seagreen', markersize=7,
         label='링크 UTCI 상관계수 r(x100)')
ax2.set_xscale('log')
ax2.set_xlabel('격자 해상도 (m, 로그스케일)')
ax2.set_ylabel('정밀도 (1mtrue 기준, %)')
ax2.set_title('해상도별 정밀도(1mtrue 대비)')
ax2.axvline(5, color='red', linestyle='--', alpha=0.5, label='5m(메인 채택)')
ax2.set_ylim(0, 105)
ax2.legend()
ax2.grid(True, which='both', alpha=0.3)

fig.suptitle('성동구 — 해상도별 산출 속도 vs 정밀도 트레이드오프', fontsize=15)
out_path = os.path.join(FIG_DIR, f'{TODAY}_resolution_tradeoff_speed_vs_precision.png')
fig.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close(fig)
print(f'\n저장: {out_path}')
