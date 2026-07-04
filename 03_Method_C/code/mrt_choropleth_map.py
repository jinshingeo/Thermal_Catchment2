"""
Method C — 링크별 MRT 공간 분포 코로플레스 지도
작성일: 2026-07-04
근거: 파일럿 55_mrt_link_map.py 스타일 준용
"""

import os, warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.colors import BoundaryNorm
import contextily as ctx
from pyproj import Transformer
from shapely.geometry import LineString
from shapely import wkt as shapely_wkt
from shapely.ops import transform as shapely_transform
warnings.filterwarnings('ignore')

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

try:
    import mapclassify
    HAS_MAPCLASSIFY = True
except ImportError:
    HAS_MAPCLASSIFY = False

SCRATCH  = "/private/tmp/claude-501/-Users-jin------TAVI/11a7aa5d-485a-4d32-8032-faf31923985e/scratchpad"
MRT_CSV  = SCRATCH + "/link_mrt_seongdong/link_mrt_method_c.csv"
NET_PATH = "/Users/jin/석사논문/성동구_STP연구/01_네트워크/seongdong_walk_network.graphml"
JBG_PATH = "/Users/jin/석사논문/통계지역경계/집계구.shp"
OUT_PATH = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-04_mrt_choropleth_methodC.png"
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

# ── 네트워크 로드 → GeoDataFrame (EPSG:3857) ─────────────────────────────
print("네트워크 로드...")
G = nx.read_graphml(NET_PATH)
wgs2wm = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

def to_wm(geom_wgs):
    """WGS84 shapely geometry → EPSG:3857"""
    return shapely_transform(wgs2wm.transform, geom_wgs)

edge_rows = []
for u, v, d in G.edges(data=True):
    un, vn = G.nodes[u], G.nodes[v]
    # GraphML에 실제 도로 곡선 geometry가 WKT로 저장돼 있으면 사용
    # 없으면 노드 좌표로 직선 대체
    if 'geometry' in d:
        geom = to_wm(shapely_wkt.loads(d['geometry']))
    else:
        ux, uy = wgs2wm.transform(float(un['x']), float(un['y']))
        vx, vy = wgs2wm.transform(float(vn['x']), float(vn['y']))
        geom = LineString([(ux, uy), (vx, vy)])
    edge_rows.append({'u': str(u), 'v': str(v), 'geometry': geom})

edges_gdf = gpd.GeoDataFrame(edge_rows, crs="EPSG:3857")
print(f"  링크: {len(edges_gdf):,}개")

# ── MRT 로드 및 병합 ─────────────────────────────────────────────────────
print("MRT 로드...")
mrt_df = pd.read_csv(MRT_CSV)
mrt_df['u'] = mrt_df['u'].apply(lambda x: str(int(float(x))))
mrt_df['v'] = mrt_df['v'].apply(lambda x: str(int(float(x))))
print(f"  MRT 유효 링크: {mrt_df['mrt'].notna().sum():,}개")
print(f"  MRT 범위: {mrt_df['mrt'].min():.1f} ~ {mrt_df['mrt'].max():.1f}°C")

edges_merged = edges_gdf.merge(mrt_df[['u','v','mrt']], on=['u','v'], how='left')
valid  = edges_merged.dropna(subset=['mrt']).copy()
no_mrt = edges_merged[edges_merged['mrt'].isna()].copy()

# ── 5분위 분류 ───────────────────────────────────────────────────────────
vals = valid['mrt'].values
# GLO-30 30m SOLWEIG 특성상 공간 분화가 좁음(58.4~61.6°C) → 등간격 수동 지정
# Method A와 비교 가능하도록 5구간 동일 수 유지
breaks = [58.0, 59.0, 60.0, 61.0, 61.5, 62.0]
print(f"  분류 급간(등간격 수동): {breaks}")

colors_hex = ['#FFCC99', '#FF9933', '#FF6600', '#FF2200', '#990000']
cmap = mcolors.ListedColormap(colors_hex)

def assign_class(val):
    for j in range(len(breaks) - 1):
        if val <= breaks[j + 1]:
            return j
    return len(breaks) - 2

valid['cls'] = valid['mrt'].apply(assign_class)

# ── 집계구 경계 (성동구 = '11040' 접두) ─────────────────────────────────
print("집계구 경계 로드...")
jbg = gpd.read_file(JBG_PATH)
if jbg.crs is None:
    jbg = jbg.set_crs('EPSG:5179', allow_override=True)
jbg = jbg[jbg['TOT_REG_CD'].astype(str).str.startswith('11040')].to_crs('EPSG:3857')

# ── 시각화 ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 12), dpi=150)

# MRT 없는 링크 (회색)
if not no_mrt.empty:
    no_mrt.plot(ax=ax, color='#CCCCCC', linewidth=0.4, alpha=0.5, zorder=2)

# MRT 링크 — 급간별 색상 (낮은 급간 먼저, 높은 급간이 위에 표시)
for cls_idx, color in enumerate(colors_hex):
    subset = valid[valid['cls'] == cls_idx]
    if subset.empty:
        continue
    lw = 1.0 if cls_idx < 4 else 1.4
    subset.plot(ax=ax, color=color, linewidth=lw, alpha=0.9, zorder=3 + cls_idx)

# 베이스맵
try:
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=14, alpha=0.6)
except Exception as e:
    print(f"  베이스맵 오류(무시): {e}")

# 집계구 경계
jbg.plot(ax=ax, facecolor='none', edgecolor='#AAAAAA', linewidth=0.6, alpha=0.6, zorder=1)

# ── 범례 ────────────────────────────────────────────────────────────────
legend_patches = []
for j in range(len(colors_hex)):
    lo  = breaks[j]
    hi  = breaks[j + 1]
    cnt = (valid['cls'] == j).sum()
    legend_patches.append(
        mpatches.Patch(facecolor=colors_hex[j], edgecolor='#555',
                       label=f'{lo:.1f}–{hi:.1f}°C  ({cnt:,}개)')
    )
legend_patches.append(
    mpatches.Patch(facecolor='none', edgecolor='#888888',
                   linewidth=1.0, label='집계구 경계')
)

ax.legend(handles=legend_patches, title='MRT (°C)', loc='upper left',
          fontsize=12, title_fontsize=13, framealpha=0.92,
          edgecolor='#999', fancybox=False,
          handleheight=1.8, handlelength=2.0,
          borderpad=1.0, labelspacing=0.7)

ax.set_title(
    '링크별 평균복사온도(MRT) 공간 분포\n'
    '14시 기준 | 성동구 | SOLWEIG + GLO-30 30m DSM (Method C)',
    fontsize=13, fontweight='bold', pad=12
)
ax.set_axis_off()
plt.tight_layout()
plt.savefig(OUT_PATH, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"\n저장: {OUT_PATH}")
