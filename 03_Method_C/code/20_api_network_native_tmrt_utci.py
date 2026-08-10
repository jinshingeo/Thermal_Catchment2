"""
서울시 도보 네트워크 API(TbTraficWlkNet) 링크에 Tmrt/UTCI를 "직접" 부여
================================================================
기존 seoul_wide_api_network_contour.py는 OSM 링크의 Tmrt/UTCI 값을
최근접매칭으로 "상속"만 했다. 이 스크립트는 그 대신 API 링크 지오메트리에
직접 버퍼+zonal mean(17_assign_tmrt_to_links_seoul_5m.py와 동일 방식)을
적용해 Tmrt를 산출하고, KMA 격자기상을 이용해(07_compute_utci_kma_gridded.py
와 동일 방식) UTCI까지 계산한다.

도로폭(width)만은 API 네트워크 자체에 필드가 없어 기존 방식대로 OSM
최근접매칭으로 상속한다(CLAUDE.md에 이미 문서화된 방식) — Tmrt/UTCI "값"만
독립적으로 재계산하는 것이 이 스크립트의 목적.
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
from pyproj import Transformer
from scipy.spatial import cKDTree
from pythermalcomfort.models import utci

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
API_NET = os.path.join(PROJ, 'data', 'network', '2026-08-02_seoul_walk_api_network.gpkg')
OSM_NET = os.path.join(PROJ, 'data', 'network', 'seoul_walk_network.gpkg')
TMRT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'solweig_seoul_5m_v2_mosaic')
KMA_CACHE = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results')

TARGET_CRS = 'EPSG:5186'
HOURS = list(range(6, 20))

HIGHWAY_WIDTH_DEFAULT = {
    'footway': 2.0, 'path': 2.0, 'pedestrian': 3.0, 'steps': 2.0,
    'living_street': 6.0, 'residential': 6.0, 'service': 4.0,
    'unclassified': 6.0, 'tertiary': 9.0, 'secondary': 15.0,
    'primary': 20.0, 'trunk': 25.0,
}
DEFAULT_WIDTH = 6.0

t0 = time.time()


def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)


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


# ── 1. API 네트워크 로드 ──────────────────────────────────────────────────
log("API 네트워크 로드...")
api = gpd.read_file(API_NET)
api = api[api['LNKG_TYPE_CD'].str.startswith('1')].copy()
api = api.to_crs(TARGET_CRS)
api['LNKG_LEN'] = api['LNKG_LEN'].astype(float)
api = api[api['LNKG_LEN'] > 0].reset_index(drop=True).copy()
log(f"  API 보행 링크: {len(api):,}개")

# ── 2. 도로폭 — OSM 최근접매칭으로 상속(기존 방식 그대로) ──────────────────
log("OSM 네트워크 로드 및 width_final 계산...")
osm = gpd.read_file(OSM_NET, layer='edges').to_crs(TARGET_CRS)
osm = osm[osm.geometry.type.isin(['LineString', 'MultiLineString'])].copy()
osm['highway_1'] = osm['highway'].apply(parse_highway)
osm['width_osm'] = osm['width'].apply(parse_width)
osm['width_final'] = osm['width_osm']
mask_missing = osm['width_final'].isna()
osm.loc[mask_missing, 'width_final'] = osm.loc[mask_missing, 'highway_1'].map(
    HIGHWAY_WIDTH_DEFAULT).fillna(DEFAULT_WIDTH)
osm = osm[osm['width_final'] > 0].copy()
log(f"  OSM 링크(width 계산됨): {len(osm):,}개")

log("API 링크 -> 최근접 OSM 링크 width 매칭...")
api_pts = gpd.GeoDataFrame(api[['LNKG_ID']], geometry=api.geometry.centroid, crs=TARGET_CRS)
osm_small = osm[['width_final', 'geometry']].copy()
joined_w = gpd.sjoin_nearest(api_pts, osm_small, how='left', distance_col='dist_w_m')
joined_w = joined_w.drop_duplicates(subset='LNKG_ID')
api = api.merge(joined_w[['LNKG_ID', 'width_final']], on='LNKG_ID', how='left')
api['width_final'] = api['width_final'].fillna(DEFAULT_WIDTH)
log(f"  width 매칭 완료 (평균 {api['width_final'].mean():.1f}m)")

api['buffer_geom'] = api.buffer(api['width_final'] / 2)

# ── 3. Tmrt 래스터 -> API 링크 버퍼 zonal mean (직접 집계, 상속 아님) ───────
tmrt_files = sorted(glob.glob(os.path.join(TMRT_DIR, 'Tmrt_seoul_5m_*.tif')))
tmrt_files = [f for f in tmrt_files if 'average' not in f]
log(f"Tmrt 래스터 {len(tmrt_files)}개 - API 링크 직접 zonal mean 계산 시작...")

result = api[['LNKG_ID', 'BGNG_LNKG_ID', 'END_LNKG_ID', 'LNKG_LEN', 'width_final']].copy()

for f in tmrt_files:
    th = time.time()
    hour = os.path.basename(f).split('_')[-1][:2]
    with rasterio.open(f) as src:
        affine = src.transform
        arr = src.read(1)
        arr = np.where((arr <= -100) | (arr >= 200), np.nan, arr)
    stats = zonal_stats(api['buffer_geom'], arr, affine=affine,
                         stats=['mean'], nodata=np.nan, all_touched=True)
    result[f'Tmrt_{hour}'] = [s['mean'] for s in stats]
    n_missing = sum(s['mean'] is None for s in stats)
    log(f"  {hour}시 완료 (결측 {n_missing}개, {time.time()-th:.0f}초)")

# ── 4. API 링크 -> KMA 격자 인덱스 매핑 (link_idx = result 순서) ────────────
log("KMA 격자 위경도 로드 및 API 링크 최근접 격자 탐색...")


def load_grid(path):
    with open(path) as fh:
        lines = fh.read().strip().split('\n')
    nrow, ncol = int(lines[0].split(',')[0]), int(lines[0].split(',')[1])
    vals = []
    for line in lines[1:]:
        row = [float(x) for x in line.strip().rstrip(',').split(',') if x]
        vals.extend(row)
    return np.array(vals, dtype=np.float64).reshape(nrow, ncol)


lat_grid = load_grid(os.path.join(KMA_CACHE, 'grid_lat.txt'))
lon_grid = load_grid(os.path.join(KMA_CACHE, 'grid_lon.txt'))

centroids = api.geometry.centroid
xs, ys = centroids.x.values, centroids.y.values
wgs = Transformer.from_crs(TARGET_CRS, 'EPSG:4326', always_xy=True)
link_lon, link_lat = wgs.transform(xs, ys)

margin = 0.1
mask = ((lon_grid >= link_lon.min() - margin) & (lon_grid <= link_lon.max() + margin) &
        (lat_grid >= link_lat.min() - margin) & (lat_grid <= link_lat.max() + margin))
rows, cols = np.where(mask)
grid_points = np.column_stack([lon_grid[rows, cols], lat_grid[rows, cols]])
tree = cKDTree(grid_points)
link_points = np.column_stack([link_lon, link_lat])
dist, idx = tree.query(link_points, k=1)

result['grid_row'] = rows[idx]
result['grid_col'] = cols[idx]
log(f"  격자 매칭 완료 (최대거리 {dist.max()*111000:.0f}m)")

# ── 5. KMA 기상값 배정 + UTCI 계산 (07_compute_utci_kma_gridded.py와 동일 로직) ──
log("KMA 격자 기상값 로드 및 UTCI 계산...")
met = pd.read_csv(os.path.join(KMA_CACHE, 'kma_grid_met_12day_avg.csv'))

for h in HOURS:
    h_met = met[met['hour'] == h]
    merged = result[['grid_row', 'grid_col']].merge(
        h_met, on=['grid_row', 'grid_col'], how='left')
    ta = merged['ta'].values
    rh = merged['hm'].values
    ws = merged['ws_10m'].values
    tmrt = result[f'Tmrt_{h:02d}'].values

    valid = ~(np.isnan(ta) | np.isnan(rh) | np.isnan(ws) | np.isnan(tmrt))
    utci_vals = np.full(len(result), np.nan)
    res = utci(tdb=ta[valid].tolist(), tr=tmrt[valid].tolist(),
               v=ws[valid].tolist(), rh=rh[valid].tolist(),
               limit_inputs=False, round_output=False)
    utci_vals[valid] = np.array(res.utci)
    result[f'UTCI_{h:02d}'] = utci_vals
    log(f"  {h:02d}시 UTCI 완료 (유효 {valid.sum():,}/{len(result):,})")

# ── 6. 저장 ─────────────────────────────────────────────────────────────
out_gdf = gpd.GeoDataFrame(result, geometry=api.geometry, crs=TARGET_CRS)
out_path = os.path.join(OUT_DIR, '2026-08-11_link_tmrt_utci_seoul_5m_api_network_native.gpkg')
out_gdf.to_file(out_path, driver='GPKG')
log(f"저장: {out_path}")

csv_path = out_path.replace('.gpkg', '.csv')
result.to_csv(csv_path, index=False, encoding='utf-8-sig')
log(f"저장: {csv_path}")
log(f"총 소요시간: {(time.time()-t0)/60:.1f}분")
