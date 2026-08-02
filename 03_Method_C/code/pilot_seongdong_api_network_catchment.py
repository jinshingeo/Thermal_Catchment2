"""
성동구 파일럿 — 서울시 도보 네트워크 API(TbTraficWlkNet)로 접근성 재현
================================================================
작성일: 2026-08-02
목적: OSM 네트워크 대신 서울시 도보 네트워크 API로 Hard Cut 접근성(Classic vs
      Thermal)을 재현해보고, 기존 OSM 기반 결과와 비교.
방식: Tmrt/UTCI는 재계산하지 않음 — 이미 OSM 링크 단위로 계산된 값
      (2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg)을 API 링크마다 최근접
      OSM 링크에서 그대로 상속(nearest spatial join). 폭/버퍼 문제 우회.
근거: WALK_SPEED=4.0km/h(Bröde et al. 2012), THRESHOLDS=[38.0, 42.4]°C —
      seoul_wide_jibgyegu_contour.py와 동일 파라미터
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
import warnings
warnings.filterwarnings('ignore')

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
API_NET = os.path.join(PROJ, 'data/network/2026-08-02_seoul_walk_api_network.gpkg')
OSM_RESULT = os.path.join(PROJ, '03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg')
STATIONS = os.path.join(PROJ, 'data/facilities/seoul_subway_stations.gpkg')
OUT_DIR = os.path.join(PROJ, '03_Method_C/results')

TARGET_CRS = 'EPSG:5186'
WALK_SPEED = 4.0 * 1000 / 3600
TIME_BUDGET = 15 * 60
THRESHOLDS = [38.0, 42.4]
HOURS = [f'{h:02d}' for h in range(6, 20)]

# ── 1. API 네트워크 — 성동구 보행 링크만 ────────────────────────────────────
print("API 네트워크 로드...")
api = gpd.read_file(API_NET)
api_sd = api[(api['SGG_NM'] == '성동구') & (api['LNKG_TYPE_CD'].str.startswith('1'))].copy()
api_sd = api_sd.to_crs(TARGET_CRS)
api_sd['LNKG_LEN'] = api_sd['LNKG_LEN'].astype(float)
print(f"  성동구 보행 링크: {len(api_sd):,}개")

# ── 2. OSM 기반 Tmrt/UTCI 결과 — 성동구 클립 ────────────────────────────────
print("OSM 기반 링크 Tmrt/UTCI 결과 로드...")
osm_bounds = api_sd.total_bounds
osm = gpd.read_file(OSM_RESULT, bbox=tuple(osm_bounds))
print(f"  OSM 결과 링크(bbox): {len(osm):,}개")

# ── 3. 최근접 매칭 — API 링크 중심점 기준 OSM 링크에서 값 상속 ──────────────
print("최근접 매칭(Tmrt/UTCI 값 상속)...")
api_sd['centroid'] = api_sd.geometry.centroid
api_pts = gpd.GeoDataFrame(api_sd[['LNKG_ID']], geometry=api_sd['centroid'], crs=TARGET_CRS)
value_cols = [c for c in osm.columns if c.startswith('Tmrt_') or c.startswith('UTCI_')]
joined = gpd.sjoin_nearest(api_pts, osm[value_cols + ['geometry']], how='left', distance_col='dist_m')
joined = joined.drop_duplicates(subset='LNKG_ID')
print(f"  평균 매칭 거리: {joined['dist_m'].mean():.1f}m / 최대: {joined['dist_m'].max():.1f}m")

api_sd = api_sd.merge(joined[['LNKG_ID', 'dist_m'] + value_cols], on='LNKG_ID', how='left')
api_sd = api_sd.drop(columns='centroid')

# ── 4. 그래프 구성 (API 네트워크 자체 위상) ─────────────────────────────────
print("그래프 구성...")
G = nx.Graph()
for _, row in api_sd.iterrows():
    u, v = row['BGNG_LNKG_ID'], row['END_LNKG_ID']
    G.add_edge(u, v, LNKG_ID=row['LNKG_ID'], length=row['LNKG_LEN'],
               travel_time=row['LNKG_LEN'] / WALK_SPEED,
               **{c: row[c] for c in value_cols})
print(f"  노드: {G.number_of_nodes():,} / 엣지: {G.number_of_edges():,}")

# 노드 좌표 (양끝 API 링크 지오메트리에서 추출)
node_xy = {}
for _, row in api_sd.iterrows():
    coords = list(row.geometry.coords)
    node_xy[row['BGNG_LNKG_ID']] = coords[0]
    node_xy[row['END_LNKG_ID']] = coords[-1]

# ── 5. 정류장 위치 → 최근접 노드 스냅 ───────────────────────────────────────
stations = gpd.read_file(STATIONS).to_crs(TARGET_CRS)
targets = {}
for key, name in [('eungbong', '응봉'), ('sungsoo', '성수')]:
    pt = stations[stations['name'] == name].geometry.iloc[0]
    best_node, best_d = None, 1e18
    for nid, (x, y) in node_xy.items():
        d = (x - pt.x) ** 2 + (y - pt.y) ** 2
        if d < best_d:
            best_d, best_node = d, nid
    targets[key] = {'node': best_node, 'label': f'{name}역 인근', 'dist': best_d ** 0.5}
    print(f"  {name}역 → 노드 {best_node} (거리 {best_d**0.5:.0f}m)")

# ── 6. Hard Cut 접근성 계산 + 시각화 ────────────────────────────────────────
def compute_catchment(G, origin, hot_edges):
    classic = set(nx.single_source_dijkstra_path_length(
        G, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())
    G_th = G.copy()
    remove = [(u, v) for u, v, d in G_th.edges(data=True) if (u, v) in hot_edges or (v, u) in hot_edges]
    G_th.remove_edges_from(remove)
    thermal = set(nx.single_source_dijkstra_path_length(
        G_th, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())
    return classic, thermal

results = []
for threshold in THRESHOLDS:
    for hour in HOURS:
        utci_col = f'UTCI_{hour}'
        hot_edges = {(u, v) for u, v, d in G.edges(data=True)
                     if pd.notna(d.get(utci_col)) and d[utci_col] >= threshold}
        for key, cfg in targets.items():
            classic, thermal = compute_catchment(G, cfg['node'], hot_edges)
            reduction = (len(classic) - len(thermal)) / max(len(classic), 1) * 100
            results.append({'station': cfg['label'], 'threshold': threshold, 'hour': hour,
                             'classic_nodes': len(classic), 'thermal_nodes': len(thermal),
                             'reduction_pct': round(reduction, 1)})
            print(f"  [{cfg['label']}] threshold={threshold} hour={hour}: "
                  f"{len(classic)}→{len(thermal)} (감소율 {reduction:.1f}%)")

res_df = pd.DataFrame(results)
res_csv = os.path.join(OUT_DIR, '2026-08-02_pilot_seongdong_api_network_catchment.csv')
res_df.to_csv(res_csv, index=False, encoding='utf-8-sig')
print(f"\n저장: {res_csv}")

# ── 7. 시각화 (14시, threshold=38 기준 예시) ────────────────────────────────
edge_rows = []
for u, v, d in G.edges(data=True):
    ux, uy = node_xy[u]
    vx, vy = node_xy[v]
    edge_rows.append({'u': u, 'v': v, 'UTCI_14': d.get('UTCI_14'),
                       'geometry': gpd.points_from_xy([ux], [uy])[0].buffer(0).union(
                           gpd.points_from_xy([vx], [vy])[0].buffer(0))})
from shapely.geometry import LineString
edge_rows = []
for u, v, d in G.edges(data=True):
    ux, uy = node_xy[u]
    vx, vy = node_xy[v]
    edge_rows.append({'u': u, 'v': v, 'UTCI_14': d.get('UTCI_14'),
                       'geometry': LineString([(ux, uy), (vx, vy)])})
edges_gdf = gpd.GeoDataFrame(edge_rows, crs=TARGET_CRS).to_crs(3857)

hot_edges_14_38 = {(u, v) for u, v, d in G.edges(data=True)
                    if pd.notna(d.get('UTCI_14')) and d['UTCI_14'] >= 38.0}

for key, cfg in targets.items():
    classic, thermal = compute_catchment(G, cfg['node'], hot_edges_14_38)
    lost = classic - thermal

    def classify(row):
        u, v = row['u'], row['v']
        if u in thermal and v in thermal:
            return 'thermal'
        elif u in classic and v in classic:
            return 'lost'
        return 'outside'
    edges_gdf['etype'] = edges_gdf.apply(classify, axis=1)

    ox_, oy_ = node_xy[cfg['node']]
    import pyproj
    transformer = pyproj.Transformer.from_crs(TARGET_CRS, 3857, always_xy=True)
    cx, cy = transformer.transform(ox_, oy_)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    PAD = 1600
    ax.set_xlim(cx - PAD, cx + PAD)
    ax.set_ylim(cy - PAD, cy + PAD)
    try:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=15, alpha=0.65)
    except Exception as e:
        print(f"  베이스맵 오류(무시): {e}")

    e_lost = edges_gdf[edges_gdf['etype'] == 'lost']
    e_thermal = edges_gdf[edges_gdf['etype'] == 'thermal']
    if not e_lost.empty:
        e_lost.plot(ax=ax, color='#E53935', linewidth=1.6, alpha=0.9, zorder=4)
    if not e_thermal.empty:
        e_thermal.plot(ax=ax, color='#43A047', linewidth=1.6, alpha=0.9, zorder=3)
    ax.scatter([cx], [cy], c='#212121', s=80, zorder=6)
    reduction = len(lost) / max(len(classic), 1) * 100
    ax.annotate(
        f"{cfg['label']} (API 네트워크)\n14시, UTCI≥38°C\n"
        f"Classic: {len(classic):,} / Thermal: {len(thermal):,}\n감소율: {reduction:.1f}%",
        xy=(0.03, 0.97), xycoords='axes fraction', va='top', ha='left', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.85), zorder=7)
    ax.set_axis_off()
    plt.tight_layout(pad=0)
    out_png = os.path.join(OUT_DIR, f'figures/2026-08-02_catchment_api_network_{key}.png')
    plt.savefig(out_png, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"저장: {out_png}")

print("\n=== 완료 ===")
