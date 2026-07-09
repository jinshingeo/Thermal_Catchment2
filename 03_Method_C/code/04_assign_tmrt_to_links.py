"""
성동구 파일럿 — 도보 링크에 Tmrt 대표값 부여 (Colaninno et al. 2024 방식)
================================================================
"세그먼트에 버퍼(폴리곤) 씌우고 그 안 픽셀 평균" 방식 채택.
버퍼 폭은 OSM width 태그가 있으면 그 값, 없으면 도로유형(highway)별
통상 폭 가정값 사용.

⚠️ 도로유형별 폭 가정값은 아직 근거논문 미확보 — 추후 인용 가능한
출처를 찾으면 교체할 것 (오늘은 파일럿이라 통상값으로 우선 진행).
"""
import os
import re
import ast
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
NET_PATH = os.path.join(PROJ, 'data', 'network', 'seoul_walk_network.gpkg')
BND_PATH = os.path.join(PROJ, 'data', '_tmp_boundary', '행정구역.shp')
SOLWEIG_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'dsm_cdsm_seongdong',
                           'solweig_approach1_30m')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results')

TARGET_CRS = 'EPSG:5186'

# ⚠️ 근거논문 미확보 — 통상값(추후 교체 대상)
HIGHWAY_WIDTH_DEFAULT = {
    'footway': 2.0, 'path': 2.0, 'pedestrian': 3.0, 'steps': 2.0,
    'living_street': 6.0, 'residential': 6.0, 'service': 4.0,
    'unclassified': 6.0, 'tertiary': 9.0, 'secondary': 15.0,
    'primary': 20.0, 'trunk': 25.0,
}
DEFAULT_WIDTH = 6.0


def parse_highway(val):
    """OSM highway 필드가 리스트 문자열("['residential','footway']")인 경우 첫 값 사용"""
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
    """OSM width 태그 파싱 (숫자/리스트/범위 문자열 등 방어적으로 처리)"""
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


# ── 1. 성동구 경계 + 네트워크 클립 ─────────────────────────────────────────
print("네트워크 로드 중...")
bnd = gpd.read_file(BND_PATH, encoding='cp949')
seongdong = bnd[bnd['SIGUNGU_NM'] == '성동구'].dissolve()
seongdong = seongdong.set_crs('EPSG:5179', allow_override=True).to_crs(TARGET_CRS)

edges = gpd.read_file(NET_PATH, layer='edges')
edges = edges.to_crs(TARGET_CRS)
edges_sd = gpd.clip(edges, seongdong).copy()
edges_sd = edges_sd[edges_sd.geometry.type.isin(['LineString', 'MultiLineString'])]
print(f"  성동구 내 링크 수: {len(edges_sd):,}")

# ── 2. 버퍼 폭 산정 ────────────────────────────────────────────────────────
edges_sd['highway_1'] = edges_sd['highway'].apply(parse_highway)
edges_sd['width_osm'] = edges_sd['width'].apply(parse_width)
edges_sd['width_final'] = edges_sd['width_osm']
mask_missing = edges_sd['width_final'].isna()
edges_sd.loc[mask_missing, 'width_final'] = edges_sd.loc[mask_missing, 'highway_1'].map(
    HIGHWAY_WIDTH_DEFAULT).fillna(DEFAULT_WIDTH)

print(f"  OSM width 태그 사용: {(~edges_sd['width_osm'].isna()).sum()}개")
print(f"  도로유형 기본값 사용: {mask_missing.sum()}개")

edges_sd['buffer_geom'] = edges_sd.buffer(edges_sd['width_final'] / 2)

# ── 3. 시간대별 Tmrt 버퍼 zonal mean ───────────────────────────────────────
import glob
tmrt_files = sorted(glob.glob(os.path.join(SOLWEIG_DIR, 'Tmrt_2025_209_*.tif')))
print(f"\nTmrt 래스터 {len(tmrt_files)}개에 대해 링크별 zonal mean 계산 중...")

result = edges_sd[['u', 'v', 'osmid', 'highway_1', 'width_final', 'length']].copy()

for f in tmrt_files:
    hour = os.path.basename(f).split('_')[3][:2]
    with rasterio.open(f) as src:
        affine = src.transform
        arr = src.read(1)
        arr = np.where((arr <= -100) | (arr >= 200), np.nan, arr)
    stats = zonal_stats(edges_sd['buffer_geom'], arr, affine=affine,
                        stats=['mean'], nodata=np.nan, all_touched=True)
    result[f'Tmrt_{hour}'] = [s['mean'] for s in stats]
    print(f"  {hour}시 완료 (결측 {sum(s['mean'] is None for s in stats)}개)")

out_gdf = gpd.GeoDataFrame(result, geometry=edges_sd.geometry, crs=TARGET_CRS)
out_path = os.path.join(OUT_DIR, '2026-07-09_link_tmrt_approach1_30m.gpkg')
out_gdf.to_file(out_path, driver='GPKG')
print(f"\n저장: {out_path}")

csv_path = os.path.join(OUT_DIR, '2026-07-09_link_tmrt_approach1_30m.csv')
result.drop(columns=[]).to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"저장: {csv_path}")
