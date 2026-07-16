"""
서울 전체 — 도보 링크에 Tmrt 대표값 부여 (5m, 시간대별 14개 + 평균)
================================================================
13_assign_tmrt_to_links_5m.py(성동구)와 완전히 동일한 방식(Colaninno et al.
2024 버퍼+zonal mean)을 서울 전체 네트워크(469,010개 링크)에 적용.
"""
import os
import re
import ast
import glob
import time
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
NET_PATH = os.path.join(PROJ, 'data', 'network', 'seoul_walk_network.gpkg')
TMRT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'solweig_seoul_5m_v2_mosaic')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results')

TARGET_CRS = 'EPSG:5186'

HIGHWAY_WIDTH_DEFAULT = {
    'footway': 2.0, 'path': 2.0, 'pedestrian': 3.0, 'steps': 2.0,
    'living_street': 6.0, 'residential': 6.0, 'service': 4.0,
    'unclassified': 6.0, 'tertiary': 9.0, 'secondary': 15.0,
    'primary': 20.0, 'trunk': 25.0,
}
DEFAULT_WIDTH = 6.0


def parse_highway(val):
    if val is None:
        return None
    s = str(val)
    if s.startswith('['):
        try:
            lst = ast.literal_eval(s)
            return lst[0] if lst else None
        except Exception:
            return None
    return s


def parse_width(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    s = str(val)
    if s.startswith('['):
        try:
            lst = ast.literal_eval(s)
            s = str(lst[0])
        except Exception:
            return None
    m = re.search(r'[\d.]+', s)
    return float(m.group()) if m else None


t0 = time.time()
print("서울 전체 네트워크 로드 중...")
edges = gpd.read_file(NET_PATH, layer='edges').to_crs(TARGET_CRS)
edges = edges[edges.geometry.type.isin(['LineString', 'MultiLineString'])].copy()
print(f"  링크 수: {len(edges):,}")

edges['highway_1'] = edges['highway'].apply(parse_highway)
edges['width_osm'] = edges['width'].apply(parse_width)
edges['width_final'] = edges['width_osm']
mask_missing = edges['width_final'].isna()
edges.loc[mask_missing, 'width_final'] = edges.loc[mask_missing, 'highway_1'].map(
    HIGHWAY_WIDTH_DEFAULT).fillna(DEFAULT_WIDTH)

n_before = len(edges)
edges = edges[edges['width_final'] > 0].copy()
print(f"  width<=0 링크 {n_before - len(edges)}개 제외 (최종 {len(edges):,}개)")

edges['buffer_geom'] = edges.buffer(edges['width_final'] / 2)

# ── 시간대별 Tmrt 버퍼 zonal mean ────────────────────────────────────────
tmrt_files = sorted(glob.glob(os.path.join(TMRT_DIR, 'Tmrt_seoul_5m_*.tif')))
tmrt_files = [f for f in tmrt_files if 'average' not in f]
print(f"\nTmrt 래스터 {len(tmrt_files)}개(5m)에 대해 링크별 zonal mean 계산 중...")

result = edges[['u', 'v', 'osmid', 'highway_1', 'width_final', 'length']].copy()

for f in tmrt_files:
    th = time.time()
    hour = os.path.basename(f).split('_')[-1][:2]
    with rasterio.open(f) as src:
        affine = src.transform
        arr = src.read(1)
        arr = np.where((arr <= -100) | (arr >= 200), np.nan, arr)
    stats = zonal_stats(edges['buffer_geom'], arr, affine=affine,
                        stats=['mean'], nodata=np.nan, all_touched=True)
    result[f'Tmrt_{hour}'] = [s['mean'] for s in stats]
    print(f"  {hour}시 완료 (결측 {sum(s['mean'] is None for s in stats)}개, {time.time()-th:.0f}초)")

# 평균 컬럼도 추가
hour_cols = [f'Tmrt_{os.path.basename(f).split("_")[-1][:2]}' for f in tmrt_files]
result['Tmrt_avg'] = result[hour_cols].mean(axis=1)

out_gdf = gpd.GeoDataFrame(result, geometry=edges.geometry, crs=TARGET_CRS)
out_path = os.path.join(OUT_DIR, '2026-07-16_link_tmrt_seoul_5m.gpkg')
out_gdf.to_file(out_path, driver='GPKG')
print(f"\n저장: {out_path}")

csv_path = os.path.join(OUT_DIR, '2026-07-16_link_tmrt_seoul_5m.csv')
result.to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"저장: {csv_path}")
print(f"\n총 소요시간: {time.time()-t0:.0f}초 ({(time.time()-t0)/60:.1f}분)")
