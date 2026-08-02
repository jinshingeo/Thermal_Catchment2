"""1mtrue 링크 파일 재생성 — 버퍼를 width_final/2(메인 방법론과 동일)로,
all_touched=True 추가. 기존 2026-07-28_link_tmrt_utci_seongdong_1mtrue.gpkg의
고정 5m 버퍼(all_touched 없음) 버그 수정판. 새 파일로 저장, 기존 파일 보존.
"""
import os
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.warp import reproject, Resampling
from rasterstats import zonal_stats

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TMRT1_DIR = os.path.join(BASE, '03_Method_C/results/solweig_seongdong_1mtrue_mosaic_local')
UTCI1_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_1mtrue_local')
LINK_SRC = os.path.join(BASE, '03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg')
OUT_GPKG = os.path.join(BASE, '03_Method_C/results/2026-07-29_link_tmrt_utci_seongdong_1mtrue_v2.gpkg')

HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}

with rasterio.open(os.path.join(BASE, '03_Method_C/results/solweig_approach2_5m/Tmrt_2025_209_1300D.tif')) as ref:
    ref_tr, ref_crs, ref_w, ref_h = ref.transform, ref.crs, ref.width, ref.height

links = gpd.read_file(LINK_SRC)[['u', 'v', 'osmid', 'highway_1', 'width_final', 'length', 'geometry']].copy()
links_buf = links.buffer(links['width_final'] / 2)
print(f'링크 수: {len(links)}, width_final 결측: {links["width_final"].isna().sum()}', flush=True)

for h in HOURS:
    hc = HCODE[h]
    with rasterio.open(os.path.join(TMRT1_DIR, f'Tmrt_seongdong_1mtrue_{hc}.tif')) as src:
        arr = src.read(1).astype(np.float32)
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        dst = np.full((ref_h, ref_w), np.nan, dtype=np.float32)
        reproject(source=arr, destination=dst, src_transform=src.transform, src_crs=src.crs,
                  dst_transform=ref_tr, dst_crs=ref_crs, resampling=Resampling.average,
                  src_nodata=np.nan, dst_nodata=np.nan)
    st = zonal_stats(links_buf, dst, affine=ref_tr, stats=['mean'], nodata=np.nan, all_touched=True)
    links[f'Tmrt_{h:02d}'] = [s['mean'] for s in st]

    with rasterio.open(os.path.join(UTCI1_DIR, f'UTCI_seongdong_1mtrue_{h:02d}.tif')) as src:
        arr = src.read(1).astype(np.float32)
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        dstu = np.full((ref_h, ref_w), np.nan, dtype=np.float32)
        reproject(source=arr, destination=dstu, src_transform=src.transform, src_crs=src.crs,
                  dst_transform=ref_tr, dst_crs=ref_crs, resampling=Resampling.average,
                  src_nodata=np.nan, dst_nodata=np.nan)
    stu = zonal_stats(links_buf, dstu, affine=ref_tr, stats=['mean'], nodata=np.nan, all_touched=True)
    links[f'UTCI_{h:02d}'] = [s['mean'] for s in stu]
    n_missing = sum(s['mean'] is None for s in stu)
    print(f'  {h:02d}시 완료 (UTCI 결측 {n_missing}개)', flush=True)

out_gdf = gpd.GeoDataFrame(links, geometry=links.geometry, crs=links.crs)
out_gdf.to_file(OUT_GPKG, driver='GPKG')
print(f'저장: {OUT_GPKG}', flush=True)
