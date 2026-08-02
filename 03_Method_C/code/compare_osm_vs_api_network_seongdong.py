"""
작성일: 2026-08-02
목적: 성동구 지역 한정 — OSM 보행 네트워크 vs 서울시 도보 네트워크 API 오버레이 비교
"""
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'Apple SD Gothic Neo'
matplotlib.rcParams['axes.unicode_minus'] = False

JIBGYEGU_SHP = "/Users/jin/석사논문/Thermal_Catchment/data/_tmp_boundary/집계구.shp"
OSM_GPKG = "/Users/jin/석사논문/Thermal_Catchment/data/network/seoul_walk_network.gpkg"
API_GPKG = "/Users/jin/석사논문/Thermal_Catchment/data/network/2026-08-02_seoul_walk_api_network.gpkg"
OUT_PNG = "/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/figures/2026-08-02_osm_vs_api_network_seongdong.png"

print("성동구 경계 추출...")
jbg = gpd.read_file(JIBGYEGU_SHP).set_crs(5179, allow_override=True)
jbg['TOT_REG_CD'] = jbg['TOT_REG_CD'].astype(str)
seongdong = jbg[jbg['TOT_REG_CD'].str.startswith('11040')].dissolve()
seongdong_4326 = seongdong.to_crs(4326)
bounds = seongdong_4326.total_bounds  # minx, miny, maxx, maxy
print("경계:", bounds)

print("OSM 네트워크 로드 및 클립...")
osm = gpd.read_file(OSM_GPKG, layer='edges', bbox=tuple(bounds))
osm_clip = gpd.clip(osm, seongdong_4326)
print(f"  OSM 엣지: {len(osm_clip)}개")

print("API 네트워크 로드 및 클립...")
api = gpd.read_file(API_GPKG, bbox=tuple(bounds))
api_walk = api[api['LNKG_TYPE_CD'].str.startswith('1')]
api_clip = gpd.clip(api_walk, seongdong_4326)
print(f"  API 엣지: {len(api_clip)}개")

fig, axes = plt.subplots(1, 3, figsize=(21, 8))

ax = axes[0]
seongdong_4326.boundary.plot(ax=ax, color='#888', linewidth=1)
osm_clip.plot(ax=ax, color='#C3450F', linewidth=0.6)
ax.set_title(f'OSM 보행 네트워크 (n={len(osm_clip):,})', fontsize=13)
ax.set_axis_off()

ax = axes[1]
seongdong_4326.boundary.plot(ax=ax, color='#888', linewidth=1)
api_clip.plot(ax=ax, color='#1C5C82', linewidth=0.6)
ax.set_title(f'서울시 도보 네트워크 API (n={len(api_clip):,})', fontsize=13)
ax.set_axis_off()

ax = axes[2]
seongdong_4326.boundary.plot(ax=ax, color='#888', linewidth=1)
osm_clip.plot(ax=ax, color='#C3450F', linewidth=1.1, alpha=0.6, label='OSM')
api_clip.plot(ax=ax, color='#1C5C82', linewidth=1.1, alpha=0.6, label='서울시API')
ax.set_title('중첩 비교 (주황=OSM, 파랑=서울시API)', fontsize=13)
ax.set_axis_off()

fig.suptitle('성동구 — OSM vs 서울시 도보 네트워크 API 비교', fontsize=15)
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=170, bbox_inches='tight', facecolor='white')
print(f"저장: {OUT_PNG}")

print()
print(f"길이 비교(km): OSM={osm_clip.geometry.to_crs(5179).length.sum()/1000:.1f}, API={api_clip.geometry.to_crs(5179).length.sum()/1000:.1f}")
