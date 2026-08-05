"""
MRT / UTCI 2D 초콜릿맵 — 서울 전체, 19시
================================================================
범례/제목/축 없이 링크만 렌더링(투명배경) + 범례는 별도 PNG로 저장.
단일톤 시퀀셜 컬러(양방향 없음) — Oranges(MRT), Reds(UTCI).
"""
import os
import numpy as np
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
GPKG = os.path.join(PROJ, '03_Method_C', 'results',
                     '2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg')
OUT_2D = os.path.join(PROJ, 'figures', '발표용_20260805', '2d')
OUT_LEG = os.path.join(PROJ, 'figures', '발표용_20260805', 'legends')
HOUR = 19
FIGSIZE, DPI = (12, 12), 150


def render_map(gdf, col, cmap_name, out_path, lw=0.4):
    vals = gdf[col].values
    vmin, vmax = np.nanpercentile(vals, [2, 98])
    cmap = cm.get_cmap(cmap_name)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)

    segments = []
    colors = []
    for geom, v in zip(gdf.geometry, vals):
        if geom is None or geom.is_empty or np.isnan(v):
            continue
        xs, ys = geom.xy
        segments.append(np.column_stack([xs, ys]))
        colors.append(cmap(norm(v)))

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    lc = LineCollection(segments, colors=colors, linewidths=lw)
    ax.add_collection(lc)
    ax.set_xlim(gdf.total_bounds[0], gdf.total_bounds[2])
    ax.set_ylim(gdf.total_bounds[1], gdf.total_bounds[3])
    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', pad_inches=0,
                transparent=True)
    plt.close(fig)
    print(f"저장: {out_path}")
    return vmin, vmax, cmap


def render_legend(vmin, vmax, cmap, label, out_path):
    fig, ax = plt.subplots(figsize=(1.2, 4), dpi=DPI)
    fig.patch.set_alpha(0)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cb = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm,
                                           orientation='vertical')
    cb.set_label(label, fontsize=11)
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', transparent=True)
    plt.close(fig)
    print(f"저장: {out_path}")


print("링크 데이터 로드...")
gdf = gpd.read_file(GPKG, columns=['geometry', f'Tmrt_{HOUR:02d}', f'UTCI_{HOUR:02d}'])

print(f"[1] MRT {HOUR}시...")
vmin, vmax, cmap = render_map(
    gdf, f'Tmrt_{HOUR:02d}', 'Oranges',
    os.path.join(OUT_2D, f'mrt_seoul_{HOUR}h.png'))
render_legend(vmin, vmax, cmap, 'MRT (°C)',
              os.path.join(OUT_LEG, f'legend_mrt_{HOUR}h.png'))

print(f"[2] UTCI {HOUR}시...")
vmin, vmax, cmap = render_map(
    gdf, f'UTCI_{HOUR:02d}', 'Reds',
    os.path.join(OUT_2D, f'utci_seoul_{HOUR}h.png'))
render_legend(vmin, vmax, cmap, 'UTCI (°C)',
              os.path.join(OUT_LEG, f'legend_utci_{HOUR}h.png'))

print("완료")
