"""
작성일: 2026-07-03
버전: v1.0
목적: 서울 전체 보행 네트워크에 Method C (SOLWEIG 30m DSM) MRT 집계 + Hard Cut

사전 필요:
  1. 서울 전체 보행 네트워크 GraphML: data/seoul_walk_network.graphml
     (없으면 아래 download_seoul_network.py 먼저 실행)
  2. 서울 전체 SOLWEIG MRT 래스터: data/Tmrt_Seoul_2025_206_1400D.tif
     (없으면 QGIS UMEP SOLWEIG를 서울 전체 범위로 실행)

출력:
  results/YYYY-MM-DD_link_mrt_seoul_method_c.csv
  results/YYYY-MM-DD_graph_seoul_classic.graphml
  results/YYYY-MM-DD_graph_seoul_thermal_method_c.graphml
"""
import os
from datetime import date
import numpy as np
import pandas as pd
import networkx as nx
import rasterio
from rasterio.transform import rowcol
from pyproj import Transformer
from shapely.geometry import LineString

TODAY     = date.today().strftime('%Y-%m-%d')
BASE      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(BASE, 'data')
RES_DIR   = os.path.join(BASE, 'results')
os.makedirs(RES_DIR, exist_ok=True)

MRT_TIF      = os.path.join(DATA_DIR, 'Tmrt_Seoul_2025_206_1400D.tif')
NET_PATH     = os.path.join(DATA_DIR, 'seoul_walk_network.graphml')
OUT_CSV      = os.path.join(RES_DIR, f'{TODAY}_link_mrt_seoul_method_c.csv')
OUT_CLASSIC  = os.path.join(RES_DIR, f'{TODAY}_graph_seoul_classic.graphml')
OUT_THERMAL  = os.path.join(RES_DIR, f'{TODAY}_graph_seoul_thermal_method_c.graphml')

MRT_THRESHOLD   = 56.0
SAMPLE_INTERVAL = 5.0
LOG_INTERVAL    = 10000

def run():
    # ── 1. MRT 래스터
    print("=== 1. MRT 래스터 ===")
    if not os.path.exists(MRT_TIF):
        raise FileNotFoundError(f"MRT 래스터 없음: {MRT_TIF}\n"
                                "QGIS UMEP SOLWEIG를 서울 전체 범위로 먼저 실행하세요.")
    with rasterio.open(MRT_TIF) as src:
        mrt_data      = src.read(1).astype(np.float32)
        mrt_nodata    = src.nodata
        mrt_transform = src.transform
        mrt_epsg      = src.crs.to_epsg()
    print(f"  EPSG:{mrt_epsg}, 해상도 {abs(mrt_transform.a):.0f}m")

    # ── 2. 네트워크
    print("\n=== 2. 서울 보행 네트워크 ===")
    if not os.path.exists(NET_PATH):
        raise FileNotFoundError(f"네트워크 없음: {NET_PATH}\n"
                                "download_seoul_network.py 먼저 실행하세요.")
    G = nx.read_graphml(NET_PATH)
    wgs2utm = Transformer.from_crs("EPSG:4326", f"EPSG:{mrt_epsg}", always_xy=True)
    for nid, attrs in G.nodes(data=True):
        x, y = wgs2utm.transform(float(attrs['x']), float(attrs['y']))
        attrs['x_utm'], attrs['y_utm'] = x, y
    n_total = G.number_of_edges()
    print(f"  노드: {G.number_of_nodes():,}, 엣지: {n_total:,}")

    # ── 3. MRT 집계
    def sample_mrt(u_attrs, v_attrs):
        geom = LineString([(u_attrs['x_utm'], u_attrs['y_utm']),
                           (v_attrs['x_utm'], v_attrs['y_utm'])])
        length = geom.length
        if length == 0:
            return np.nan
        n = max(2, int(length / SAMPLE_INTERVAL) + 1)
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
    records = []
    for i, (u, v, data) in enumerate(G.edges(data=True)):
        if i % LOG_INTERVAL == 0:
            print(f"  {i:,}/{n_total:,} ({i/n_total*100:.1f}%)")
        t_e = sample_mrt(G.nodes[u], G.nodes[v])
        records.append({'u': u, 'v': v,
                        'mrt': t_e, 'length': float(data.get('length', 0))})

    df = pd.DataFrame(records)
    valid = df.dropna(subset=['mrt'])
    n_cut = (valid['mrt'] >= MRT_THRESHOLD).sum()
    print(f"\n[통계]")
    print(f"  유효 링크: {len(valid):,} / {n_total:,}")
    print(f"  MRT {valid['mrt'].min():.1f}~{valid['mrt'].max():.1f}°C, "
          f"평균 {valid['mrt'].mean():.1f}°C")
    print(f"  Hard Cut ≥{MRT_THRESHOLD}°C: {n_cut:,} ({n_cut/len(valid)*100:.1f}%)")
    df.to_csv(OUT_CSV, index=False)
    print(f"  CSV: {OUT_CSV}")

    # ── 4. Hard Cut
    print("\n=== 4. Hard Cut → GraphML ===")
    hot = set()
    for _, row in df.dropna(subset=['mrt']).iterrows():
        if row['mrt'] >= MRT_THRESHOLD:
            hot.add((row['u'], row['v']))
            hot.add((row['v'], row['u']))
    G_thermal = G.copy()
    rem = [(u, v) for u, v in G_thermal.edges() if (u, v) in hot]
    G_thermal.remove_edges_from(rem)
    G_thermal.remove_nodes_from([n for n in G_thermal.nodes()
                                  if G_thermal.degree(n) == 0])
    nx.write_graphml(G,         OUT_CLASSIC)
    nx.write_graphml(G_thermal, OUT_THERMAL)
    print(f"  제거: {len(rem):,} / 잔여: {G_thermal.number_of_edges():,}")
    print(f"  Classic : {OUT_CLASSIC}")
    print(f"  Thermal : {OUT_THERMAL}")
    print("\n=== 완료 ===")

if __name__ == '__main__':
    run()
