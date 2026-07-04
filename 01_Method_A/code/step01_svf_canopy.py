"""
Method A — Step 1: 링크별 SVF(Sky View Factor) 및 수목 캐노피 비율 산출
==========================================================================
작성일: 2026-07-04 | 연구: Thermal Catchment Area (파일럿: 성동구)

【방법론 요약】
Oke(1987)의 도시 협곡(Street Canyon) H/W 공식으로 링크별 SVF를 산출한다.
  SVF = 1 / √(1 + (H_eff / W)²)

  H_eff = 링크 버퍼 20m 내 건물 평균 높이 (층수 × 3m)
          + 수목 높이 보정 (TREE_HEIGHT × canopy_ratio)
  W     = 도로 유형(OSM highway 태그)별 표준 폭 (국토부 도로설계기준)

수목 캐노피 비율:
  링크 버퍼 15m 내 도시숲(면) 폴리곤 면적 / 버퍼 면적

【입력 데이터】
  - 보행 네트워크: seongdong_walk_network.graphml (EPSG:4326)
  - 건물 SHP: 도로명주소 건물 (국토교통부, 2026년 3월)
  - 도시숲 SHP: 서울시 도시숲 전체 면 데이터 (중분류)

【출력】
  - link_svf_canopy.csv: 링크별 SVF, 건물 평균 높이, 도로 폭, H/W 비율, 캐노피 비율

【참고문헌】
  Oke, T.R. (1987). Boundary Layer Climates (2nd ed.). Routledge.
  Lindberg, F. et al. (UMEP TreePlanter Tutorial) — 수목 높이 10m 기본값.
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import osmnx as ox
from shapely.geometry import Point

# ── 경로 설정 ────────────────────────────────────────────────────────────────
STP_BASE   = '/Users/jin/석사논문/성동구_STP연구'
NET_PATH   = os.path.join(STP_BASE, '01_네트워크/seongdong_walk_network.graphml')
GREEN_PATH = '/Users/jin/Green_Space_2SFCA/코드/data/도시숲전체_면_서울_최종_중분류.shp'
BULD_PATH  = '/Users/jin/석사논문/TAVI/03_건물데이터/(도로명주소)건물_서울/TL_SPBD_BULD_11_202603.shp'
OUT_PATH   = 'results/link_svf_canopy.csv'

# ── 하이퍼파라미터 ──────────────────────────────────────────────────────────
BULD_BUFFER   = 20    # m — SVF 계산용 건물 탐색 반경 (링크 중심에서 양측 20m)
CANOPY_BUFFER = 15    # m — 수목 캐노피 측정 버퍼 반경
TREE_HEIGHT   = 10.0  # m — 수목 캐노피 높이 가정 (UMEP TreePlanter Tutorial)
FLOOR_HEIGHT  = 3.0   # m/층 — 건물 층당 높이 (국내 표준)

# 도로 유형별 표준 폭 (m) — 양방향 차로 포함 전체 노면폭
# 근거: 국토교통부 도로설계기준 및 OSM 실측 통계
WIDTH_BY_HIGHWAY = {
    'trunk': 24.0, 'trunk_link': 10.0,
    'primary': 16.0, 'primary_link': 8.0,
    'secondary': 12.0, 'secondary_link': 6.0,
    'tertiary': 9.0, 'tertiary_link': 6.0,
    'residential': 6.0, 'living_street': 5.0,
    'service': 5.0, 'footway': 3.0,
    'pedestrian': 4.0, 'path': 2.0,
    'steps': 2.0, 'corridor': 3.0,
    'unclassified': 6.0,
}
DEFAULT_WIDTH = 6.0


def get_width(highway_val):
    """OSM highway 태그 → 도로 폭 반환"""
    if isinstance(highway_val, list):
        highway_val = highway_val[0]
    if isinstance(highway_val, str) and highway_val.startswith('['):
        import ast
        try:
            vals = ast.literal_eval(highway_val)
            highway_val = vals[0] if vals else 'unclassified'
        except Exception:
            highway_val = 'unclassified'
    return WIDTH_BY_HIGHWAY.get(str(highway_val).strip(), DEFAULT_WIDTH)


# ── 데이터 로드 ─────────────────────────────────────────────────────────────
print("보행 네트워크 로드...")
G = ox.load_graphml(NET_PATH)
G = G.to_undirected()
_, edges_gdf = ox.graph_to_gdfs(G)
# EPSG:5186(Korea 중부원점)으로 변환 — 미터 단위 거리 계산 필요
edges_utm = edges_gdf.to_crs('EPSG:5186').copy()
print(f"  링크 수: {len(edges_utm):,}")

print("건물 데이터 로드...")
buld_raw = gpd.read_file(BULD_PATH)
# 성동구 SIG_CD = '11200'
buld = buld_raw[buld_raw['SIG_CD'] == '11200'][['GRO_FLO_CO', 'geometry']].copy()
buld['height_m'] = buld['GRO_FLO_CO'].clip(lower=1) * FLOOR_HEIGHT
buld = buld.to_crs('EPSG:5186')
buld['geometry'] = buld.geometry.buffer(0)   # 위상 오류 수정
buld = buld[buld.geometry.is_valid].copy().reset_index(drop=True)
buld_sindex = buld.sindex
print(f"  성동구 건물: {len(buld):,}개")

print("도시숲 데이터 로드...")
green_raw = gpd.read_file(GREEN_PATH)
# 성동구 부근만 clipping (성능 최적화)
bbox_gdf = gpd.GeoDataFrame(
    geometry=[Point(127.015, 37.535), Point(127.065, 37.565)], crs='EPSG:4326'
).to_crs('EPSG:5186')
xmin, ymin = bbox_gdf.geometry[0].x, bbox_gdf.geometry[0].y
xmax, ymax = bbox_gdf.geometry[1].x, bbox_gdf.geometry[1].y
street_trees = green_raw.cx[xmin:xmax, ymin:ymax].copy().reset_index(drop=True)
tree_sindex = street_trees.sindex
print(f"  성동구 도시숲: {len(street_trees):,}개")


# ── SVF 계산 함수 (Oke 1987) ─────────────────────────────────────────────────
def calc_svf_hw(link_geom, highway_val, canopy_ratio=0.0):
    """
    Oke(1987) H/W street canyon 공식으로 SVF 계산.
    H_eff = 건물 평균 높이 + TREE_HEIGHT × canopy_ratio (수목 차폐 보정)
    건물·수목 모두 없으면 SVF=1.0 (완전 개활지).
    """
    W = get_width(highway_val)
    buf = link_geom.buffer(BULD_BUFFER)

    cands_idx = list(buld_sindex.intersection(buf.bounds))
    if not cands_idx:
        H_bld = 0.0
    else:
        cands = buld.iloc[cands_idx]
        cands = cands[cands.geometry.intersects(buf)]
        H_bld = float(cands['height_m'].mean()) if len(cands) > 0 else 0.0

    H_eff = H_bld + TREE_HEIGHT * canopy_ratio
    if H_eff == 0.0:
        return 1.0, round(H_bld, 1), W

    svf = 1.0 / np.sqrt(1.0 + (H_eff / W) ** 2)
    return round(svf, 4), round(H_bld, 1), W


def calc_canopy_ratio(link_geom):
    """링크 버퍼 15m 내 수목 캐노피 면적 비율 (0~1)"""
    buf = link_geom.buffer(CANOPY_BUFFER)
    cands_idx = list(tree_sindex.intersection(buf.bounds))
    if not cands_idx:
        return 0.0
    cands = street_trees.iloc[cands_idx]
    cands = cands[cands.geometry.intersects(buf)]
    if len(cands) == 0:
        return 0.0
    clipped_area = cands.geometry.intersection(buf).area.sum()
    return round(float(clipped_area / buf.area), 4)


# ── 전체 링크 처리 ───────────────────────────────────────────────────────────
print(f"\n링크별 SVF + 캐노피 계산 ({len(edges_utm):,}개)...")
rows = []
for i, (idx, row) in enumerate(edges_utm.iterrows()):
    if i % 1000 == 0:
        print(f"  {i:,}/{len(edges_utm):,} ({i/len(edges_utm)*100:.0f}%)")

    u, v   = idx[0], idx[1]
    hw     = row.get('highway', 'unclassified')
    canopy = calc_canopy_ratio(row.geometry)
    svf, H, W = calc_svf_hw(row.geometry, hw, canopy_ratio=canopy)

    rows.append({
        'u': u, 'v': v,
        'svf': svf,
        'mean_bld_H': H,   # 링크 주변 건물 평균 높이 (m)
        'road_W': W,        # 도로 폭 (m)
        'HW_ratio': round(H / W, 3) if W > 0 else 0,
        'canopy_ratio': canopy,
        'highway': hw,
    })

df_out = pd.DataFrame(rows)
os.makedirs('results', exist_ok=True)
df_out.to_csv(OUT_PATH, index=False, encoding='utf-8-sig')

print(f"\n=== 결과 요약 ===")
print(f"저장: {OUT_PATH}")
print(f"SVF 분포: min={df_out['svf'].min():.3f}, mean={df_out['svf'].mean():.3f}, max={df_out['svf'].max():.3f}")
print(f"캐노피>0 링크: {(df_out['canopy_ratio']>0).sum():,}개 ({(df_out['canopy_ratio']>0).mean()*100:.1f}%)")
