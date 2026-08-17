"""
서울 전체 — 링크에 UTCI 대표값 부여, 버퍼 없이 (서버용)
================================================================
17c_assign_tmrt_utci_links_seoul_v3_server.py는 도로폭 버퍼+zonal mean을
썼으나, 이번엔 버퍼 없이 링크 선형이 실제로 지나는 픽셀만 사용한다
(zonal_stats all_touched=True, 버퍼 폴리곤 생성 단계 자체를 없앰).
입력은 29번 스크립트가 만든 픽셀 단위 KMA 격자기상 반영 UTCI 래스터.
"""
import os
import glob
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats

BASE = '/home/sj/thermal_catchment'
NET_PATH = os.path.join(BASE, 'data', 'network', 'seoul_walk_network.gpkg')
UTCI_DIR = os.path.join(BASE, '03_Method_C', 'results', 'utci_seoul_5m_kma_pixel')
OUT_DIR = os.path.join(BASE, '03_Method_C', 'results')

TARGET_CRS = 'EPSG:5186'

t0 = time.time()
print("서울 전체 네트워크 로드 중...", flush=True)
edges = gpd.read_file(NET_PATH, layer='edges').to_crs(TARGET_CRS)
edges = edges[edges.geometry.type.isin(['LineString', 'MultiLineString'])].copy()
print(f"  링크 수: {len(edges):,}", flush=True)

result = edges[['u', 'v', 'osmid', 'highway']].copy()
result['geometry'] = edges.geometry

utci_files = sorted(glob.glob(os.path.join(UTCI_DIR, 'UTCI_seoul_5m_kma_pixel_*.tif')))
utci_files = [f for f in utci_files if 'average' not in f]
print(f"\nUTCI 래스터 {len(utci_files)}개 시간대, 버퍼 없이 링크 zonal mean 계산 중...", flush=True)

for f in utci_files:
    th = time.time()
    hour = os.path.basename(f).split('_')[-1][:2]
    with rasterio.open(f) as src:
        affine = src.transform
        arr = src.read(1)
        arr = np.where(np.isnan(arr), np.nan, arr)

    stats = zonal_stats(edges.geometry, arr, affine=affine,
                         stats=['mean'], nodata=np.nan, all_touched=True)
    utci_vals = [s['mean'] for s in stats]
    result[f'UTCI_{hour}'] = utci_vals

    n_missing = sum(v is None for v in utci_vals)
    print(f"  {hour}시 완료 (결측 {n_missing}개, {time.time()-th:.0f}초)", flush=True)

result_gdf = gpd.GeoDataFrame(result, geometry='geometry', crs=TARGET_CRS)

out_gpkg = os.path.join(OUT_DIR, '2026-08-17_link_utci_seoul_5m_kma_pixel_nobuffer.gpkg')
result_gdf.to_file(out_gpkg, driver='GPKG')
print(f"저장: {out_gpkg}", flush=True)

out_csv = os.path.join(OUT_DIR, '2026-08-17_link_utci_seoul_5m_kma_pixel_nobuffer.csv')
result_gdf.drop(columns='geometry').to_csv(out_csv, index=False, encoding='utf-8-sig')
print(f"저장: {out_csv}", flush=True)

print(f"\n총 소요시간: {time.time()-t0:.1f}초 ({(time.time()-t0)/60:.1f}분)", flush=True)
