"""
서울 링크(46.9만개) -> KMA 500m 융합격자 인덱스 매핑 (1회 실행, 결과 재사용)
================================================================
03_Method_C의 링크별 Tmrt gpkg(EPSG:5186)에서 링크 중심점을 뽑아 lon/lat으로
변환하고, KMA 격자자료의 위경도 배열(전국 2049x2049)에서 가장 가까운 격자
인덱스(row,col)를 찾아 저장한다. 이후 기상요소 다운로드 스크립트가 이 매핑을
재사용해 격자값을 링크에 배정한다.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer
from scipy.spatial import cKDTree

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
CACHE = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache')
TMRT_GPKG = os.path.join(PROJ, '03_Method_C', 'results', '2026-07-16_link_tmrt_seoul_5m.gpkg')
OUT_PATH = os.path.join(CACHE, 'link_to_kma_grid_index.csv')


def load_grid(path):
    with open(path) as f:
        lines = f.read().strip().split('\n')
    nrow, ncol = int(lines[0].split(',')[0]), int(lines[0].split(',')[1])
    vals = []
    for line in lines[1:]:
        row = [float(x) for x in line.strip().rstrip(',').split(',') if x]
        vals.extend(row)
    arr = np.array(vals, dtype=np.float64).reshape(nrow, ncol)
    return arr


print("격자 위경도 로드 중...")
lat_grid = load_grid(os.path.join(CACHE, 'grid_lat.txt'))
lon_grid = load_grid(os.path.join(CACHE, 'grid_lon.txt'))
nrow, ncol = lat_grid.shape
print(f"  격자 크기: {nrow} x {ncol}")

print("링크 중심점 로드 중...")
gdf = gpd.read_file(TMRT_GPKG, columns=['geometry'])
centroids = gdf.geometry.centroid
xs, ys = centroids.x.values, centroids.y.values

wgs = Transformer.from_crs('EPSG:5186', 'EPSG:4326', always_xy=True)
link_lon, link_lat = wgs.transform(xs, ys)
print(f"  링크 수: {len(link_lon):,}")
print(f"  링크 lon/lat 범위: {link_lon.min():.3f}~{link_lon.max():.3f}, "
      f"{link_lat.min():.3f}~{link_lat.max():.3f}")

# 서울 범위만 크롭해서 KDTree 크기 축소 (여유 0.1도)
margin = 0.1
mask = ((lon_grid >= link_lon.min() - margin) & (lon_grid <= link_lon.max() + margin) &
        (lat_grid >= link_lat.min() - margin) & (lat_grid <= link_lat.max() + margin))
rows, cols = np.where(mask)
print(f"  크롭된 격자 셀 수: {len(rows):,}")

grid_points = np.column_stack([lon_grid[rows, cols], lat_grid[rows, cols]])
print("KDTree 생성 중...")
tree = cKDTree(grid_points)

print("최근접 격자 탐색 중...")
link_points = np.column_stack([link_lon, link_lat])
dist, idx = tree.query(link_points, k=1)

out = pd.DataFrame({
    'link_idx': np.arange(len(gdf)),
    'grid_row': rows[idx],
    'grid_col': cols[idx],
    'link_lon': link_lon,
    'link_lat': link_lat,
    'grid_lon': grid_points[idx, 0],
    'grid_lat': grid_points[idx, 1],
    'dist_deg': dist,
})
out.to_csv(OUT_PATH, index=False)
print(f"저장: {OUT_PATH}")
print(f"  고유 격자 셀 수: {out.groupby(['grid_row','grid_col']).ngroups:,}")
print(f"  최대 거리(도): {dist.max():.5f} (약 {dist.max()*111:.0f}m)")
