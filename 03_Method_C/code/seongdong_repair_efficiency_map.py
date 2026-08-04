"""
성동구 집계구별 병목 링크 복구 효율 지도
================================================================
seongdong_jibgyegu_repair_efficiency.py 결과(집계구별 "CA 대비 50% 회복까지
필요한 누적 m")를 집계구 폴리곤에 조인해 choropleth로 시각화.
값이 작을수록(밝은색) 조금만 고쳐도 크게 좋아지는 지역, 클수록(진한색)
많이 고쳐야 하는 지역. 50%에 끝내 도달 못한 지점은 회색 해칭, CA=0(반경 내
기회 자체 없음)은 흰색으로 구분.
"""
import geopandas as gpd
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

PROJ_DIR = '/Users/jin/석사논문/Thermal_Catchment'
CSV = f'{PROJ_DIR}/03_Method_C/results/2026-08-04_seongdong_jibgyegu_repair_efficiency.csv'
JIBGYEGU_SHP = f'{PROJ_DIR}/data/_tmp_boundary/집계구.shp'
OUT_DIR = f'{PROJ_DIR}/03_Method_C/results/figures/2026-08-04_bottleneck_repair_pptset'

df = pd.read_csv(CSV, dtype={'TOT_REG_CD': str})
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True)
jbg = jbg[jbg['TOT_REG_CD'].str[:5] == '11040'].copy()
jbg = jbg.merge(df, on='TOT_REG_CD', how='left', suffixes=('', '_r'))

no_opp = jbg['ca'] == 0
not_reached = (jbg['reached_50pct'] == False) & (~no_opp)
reached = jbg['reached_50pct'] == True

fig, ax = plt.subplots(figsize=(9, 9), dpi=150)

jbg[reached].plot(ax=ax, column='len_to_50pct_m', cmap='YlOrRd', legend=True,
                   edgecolor='white', linewidth=0.2,
                   legend_kwds={'label': 'CA 대비 50% 회복까지 필요한 누적 복구 길이 (m)', 'shrink': 0.6})
if not_reached.any():
    jbg[not_reached].plot(ax=ax, facecolor='none', edgecolor='white', linewidth=0.2,
                           hatch='///', color='#8a8a8a')
jbg[no_opp].plot(ax=ax, facecolor='white', edgecolor='#cccccc', linewidth=0.3)

handles = [mpatches.Patch(facecolor='white', edgecolor='#cccccc', label='반경 내 기회(CA) 없음')]
if not_reached.any():
    handles.insert(0, mpatches.Patch(facecolor='#8a8a8a', hatch='///', edgecolor='white', label='50% 미도달'))
ax.legend(handles=handles, loc='lower left', fontsize=9, frameon=True)

ax.set_title('성동구 집계구별 병목 링크 복구 효율\n(09시, UTCI 38°C 기준, 탐욕적 순서 — 값이 작을수록 적은 개입으로 크게 회복)',
              fontsize=12)
ax.set_axis_off()
plt.tight_layout()
out_png = f'{OUT_DIR}/seongdong_jibgyegu_repair_efficiency_map.png'
plt.savefig(out_png, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('저장:', out_png)
