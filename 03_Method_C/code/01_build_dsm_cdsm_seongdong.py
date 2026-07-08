"""
성동구 파일럿 — DSM(건물)·CDSM(수목) 래스터 생성 (접근1: 30m / 접근2: 1m)
================================================================
접근1: 지면(GLO-30)+건물+수목 동일 자료를 30m 격자로
접근2: 동일 자료를 1m로 다운스케일링 (지면은 보간뿐, 건물·수목은 벡터속성 그대로 반영)

DSM = 지면(DEM) + 건물높이  (masl, 절대표고 — 건물은 불투명이라 지면과 합산)
CDSM = 수목높이만 (magl, 상대높이 — SOLWEIG 요구사항, DEM 미가산)

건물높이 4단계: F_FAC_BUILDING 실측 HEIGHT → 자체 GRND_FLR×3m →
               TL_SPBD_BULD 교차보완(BD_MGT_SN)×3m → 기본값 3m
수목높이: 임상도(산림청) HEIGHT 필드 직접 사용 (임분고코드, 실측)

참고: writing/2026-07-07_MethodC_SOLWEIG파일럿_진행기록.md (v2)
"""

import os
os.environ.setdefault(
    'PROJ_DATA',
    '/opt/miniconda3/lib/python3.13/site-packages/rasterio/proj_data')  # conda proj.db 버전충돌 회피

import numpy as np
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'dsm_cdsm_seongdong')
os.makedirs(OUT_DIR, exist_ok=True)

DEM_PATH = os.path.join(PROJ, 'data', 'GLO30_DSM', 'GLO30_Seoul_EPSG5186_30m.tif')
BND_PATH = os.path.join(PROJ, 'data', '_tmp_boundary', '행정구역.shp')
FAC_PATH = os.path.join(PROJ, 'data', 'F_FAC_BUILDING_서울', 'F_FAC_BUILDING_11_202606.shp')
TL_PATH = '/Users/jin/석사논문/TAVI/03_건물데이터/(도로명주소)건물_서울/TL_SPBD_BULD_11_202603.shp'
FOREST_PATH = os.path.join(PROJ, 'data', '녹지데이터 복사본', '임상도', '11_서울시', '11.shp')

TARGET_CRS = 'EPSG:5186'
DEFAULT_HEIGHT = 3.0  # 1개층 상당 기본값


# ── 1. 성동구 경계 ────────────────────────────────────────────────────────
bnd = gpd.read_file(BND_PATH, encoding='cp949')
seongdong = bnd[bnd['SIGUNGU_NM'] == '성동구'].dissolve()
seongdong = seongdong.set_crs('EPSG:5179', allow_override=True).to_crs(TARGET_CRS)
print(f"성동구 경계: {seongdong.geometry.area.iloc[0]/1e6:.2f} km²")


# ── 2. 건물 높이 (4단계 하이브리드) ───────────────────────────────────────
print("\n건물 높이 계산 중...")
fac = gpd.read_file(FAC_PATH, encoding='cp949')
assert fac.crs.to_string() == TARGET_CRS, f"F_FAC_BUILDING CRS 불일치: {fac.crs}"
fac_sd = gpd.clip(fac, seongdong)

tl = gpd.read_file(TL_PATH, encoding='cp949')
tl['geometry'] = tl.geometry.buffer(0)
tl_sd = gpd.clip(tl, seongdong.to_crs(tl.crs)).to_crs(TARGET_CRS)
tl_height_lookup = (tl_sd[tl_sd['GRO_FLO_CO'].notna() & (tl_sd['GRO_FLO_CO'] > 0)]
                     .set_index('BD_MGT_SN')['GRO_FLO_CO'] * DEFAULT_HEIGHT).to_dict()

fac_sd = fac_sd.copy()
fac_sd['HEIGHT_FINAL'] = np.nan
valid = (fac_sd['HEIGHT'] > 0) & (fac_sd['HEIGHT'] < 200)
fac_sd.loc[valid, 'HEIGHT_FINAL'] = fac_sd.loc[valid, 'HEIGHT']

need2 = fac_sd['HEIGHT_FINAL'].isna() & (fac_sd['GRND_FLR'] > 0)
fac_sd.loc[need2, 'HEIGHT_FINAL'] = fac_sd.loc[need2, 'GRND_FLR'] * DEFAULT_HEIGHT

need3 = fac_sd['HEIGHT_FINAL'].isna() & fac_sd['BD_MGT_SN'].isin(tl_height_lookup)
fac_sd.loc[need3, 'HEIGHT_FINAL'] = fac_sd.loc[need3, 'BD_MGT_SN'].map(tl_height_lookup)

