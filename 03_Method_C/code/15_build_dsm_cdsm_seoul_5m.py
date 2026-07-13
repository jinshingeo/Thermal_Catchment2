"""
서울 전체 5m 파일럿 — DSM(건물)·CDSM(수목) 래스터 생성
================================================================
01_build_dsm_cdsm_seongdong.py와 동일한 방법론(4단계 건물높이 하이브리드,
임상도 수목높이 실측값), 공간범위만 성동구→서울 전체, 해상도는 5m 직접 rasterize
(1m 경유 리샘플링 아님 — 처음부터 5m 격자로 벡터를 직접 굽는 방식, 접근1/2와
동일한 "direct rasterize" 계열).

DSM = 지면(DEM) + 건물높이 (masl)
CDSM = 수목높이만 (magl)
"""

import os
os.environ.setdefault(
    'PROJ_DATA',
    '/opt/miniconda3/lib/python3.13/site-packages/rasterio/proj_data')

import numpy as np
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'dsm_cdsm_seoul_5m')
os.makedirs(OUT_DIR, exist_ok=True)

DEM_PATH = os.path.join(PROJ, 'data', 'GLO30_DSM', 'GLO30_Seoul_EPSG5186_30m.tif')
BND_PATH = os.path.join(PROJ, 'data', '_tmp_boundary', '행정구역.shp')
FAC_PATH = os.path.join(PROJ, 'data', 'F_FAC_BUILDING_서울', 'F_FAC_BUILDING_11_202606.shp')
TL_PATH = '/Users/jin/석사논문/TAVI/03_건물데이터/(도로명주소)건물_서울/TL_SPBD_BULD_11_202603.shp'
FOREST_PATH = os.path.join(PROJ, 'data', '녹지데이터 복사본', '임상도', '11_서울시', '11.shp')

TARGET_CRS = 'EPSG:5186'
DEFAULT_HEIGHT = 3.0
RES = 5.0

# ── 1. 서울 전체 경계 (25개 자치구 dissolve) ─────────────────────────────
bnd = gpd.read_file(BND_PATH, encoding='cp949')
print(f"SIDO_NM 종류: {bnd['SIDO_NM'].unique()}")
seoul = bnd[bnd['SIDO_NM'] == '서울특별시'].dissolve()
seoul = seoul.set_crs('EPSG:5179', allow_override=True).to_crs(TARGET_CRS)
seoul['geometry'] = seoul.geometry.buffer(0)  # dissolve 후 위상오류(TopologyException) 방지
print(f"서울 전체 경계: {seoul.geometry.area.iloc[0]/1e6:.2f} km²")


# ── 2. 건물 높이 (4단계 하이브리드, 서울 전체) ────────────────────────────
print("\n건물 높이 계산 중 (서울 전체)...")
fac = gpd.read_file(FAC_PATH, encoding='cp949')
assert fac.crs.to_string() == TARGET_CRS, f"F_FAC_BUILDING CRS 불일치: {fac.crs}"
fac['geometry'] = fac.geometry.buffer(0)  # 위상오류(TopologyException) 방지
fac_seoul = gpd.clip(fac, seoul)
print(f"  건물 {len(fac_seoul):,}동 로드")

tl = gpd.read_file(TL_PATH, encoding='cp949')
tl['geometry'] = tl.geometry.buffer(0)
tl_seoul = gpd.clip(tl, seoul.to_crs(tl.crs)).to_crs(TARGET_CRS)
tl_height_lookup = (tl_seoul[tl_seoul['GRO_FLO_CO'].notna() & (tl_seoul['GRO_FLO_CO'] > 0)]
                     .set_index('BD_MGT_SN')['GRO_FLO_CO'] * DEFAULT_HEIGHT).to_dict()

fac_seoul = fac_seoul.copy()
fac_seoul['HEIGHT_FINAL'] = np.nan
valid = (fac_seoul['HEIGHT'] > 0) & (fac_seoul['HEIGHT'] < 200)
fac_seoul.loc[valid, 'HEIGHT_FINAL'] = fac_seoul.loc[valid, 'HEIGHT']

need2 = fac_seoul['HEIGHT_FINAL'].isna() & (fac_seoul['GRND_FLR'] > 0)
fac_seoul.loc[need2, 'HEIGHT_FINAL'] = fac_seoul.loc[need2, 'GRND_FLR'] * DEFAULT_HEIGHT

