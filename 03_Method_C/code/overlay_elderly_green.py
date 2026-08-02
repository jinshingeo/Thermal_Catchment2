"""
구 단위 감소율과 고령인구비율·녹지비율 비교
================================================
- 고령인구: data/등록인구/등록인구(연령별_동별)_20260729224302.csv (자치구 단위, 2025)
- 녹지: data/landcover_seoul_L3_merged.gpkg (L1_NAME in 산림지역/초지) 면적비
- 감소율: 03_Method_C/results/figures/spatial_hotspot/2026-07-31_gu_reduction_{09,19}h.csv
"""
import pandas as pd
import geopandas as gpd

JIBGYEGU_SHP = "/Users/jin/석사논문/Thermal_Catchment/data/_tmp_boundary/집계구.shp"
LANDCOVER = "/Users/jin/석사논문/Thermal_Catchment/data/landcover_seoul_L3_merged.gpkg"
POP_CSV = "/Users/jin/석사논문/Thermal_Catchment/data/등록인구/등록인구(연령별_동별)_20260729224302.csv"
RED_09 = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/spatial_hotspot/2026-07-31_gu_reduction_09h.csv"
RED_19 = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/spatial_hotspot/2026-07-31_gu_reduction_19h.csv"
OUT_CSV = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-08-02_gu_reduction_vs_elderly_green.csv"

GU_CODE = {
'11010':'종로구','11020':'중구','11030':'용산구','11040':'성동구','11050':'광진구',
'11060':'동대문구','11070':'중랑구','11080':'성북구','11090':'강북구','11100':'도봉구',
'11110':'노원구','11120':'은평구','11130':'서대문구','11140':'마포구','11150':'양천구',
'11160':'강서구','11170':'구로구','11180':'금천구','11190':'영등포구','11200':'동작구',
'11210':'관악구','11220':'서초구','11230':'강남구','11240':'송파구','11250':'강동구',
}

print("1) 고령인구비율 계산...")
pop = pd.read_csv(POP_CSV, encoding='utf-8')
pop = pop[pop['항목'] == '계'].copy()
pop = pop[pop['동별(1)'].isin(GU_CODE.values())].copy()
age_cols = [c for c in pop.columns if c.startswith('2025.')]
# .1=0~4 ... .13=60~64, .14=65~69, .15=70~74, .16=75~79, .17=80~84 ... .21=100+
elderly65_cols = [f'2025.{i}' for i in range(14, 22)]
elderly80_cols = [f'2025.{i}' for i in range(17, 22)]
for c in age_cols + ['2025']:
    pop[c] = pd.to_numeric(pop[c], errors='coerce')
pop['총인구'] = pop['2025']
pop['65세이상'] = pop[elderly65_cols].sum(axis=1)
pop['80세이상'] = pop[elderly80_cols].sum(axis=1)
pop['고령비율_65+'] = (pop['65세이상'] / pop['총인구'] * 100).round(1)
pop['고령비율_80+'] = (pop['80세이상'] / pop['총인구'] * 100).round(1)
pop = pop[['동별(1)', '총인구', '고령비율_65+', '고령비율_80+']].rename(columns={'동별(1)': 'GU_NM'})

print("2) 집계구/구 폴리곤 로드...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True)
jbg['TOT_REG_CD'] = jbg['TOT_REG_CD'].astype(str)
jbg['GU_CD'] = jbg['TOT_REG_CD'].str[:5]
jbg['GU_NM'] = jbg['GU_CD'].map(GU_CODE)
gu_poly = jbg.dissolve(by='GU_NM').reset_index()[['GU_NM', 'geometry']]
gu_poly['area_gu'] = gu_poly.geometry.area

print("3) 녹지(산림+초지) 폴리곤 로드 및 면적 계산...")
lc = gpd.read_file(LANDCOVER)
green = lc[lc['L1_NAME'].isin(['산림지역', '초지'])][['geometry']].to_crs(5179)
green = green.dissolve()
overlay = gpd.overlay(gu_poly, green, how='intersection')
overlay['green_area'] = overlay.geometry.area
green_by_gu = overlay.groupby('GU_NM')['green_area'].sum().reset_index()
gu_poly = gu_poly.merge(green_by_gu, on='GU_NM', how='left')
gu_poly['green_area'] = gu_poly['green_area'].fillna(0)
gu_poly['녹지비율'] = (gu_poly['green_area'] / gu_poly['area_gu'] * 100).round(1)

print("4) 감소율 데이터 병합...")
red09 = pd.read_csv(RED_09).rename(columns={'reduction_pct': '감소율_09h'})
red19 = pd.read_csv(RED_19).rename(columns={'reduction_pct': '감소율_19h'})

result = red09.merge(red19, on='GU_NM').merge(pop, on='GU_NM').merge(
    gu_poly[['GU_NM', '녹지비율']], on='GU_NM')
result = result.sort_values('감소율_19h', ascending=False)
result.to_csv(OUT_CSV, index=False)
print(f"저장: {OUT_CSV}")
print(result.to_string(index=False))

print("\n상관계수 (19시 감소율 기준):")
print("고령비율(65+) 상관:", result['감소율_19h'].corr(result['고령비율_65+']).round(3))
print("고령비율(80+) 상관:", result['감소율_19h'].corr(result['고령비율_80+']).round(3))
print("녹지비율 상관:", result['감소율_19h'].corr(result['녹지비율']).round(3))
