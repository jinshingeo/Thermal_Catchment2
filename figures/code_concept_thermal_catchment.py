"""
Thermal Catchment Area 개념도 재제작
================================================================
기존 concept_thermal_catchment.png(2026-06-23 제작)은 2026-07-16 방법론 대전환
이전 버전이라 "MRT≥55°C" 라벨(폐기된 역산 MRT 방식)과 "TARR"(사용 금지 용어)를
쓰고 있었음. 동일한 구도(직접 차단 vs 간접 고립)를 유지하되 라벨만
"UTCI≥38°C"·"감소율(%)"로 교체.

직접 차단(direct blockage): 제거된 링크를 실제로 지나야 하는 노드
간접 고립(indirect isolation): 그 자체는 안 덥지만 대체 경로가 없어 도달 불가
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 노드 위치 (두 패널 공통) ────────────────────────────────────────────
pos = {
    'O': (0.5, 1.6), 'A': (1.6, 2.6), 'B': (2.8, 2.6), 'C': (4.0, 2.6),
    'D': (5.0, 2.6), 'E': (1.4, 0.7), 'F': (0.4, -0.2), 'G': (2.2, -0.2),
}
edges = [('O', 'A'), ('A', 'B'), ('B', 'C'), ('C', 'D'),
         ('O', 'E'), ('E', 'F'), ('E', 'G')]
HOT_EDGE = ('B', 'C')

GREEN = '#4CAF50'
GOLD = '#D4A017'
RED = '#D32F2F'
DARK_ORANGE = '#E65100'
AMBER = '#FF8F00'
GRAY = '#9E9E9E'


def draw_node(ax, name, color, label_extra=''):
    x, y = pos[name]
    ax.scatter([x], [y], s=800, color=color, zorder=5, edgecolor='white', linewidth=2)
    ax.annotate(name + label_extra, (x, y), ha='center', va='center',
                fontsize=13, fontweight='bold', color='white', zorder=6)


def draw_edge(ax, u, v, color, style='-', lw=3, zorder=2):
    x1, y1 = pos[u]
    x2, y2 = pos[v]
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw,
             linestyle=style, zorder=zorder, solid_capstyle='round')


fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), dpi=150)

# ═══ 좌: Classic Catchment ═══════════════════════════════════════════
ax = axes[0]
for (u, v) in edges:
    color = AMBER if (u, v) == HOT_EDGE else GREEN
    draw_edge(ax, u, v, color, lw=4 if (u, v) == HOT_EDGE else 3)
for n in pos:
    draw_node(ax, n, GOLD if n == 'O' else GREEN)
ax.annotate('UTCI ≥ 38°C\n(Classic에서만 통행 가능)', xy=pos['B'], xytext=(3.2, 3.5),
            fontsize=10, color=AMBER, ha='center',
            arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.2))
ax.set_title('Classic Catchment', fontsize=15, fontweight='bold', pad=15)
ax.text(0.5, -1.1, '모든 노드 도달 가능(15분 보행 예산)\n예: 정류장 7개소 접근 가능',
        ha='center', fontsize=10.5)

# ═══ 우: Thermal Catchment ═══════════════════════════════════════════
ax = axes[1]
for (u, v) in edges:
    if (u, v) == HOT_EDGE:
        draw_edge(ax, u, v, RED, style=(0, (5, 3)), lw=2.5, zorder=1)
    else:
        draw_edge(ax, u, v, GREEN, lw=3)
for n in pos:
    if n == 'O':
        c = GOLD
    elif n == 'C':
        c = RED             # 직접 차단
    elif n == 'D':
        c = DARK_ORANGE      # 간접 고립
    else:
        c = GREEN
    draw_node(ax, n, c)
ax.set_title('Thermal Catchment Area', fontsize=15, fontweight='bold', pad=15)
ax.text(4.0, 3.3, '직접 차단', color=RED, fontsize=10, ha='center', fontweight='bold')
ax.text(5.0, 3.3, '간접 고립', color=DARK_ORANGE, fontsize=10, ha='center', fontweight='bold')
ax.text(0.5, -1.1, '도달 가능 범위 축소\n예: 정류장 5개소 접근 가능 → 감소율 28.6%',
        ha='center', fontsize=10.5)

for ax in axes:
    ax.set_xlim(-0.6, 5.8)
    ax.set_ylim(-1.6, 3.9)
    ax.set_axis_off()

# ═══ 범례 ═════════════════════════════════════════════════════════════
from matplotlib.lines import Line2D
legend_elems = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=GREEN, markersize=14, label='정상 노드/링크 (Thermal Catchment 내 도달 가능)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=GOLD, markersize=14, label='출발지(집계구 중심점 등)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=RED, markersize=14, label='직접 차단 노드 (제거된 링크만 경로로 사용)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=DARK_ORANGE, markersize=14, label='간접 고립 노드 (열적으로는 안전하나 대체 경로 없음)'),
    Line2D([0], [0], color=AMBER, lw=3, label='UTCI ≥ 38°C 링크 (Classic Catchment에서만 통행 가능)'),
    Line2D([0], [0], color=RED, lw=2.5, linestyle=(0, (5, 3)), label='이진적으로 제거된 링크'),
]
fig.legend(handles=legend_elems, loc='lower center', ncol=2, fontsize=9.5,
           frameon=False, bbox_to_anchor=(0.5, -0.06))
plt.tight_layout(rect=[0, 0.08, 1, 1])
out_path = '/Users/jin/석사논문/Thermal_Catchment/figures/concept_thermal_catchment_v2.png'
plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
print('저장:', out_path)
