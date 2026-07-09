"""
성동구 파일럿 — 토지피복 래스터 생성 (접근1: 30m / 접근2: 1m)
================================================================
환경부 세분류(L3) 토지피복(서울 전체 병합본)을 크로스워크 표로
UMEP landcoverclasses_2016a.txt 코드로 변환 후, DSM/CDSM과 동일한
그리드(성동구, 30m/1m)로 rasterize.

UMEP landcover 코드 (~/Library/.../UMEP/SOLWEIG/landcoverclasses_2016a.txt):
  0=Cobble_stone_2014a  1=Dark_asphalt  2=Roofs(buildings)
  5=Grass_unmanaged  6=bare_soil  7=Water  99=Walls

크로스워크 5클래스 -> UMEP 코드:
  paved->1(Dark_asphalt), building->2(Roofs), grass->5, bare_soil->6, water->7
  산림(CDSM 처리, landcover 미적용) -> 지면은 grass(5)로 처리
  (참고: writing/2026-07-07_MethodC_SOLWEIG파일럿_진행기록.md)
"""

import os
os.environ.setdefault(
    'PROJ_DATA',
    '/opt/miniconda3/lib/python3.13/site-packages/rasterio/proj_data')

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'dsm_cdsm_seongdong')

BND_PATH = os.path.join(PROJ, 'data', '_tmp_boundary', '행정구역.shp')
LC_PATH = os.path.join(PROJ, 'data', 'landcover_seoul_L3_merged.gpkg')
CROSSWALK_PATH = os.path.join(PROJ, '03_Method_C', 'code',
                              'landcover_crosswalk_L3_to_UMEP.csv')

TARGET_CRS = 'EPSG:5186'

UMEP_CODE = {
    'paved': 1,       # Dark_asphalt
    'building': 2,    # Roofs(buildings)
    'grass': 5,       # Grass_unmanaged
    'bare_soil': 6,
    'water': 7,
    'CDSM': 5,        # 산림 지면부 -> grass로 근사 (수목 자체는 CDSM에서 따로 반영)
}
FILL_CODE = 6  # 폴리곤 커버 안 된 픽셀(공백) 기본값: bare_soil


# ── 1. 성동구 경계 ────────────────────────────────────────────────────────
bnd = gpd.read_file(BND_PATH, encoding='cp949')
seongdong = bnd[bnd['SIGUNGU_NM'] == '성동구'].dissolve()
seongdong = seongdong.set_crs('EPSG:5179', allow_override=True).to_crs(TARGET_CRS)


# ── 2. 크로스워크 적용 ─────────────────────────────────────────────────────
print("토지피복 로드 및 크로스워크 적용 중...")
crosswalk = pd.read_csv(CROSSWALK_PATH, dtype={'L3_CODE': str})
code_map = dict(zip(crosswalk['L3_CODE'], crosswalk['UMEP_class']))

lc = gpd.read_file(LC_PATH)
lc = lc.set_crs(TARGET_CRS, allow_override=True)  # WKT가 EPSG:5186과 수치상 동일함 확인됨(2026-07-07)
lc_sd = gpd.clip(lc, seongdong)
lc_sd = lc_sd.copy()
lc_sd['L3_CODE'] = lc_sd['L3_CODE'].astype(str)
lc_sd['UMEP_CLASS'] = lc_sd['L3_CODE'].map(code_map)
lc_sd['UMEP_NUM'] = lc_sd['UMEP_CLASS'].map(UMEP_CODE)

n_unmatched = lc_sd['UMEP_NUM'].isna().sum()
print(f"  성동구 피처 {len(lc_sd):,}개, 매핑 안 된 것 {n_unmatched}개")
lc_sd = lc_sd.dropna(subset=['UMEP_NUM'])
print(lc_sd['UMEP_CLASS'].value_counts())


# ── 3. 그리드 정의 (DSM/CDSM 스크립트와 동일 기준) ─────────────────────────
minx, miny, maxx, maxy = seongdong.total_bounds
minx, miny = np.floor(minx / 30) * 30, np.floor(miny / 30) * 30
maxx, maxy = np.ceil(maxx / 30) * 30, np.ceil(maxy / 30) * 30

grids = {
    'approach1_30m': 30.0,
    'approach2_1m': 1.0,
}

for label, res in grids.items():
    width = int(round((maxx - minx) / res))
    height = int(round((maxy - miny) / res))
    transform = from_origin(minx, maxy, res, res)
    out_shape = (height, width)
    print(f"\n[{label}] 그리드: {width}x{height} px @ {res}m")

    shapes = [(geom, code) for geom, code in
              zip(lc_sd.geometry, lc_sd['UMEP_NUM']) if geom is not None]
    lc_raster = rasterize(
        shapes, out_shape=out_shape, transform=transform,
        fill=FILL_CODE, dtype='uint8',
    )

    profile = {
        'driver': 'GTiff', 'height': height, 'width': width, 'count': 1,
        'dtype': 'uint8', 'crs': TARGET_CRS, 'transform': transform,
        'nodata': 255,
    }
    out_path = os.path.join(OUT_DIR, f'LandCover_{label}.tif')
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(lc_raster, 1)

    vals, counts = np.unique(lc_raster, return_counts=True)
    dist = {int(v): int(c) for v, c in zip(vals, counts)}
    print(f"  코드 분포: {dist}")
    print(f"  저장: {out_path}")

print("\n완료.")
