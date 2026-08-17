"""
SEAR 감소율 지도 — 집계구/행정동/구 3단계, 대표 시각(09/14/18시), 6급간 자연분류
================================================================
2026-08-17 재산출 결과(2026-08-17_seoul_jibgyegu_contour_CA_vs_SEAR_allhours_
kma_pixel_nobuffer.csv, 버퍼 없이·픽셀 우선계산 방식)를 집계구 원해상도 및
행정동/구 단위로 집계(sum 기반 재계산, 개별 reduction_pct 평균 아님)하여
choropleth로 시각화.

스타일: 범례·방위표 없음(PPT에서 별도 추가), 5km 축척바(검은 막대, 우측하단,
흰배경 없음 — 기존 MRT/UTCI 래스터 지도와 동일 스타일), 6급간 자연분류(Jenks,
시간대 풀링) 후 Reds 컬러맵, 하천 레이어 유/무 각각 저장, 네트워크는 서울시
도보 네트워크 API 기반 집계 결과.

2026-08-17 수정:
- 모든 레이어(집계구/행정동/구/하천)를 서울 행정경계로 클립 — 경계 밖으로
  하천이 삐져나가는 문제 해소.
- opp_CA=0(기회 도달 불가 등으로 감소율 계산 자체가 안 되는 경우)은 6급간
  자연분류 계산에서 제외하고, 회색+빗금(hatch)으로 별도 표시.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import mapclassify

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
RESULT_CSV = os.path.join(PROJ, '03_Method_C', 'results',
                           '2026-08-18_seoul_jibgyegu_contour_CA_vs_SEAR_api_network_nobuffer.csv')
JIBGYEGU_SHP = os.path.join(PROJ, 'data', '_tmp_boundary', '집계구.shp')
ADM_SHP = os.path.join(PROJ, 'data', '_tmp_boundary', '행정구역.shp')
WATER_GPKG = os.path.join(PROJ, 'data', '_tmp_boundary', 'seoul_water.gpkg')
OUT_DIR = os.path.join(PROJ, 'figures', 'figure_SEAR감소율_3단계지도', '서울')
os.makedirs(OUT_DIR, exist_ok=True)

HOURS = [9, 14, 18]
N_CLASSES = 6
CMAP = plt.cm.Reds
NODATA_COLOR = '#c8c8c8'

print("경계 로드...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True)
adm = gpd.read_file(ADM_SHP).set_crs(5179, allow_override=True)
water_raw = gpd.read_file(WATER_GPKG)

# 구는 디졸브 후 슬리버(행정동 간 부동소수점 경계 불일치)가 남는데, KHU_GIS_Project
# 강의노트(jparkgeo, Geospatial_Data_Visualization.ipynb) 방식대로 디졸브 직후
# 양수 buffer(5m) 한 번으로 해결 — 부풀렸다 깎는(erode) 방식은 오히려 구멍/스프링
# 모양 부작용을 만들어 폐기함(2026-08-17 확인).
gu = adm.dissolve(by='SIGUNGU_CD', as_index=False).loc[:, ['SIGUNGU_CD', 'SIGUNGU_NM', 'geometry']]
gu['geometry'] = gu.geometry.buffer(5.0)

dong = adm.loc[:, ['ADM_CD', 'ADM_NM', 'geometry']].copy()

print("서울 행정경계로 클립 중...")
seoul_boundary = adm.dissolve()[['geometry']]
jbg = gpd.clip(jbg, seoul_boundary)
dong = gpd.clip(dong, seoul_boundary)
gu = gpd.clip(gu, seoul_boundary)
water = gpd.clip(water_raw, seoul_boundary)

# clip() 자체도 경계에서 미세한 구멍을 다시 만들 수 있어(2026-08-17 확인),
# 같은 방식(양수 buffer)을 클립 후 한 번 더 적용.
gu['geometry'] = gu.geometry.buffer(5.0)

# 하천은 그냥 별도 레이어로 위에 얹기만 한다(land에서 지우지 않음) — difference로
# 지우려다가 하천 폴리곤이 1,871개 조각(작은 개천 다수 포함)이라 오히려 구 내부에
# 805개의 미세한 구멍을 만드는 부작용이 있었음(2026-08-17 확인 후 폐기).

FULL_BOUNDS = tuple(adm.total_bounds)
print(f"  고정 지도 범위: {FULL_BOUNDS}")

print("SEAR 결과 로드 및 집계구 원자료 결합...")
res = pd.read_csv(RESULT_CSV)
res = res[res['hour'].isin(HOURS)].copy()
res['TOT_REG_CD'] = res['TOT_REG_CD'].astype(str)
jbg['TOT_REG_CD'] = jbg['TOT_REG_CD'].astype(str)
jbg_key = jbg[['TOT_REG_CD', 'ADM_CD', 'geometry']].drop_duplicates(subset='TOT_REG_CD')

res_jbg = res.merge(jbg_key, on='TOT_REG_CD', how='inner')
print(f"  집계구 결합: {res_jbg['TOT_REG_CD'].nunique():,}개 (원본 {res['TOT_REG_CD'].nunique():,}개 중)")


def compute_reduction(g):
    # opp_CA=0(기회 도달 불가 등)이면 감소율 자체가 정의 안 됨 -> NaN(결측)으로 남김
    g['reduction_pct'] = np.where(
        g['opp_CA'] > 0, (g['opp_CA'] - g['opp_SEAR']) / g['opp_CA'] * 100, np.nan)
    return g


agg_jbg = res_jbg.groupby(['TOT_REG_CD', 'hour'], as_index=False).agg(
    opp_CA=('opp_CA', 'sum'), opp_SEAR=('opp_SEAR', 'sum'))
agg_jbg = compute_reduction(agg_jbg)


def agg_level(df, group_col):
    g = df.groupby([group_col, 'hour'], as_index=False).agg(
        opp_CA=('opp_CA', 'sum'), opp_SEAR=('opp_SEAR', 'sum'))
    return compute_reduction(g)


agg_dong = agg_level(res_jbg, 'ADM_CD')
agg_gu = agg_level(res_jbg.merge(adm[['ADM_CD', 'SIGUNGU_CD']].drop_duplicates(), on='ADM_CD', how='left'), 'SIGUNGU_CD')

levels = {
    'jibgyegu': (jbg[['TOT_REG_CD', 'geometry']].drop_duplicates(subset='TOT_REG_CD'), agg_jbg, 'TOT_REG_CD'),
    'dong': (dong, agg_dong, 'ADM_CD'),
    'gu': (gu, agg_gu, 'SIGUNGU_CD'),
}


MARGIN = 800  # m


def add_scalebar(ax, length_km=5):
    # 기존 utci_raster_seoul_*_18h_축척.png 실측 비율(가로 83.9%~97.5%, 세로
    # 하단에서 3.2%~4.1%)과 동일한 위치·스타일(검은 막대, 흰배경 없음)
    xmin, xmax, ymin, ymax = ax.get_xlim() + ax.get_ylim()
    x0 = xmin + (xmax - xmin) * 0.839
    y0 = ymin + (ymax - ymin) * 0.032
    length_m = length_km * 1000
    ax.plot([x0, x0 + length_m], [y0, y0], color='black', linewidth=4, solid_capstyle='butt')
    ax.text(x0, y0 + (ymax - ymin) * 0.012, '0', ha='center', va='bottom', fontsize=13)
    ax.text(x0 + length_m, y0 + (ymax - ymin) * 0.012, f'{length_km} km', ha='center', va='bottom', fontsize=13)


# 집계구는 원래 스타일(흰색 경계) 유지, 동/구는 옅은 회색 경계선으로
# 개별 단위 구분이 더 잘 보이게(2026-08-17 사용자 요청)
EDGE_COLOR = {'jibgyegu': 'white', 'dong': '#8a8a8a', 'gu': '#8a8a8a'}


def render(gdf, level_name, hour, with_river):
    fig, ax = plt.subplots(figsize=(9, 8), dpi=200)
    edge = EDGE_COLOR[level_name]

    nodata = gdf[gdf['reduction_pct'].isna()]
    valid = gdf[gdf['reduction_pct'].notna()]

    if len(nodata):
        nodata.plot(ax=ax, facecolor=NODATA_COLOR, edgecolor=edge, linewidth=0.15,
                    hatch='///')
    if len(valid):
        valid.plot(column='class', ax=ax, cmap=CMAP, vmin=0, vmax=N_CLASSES - 1,
                   linewidth=0.15, edgecolor=edge)

    if with_river:
        # 하천은 land와 완전히 무관한 별도 레이어 — 가공 없이 원본 그대로
        # 얹기만 한다. (2026-08-17: 이전에 20m 버퍼를 걸었더니 하천 내부
        # 섬 주변에서 렌더링 부작용이 생겨 제거함. 구 경계 자체는 하천과
        # 무관하게 이미 정상임을 별도로 확인했음.)
        water.plot(ax=ax, color='#8fb8d6', linewidth=0, zorder=3)

    x0, y0, x1, y1 = FULL_BOUNDS
    ax.set_xlim(x0 - MARGIN, x1 + MARGIN)
    ax.set_ylim(y0 - MARGIN, y1 + MARGIN)
    ax.set_axis_off()
    ax.set_aspect('equal')
    add_scalebar(ax)
    tag = 'river' if with_river else 'norriver'
    out = os.path.join(OUT_DIR, f'sear_reduction_{level_name}_{hour:02d}h_{tag}.png')
    fig.savefig(out, bbox_inches='tight', pad_inches=0.05, transparent=True)
    plt.close(fig)
    return out


def render_legend(level_name):
    fig, ax = plt.subplots(figsize=(1.2, 4.6), dpi=200)
    for i in range(N_CLASSES):
        color = CMAP(i / (N_CLASSES - 1))
        ax.add_patch(plt.Rectangle((0, i + 1), 1, 1, color=color))
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, facecolor=NODATA_COLOR, edgecolor='white',
                                linewidth=0.5, hatch='///'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, N_CLASSES + 1)
    ax.set_axis_off()
    out = os.path.join(OUT_DIR, f'legend_sear_{level_name}_barsonly.png')
    fig.savefig(out, bbox_inches='tight', pad_inches=0.02, transparent=True)
    plt.close(fig)
    return out


print("\n지도 생성 중...")
breaks_info = {}
for level_name, (geom, agg, key) in levels.items():
    pooled = agg.loc[agg['reduction_pct'].notna(), 'reduction_pct'].values
    n_nodata = agg['reduction_pct'].isna().sum()
    nb = mapclassify.NaturalBreaks(pooled, k=N_CLASSES)
    breaks_info[level_name] = nb.bins.tolist()
    print(f"  [{level_name}] 자연분류 6급간(결측 {n_nodata}건 제외, 시간대 풀링): "
          f"{[round(b,1) for b in nb.bins]}")

    for hour in HOURS:
        sub = agg[agg['hour'] == hour][[key, 'reduction_pct']]
        merged = geom.merge(sub, on=key, how='left')
        cls = np.full(len(merged), -1, dtype=int)
        valid_mask = merged['reduction_pct'].notna().values
        cls[valid_mask] = mapclassify.UserDefined(
            merged.loc[valid_mask, 'reduction_pct'].values, bins=nb.bins).yb
        merged['class'] = cls
        for with_river in (True, False):
            out = render(merged, level_name, hour, with_river)
            print(f"    {os.path.basename(out)}")

    render_legend(level_name)
    print(f"    legend_sear_{level_name}_barsonly.png")

print("\n완료. breaks 정리:")
for lv, b in breaks_info.items():
    print(f"  {lv}: {[round(x,1) for x in b]}")
