"""
감소율 3단계 공간 시각화 — 집계구 / 동 / 구
================================================
09시·19시(38도 기준), 각 시간대마다 집계구-동-구 세 단계로 감소율을 시각화.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

# 단일 색조(모노크롬) 그라데이션 — 밝은 회백색 -> 짙은 적갈색(단일 hue)
MONO_CMAP = LinearSegmentedColormap.from_list(
    'mono_heat', ['#FBF6EF', '#F0C9A8', '#D98A4E', '#B34E1C', '#7A2C0A'])

GU_CODE = {
'11010':'종로구','11020':'중구','11030':'용산구','11040':'성동구','11050':'광진구',
'11060':'동대문구','11070':'중랑구','11080':'성북구','11090':'강북구','11100':'도봉구',
'11110':'노원구','11120':'은평구','11130':'서대문구','11140':'마포구','11150':'양천구',
'11160':'강서구','11170':'구로구','11180':'금천구','11190':'영등포구','11200':'동작구',
'11210':'관악구','11220':'서초구','11230':'강남구','11240':'송파구','11250':'강동구',
}

JIBGYEGU_SHP = "/Users/jin/석사논문/Thermal_Catchment/data/_tmp_boundary/집계구.shp"
WATER_GPKG = "/Users/jin/석사논문/Thermal_Catchment/data/_tmp_boundary/seoul_water.gpkg"
CSV = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-30_seoul_jibgyegu_contour_CA_vs_TCA_allhours.csv"
FIG_DIR = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/spatial_hotspot"
os.makedirs(FIG_DIR, exist_ok=True)

print("집계구 폴리곤 로드...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True)
water = gpd.read_file(WATER_GPKG)
jbg['TOT_REG_CD'] = jbg['TOT_REG_CD'].astype(str)
jbg['GU_CD'] = jbg['TOT_REG_CD'].str[:5]
jbg['GU_NM'] = jbg['GU_CD'].map(GU_CODE)

df = pd.read_csv(CSV)
df38 = df[df['threshold'] == 38.0].copy()
df38['TOT_REG_CD'] = df38['TOT_REG_CD'].astype(str)

HOURS = [9, 19]
LABELS = {9: '아침(09시)', 19: '저녁(19시)'}
CMAP = MONO_CMAP

fig, axes = plt.subplots(2, 3, figsize=(19, 13))

for row_idx, hour in enumerate(HOURS):
    sub = df38[df38['hour'] == hour][['TOT_REG_CD', 'reduction_pct']]
    gdf = jbg.merge(sub, on='TOT_REG_CD', how='inner')

    # 1) 집계구 단위
    ax = axes[row_idx, 0]
    gdf.plot(column='reduction_pct', cmap=CMAP, ax=ax, edgecolor='none', vmin=0, vmax=100)
    water.plot(ax=ax, color='#4A7FA6', edgecolor='none', zorder=5)
    ax.set_title(f'{LABELS[hour]} — 집계구 단위 (n={len(gdf):,})', fontsize=12)
    ax.set_axis_off()

    # 2) 동 단위 (평균)
    dong = gdf.dissolve(by='ADM_NM', aggfunc={'reduction_pct': 'mean'}).reset_index()
    ax = axes[row_idx, 1]
    dong.plot(column='reduction_pct', cmap=CMAP, ax=ax, edgecolor='white', linewidth=0.15, vmin=0, vmax=100)
    water.plot(ax=ax, color='#4A7FA6', edgecolor='none', zorder=5)
    ax.set_title(f'{LABELS[hour]} — 행정동 단위 (n={len(dong):,})', fontsize=12)
    ax.set_axis_off()

    # 3) 구 단위 (평균) + 라벨
    gu = gdf.dissolve(by='GU_NM', aggfunc={'reduction_pct': 'mean'}).reset_index()
    ax = axes[row_idx, 2]
    gu.plot(column='reduction_pct', cmap=CMAP, ax=ax, edgecolor='white', linewidth=0.6, vmin=0, vmax=100)
    for _, r in gu.iterrows():
        c = r.geometry.representative_point()
        txt_color = 'white' if r['reduction_pct'] >= 55 else '#3A2A1E'
        ax.annotate(f"{r['GU_NM']}\n{r['reduction_pct']:.0f}%", (c.x, c.y),
                    ha='center', va='center', fontsize=7.5, color=txt_color,
                    path_effects=None)
    water.plot(ax=ax, color='#4A7FA6', edgecolor='none', zorder=5)
    ax.set_title(f'{LABELS[hour]} — 자치구 단위 (n=25)', fontsize=12)
    ax.set_axis_off()

    # 저장용 CSV
    gu[['GU_NM', 'reduction_pct']].sort_values('reduction_pct', ascending=False).to_csv(
        f"{FIG_DIR}/2026-07-31_gu_reduction_{hour:02d}h.csv", index=False)

sm = ScalarMappable(norm=Normalize(vmin=0, vmax=100), cmap=CMAP)
cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.015])
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_label('감소율(%)')

fig.suptitle('서울 전역 Thermal Catchment 감소율 — 집계구/행정동/자치구 3단계 비교 (Hard Cut 38°C)', fontsize=15)
plt.tight_layout(rect=[0.02, 0.05, 1, 0.96])
out_path = f"{FIG_DIR}/2026-07-31_reduction_3levels_09h_19h.png"
plt.savefig(out_path, dpi=160, bbox_inches='tight', facecolor='white')
print(f"저장: {out_path}")
