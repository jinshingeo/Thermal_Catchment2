"""
Method A — Step 3: Thermal Catchment Area (TCA) 산출 및 시각화
=================================================================
작성일: 2026-07-04 | 연구: Thermal Catchment Area (파일럿: 성동구)

【방법론 요약】
Hard Cut 방식으로 보행 네트워크에서 열노출 초과 링크를 제거하고,
15분 도달 가능 범위(Thermal Catchment Area)를 산출한다.

  Hard Cut 조건: UTCI_corrected ≥ THRESHOLD (38°C)
    → UTCI 38°C = Very Strong Heat Stress 하한 (Bröde et al. 2012)
    → 해당 링크를 네트워크에서 완전 제거 (페널티 방식 아님)

  Classic Catchment: 전체 네트워크, 단순 이동시간 기반
  Thermal Catchment: 열노출 초과 링크 제거 후 네트워크, 동일 시간예산

  [검증 지표] = (Classic − Thermal) / Classic × 100 (%)

【핵심 파라미터 (확정)】
  WALK_SPEED  = 4.5 km/h (=1.25 m/s)
  TIME_BUDGET = 15분 (=900초, ≈1,125m)
  THRESHOLD   = 38.0°C (UTCI) — Bröde et al. (2012)

【입력 데이터】
  - seongdong_walk_network.graphml : 성동구 보행 네트워크 (osmnx)
  - link_utci_corrected.csv        : Step 2 산출 링크별 보정 UTCI

【출력】
  - results/figures/catchment_contrast_{station}_h{hour}.png : 역별 비교 지도
  - results/catchment_summary.json : 감소율 요약

【참고문헌】
  Bröde, P. et al. (2012). Deriving the operational procedure for the
    Universal Thermal Climate Index (UTCI). International Journal of
    Biometeorology, 56(3), 481-494.
    — UTCI 38°C = Very Strong Heat Stress 하한 (Table 3, p.489)

  Geurs, K.T. & van Wee, B. (2004). Accessibility evaluation of land-use
    and transport strategies: review and research directions. Journal of
    Transport Geography, 12(2), 127-140.
    — contour measure 접근성 이론 위치

  Buo, I. et al. (2026). Mapping pedestrian thermal comfort using
    SOLWEIG and Dijkstra routing. Building and Environment, 298, 114622.
    — 링크 단위 MRT 기반 네트워크 분석 방법론 선례
"""

import os
import json
import numpy as np
import pandas as pd
import networkx as nx
import osmnx as ox
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import contextily as ctx

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 경로 설정 ────────────────────────────────────────────────────────────────
STP_BASE  = '/Users/jin/석사논문/성동구_STP연구'
NET_PATH  = os.path.join(STP_BASE, '01_네트워크/seongdong_walk_network.graphml')
UTCI_PATH = 'results/link_utci_corrected.csv'
FIG_DIR   = 'results/figures'
os.makedirs(FIG_DIR, exist_ok=True)

# ── 핵심 파라미터 ────────────────────────────────────────────────────────────
WALK_SPEED  = 4.5 * 1000 / 3600   # m/s
TIME_BUDGET = 15 * 60              # 초 (900s ≈ 1,125m)
THRESHOLD   = 38.0                 # °C UTCI — Bröde et al.(2012) Very Strong HS 하한

# 분석 대상 역 및 시간대
# 역 노드 ID: osmnx nearest_nodes 결과, 변경 시 재탐색 필요
TARGETS = {
    '응봉역': {
        'lat': 37.5520, 'lon': 127.0353,
        'net_node': '7838649561',
        'color': '#8E24AA',
    },
    '성수역': {
        'lat': 37.5447, 'lon': 127.0561,
        'net_node': '436855717',
        'color': '#1E88E5',
    },
}
TARGET_HOURS = [7, 10, 13, 16]   # 분석 시간대

# ── 네트워크 로드 ─────────────────────────────────────────────────────────────
print("보행 네트워크 로드...")
G_base = ox.load_graphml(NET_PATH)
G_base = G_base.to_undirected()
nodes_gdf, edges_gdf = ox.graph_to_gdfs(G_base)
# 시각화용 Web Mercator 변환
nodes_wm = nodes_gdf.to_crs(epsg=3857)
edges_wm = edges_gdf.to_crs(epsg=3857)
print(f"  노드: {G_base.number_of_nodes():,}, 링크: {G_base.number_of_edges():,}")

# ── UTCI 로드 및 시간대별 Hard Cut 링크 집합 구성 ──────────────────────────
print("보정 UTCI 로드...")
utci_df = pd.read_csv(UTCI_PATH, encoding='utf-8-sig')

# 시간대별 hot_edges 딕셔너리 미리 구성 (반복 조회 최적화)
hot_edges_by_hour = {}
for hour in TARGET_HOURS:
    h_df = utci_df[(utci_df['hour'] == hour) & (utci_df['utci_corrected'] >= THRESHOLD)]
    # (u, v, hour) 튜플로 저장 — 양방향 링크 모두 포함
    hot_edges_by_hour[hour] = set(
        zip(h_df['u'].astype(str), h_df['v'].astype(str), h_df['hour'])
    )
    total = len(utci_df[utci_df['hour'] == hour])
    print(f"  {hour:02d}시 Hard Cut 대상: {len(h_df):,}/{total:,}개 ({len(h_df)/total*100:.1f}%)")


