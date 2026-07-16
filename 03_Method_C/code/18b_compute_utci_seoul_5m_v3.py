"""
서울 전체 5m (v3, 진짜 1m DEM 소스) — UTCI 산출
================================================================
기상요인 단일값(도메인 전체, 시간대별) + MRT만 공간화 방식 최종 채택
(2026-07-17 확정, writing/2026-07-16_방법론_단일기상값_MRT공간화_근거.md 참고).

방법: MRT(SOLWEIG, 공간분포, v3=1m DEM 소스 5m 계산격자) + 기상요소(Ta/RH/풍속,
met.txt 단일값·시간별 변화만)를 Bröde et al.(2012) 표준 UTCI 회귀식
(pythermalcomfort)으로 조합해 픽셀별 UTCI 계산.
"""
import os
import glob
import time
import numpy as np
import pandas as pd
import rasterio
from pythermalcomfort.models import utci

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
TMRT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'solweig_seoul_5m_v3_mosaic')
MET_CSV = os.path.join(PROJ, '04_MeteoComparison', 'results', 'seoul_met_profile_06_19h.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'utci_seoul_5m_v3')
os.makedirs(OUT_DIR, exist_ok=True)

met = pd.read_csv(MET_CSV)
met = met.set_index('hour')

t0 = time.time()
tmrt_files = sorted(glob.glob(os.path.join(TMRT_DIR, 'Tmrt_seoul_5m_*.tif')))
tmrt_files = [f for f in tmrt_files if 'average' not in f]

utci_arrays = {}
for f in tmrt_files:
    th = time.time()
    hour = int(os.path.basename(f).split('_')[-1][:2])
    Ta = met.loc[hour, 'Ta']
    RH = met.loc[hour, 'RH']
    wind = met.loc[hour, 'wind']

    with rasterio.open(f) as src:
        tmrt = src.read(1).astype(float)
        profile = src.profile
        mask = (tmrt <= -100) | (tmrt >= 200)
        tmrt[mask] = np.nan

    valid = ~np.isnan(tmrt)
    flat_tmrt = tmrt[valid]

    result = utci(tdb=Ta, tr=flat_tmrt.tolist(), v=wind, rh=RH,
                  limit_inputs=False, round_output=False)
    utci_flat = np.array(result.utci)

    utci_grid = np.full(tmrt.shape, np.nan, dtype=np.float32)
    utci_grid[valid] = utci_flat

    utci_arrays[hour] = utci_grid
    out_path = os.path.join(OUT_DIR, f'UTCI_seoul_5m_v3_{hour:02d}.tif')
    profile.update(dtype='float32', nodata=np.nan)
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(utci_grid, 1)
    print(f"  {hour:02d}시 (Ta={Ta}, RH={RH}, wind={wind}) -> "
          f"UTCI {np.nanmin(utci_grid):.1f}~{np.nanmax(utci_grid):.1f}degC, "
          f"{time.time()-th:.1f}초", flush=True)

avg = np.nanmean(list(utci_arrays.values()), axis=0)
with rasterio.open(os.path.join(OUT_DIR, 'UTCI_seoul_5m_v3_average.tif'), 'w', **profile) as dst:
    dst.write(avg.astype(np.float32), 1)

total_t = time.time() - t0
print(f"\n총 소요시간: {total_t:.1f}초 ({total_t/60:.2f}분)")
print("v3(1m DEM 소스) UTCI 산출 완료 — 단일 기상값 방식 최종 채택 반영")