fac_sd['HEIGHT_FINAL'] = fac_sd['HEIGHT_FINAL'].fillna(DEFAULT_HEIGHT)

n1, n2, n3 = valid.sum(), need2.sum(), need3.sum()
n4 = len(fac_sd) - n1 - n2 - n3
print(f"  전체 {len(fac_sd):,}동 | 실측 {n1:,} | 자체층수 {n2:,} | "
      f"교차보완 {n3:,} | 기본값 {n4:,}")


# ── 3. 수목 높이 (임상도) ──────────────────────────────────────────────────
print("\n수목 높이 로드 중...")
forest = gpd.read_file(FOREST_PATH, encoding='cp949')
forest_sd = gpd.clip(forest, seongdong.to_crs(forest.crs)).to_crs(TARGET_CRS)
forest_sd = forest_sd[forest_sd['FRTP_NM'] != '무립목지/비산림'].copy()
forest_sd = forest_sd.dropna(subset=['HEIGHT'])
forest_sd['HEIGHT_NUM'] = forest_sd['HEIGHT'].astype(float)
print(f"  산림 폴리곤 {len(forest_sd)}개, 평균수고 {forest_sd['HEIGHT_NUM'].mean():.1f}m")


# ── 4. 그리드 정의 (접근1: 30m / 접근2: 1m) ────────────────────────────────
minx, miny, maxx, maxy = seongdong.total_bounds
minx, miny = np.floor(minx / 30) * 30, np.floor(miny / 30) * 30
maxx, maxy = np.ceil(maxx / 30) * 30, np.ceil(maxy / 30) * 30

grids = {
    'approach1_30m': (30.0, minx, miny, maxx, maxy),
    'approach2_1m':  (1.0,  minx, miny, maxx, maxy),
}

with rasterio.open(DEM_PATH) as dem_src:
    dem_data = dem_src.read(1)
    dem_transform = dem_src.transform
    dem_crs = dem_src.crs

for label, (res, gx0, gy0, gx1, gy1) in grids.items():
    width = int(round((gx1 - gx0) / res))
    height = int(round((gy1 - gy0) / res))
    transform = from_origin(gx0, gy1, res, res)
    out_shape = (height, width)
    print(f"\n[{label}] 그리드: {width}x{height} px @ {res}m")

    # 4-1. 지면(DEM) 리샘플링
    dem_resampled = np.zeros(out_shape, dtype=np.float32)
    reproject(
        source=dem_data, destination=dem_resampled,
        src_transform=dem_transform, src_crs=dem_crs,
        dst_transform=transform, dst_crs=TARGET_CRS,
        resampling=Resampling.bilinear,
    )

    # 4-2. 건물 높이 래스터화
    bld_shapes = [(geom, h) for geom, h in
                  zip(fac_sd.geometry, fac_sd['HEIGHT_FINAL']) if geom is not None]
    bld_raster = rasterize(
        bld_shapes, out_shape=out_shape, transform=transform,
        fill=0.0, dtype='float32',
    )

    # 4-3. 수목 높이 래스터화
    tree_shapes = [(geom, h) for geom, h in
                   zip(forest_sd.geometry, forest_sd['HEIGHT_NUM']) if geom is not None]
    tree_raster = rasterize(
        tree_shapes, out_shape=out_shape, transform=transform,
        fill=0.0, dtype='float32',
    )

    # 4-4. DSM = DEM + 건물높이 (masl)
    dsm = dem_resampled + bld_raster
    # 4-5. CDSM = 수목높이만 (magl)
    cdsm = tree_raster

    profile = {
        'driver': 'GTiff', 'height': height, 'width': width, 'count': 1,
        'dtype': 'float32', 'crs': TARGET_CRS, 'transform': transform,
        'nodata': -9999,
    }
    dsm_path = os.path.join(OUT_DIR, f'DSM_{label}.tif')
    cdsm_path = os.path.join(OUT_DIR, f'CDSM_{label}.tif')
    with rasterio.open(dsm_path, 'w', **profile) as dst:
        dst.write(dsm, 1)
    with rasterio.open(cdsm_path, 'w', **profile) as dst:
        dst.write(cdsm, 1)

    print(f"  DSM  범위 {dsm.min():.1f}~{dsm.max():.1f}m | 저장: {dsm_path}")
    print(f"  CDSM 범위 {cdsm.min():.1f}~{cdsm.max():.1f}m (0={len(cdsm[cdsm==0])/cdsm.size*100:.1f}%) | 저장: {cdsm_path}")

print("\n완료.")