# ── Catchment 계산 함수 ─────────────────────────────────────────────────────
def compute_catchment(G, origin_node, hot_set, hour):
    """
    Classic: 전체 그래프, 이동시간 기반 15분 도달 범위
    Thermal: Hard Cut 링크 제거 후 동일 범위
    반환: 노드 집합 및 감소율
    """
    # 모든 링크에 이동시간 가중치 부여 (거리 / 보행속도)
    for u, v, d in G.edges(data=True):
        d['travel_time'] = d.get('length', 0) / WALK_SPEED

    classic_nodes = set(nx.single_source_dijkstra_path_length(
        G, origin_node, cutoff=TIME_BUDGET, weight='travel_time'
    ).keys())

    # Hard Cut: 열노출 초과 링크 물리적 제거
    G_th = G.copy()
    remove = [(u, v) for u, v in G_th.edges()
              if (str(u), str(v), hour) in hot_set
              or (str(v), str(u), hour) in hot_set]
    G_th.remove_edges_from(remove)

    thermal_nodes = set(nx.single_source_dijkstra_path_length(
        G_th, origin_node, cutoff=TIME_BUDGET, weight='travel_time'
    ).keys())

    lost_nodes  = classic_nodes - thermal_nodes
    reduction   = round(len(lost_nodes) / max(len(classic_nodes), 1) * 100, 1)

    return {
        'classic_nodes':   classic_nodes,
        'thermal_nodes':   thermal_nodes,
        'lost_nodes':      lost_nodes,
        'classic_count':   len(classic_nodes),
        'thermal_count':   len(thermal_nodes),
        'lost_count':      len(lost_nodes),
        'reduction_pct':   reduction,
        'removed_edges':   len(remove),
    }


# ── 분석 실행 ────────────────────────────────────────────────────────────────
print("\n=== Thermal Catchment Area 계산 ===")
all_results = {}
for name, info in TARGETS.items():
    all_results[name] = {}
    for hour in TARGET_HOURS:
        G = G_base.copy()
        result = compute_catchment(G, info['net_node'], hot_edges_by_hour[hour], hour)
        all_results[name][hour] = result
        print(f"  [{name}] {hour:02d}시 | Classic {result['classic_count']:,} → "
              f"Thermal {result['thermal_count']:,} (−{result['reduction_pct']}%)")


# ── 시각화: 역별 Classic vs Thermal 비교 지도 (13시) ───────────────────────
def make_contrast_map(station_name, hour):
    """Classic(빨강) vs Thermal(초록) 보행 네트워크 오버레이 지도 생성"""
    result = all_results[station_name][hour]
    classic = result['classic_nodes']
    thermal = result['thermal_nodes']
    info    = TARGETS[station_name]

    # 링크 유형 분류
    def classify_edge(idx):
        u, v = str(idx[0]), str(idx[1])
        in_cl = (u in classic) and (v in classic)
        in_th = (u in thermal) and (v in thermal)
        if in_th:   return 'thermal'     # Thermal Catchment 내 링크 (초록)
        elif in_cl: return 'lost'        # Classic에만 포함된 링크 (빨강)
        else:       return 'outside'

    e = edges_wm.copy()
    e['etype'] = e.index.map(classify_edge)

    # 출발 역 좌표 (EPSG:3857)
    origin_pt = nodes_wm.loc[info['net_node']].geometry
    cx, cy    = origin_pt.x, origin_pt.y

    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    pad = 1600   # m (15분 보행 반경 ≈ 1125m보다 여유)
    ax.set_xlim(cx - pad, cx + pad)
    ax.set_ylim(cy - pad, cy + pad)

    try:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=15, alpha=0.65)
    except Exception:
        pass

    # Thermal Catchment: 초록 (#43A047)
    e_th = e[e['etype'] == 'thermal']
    if not e_th.empty:
        e_th.plot(ax=ax, color='#43A047', linewidth=1.6, alpha=0.9, zorder=3)

    # Classic only (lost): 빨강 (#E53935)
    e_lost = e[e['etype'] == 'lost']
    if not e_lost.empty:
        e_lost.plot(ax=ax, color='#E53935', linewidth=1.6, alpha=0.9, zorder=4)

    # 출발 역 마커
    ax.scatter([cx], [cy], c='#212121', s=80, zorder=6)

    # 범례 텍스트 박스
    ax.annotate(
        f"{station_name}\nClassic:  {result['classic_count']:,} nodes\n"
        f"Thermal: {result['thermal_count']:,} nodes\n"
        f"[검증지표]: {result['reduction_pct']}%",
        xy=(0.03, 0.97), xycoords='axes fraction', va='top', ha='left',
        fontsize=10, bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.85),
        zorder=7,
    )
    ax.set_axis_off()
    plt.tight_layout(pad=0)

    fname = f"catchment_contrast_{station_name.replace('역','')}_h{hour:02d}.png"
    fig.savefig(os.path.join(FIG_DIR, fname), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  저장: {fname}")


print("\n=== 비교 지도 생성 (13시) ===")
for name in TARGETS:
    make_contrast_map(name, hour=13)


# ── 결과 요약 저장 ──────────────────────────────────────────────────────────
summary = {
    'model': 'method_a_svf_hw_hard_cut',
    'threshold_utci_c': THRESHOLD,
    'time_budget_min': 15,
    'walk_speed_kmh': 4.5,
}
for name in TARGETS:
    summary[name] = {}
    for hour in TARGET_HOURS:
        r = all_results[name][hour]
        summary[name][f'h{hour:02d}'] = {
            'classic_nodes': r['classic_count'],
            'thermal_nodes': r['thermal_count'],
            'lost_nodes':    r['lost_count'],
            'reduction_pct': r['reduction_pct'],
        }

out_json = 'results/catchment_summary_method_a.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"\n=== 최종 결과 (13시) ===")
for name in TARGETS:
    r = all_results[name][13]
    print(f"  {name}: Classic {r['classic_count']:,} → Thermal {r['thermal_count']:,} (−{r['reduction_pct']}%)")
print(f"\n요약 저장: {out_json}")
