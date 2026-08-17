"""
5m 픽셀(서울 전역 Tmrt 래스터) -> KMA 500m 융합격자 인덱스 매핑
================================================================
03_build_kma_grid_index.py(링크 중심점 기준)를 픽셀 중심점 기준으로 확장.
Tmrt 래스터 실제 파일은 서버에만 있어 전송하지 않고, 이미 확인된 헤더
정보(CRS/해상도/크기/bounds)로 픽셀 중심 좌표를 직접 생성한다.

Tmrt_seoul_5m_1400D.tif 기준 헤더(2026-08-17 서버에서 rasterio로 확인):
  CRS EPSG:5186, res 5.0m, width 7410, height 6063,
  bounds left=179189 bottom=536549 right=216239 top=566864

출력: 픽셀별 grid_row/grid_col을 (height,width) 배열로 저장(.npy, 컴팩트)
      + 필요한 고유 격자셀 목록(pixel_to_kma_grid_cells.csv, API 재호출용)
"""
import os
import time
import numpy as np
import pandas as pd
from pyproj import Transformer
from scipy.spatial import cKDTree

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
CACHE = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache')
OUT_ROW = os.path.join(CACHE, 'pixel_grid_row.npy')
OUT_COL = os.path.join(CACHE, 'pixel_grid_col.npy')
OUT_CELLS = os.path.join(CACHE, 'pixel_to_kma_grid_cells.csv')

# Tmrt_seoul_5m_1400D.tif 헤더 (서버 확인값)
LEFT, BOTTOM, RIGHT, TOP = 179189.0, 536549.0, 216239.0, 566864.0
RES = 5.0
WIDTH, HEIGHT = 7410, 6063
SRC_CRS = 'EPSG:5186'


def load_grid(path):
    with open(path) as f:
        lines = f.read().strip().split('\n')
    nrow, ncol = int(lines[0].split(',')[0]), int(lines[0].split(',')[1])
    vals = []
    for line in lines[1:]:
        row = [float(x) for x in line.strip().rstrip(',').split(',') if x]
        vals.extend(row)
    return np.array(vals, dtype=np.float64).reshape(nrow, ncol)


t0 = time.time()
print("격자 위경도 로드 중...")
lat_grid = load_grid(os.path.join(CACHE, 'grid_lat.txt'))
lon_grid = load_grid(os.path.join(CACHE, 'grid_lon.txt'))
print(f"  전국 격자 크기: {lat_grid.shape}")

# Tmrt bounds를 대략의 위경도 범위로 미리 변환해 크롭 마진 계산
wgs = Transformer.from_crs(SRC_CRS, 'EPSG:4326', always_xy=True)
corner_lon, corner_lat = wgs.transform(
    [LEFT, RIGHT, LEFT, RIGHT], [BOTTOM, BOTTOM, TOP, TOP])
lon_min, lon_max = min(corner_lon), max(corner_lon)
lat_min, lat_max = min(corner_lat), max(corner_lat)
print(f"  Tmrt 도메인 위경도 범위(대략): {lon_min:.3f}~{lon_max:.3f}, {lat_min:.3f}~{lat_max:.3f}")

margin = 0.1
mask = ((lon_grid >= lon_min - margin) & (lon_grid <= lon_max + margin) &
        (lat_grid >= lat_min - margin) & (lat_grid <= lat_max + margin))
rows, cols = np.where(mask)
print(f"  크롭된 격자 셀 수(KDTree 대상): {len(rows):,}")

grid_points = np.column_stack([lon_grid[rows, cols], lat_grid[rows, cols]])
print("KDTree 생성 중...")
tree = cKDTree(grid_points)

print(f"픽셀 중심좌표 생성 중... ({WIDTH}x{HEIGHT} = {WIDTH*HEIGHT:,}개)")
grid_row_out = np.zeros((HEIGHT, WIDTH), dtype=np.uint16)
grid_col_out = np.zeros((HEIGHT, WIDTH), dtype=np.uint16)

CHUNK = 300  # 행 단위 청크 (300행 x 7410열 = 222만 포인트/청크)
n_chunks = int(np.ceil(HEIGHT / CHUNK))
for ci in range(n_chunks):
    r0 = ci * CHUNK
    r1 = min(r0 + CHUNK, HEIGHT)
    rr = np.arange(r0, r1)
    cc = np.arange(WIDTH)
    col_idx, row_idx = np.meshgrid(cc, rr)  # shape (r1-r0, WIDTH)

    xs = LEFT + (col_idx.ravel() + 0.5) * RES
    ys = TOP - (row_idx.ravel() + 0.5) * RES
    lons, lats = wgs.transform(xs, ys)

    pts = np.column_stack([lons, lats])
    dist, idx = tree.query(pts, k=1)

    grid_row_out[r0:r1, :] = rows[idx].reshape(r1 - r0, WIDTH)
    grid_col_out[r0:r1, :] = cols[idx].reshape(r1 - r0, WIDTH)

    if ci % 5 == 0 or ci == n_chunks - 1:
        print(f"  청크 {ci+1}/{n_chunks} 완료 ({time.time()-t0:.0f}초 경과)", flush=True)

np.save(OUT_ROW, grid_row_out)
np.save(OUT_COL, grid_col_out)
print(f"저장: {OUT_ROW}, {OUT_COL}")

cell_ids = np.stack([grid_row_out.ravel(), grid_col_out.ravel()], axis=1)
unique_cells = np.unique(cell_ids, axis=0)
print(f"\n필요한 고유 KMA 격자셀 수: {len(unique_cells):,}")

cells_df = pd.DataFrame(unique_cells, columns=['grid_row', 'grid_col'])
cells_df.to_csv(OUT_CELLS, index=False)
print(f"저장: {OUT_CELLS}")

# 기존(링크 기반) 캐시와 비교
existing_idx_path = os.path.join(CACHE, 'link_to_kma_grid_index.csv')
if os.path.exists(existing_idx_path):
    existing = pd.read_csv(existing_idx_path)[['grid_row', 'grid_col']].drop_duplicates()
    existing_set = set(map(tuple, existing.values))
    new_set = set(map(tuple, unique_cells))
    overlap = existing_set & new_set
    missing = new_set - existing_set
    print(f"\n기존 링크 기반 캐시 셀 수: {len(existing_set):,}")
    print(f"  겹치는 셀: {len(overlap):,}")
    print(f"  신규로 필요한 셀(API 재호출 대상): {len(missing):,}")

print(f"\n총 소요시간: {time.time()-t0:.1f}초")
