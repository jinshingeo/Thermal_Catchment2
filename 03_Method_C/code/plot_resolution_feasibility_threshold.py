"""
해상도별 소요시간·정밀도 — "매끄러운 엘보" 대신 "실행가능선(feasibility threshold)" 프레임
================================================================
1m은 성동구(연산 도메인 29.16km²) 기준으로도 24시간 가까이 걸려, 서울 전체
(605.70km², 약 20.8배)로 선형 추정 시 약 20.7일 — 명백히 비현실적.
반면 5/10/30m은 셋 다 "실행 가능한 영역" 안에 있고, 이미 서울 전역 5m은
실제로 완주해 메인 분석에 쓰고 있음(추정이 아니라 실증된 사실).
"실행 가능한 영역" 안에서는 정밀도가 가장 높은 5m을 택하는 것이 합리적.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/'
                  'compare_resolution_tradeoff/2026-07-29_tradeoff_merged.csv')
df = df.set_index('resolution').loc[['1m', '5m', '10m', '30m']]

SEONGDONG_DOMAIN_KM2 = 29.16   # 연산 도메인(버퍼 포함) 면적, 직접 계산
SEOUL_KM2 = 605.70              # 기존 문서 기록값(연구지역 정의)
SCALE = SEOUL_KM2 / SEONGDONG_DOMAIN_KM2  # ≈20.77배

df['seoul_est_hours'] = df['total_seconds'] * SCALE / 3600
print(f"면적 배율(서울/성동구 도메인): {SCALE:.2f}배")
print(df[['total_seconds', 'seoul_est_hours', 'link_HardCut38_agree_pct']])

FEASIBLE_LIMIT_HOURS = 48  # SCI 투고 타임라인상 실행 가능하다고 볼 수 있는 대략적 상한(참고용)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ── 왼쪽: 서울 전역 추정 소요시간(로그스케일) ──────────────────────────────
resolutions = df.index.tolist()
x = range(len(resolutions))
colors = ['#B71C1C' if h > FEASIBLE_LIMIT_HOURS else '#1565C0' for h in df['seoul_est_hours']]
bars = ax1.bar(x, df['seoul_est_hours'], color=colors)
ax1.set_yscale('log')
ax1.set_xticks(list(x))
ax1.set_xticklabels(resolutions, fontsize=12)
ax1.axhline(FEASIBLE_LIMIT_HOURS, color='gray', linestyle='--', linewidth=1)
ax1.text(0.02, FEASIBLE_LIMIT_HOURS * 1.3, f'참고선: {FEASIBLE_LIMIT_HOURS}시간',
          transform=ax1.get_yaxis_transform(), fontsize=9, color='gray')
for i, h in enumerate(df['seoul_est_hours']):
    label = f'{h:.0f}h' if h >= 1 else f'{h*60:.0f}min'
    ax1.text(i, h * 1.15, label, ha='center', fontsize=10)
ax1.set_ylabel('서울 전역 추정 소요시간(시간, 로그스케일)\n(성동구 실측 × 면적비 20.77배, 거친 선형 추정)', fontsize=10)
ax1.set_title('해상도별 서울 전역 추정 소요시간\n(빨강=실행 사실상 불가능, 파랑=실행 가능 영역)', fontsize=12)

# ── 오른쪽: 정밀도(Hard Cut 일치율) ────────────────────────────────────────
ax2.plot(x, df['link_HardCut38_agree_pct'], marker='o', markersize=10,
          linewidth=2, color='#2E7D32')
for i, v in enumerate(df['link_HardCut38_agree_pct']):
    ax2.annotate(f'{v:.2f}%', (i, v), textcoords="offset points", xytext=(0, 10),
                  ha='center', fontsize=10)
ax2.set_xticks(list(x))
ax2.set_xticklabels(resolutions, fontsize=12)
ax2.set_ylabel('링크 단위 Hard Cut(38°C) 일치율(%, 1mtrue 기준)', fontsize=10)
ax2.set_ylim(97, 100.5)
ax2.set_title('"실행 가능한" 해상도(5/10/30m) 중 정밀도 비교\n— 5m이 가장 높음', fontsize=12)
ax2.axvspan(-0.5, 0.5, alpha=0.08, color='red')
ax2.text(0, 97.3, '1m\n(기준값,\n비교대상 아님)', ha='center', fontsize=8, color='gray')

fig.suptitle('해상도 선택의 실행가능선(feasibility threshold) 프레임\n'
             '1m=서울 전역 확장 시 사실상 불가능 / 5·10·30m=전부 실행 가능 → 그중 가장 정밀한 5m 채택',
             fontsize=13, y=1.04)
fig.tight_layout()
path = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/' \
       '2026-07-29_resolution_feasibility_threshold.png'
fig.savefig(path, dpi=150, bbox_inches='tight')
print(f"저장: {path}")
