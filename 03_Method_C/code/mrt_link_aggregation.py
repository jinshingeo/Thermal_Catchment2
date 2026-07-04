"""
작성일: 2026-07-03
버전: v3.0
근거논문:
  - Buo et al. (2026) Building and Environment 298:114622
    Supplementary Algorithm 1: sample_mrt_along_geometry 방식 (단순 평균)
  - Bröde et al. (2012) UTCI ≥42°C → MRT 역산 임계값 56°C

목적:
  파일럿과 동일한 보행 네트워크(seongdong_walk_network.graphml)에
  Method C (SOLWEIG 30m DSM) MRT를 링크별로 집계하고 Hard Cut 적용.
  → 파일럿(Method A) 결과와 동일 네트워크 위에서 직접 비교 가능.

변경(v3): ox.load_graphml → nx.read_graphml (osmnx 2.x 호환성 문제 우회)
"""
import os
import numpy as np
import pandas as pd
import networkx as nx
import rasterio
from rasterio.transform import rowcol
from pyproj import Transformer
from shapely.geometry import LineString

SCRATCH   = "/private/tmp/claude-501/-Users-jin------TAVI/11a7aa5d-485a-4d32-8032-faf31923985e/scratchpad"
MRT_TIF   = SCRATCH + "/umep_output_seongdong_v2/solweig_out/Tmrt_2025_206_1400D.tif"
NET_PATH  = "/Users/jin/석사논문/성동구_STP연구/01_네트워크/seongdong_walk_network.graphml"
OUT_DIR   = SCRATCH + "/link_mrt_seongdong"
os.makedirs(OUT_DIR, exist_ok=True)

MRT_THRESHOLD   = 56.0
SAMPLE_INTERVAL = 5.0

# ── 1. MRT 래스터
print("=== 1. MRT 래스터 로드 ===")
with rasterio.open(MRT_TIF) as src:
    mrt_data      = src.read(1).astype(np.float32)
    mrt_nodata    = src.nodata      # -9999.0
    mrt_transform = src.transform
    mrt_epsg = src.crs.to_epsg() or 32652  # SOLWEIG 출력 고정 EPSG:32652
print(f"  EPSG:{mrt_epsg}, 해상도: {abs(mrt_transform.a):.0f}m")
print(f"  MRT 유효 범위: {mrt_data[mrt_data != mrt_nodata].min():.1f} ~ "
      f"{mrt_data[mrt_data != mrt_nodata].max():.1f}°C")

# ── 2. 네트워크 (networkx 직접 읽기 — osmnx 2.x 다운로드 우회)
print("\n=== 2. 보행 네트워크 로드 ===")
G_raw = nx.read_graphml(NET_PATH)
# WGS84 → UTM52N 변환기
wgs2utm = Transformer.from_crs("EPSG:4326", f"EPSG:{mrt_epsg}", always_xy=True)
for nid, attrs in G_raw.nodes(data=True):
    lon, lat = float(attrs['x']), float(attrs['y'])
    ux, uy = wgs2utm.transform(lon, lat)
    attrs['x_utm'], attrs['y_utm'] = ux, uy
print(f"  노드: {G_raw.number_of_nodes():,}, 엣지: {G_raw.number_of_edges():,}")

# ── 3. MRT 집계
def sample_mrt(geom, interval=5.0):
    """Buo et al. (2026) Supp. Alg.1: 선분 interval 간격 샘플링 → 단순 평균"""
    length = geom.length
    if length == 0:
        return np.nan
    n = max(2, int(length / interval) + 1)
    vals = []
    for d in np.linspace(0, length, n):
        pt = geom.interpolate(d)
        row, col = rowcol(mrt_transform, pt.x, pt.y)
        r, c = int(row), int(col)
        if 0 <= r < mrt_data.shape[0] and 0 <= c < mrt_data.shape[1]:
            v = float(mrt_data[r, c])
            if v != mrt_nodata:
                vals.append(v)
    return float(np.mean(vals)) if vals else np.nan

print("\n=== 3. 링크별 MRT 집계 ===")
n_total = G_raw.number_of_edges()
records = []
for i, (u, v, data) in enumerate(G_raw.edges(data=True)):
    if i % 3000 == 0:
        print(f"  {i:,}/{n_total:,} ({i/n_total*100:.0f}%)")
    un  = G_raw.nodes[u]
    vn  = G_raw.nodes[v]
    geom = LineString([(un['x_utm'], un['y_utm']), (vn['x_utm'], vn['y_utm'])])
    t_e = sample_mrt(geom)
    records.append({'u': u, 'v': v, 'mrt': t_e,
                    'length': float(data.get('length', 0))})
print(f"  {n_total:,}/{n_total:,} (100%) — 완료")

# ── 4. 통계
df = pd.DataFrame(records)
valid = df.dropna(subset=['mrt'])
n_cut = (valid['mrt'] >= MRT_THRESHOLD).sum()
print(f"\n[링크 MRT 통계]")
print(f"  전체: {n_total:,} / 유효: {len(valid):,} ({len(valid)/n_total*100:.1f}%)")
print(f"  MRT {valid['mrt'].min():.1f} ~ {valid['mrt'].max():.1f}°C, "
      f"평균 {valid['mrt'].mean():.1f}°C")
print(f"  Hard Cut (≥{MRT_THRESHOLD}°C): {n_cut:,} ({n_cut/len(valid)*100:.1f}%)")

csv_path = OUT_DIR + '/link_mrt_method_c.csv'
df.to_csv(csv_path, index=False)
print(f"  CSV 저장: {csv_path}")

# ── 5. Hard Cut → GraphML 저장
print(f"\n=== 4. Hard Cut → GraphML 저장 ===")
hot_set = set()
for _, row in df.dropna(subset=['mrt']).iterrows():
    if row['mrt'] >= MRT_THRESHOLD:
        hot_set.add((row['u'], row['v']))
        hot_set.add((row['v'], row['u']))

G_thermal = G_raw.copy()
to_remove = [(u, v) for u, v in G_thermal.edges() if (u, v) in hot_set]
G_thermal.remove_edges_from(to_remove)
isolated = [n for n in G_thermal.nodes() if G_thermal.degree(n) == 0]
G_thermal.remove_nodes_from(isolated)

nx.write_graphml(G_raw,     OUT_DIR + '/graph_classic.graphml')
nx.write_graphml(G_thermal, OUT_DIR + '/graph_thermal_method_c.graphml')
print(f"  제거 링크: {len(to_remove):,} / {n_total:,} ({len(to_remove)/n_total*100:.1f}%)")
print(f"  잔여: 노드 {G_thermal.number_of_nodes():,}, 엣지 {G_thermal.number_of_edges():,}")
print(f"  저장 완료: {OUT_DIR}/")
print("\n=== 모든 단계 완료 ===")
