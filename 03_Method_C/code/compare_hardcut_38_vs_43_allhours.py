"""
Hard Cut 38°C vs 42.7°C — 전 시간대(06~19시) 비교
================================================
같은 출발점·같은 시간예산(15분)에서 Hard Cut 임계값을 38°C(현재 채택 기준)와
42.7°C(Monte Carlo 기반 위험임계값, 2026-07-29)로 각각 적용했을 때 도달 가능한
캐치먼트(TCA)가 얼마나 달라지는지 전 시간대에 걸쳐 비교.
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

FIG_DIR = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_hardcut_38_vs_43"
os.makedirs(FIG_DIR, exist_ok=True)
NET_PATH = "/Users/jin/석사논문/성동구_STP연구/01_네트워크/seongdong_walk_network.graphml"
UTCI_GPKG = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg"

WALK_SPEED = 4.5 * 1000 / 3600
TIME_BUDGET = 15 * 60
THR_A = 38.0     # 현재 채택 기준
THR_B = 42.7     # Monte Carlo 기반 위험임계값

HOURS = list(range(6, 20))          # 전 시간대(06~19시)
MAP_HOURS = HOURS                   # 전 시간대 지도 다 생성

TARGETS = {
    'eungbong': {'net_node': '7838649561', 'label': '응봉역 인근'},
    'sungsoo': {'net_node': '436855717', 'label': '성수역 인근'},
}

print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
wgs2wm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
for u, v, d in G.edges(data=True):
    d['travel_time'] = float(d.get('length', 0)) / WALK_SPEED

print("UTCI 링크 데이터 로드...")
utci_gdf = gpd.read_file(UTCI_GPKG)
utci_gdf['u'] = utci_gdf['u'].astype(str)
utci_gdf['v'] = utci_gdf['v'].astype(str)

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
    if col not in utci_gdf.columns:
        print(f"  {hour}시 컬럼 없음 — 스킵")
        continue
    print(f"\n===== {hour}시 =====")
    utci_lookup = {}
    for _, row in utci_gdf.dropna(subset=[col]).iterrows():
        u, v, val = row['u'], row['v'], row[col]
        utci_lookup[(u, v)] = val
        utci_lookup[(v, u)] = val

    for u, v, d in G.edges(data=True):
        d['utci'] = utci_lookup.get((u, v), np.nan)

    G_a = G.copy()  # 38도 기준
    remove_a = [(u, v) for u, v, d in G_a.edges(data=True)
                if not np.isnan(d['utci']) and d['utci'] >= THR_A]
    G_a.remove_edges_from(remove_a)

    G_b = G.copy()  # 42.7도 기준
    remove_b = [(u, v) for u, v, d in G_b.edges(data=True)
                if not np.isnan(d['utci']) and d['utci'] >= THR_B]
    G_b.remove_edges_from(remove_b)

    print(f"  38도 제거 엣지: {len(remove_a)}개 / 42.7도 제거 엣지: {len(remove_b)}개")

    for key, cfg in TARGETS.items():
        origin = cfg['net_node']
        if origin not in G:
            continue

        nodes_a = set(nx.single_source_dijkstra_path_length(
            G_a, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())
        nodes_b = set(nx.single_source_dijkstra_path_length(
            G_b, origin, cutoff=TIME_BUDGET, weight='travel_time').keys())

        extra_nodes = nodes_b - nodes_a
        pct_diff = (len(nodes_b) - len(nodes_a)) / max(len(nodes_a), 1) * 100
        print(f"  [{cfg['label']}] 38도={len(nodes_a)} / 42.7도={len(nodes_b)} "
              f"/ 차이={len(extra_nodes)} ({pct_diff:+.1f}%)")

        summary_rows.append({
            'station': cfg['label'], 'hour': hour,
            'nodes_38': len(nodes_a), 'nodes_42_7': len(nodes_b),
            'extra_nodes': len(extra_nodes), 'pct_diff': round(pct_diff, 1),
        })

        if hour in MAP_HOURS:
            def classify(row):
                u, v = row['u'], row['v']
                in_a = (u in nodes_a) and (v in nodes_a)
                in_b = (u in nodes_b) and (v in nodes_b)
                if in_a:
                    return 'both'
                elif in_b:
                    return 'b_only'
                else:
                    return 'outside'
            edges_gdf['etype'] = edges_gdf.apply(classify, axis=1)
            edges_gdf['utci_val'] = edges_gdf.apply(
                lambda r: utci_lookup.get((r['u'], r['v']), np.nan), axis=1)

            e_only = edges_gdf[edges_gdf['etype'] == 'b_only']
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
                            label='38·42.7도 공통 도달')
            if not e_only.empty:
                norm = Normalize(vmin=38, vmax=max(46, e_only['utci_val'].max()))
                e_only.plot(ax=ax, column='utci_val', cmap='inferno', norm=norm,
                            linewidth=2.2, alpha=0.95, zorder=4)
                sm = ScalarMappable(norm=norm, cmap='inferno')
                cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
                cbar.set_label('42.7도 기준에서만 도달 가능한 구간의 UTCI(°C)')

            ax.scatter([cx], [cy], c='#212121', s=90, zorder=6)
            ax.annotate(
                f"{cfg['label']} — {hour}시\n"
                f"38°C 기준: {len(nodes_a):,} nodes\n"
                f"42.7°C 기준: {len(nodes_b):,} nodes\n"
                f"차이: {len(extra_nodes):,} ({pct_diff:+.1f}%)",
                xy=(0.03, 0.97), xycoords='axes fraction', va='top', ha='left', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.88), zorder=7)
            ax.set_axis_off()
            plt.tight_layout(pad=0)
            out_path = os.path.join(FIG_DIR, f'2026-07-29_{key}_38vs42-7_{hour:02d}h.png')
            plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()
            print(f"    지도 저장: {out_path}")

summary_df = pd.DataFrame(summary_rows)
out_csv = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-29_hardcut_38vs42-7_allhours_summary.csv"
summary_df.to_csv(out_csv, index=False)
print(f"\n요약 저장: {out_csv}")

# 전 시간대 추이 그래프
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, (key, cfg) in zip(axes, TARGETS.items()):
    sub = summary_df[summary_df['station'] == cfg['label']].sort_values('hour')
    ax.plot(sub['hour'], sub['nodes_38'], marker='o', color='#D32F2F', label='Hard Cut 38°C')
    ax.plot(sub['hour'], sub['nodes_42_7'], marker='o', color='#1976D2', label='Hard Cut 42.7°C')
    ax.set_title(cfg['label'])
    ax.set_xlabel('시각')
    ax.set_ylabel('도달 가능 노드 수 (15분 예산)')
    ax.set_xticks(HOURS)
    ax.legend()
    ax.grid(alpha=0.3)
fig.suptitle('시간대별 Hard Cut 38°C vs 42.7°C 도달범위 비교')
plt.tight_layout()
trend_path = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/compare_hardcut_38_vs_43/2026-07-29_allhours_trend.png"
plt.savefig(trend_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f"추이 그래프 저장: {trend_path}")
