"""
Hard Cut(이진적 제거) vs 연속형 페널티 — 실제 캐치먼트(TCA) 모양 비교
================================================================
같은 출발점·같은 시간예산(15분)에서 (a) UTCI>=38 링크를 완전히 제거하는
Hard Cut 방식과 (b) 링크 제거 없이 UTCI에 비례해 통과비용만 늘리는 연속형
페널티 방식을 비교. 연속형 방식이 매우 더운 링크를 "통과 가능"으로 처리해
비논리적으로 도달범위를 넓히는지 확인.
"""
import os
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from pyproj import Transformer
from shapely.geometry import LineString, Point
warnings.filterwarnings('ignore')

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

FIG_DIR = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_hardcut_vs_continuous_catchment"
os.makedirs(FIG_DIR, exist_ok=True)
NET_PATH = "/Users/jin/석사논문/성동구_STP연구/01_네트워크/seongdong_walk_network.graphml"
UTCI_GPKG = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-28_link_tmrt_utci_seongdong_1mtrue.gpkg"

WALK_SPEED = 4.5 * 1000 / 3600
TIME_BUDGET = 15 * 60
HARDCUT_THR = 38.0
COMFORT_T = 26.0
PENALTY_SCALE = 12.0  # UTCI 38(=comfort+12)에서 비용 2배가 되도록

HOURS = [13, 7]  # 낮 시간대 우선, 아침 대비

TARGETS = {
    'eungbong': {'net_node': '7838649561', 'label': '응봉역 인근'},
    'sungsoo': {'net_node': '436855717', 'label': '성수역 인근'},
}

print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
wgs2wm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
for u, v, d in G.edges(data=True):
    d['travel_time'] = float(d.get('length', 0)) / WALK_SPEED
    d['length_m'] = float(d.get('length', 0))

print("UTCI 링크 데이터 로드...")
utci_gdf = gpd.read_file(UTCI_GPKG)
utci_gdf['u'] = utci_gdf['u'].astype(str)
utci_gdf['v'] = utci_gdf['v'].astype(str)

edges_gdf_wgs = []
node_rows = []
for nid, attrs in G.nodes(data=True):
    nx_, ny_ = wgs2wm.transform(float(attrs['x']), float(attrs['y']))
    node_rows.append({'nid': nid, 'geometry': Point(nx_, ny_)})
nodes_gdf = gpd.GeoDataFrame(node_rows, crs="EPSG:3857").set_index('nid')

edge_rows = []
for u, v, d in G.edges(data=True):
    un, vn = G.nodes[u], G.nodes[v]
    ux, uy = wgs2wm.transform(float(un['x']), float(un['y']))
    vx, vy = wgs2wm.transform(float(vn['x']), float(vn['y']))
    edge_rows.append({'u': u, 'v': v, 'geometry': LineString([(ux, uy), (vx, vy)])})
edges_gdf = gpd.GeoDataFrame(edge_rows, crs="EPSG:3857")

summary_rows = []

