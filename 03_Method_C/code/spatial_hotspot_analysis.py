"""
감소율의 공간적 특성 분석 — Local Moran's I (LISA)
====================================================
집계구 단위 감소율(38도 기준, 09시/19시 — 공간 편차가 가장 큰 두 시간대)에
대해 국지적 공간자기상관(Local Moran's I)을 계산하여 hot-spot(감소율 높은
지역의 군집)/cold-spot을 식별.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from libpysal.weights import Queen
from esda.moran import Moran_Local

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

JIBGYEGU_SHP = "/Users/jin/석사논문/Thermal_Catchment/data/_tmp_boundary/집계구.shp"
CSV = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-30_seoul_jibgyegu_contour_CA_vs_TCA_allhours.csv"
FIG_DIR = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/spatial_hotspot"
import os
os.makedirs(FIG_DIR, exist_ok=True)

print("집계구 폴리곤 로드...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True)
jbg = jbg.dissolve(by='TOT_REG_CD', as_index=False)  # 혹시 중복 코드 있으면 병합

df = pd.read_csv(CSV)
df38 = df[df['threshold'] == 38.0]

HOURS = [9, 19]
LABELS = {9: '아침(09시)', 19: '저녁(19시)'}

fig, axes = plt.subplots(2, 2, figsize=(13, 13))

for col_idx, hour in enumerate(HOURS):
    sub = df38[df38['hour'] == hour][['TOT_REG_CD', 'reduction_pct']]
    sub['TOT_REG_CD'] = sub['TOT_REG_CD'].astype(str)
    jbg['TOT_REG_CD'] = jbg['TOT_REG_CD'].astype(str)

    gdf = jbg.merge(sub, on='TOT_REG_CD', how='inner')
    print(f"{hour}시: 매칭 집계구 {len(gdf)}개 / 전체 {len(jbg)}개")

    w = Queen.from_dataframe(gdf, use_index=False)
    w.transform = 'r'

    y = gdf['reduction_pct'].values
    lisa = Moran_Local(y, w, seed=42)

    sig = lisa.p_sim < 0.05
    q = lisa.q  # 1=HH, 2=LH, 3=LL, 4=HL
    cluster = np.where(~sig, 0, q)
    gdf['cluster'] = cluster

    cmap = {0: '#E0E0E0', 1: '#C3450F', 2: '#F0A87A', 3: '#1C5C82', 4: '#9CC3D8'}
    labels = {0: '유의하지 않음', 1: 'High-High(고감소 군집)', 2: 'Low-High', 3: 'Low-Low(저감소 군집)', 4: 'High-Low'}

    # 상단: 감소율 원본 choropleth
    ax1 = axes[0, col_idx]
    gdf.plot(column='reduction_pct', cmap='inferno_r', legend=True, ax=ax1,
              edgecolor='none', vmin=0, vmax=100,
              legend_kwds={'label': '감소율(%)', 'shrink': 0.6})
    ax1.set_title(f'{LABELS[hour]} — 감소율 원본')
    ax1.set_axis_off()

    # 하단: LISA 클러스터
    ax2 = axes[1, col_idx]
    for code, color in cmap.items():
        gdf[gdf['cluster'] == code].plot(ax=ax2, color=color, edgecolor='none', label=labels[code])
    ax2.set_title(f'{LABELS[hour]} — LISA 군집(p<0.05)')
    ax2.set_axis_off()
    if col_idx == 1:
        ax2.legend(loc='lower left', fontsize=8, framealpha=0.9)

    n_hh = (cluster == 1).sum()
    n_ll = (cluster == 3).sum()
    print(f"  {hour}시: HH(고감소 군집) {n_hh}개 집계구 / LL(저감소 군집) {n_ll}개 집계구 (유의 p<0.05)")

    gdf[['TOT_REG_CD', 'ADM_NM', 'reduction_pct', 'cluster']].to_csv(
        f"{FIG_DIR}/2026-07-31_lisa_{hour:02d}h.csv", index=False)

plt.tight_layout()
out_path = f"{FIG_DIR}/2026-07-31_spatial_hotspot_09h_19h.png"
plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"\n저장: {out_path}")