need3 = fac_seoul['HEIGHT_FINAL'].isna() & fac_seoul['BD_MGT_SN'].isin(tl_height_lookup)
fac_seoul.loc[need3, 'HEIGHT_FINAL'] = fac_seoul.loc[need3, 'BD_MGT_SN'].map(tl_height_lookup)

fac_seoul['HEIGHT_FINAL'] = fac_seoul['HEIGHT_FINAL'].fillna(DEFAULT_HEIGHT)

n1, n2, n3 = valid.sum(), need2.sum(), need3.sum()
n4 = len(fac_seoul) - n1 - n2 - n3
print(f"  전체 {len(fac_seoul):,}동 | 실측 {n1:,} | 자체층수 {n2:,} | "
      f"교차보완 {n3:,} | 기본값 {n4:,}")


# ── 3. 수목 높이 (임상도, 서울 전체) ───────────────────────────────────────
print("\n수목 높이 로드 중 (서울 전체)...")
forest = gpd.read_file(FOREST_PATH, encoding='cp949')
forest_seoul = gpd.clip(forest, seoul.to_crs(forest.crs)).to_crs(TARGET_CRS)
forest_seoul = forest_seoul[forest_seoul['FRTP_NM'] != '무립목지/비산림'].copy()
forest_seoul = forest_seoul.dropna(subset=['HEIGHT'])
forest_seoul['HEIGHT_NUM'] = forest_seoul['HEIGHT'].astype(float)
print(f"  산림 폴리곤 {len(forest_seoul):,}개, 평균수고 {forest_seoul['HEIGHT_NUM'].mean():.1f}m")


# ── 4. 5m 그리드 직접 구축 ─────────────────────────────────────────────────
minx, miny, maxx, maxy = seoul.total_bounds
minx, miny = np.floor(minx / RES) * RES, np.floor(miny / RES) * RES
maxx, maxy = np.ceil(maxx / RES) * RES, np.ceil(maxy / RES) * RES

width = int(round((maxx - minx) / RES))
height = int(round((maxy - miny) / RES))
transform = from_origin(minx, maxy, RES, RES)
out_shape = (height, width)
print(f"\n[서울 5m] 그리드: {width}x{height} px @ {RES}m ({width*height/1e6:.1f}M px)")

with rasterio.open(DEM_PATH) as dem_src:
    dem_data = dem_src.read(1)
    dem_transform = dem_src.transform
    dem_crs = dem_src.crs

dem_resampled = np.zeros(out_shape, dtype=np.float32)
reproject(
    source=dem_data, destination=dem_resampled,
    src_transform=dem_transform, src_crs=dem_crs,
    dst_transform=transform, dst_crs=TARGET_CRS,
    resampling=Resampling.bilinear,
)

bld_shapes = [(geom, h) for geom, h in
              zip(fac_seoul.geometry, fac_seoul['HEIGHT_FINAL']) if geom is not None]
bld_raster = rasterize(bld_shapes, out_shape=out_shape, transform=transform,
                        fill=0.0, dtype='float32')

tree_shapes = [(geom, h) for geom, h in
               zip(forest_seoul.geometry, forest_seoul['HEIGHT_NUM']) if geom is not None]
tree_raster = rasterize(tree_shapes, out_shape=out_shape, transform=transform,
                         fill=0.0, dtype='float32')

dsm = dem_resampled + bld_raster
cdsm = tree_raster
dem_only = dem_resampled.astype(np.float32)

profile = {
    'driver': 'GTiff', 'height': height, 'width': width, 'count': 1,
    'dtype': 'float32', 'crs': TARGET_CRS, 'transform': transform,
    'nodata': -9999,
}
for name, arr in [('DSM', dsm), ('CDSM', cdsm), ('DEM', dem_only)]:
    path = os.path.join(OUT_DIR, f'{name}_seoul_5m.tif')
    with rasterio.open(path, 'w', **profile) as dst:
        dst.write(arr, 1)
    print(f"  {name} 범위 {arr.min():.1f}~{arr.max():.1f}m | 저장: {path}")

print("\nDSM/CDSM/DEM 완료.")
