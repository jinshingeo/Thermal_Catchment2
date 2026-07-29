"""
Hard Cut 임계값 Monte Carlo (A안: Thorsson2014 5%위험증가 지점 기준)
근거논문: Thorsson et al.(2014) Table 4 (p.339) -> UTCI 환산
인구비중: 서울 열린데이터광장 등록인구(연령별/동별), 2025, "계"(한국인+등록외국인)
개인차(SD): 문헌 미확보 -> 가정 시나리오(1/2/3도) 민감도 분석
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["font.family"] = "AppleGothic"
mpl.rcParams["axes.unicode_minus"] = False

np.random.seed(42)

# 나이그룹별 평균 위험 UTCI (Thorsson2014 Table4, p.339, 5%위험증가 지점 -> UTCI 환산)
groups = {
    "45-79": {"mean": 42.90, "weight": 4724143},
    "80+":   {"mean": 42.10, "weight": 768429},
}
total_pop = sum(g["weight"] for g in groups.values())
for g in groups.values():
    g["prob"] = g["weight"] / total_pop

print("인구 비중:")
for name, g in groups.items():
    print(f"  {name}: {g['prob']*100:.2f}%  (평균 위험 UTCI={g['mean']}C)")

N = 1000000
sd_scenarios = [1.0, 2.0, 3.0]
HARDCUT_REF = 38.0

group_names = list(groups.keys())
group_probs = [groups[n]["prob"] for n in group_names]
group_means = {n: groups[n]["mean"] for n in group_names}

results_summary = []
all_samples = {}

for sd in sd_scenarios:
    assigned = np.random.choice(group_names, size=N, p=group_probs)
    samples = np.array([np.random.normal(group_means[g], sd) for g in assigned])
    all_samples[sd] = samples

    # mode: 0.2도 간격 히스토그램에서 최빈 bin 중심값
    bins = np.arange(30, 48, 0.2)
    counts, edges = np.histogram(samples, bins=bins)
    peak_idx = np.argmax(counts)
    mode_val = (edges[peak_idx] + edges[peak_idx+1]) / 2

    results_summary.append({
        "SD 시나리오(°C)": sd,
        "mode(°C)": round(mode_val, 2),
        "평균": round(samples.mean(), 2),
        "38°C 대비": round(mode_val - HARDCUT_REF, 2),
    })

summary_df = pd.DataFrame(results_summary)
print("\n결과 요약:")
print(summary_df.to_string(index=False))

summary_df.to_csv("/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-29_montecarlo_summary.csv", index=False)

# 시각화: SD 시나리오별 히스토그램 3개
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
colors = ["#4C72B0", "#DD8452", "#55A868"]

for ax, sd, color in zip(axes, sd_scenarios, colors):
    samples = all_samples[sd]
    bins = np.arange(30, 48, 0.5)
    ax.hist(samples, bins=bins, color=color, alpha=0.75, edgecolor="white")
    row = summary_df[summary_df["SD 시나리오(°C)"] == sd].iloc[0]
    ax.axvline(row["mode(°C)"], color="black", linestyle="--", linewidth=1.5,
               label=f"mode={row['mode(°C)']}°C")
    ax.axvline(HARDCUT_REF, color="red", linestyle=":", linewidth=1.5,
               label=f"현재 Hard Cut={HARDCUT_REF}°C")
    ax.set_title(f"개인차 가정 ±{sd}°C")
    ax.set_xlabel("UTCI 위험 임계값 (°C)")
    ax.legend(fontsize=9)

axes[0].set_ylabel(f"사람 수 (N={N:,} 중)")
fig.suptitle("Hard Cut 임계값 Monte Carlo — Thorsson2014 기반 (45-79세/80+ 인구가중)", fontsize=13)
plt.tight_layout()
plt.savefig("/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/monte_carlo_hardcut/2026-07-29_montecarlo_histogram_3scenarios.png",
            dpi=150, bbox_inches="tight")
print("\n그림 저장 완료")
