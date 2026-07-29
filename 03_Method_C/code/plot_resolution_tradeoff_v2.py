"""해상도 트레이드오프 그래프 v2 — 등간격 범주형 x축 + 소요시간 축절단(물결선)
사용자 피드백 반영: x축은 30m/15m/10m/5m/1m 순서 등간격, y축은 로그 대신 물결선
축절단으로 5m→1m 구간의 급격한 증가를 시각적으로 표현.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/compare_resolution_tradeoff'
FIG_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures'

df = pd.read_csv(f'{BASE}/2026-07-29_tradeoff_merged_v2.csv')
ORDER = ['30m', '15m', '10m', '5m', '1m']
df = df.set_index('resolution').loc[ORDER].reset_index()
x = range(len(ORDER))

SEONGDONG_KM2 = 29.16
SEOUL_KM2 = 605.70
SCALE = SEOUL_KM2 / SEONGDONG_KM2

# ── 그래프 1: 소요시간(물결축절단) + 정밀도 ────────────────────────────────
fig = plt.figure(figsize=(14, 6.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 3], hspace=0.08, wspace=0.28)
ax_top = fig.add_subplot(gs[0, 0])
ax_bot = fig.add_subplot(gs[1, 0], sharex=ax_top)
ax2 = fig.add_subplot(gs[:, 1])

bars_top = ax_top.bar(x, df['total_seconds'], color='#1565C0', width=0.5)
bars_bot = ax_bot.bar(x, df['total_seconds'], color='#1565C0', width=0.5)

ax_top.set_ylim(70000, 90000)
ax_bot.set_ylim(0, 1300)
ax_top.spines['bottom'].set_visible(False)
ax_bot.spines['top'].set_visible(False)
ax_top.tick_params(labeltop=False, bottom=False)
ax_top.set_xticks([])

d = .5
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12, linestyle='none',
              color='k', mec='k', mew=1, clip_on=False)
ax_top.plot([0, 1], [0, 0], transform=ax_top.transAxes, **kwargs)
ax_bot.plot([0, 1], [1, 1], transform=ax_bot.transAxes, **kwargs)

for i, v in enumerate(df['total_seconds']):
    if v > 1300:
        ax_top.text(i, v + 1000, f'{v/3600:.1f}h', ha='center', fontsize=10, fontweight='bold')
    else:
        ax_bot.text(i, v + 30, f'{v}s', ha='center', fontsize=10)

ax_bot.set_xticks(list(x))
ax_bot.set_xticklabels(ORDER, fontsize=12)
ax_bot.set_ylabel('소요시간(초)', fontsize=11)
ax_bot.annotate('', xy=(4, 1250), xytext=(3, 1150),
                 arrowprops=dict(arrowstyle='->', color='#B71C1C', lw=2))
ax_bot.text(3.5, 1280, '5m→1m 급격히 증가', color='#B71C1C', fontsize=9, ha='center')
fig.text(0.28, 0.93, '해상도별 성동구 소요시간(축절단, 물결선=70,000~90,000초 구간 생략)',
          ha='center', fontsize=12)

ax2.plot(x, df['link_HardCut38_agree_pct'], marker='o', markersize=9, linewidth=2,
          color='#2E7D32', label='링크 Hard Cut(38°C) 일치율(%)')
ax2b = ax2.twinx()
ax2b.plot(x, df['link_UTCI_r'], marker='s', markersize=9, linewidth=2,
           color='#EF6C00', label='링크 UTCI 상관계수 r')
ax2.set_xticks(list(x))
ax2.set_xticklabels(ORDER, fontsize=12)
ax2.set_ylabel('Hard Cut 일치율(%)', color='#2E7D32', fontsize=11)
ax2b.set_ylabel('UTCI 상관계수 r', color='#EF6C00', fontsize=11)
ax2.set_ylim(95, 100.5)
ax2b.set_ylim(0.3, 1.05)
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='lower left', fontsize=9)
ax2.set_title('정밀도(1mtrue 기준) — Hard Cut 일치율 vs 연속값 상관계수', fontsize=12)

fig.suptitle('해상도(1/5/10/15/30m)별 소요시간 vs 정밀도 트레이드오프 (v2)', fontsize=14, y=1.0)
path1 = f'{FIG_DIR}/2026-07-29_resolution_tradeoff_speed_vs_precision_v2.png'
fig.savefig(path1, dpi=150, bbox_inches='tight')
print(f'저장: {path1}')
plt.close(fig)

# ── 그래프 2: 실행가능선 v2 ─────────────────────────────────────────────
df['seoul_est_hours'] = df['total_seconds'] * SCALE / 3600

fig2 = plt.figure(figsize=(7, 6))
gsB = fig2.add_gridspec(2, 1, height_ratios=[1, 2], hspace=0.08)
axA_top = fig2.add_subplot(gsB[0])
axA_bot = fig2.add_subplot(gsB[1], sharex=axA_top)

colors = ['#1565C0' if h <= 48 else '#B71C1C' for h in df['seoul_est_hours']]
axA_top.bar(x, df['seoul_est_hours'], color=colors, width=0.5)
axA_bot.bar(x, df['seoul_est_hours'], color=colors, width=0.5)
axA_top.set_ylim(300, 520)
axA_bot.set_ylim(0, 10)
axA_top.spines['bottom'].set_visible(False)
axA_bot.spines['top'].set_visible(False)
axA_top.tick_params(labeltop=False, bottom=False)
axA_top.set_xticks([])
axA_top.plot([0, 1], [0, 0], transform=axA_top.transAxes, **kwargs)
axA_bot.plot([0, 1], [1, 1], transform=axA_bot.transAxes, **kwargs)
axA_bot.axhline(48/1, color='gray', linestyle='--', linewidth=1)
for i, v in enumerate(df['seoul_est_hours']):
    if v > 10:
        axA_top.text(i, v + 15, f'{v:.0f}h', ha='center', fontsize=10, fontweight='bold')
    else:
        axA_bot.text(i, v + 0.3, f'{v*60:.0f}min' if v < 1 else f'{v:.1f}h', ha='center', fontsize=9)
axA_bot.set_xticks(list(x))
axA_bot.set_xticklabels(ORDER, fontsize=12)
axA_bot.set_ylabel('서울 전역 추정 소요시간(시간)', fontsize=10)
fig2.suptitle('해상도별 서울 전역 추정 소요시간\n(빨강=실행 사실상 불가능, 파랑=실행 가능)', fontsize=12)
path2a = f'{FIG_DIR}/2026-07-29_resolution_feasibility_threshold_v2_left.png'
fig2.savefig(path2a, dpi=150, bbox_inches='tight')
plt.close(fig2)

fig3, ax4 = plt.subplots(figsize=(7, 6))
ax4.plot(x, df['link_HardCut38_agree_pct'], marker='o', markersize=10, linewidth=2, color='#2E7D32')
for i, v in enumerate(df['link_HardCut38_agree_pct']):
    ax4.annotate(f'{v:.2f}%', (i, v), textcoords='offset points', xytext=(0, 10), ha='center', fontsize=10)
ax4.set_xticks(list(x))
ax4.set_xticklabels(ORDER, fontsize=12)
ax4.set_ylabel('링크 Hard Cut(38°C) 일치율(%, 1mtrue 기준)', fontsize=10)
ax4.set_ylim(97, 100.5)
ax4.axvspan(3.5, 4.5, alpha=0.08, color='red')
ax4.set_title('"실행 가능한"(30/15/10/5m) 해상도 중 정밀도 비교', fontsize=12)
path2b = f'{FIG_DIR}/2026-07-29_resolution_feasibility_threshold_v2_right.png'
fig3.savefig(path2b, dpi=150, bbox_inches='tight')
plt.close(fig3)

print(f'저장: {path2a}')
print(f'저장: {path2b}')

print(df[['resolution', 'total_seconds', 'seoul_est_hours', 'link_HardCut38_agree_pct', 'link_UTCI_r']])