for hour in HOURS:
    col = f'UTCI_{hour:02d}'
    print(f"\n===== {hour}시 =====")
    utci_lookup = {}
    for _, row in utci_gdf.dropna(subset=[col]).iterrows():
        u, v, val = row['u'], row['v'], row[col]
        utci_lookup[(u, v)] = val
        utci_lookup[(v, u)] = val

    matched = 0
    for u, v, d in G.edges(data=True):
        val = utci_lookup.get((u, v))
        if val is not None:
            d['utci'] = val
            matched += 1
        else:
            d['utci'] = np.nan
    print(f"  UTCI 매칭된 엣지: {matched}/{G.number_of_edges()}")

    # Hard Cut 네트워크: UTCI>=38 엣지 제거
    G_hardcut = G.copy()
    remove = [(u, v) for u, v, d in G_hardcut.edges(data=True)
              if not np.isnan(d['utci']) and d['utci'] >= HARDCUT_THR]
    G_hardcut.remove_edges_from(remove)
    print(f"  Hard Cut 제거 엣지: {len(remove)}개")

    # 연속형 네트워크: 비용만 증가, 제거 없음
    G_cont = G.copy()
    for u, v, d in G_cont.edges(data=True):
        utci_val = d['utci']
        if np.isnan(utci_val):
            d['travel_time_penalty'] = d['travel_time']
        else:
            factor = 1.0 + max(0.0, utci_val - COMFORT_T) / PENALTY_SCALE
            d['travel_time_penalty'] = d['travel_time'] * factor

    for key, cfg in TARGETS.items():
        origin = cfg['net_node']
        if origin not in G:
            print(f"  [경고] {cfg['label']} 노드({origin})가 그래프에 없음 — 스킵")
            continue

        hardcut_nodes = set(nx.single_source_dijkstra_path_length(
            G_hardcut, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())
        cont_nodes = set(nx.single_source_dijkstra_path_length(
            G_cont, origin, cutoff=TIME_BUDGET, weight='travel_time_penalty').keys())

        extra_nodes = cont_nodes - hardcut_nodes
        print(f"  [{cfg['label']}] HardCut={len(hardcut_nodes)} / 연속형={len(cont_nodes)} "
              f"/ 연속형만 추가 도달={len(extra_nodes)}")

        def classify(row):
            u, v = row['u'], row['v']
            in_hc = (u in hardcut_nodes) and (v in hardcut_nodes)
            in_ct = (u in cont_nodes) and (v in cont_nodes)
            if in_hc:
                return 'both'
            elif in_ct:
                return 'continuous_only'
            else:
                return 'outside'

        edges_gdf['etype'] = edges_gdf.apply(classify, axis=1)
        edges_gdf['utci_val'] = edges_gdf.apply(
            lambda r: utci_lookup.get((r['u'], r['v']), np.nan), axis=1)

        e_only = edges_gdf[edges_gdf['etype'] == 'continuous_only']
        n_hot_only = (e_only['utci_val'] >= HARDCUT_THR).sum()
        pct_hot_only = n_hot_only / max(len(e_only), 1) * 100
        print(f"    연속형만 도달 가능 구간 중 UTCI>=38 비율: {pct_hot_only:.1f}% "
              f"({n_hot_only}/{len(e_only)})")

        ox_node = nodes_gdf.loc[origin]
        cx, cy = ox_node.geometry.x, ox_node.geometry.y
        PAD = 1600
        fig, ax = plt.subplots(figsize=(9, 9), dpi=150)
        ax.set_xlim(cx - PAD, cx + PAD)
        ax.set_ylim(cy - PAD, cy + PAD)
        try:
            ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=15, alpha=0.6)
        except Exception as e:
            print(f"    베이스맵 오류(무시): {e}")

        e_both = edges_gdf[edges_gdf['etype'] == 'both']
        if not e_both.empty:
            e_both.plot(ax=ax, color='#43A047', linewidth=1.6, alpha=0.85, zorder=3,
                        label='Hard Cut·연속형 공통 도달')

        if not e_only.empty:
            norm = Normalize(vmin=26, vmax=max(46, e_only['utci_val'].max()))
            e_only.plot(ax=ax, column='utci_val', cmap='inferno', norm=norm,
                        linewidth=2.2, alpha=0.95, zorder=4)
            sm = ScalarMappable(norm=norm, cmap='inferno')
            cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
            cbar.set_label('연속형만 도달 구간의 UTCI(°C)')

        ax.scatter([cx], [cy], c='#212121', s=90, zorder=6)
        ax.annotate(
            f"{cfg['label']} — {hour}시\n"
            f"Hard Cut: {len(hardcut_nodes):,} nodes\n"
            f"연속형: {len(cont_nodes):,} nodes\n"
            f"연속형만 추가 도달: {len(extra_nodes):,}\n"
            f"그중 UTCI≥38 비율: {pct_hot_only:.1f}%",
            xy=(0.03, 0.97), xycoords='axes fraction', va='top', ha='left', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.88), zorder=7)
        ax.set_axis_off()
        plt.tight_layout(pad=0)
        out_path = os.path.join(FIG_DIR, f'2026-07-29_{key}_catchment_hardcut_vs_continuous_{hour:02d}h.png')
        plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"    저장: {out_path}")

        summary_rows.append({
            'station': cfg['label'], 'hour': hour,
            'hardcut_nodes': len(hardcut_nodes), 'continuous_nodes': len(cont_nodes),
            'extra_nodes_continuous_only': len(extra_nodes),
            'continuous_only_edges': len(e_only),
            'continuous_only_edges_hot_pct': round(pct_hot_only, 1),
        })

out_csv = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-29_hardcut_vs_continuous_catchment_summary.csv"
pd.DataFrame(summary_rows).to_csv(out_csv, index=False)
print(f"\n요약 저장: {out_csv}")
print(pd.DataFrame(summary_rows))
