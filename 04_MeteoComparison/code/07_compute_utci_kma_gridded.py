"""
KMA 500m 격자 기상(Ta/RH/풍속) 기반 링크별 UTCI 재계산
================================================================
기존 Tmrt(2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg, 이미 산출된 값 재사용 —
SOLWEIG 재실행 안 함)에, 도메인 단일값 대신 링크별 최근접 KMA 500m 격자 기상값
(06~19시, 12일 평균)을 대입해 UTCI를 다시 계산한다. 일사량은 격자자료에 없어
기존 방식(ASOS 108 단일값) 그대로 met.txt에 이미 반영되어 있던 것과 달리, 여기서는
UTCI 재계산에 직접 관여하지 않음(UTCI 입력은 Ta/RH/풍속/Tmrt 4개뿐 — Bröde et al. 2012).

출력: 03_Method_C/results/2026-08-06_link_utci_seoul_5m_KMA격자기상.gpkg
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from pythermalcomfort.models import utci

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
TMRT_GPKG = os.path.join(PROJ, '03_Method_C', 'results', '2026-07-20_link_tmrt_utci_seoul_5m_v3.gpkg')
IDX_CSV = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache', 'link_to_kma_grid_index.csv')
MET_CSV = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache', 'kma_grid_met_12day_avg.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results')

HOURS = list(range(6, 20))

print("링크 Tmrt 로드 중...")
gdf = gpd.read_file(TMRT_GPKG)
tmrt_cols = [c for c in gdf.columns if c.startswith('Tmrt_') and c != 'Tmrt_avg']
keep_cols = ['geometry'] + tmrt_cols
gdf = gdf[keep_cols].copy()
print(f"  링크 수: {len(gdf):,}")

print("링크->격자 매핑 로드...")
idx = pd.read_csv(IDX_CSV)  # link_idx, grid_row, grid_col (Tmrt gpkg와 순서 동일해야 함)
assert len(idx) == len(gdf), f"매핑 행수({len(idx)}) != 링크 수({len(gdf)})"

print("격자 기상값 로드...")
met = pd.read_csv(MET_CSV)  # grid_row, grid_col, hour, ta, hm, ws_10m

print("링크별 기상값 배정 중...")
merged = idx.merge(met, on=['grid_row', 'grid_col'], how='left')
n_missing = merged['ta'].isna().sum()
print(f"  결측 배정: {n_missing}건 (전체 {len(merged)}행 중)")

for h in HOURS:
    h_met = merged[merged['hour'] == h].set_index('link_idx')
    ta = h_met['ta'].reindex(range(len(gdf))).values
    rh = h_met['hm'].reindex(range(len(gdf))).values
    ws = h_met['ws_10m'].reindex(range(len(gdf))).values
    tmrt = gdf[f'Tmrt_{h:02d}'].values

    valid = ~(np.isnan(ta) | np.isnan(rh) | np.isnan(ws) | np.isnan(tmrt))
    utci_vals = np.full(len(gdf), np.nan)
    result = utci(tdb=ta[valid].tolist(), tr=tmrt[valid].tolist(),
                  v=ws[valid].tolist(), rh=rh[valid].tolist(),
                  limit_inputs=False, round_output=False)
    utci_vals[valid] = np.array(result.utci)
    gdf[f'UTCI_{h:02d}'] = utci_vals
    gdf[f'Ta_{h:02d}'] = ta
    gdf[f'RH_{h:02d}'] = rh
    gdf[f'WS_{h:02d}'] = ws
    print(f"  {h:02d}시 완료 (유효 {valid.sum():,}/{len(gdf):,}, "
          f"Ta 평균 {np.nanmean(ta):.1f}, UTCI 평균 {np.nanmean(utci_vals):.1f})")

gpkg_out = os.path.join(OUT_DIR, '2026-08-06_link_utci_seoul_5m_KMA격자기상.gpkg')
gdf.to_file(gpkg_out, driver='GPKG')
print(f"저장: {gpkg_out}")

csv_out = os.path.join(OUT_DIR, '2026-08-06_link_utci_seoul_5m_KMA격자기상.csv')
gdf.drop(columns='geometry').to_csv(csv_out, index=False, encoding='utf-8-sig')
print(f"저장: {csv_out}")
