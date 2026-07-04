"""
작성일: 2026-07-03
버전: v1.0
목적: 서울특별시 전체 보행 네트워크 다운로드 → GraphML 저장
      성동구 파일럿과 동일한 방식 (osmnx 1.x 호환 저장 포맷)
"""
import os
from datetime import date
import networkx as nx

try:
    import osmnx as ox
    USE_OSMNX = True
except ImportError:
    USE_OSMNX = False

TODAY    = date.today().strftime('%Y-%m-%d')
BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

OUT_PATH = os.path.join(DATA_DIR, 'seoul_walk_network.graphml')

if os.path.exists(OUT_PATH):
    G = nx.read_graphml(OUT_PATH)
    print(f"이미 존재: {OUT_PATH}")
    print(f"  노드: {G.number_of_nodes():,}, 엣지: {G.number_of_edges():,}")
else:
    if not USE_OSMNX:
        raise ImportError("osmnx가 필요합니다: pip install osmnx")
    print("서울 보행 네트워크 다운로드 중 (약 5~15분 소요)...")
    # 서울특별시 전체 행정경계 기준
    G = ox.graph_from_place("Seoul, South Korea", network_type='walk')
    print(f"  노드: {G.number_of_nodes():,}, 엣지: {G.number_of_edges():,}")
    # nx.write_graphml로 저장 (osmnx 2.x load_graphml 재다운로드 우회)
    nx.write_graphml(G, OUT_PATH)
    print(f"  저장: {OUT_PATH}")
