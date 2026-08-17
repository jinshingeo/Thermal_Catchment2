"""
5m 픽셀(서울 전역 Tmrt 래스터) -> KMA 500m 격자 인덱스, 서울 경계 클리핑판
================================================================
08번 스크립트는 Tmrt 래스터의 직사각형 bounding box 전체를 기준으로 필요한
격자셀을 계산해 4,403개(기존 캐시 2,300개 + 신규 2,103개)가 나왔으나, 확인
결과 신규 2,103개 중 95.3%(2,004개)가 서울 행정경계 바깥(클리핑 시 제거되는
영역)이었고, 경계 안쪽 99개는 전부 기존 캐시 2,300개 중 하나에서 3km 이내
(대부분 700m 이내)였다. 500m 해상도 자료에서 이 정도 거리면 기존 캐시로
충분하다고 판단, API 재호출 없이 기존 2,300개 셀만으로 인덱스를 다시 만든다.

계산 대상도 래스터 전체가 아니라 서울 행정경계 안쪽 픽셀로 제한한다(어차피
Results 시각화도 경계로 클리핑해서 씀 — 불필요한 계산 회피).

출력: pixel_grid_row_seoulclip.npy / pixel_grid_col_seoulclip.npy (그 격자칸,
      경계 밖은 -1) / pixel_seoul_mask.npy (경계 안쪽 여부, bool)
"""
import os
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio.features
from affine import Affine
from pyproj import Transformer
from scipy.spatial import cKDTree

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
CACHE = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache')
BOUNDARY_SHP = os.path.join(PROJ, 'data', '_tmp_boundary', '행정구역.shp')
OUT_ROW = os.path.join(CACHE, 'pixel_grid_row_seoulclip.npy')
OUT_COL = os.path.join(CACHE, 'pixel_grid_col_seoulclip.npy')
OUT_MASK = os.path.join(CACHE, 'pixel_seoul_mask.npy')

# Tmrt_seoul_5m_1400D.tif 헤더 (2026-08-17 서버 확인값, 08번과 동일)
LEFT, BOTTOM, RIGHT, TOP = 179189.0, 536549.0, 216239.0, 566864.0
RES = 5.0
WIDTH, HEIGHT = 7410, 6063
RASTER_CRS = 'EPSG:5186'

t0 = time.time()

print("서울 행정경계 로드 및 래스터 격자에 맞춰 마스크 생성 중...")
boundary = gpd.read_file(BOUNDARY_SHP).set_crs('EPSG:5179')
seoul = boundary.dissolve().to_crs(RASTER_CRS)

transform = Affine(RES, 0, LEFT, 0, -RES, TOP)
mask = rasterio.features.rasterize(
    [(geom, 1) for geom in seoul.geometry],
    out_shape=(HEIGHT, WIDTH), transform=transform, fill=0, dtype=np.uint8).astype(bool)
print(f"  서울 경계 안쪽 픽셀: {mask.sum():,} / 전체 {mask.size:,} ({mask.mean()*100:.1f}%)")

print("\n기존 캐시된 격자셀(링크 기반, 2,300개) 로드 중...")
cached = pd.read_csv(os.path.join(CACHE, 'link_to_kma_grid_index.csv'))
cached_cells = cached[['grid_row', 'grid_col', 'grid_lon', 'grid_lat']].drop_duplicates(
    subset=['grid_row', 'grid_col']).reset_index(drop=True)
print(f"  후보 격자셀 수: {len(cached_cells):,}")

tree = cKDTree(cached_cells[['grid_lon', 'grid_lat']].values)

wgs = Transformer.from_crs(RASTER_CRS, 'EPSG:4326', always_xy=True)

grid_row_out = np.full((HEIGHT, WIDTH), -1, dtype=np.int16)
grid_col_out = np.full((HEIGHT, WIDTH), -1, dtype=np.int16)

print(f"\n서울 경계 안쪽 픽셀만 최근접 배정 중... ({mask.sum():,}개)")
CHUNK = 300
n_chunks = int(np.ceil(HEIGHT / CHUNK))
max_dist_m = 0.0
for ci in range(n_chunks):
    r0 = ci * CHUNK
    r1 = min(r0 + CHUNK, HEIGHT)
    row_mask = mask[r0:r1, :]
    if not row_mask.any():
        continue
    rr, cc = np.where(row_mask)
    rr_abs = rr + r0

    xs = LEFT + (cc + 0.5) * RES
    ys = TOP - (rr_abs + 0.5) * RES
    lons, lats = wgs.transform(xs, ys)

    pts = np.column_stack([lons, lats])
    dist_deg, idx = tree.query(pts, k=1)
    max_dist_m = max(max_dist_m, dist_deg.max() * 111000)

    grid_row_out[rr_abs, cc] = cached_cells['grid_row'].values[idx]
    grid_col_out[rr_abs, cc] = cached_cells['grid_col'].values[idx]

    if ci % 5 == 0 or ci == n_chunks - 1:
        print(f"  청크 {ci+1}/{n_chunks} 완료 ({time.time()-t0:.0f}초 경과)", flush=True)

print(f"\n서울 경계 안쪽 픽셀의 최근접 배정 최대 거리: {max_dist_m:.0f}m")

np.save(OUT_ROW, grid_row_out)
np.save(OUT_COL, grid_col_out)
np.save(OUT_MASK, mask)
print(f"저장: {OUT_ROW}, {OUT_COL}, {OUT_MASK}")

print(f"\n총 소요시간: {time.time()-t0:.1f}초")
