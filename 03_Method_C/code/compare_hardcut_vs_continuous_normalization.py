"""이진 판단(Hard Cut) vs 연속형 정규화 평가 비교
Colaninno et al.(2024)의 0~1 min-max 정규화 방식을 우리 UTCI_avg_v2에 적용해,
폭염 조건에서 연속형 정규화도 값이 1.0 근처로 압축되는지 확인.
근거논문: 없음(자체 산출 비교). Colaninno(2024) 정규화 방식만 방법론 참고
(references/all_papers/Colaninno2024_SidewalkHeatRisk.pdf, p.4-5 원문 확인 완료).
"""
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

IN = '03_Method_C/results/2026-07-20_link_compare_v2_v3_seoul_5m.gpkg'
OUT_CSV = '03_Method_C/results/2026-07-29_hardcut_vs_continuous_normalization.csv'
OUT_FIG = '03_Method_C/results/figures/2026-07-29_hardcut_vs_continuous_normalization.png'

gdf = gpd.read_file(IN)
utci = gdf['UTCI_avg_v2'].values
hardcut = gdf['hardcut38_v2'].values

vmin, vmax = utci.min(), utci.max()
norm = (utci - vmin) / (vmax - vmin)

n_total = len(norm)
pct_ge_09 = (norm >= 0.9).mean() * 100
pct_ge_08 = (norm >= 0.8).mean() * 100

cut_norm = norm[hardcut]
nocut_norm = norm[~hardcut]

cut_pct_ge_09 = (cut_norm >= 0.9).mean() * 100
nocut_in_09band = (nocut_norm >= 0.85).mean() * 100  # False 링크 중 0.85 이상 비중 (overlap 지표)
cut_in_085to10 = ((cut_norm >= 0.85) & (cut_norm <= 1.0)).mean() * 100
nocut_in_085to10_count = ((nocut_norm >= 0.85) & (nocut_norm <= 1.0)).sum()
total_in_085to10 = ((norm >= 0.85) & (norm <= 1.0)).sum()
nocut_share_in_band = nocut_in_085to10_count / total_in_085to10 * 100 if total_in_085to10 > 0 else float('nan')

pd_out = gdf[['osmid']].copy() if 'osmid' in gdf.columns else gdf[[]].copy()
pd_out['UTCI_avg_v2'] = utci
pd_out['UTCI_norm_0to1'] = norm
pd_out['hardcut38_v2'] = hardcut
pd_out.to_csv(OUT_CSV, index=False)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].hist(nocut_norm, bins=50, alpha=0.6, label=f'Hard Cut 미적용 (n={len(nocut_norm):,})', color='steelblue')
axes[0].hist(cut_norm, bins=50, alpha=0.6, label=f'Hard Cut 적용 (n={len(cut_norm):,})', color='firebrick')
axes[0].set_xlabel('연속형 정규화 UTCI (0~1, min-max)')
axes[0].set_ylabel('링크 수')
axes[0].set_title('Hard Cut 여부별 연속형 정규화값 분포 (히스토그램)')
axes[0].legend()
axes[0].axvline(0.9, color='gray', linestyle='--', linewidth=1)

bp = axes[1].boxplot([nocut_norm, cut_norm], labels=['Hard Cut\n미적용', 'Hard Cut\n적용'],
                      patch_artist=True, showfliers=True)
bp['boxes'][0].set_facecolor('steelblue')
bp['boxes'][1].set_facecolor('firebrick')
axes[1].set_ylabel('연속형 정규화 UTCI (0~1)')
axes[1].set_title('그룹별 분포 (박스플롯)')
axes[1].axhline(0.9, color='gray', linestyle='--', linewidth=1)

plt.tight_layout()
plt.savefig(OUT_FIG, dpi=150)
print(f'그림 저장: {OUT_FIG}')

print(f'전체 링크 수: {n_total:,}')
print(f'UTCI_avg_v2 범위: {vmin:.2f} ~ {vmax:.2f}degC (범위폭 {vmax-vmin:.2f}degC)')
print(f'전체 링크 중 정규화값 >=0.9 비율: {pct_ge_09:.1f}%')
print(f'전체 링크 중 정규화값 >=0.8 비율: {pct_ge_08:.1f}%')
print(f'Hard Cut 적용 링크 중 정규화값>=0.9 비율: {cut_pct_ge_09:.1f}%')
print(f'Hard Cut 미적용 링크 중 정규화값>=0.85 비율: {nocut_in_09band:.1f}%')
print(f'정규화값 0.85~1.0 구간 내 Hard Cut 미적용 링크 비중(overlap): {nocut_share_in_band:.1f}%')
print(f'Hard Cut 적용 링크 중 0.85~1.0 구간 비중: {cut_in_085to10:.1f}%')

thresh_norm = (38.0 - vmin) / (vmax - vmin)
print(f'\n[주의] Hard Cut(UTCI>=38)이 정규화값으로 환산하면 {thresh_norm:.3f} 지점에 위치함.')
print('Hard Cut은 UTCI_avg_v2에서 직접 파생된 이진값이라, 정규화값(같은 변수의 재척도화)과')
print('비교하면 그 임계값(0.482) 기준 위/아래로 기계적으로 완전히 분리됨 - 통계적 "중첩"')
print('개념이 성립하지 않는 tautology. 실질적으로 의미있는 확인은 Hard Cut 적용 링크들이')
print('절대 UTCI 값 자체에서 얼마나 폭넓게 분포하는가임:')
cut_utci = utci[hardcut]
print(f'Hard Cut 적용 링크의 절대 UTCI 범위: {cut_utci.min():.2f} ~ {cut_utci.max():.2f}degC '
      f'(폭 {cut_utci.max()-cut_utci.min():.2f}degC, 전체 범위 {vmax-vmin:.2f}degC의 '
      f'{(cut_utci.max()-cut_utci.min())/(vmax-vmin)*100:.0f}%)')
print(f'Hard Cut 적용 링크 중 39degC 미만: {(cut_utci < 39).mean()*100:.1f}%, '
      f'40degC 이상: {(cut_utci >= 40).mean()*100:.1f}%')
