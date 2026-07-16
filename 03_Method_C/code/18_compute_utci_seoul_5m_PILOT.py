"""
[파일럿 / 미확정 방법론] 서울 전체 5m — UTCI 산출
================================================================
⚠️ 이 스크립트는 확정된 방법론이 아님 — "기존(단순) 방식으로 돌리면 어떻게
나오는지" 확인하는 파일럿 수준 실행.

방법: MRT(SOLWEIG, 공간분포) + 기상요소(Ta/RH/풍속, met.txt 단일값·시간별
변화만)를 조합해 Bröde et al.(2012) 표준 UTCI 회귀식(pythermalcomfort 라이브러리)
으로 픽셀별 UTCI 계산. 풍속·기온·습도는 서울 전체 대표 단일값(공간 보간 없음)
— Basu et al.(2024)/Colaninno et al.(2024)와 동일한 단순화(단, 이들은 ERA5,
본 연구는 S-DoT+AWS 평균). URock 등 보행자 수준 바람장 모델링은 사용하지 않음.

이 방식이 최종 채택될지는 미정 — 축2(기상 입력 방식 비교, 단일값/IDW/MQ/크리깅)
결정 이후 재검토 필요.
"""
import os
import glob
import time
import numpy as np
import pandas as pd
import rasterio
from pythermalcomfort.models import utci

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
TMRT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'solweig_seoul_5m_v2_mosaic')
MET_CSV = os.path.join(PROJ, '04_MeteoComparison', 'results', 'seoul_met_profile_06_19h.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results', 'utci_seoul_5m_PILOT_단일기상값')
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
    out_path = os.path.join(OUT_DIR, f'UTCI_seoul_5m_PILOT_{hour:02d}.tif')
    profile.update(dtype='float32', nodata=np.nan)
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(utci_grid, 1)
    print(f"  {hour:02d}시 (Ta={Ta}, RH={RH}, wind={wind}) -> "
          f"UTCI {np.nanmin(utci_grid):.1f}~{np.nanmax(utci_grid):.1f}degC, "
          f"{time.time()-th:.1f}초", flush=True)

avg = np.nanmean(list(utci_arrays.values()), axis=0)
with rasterio.open(os.path.join(OUT_DIR, 'UTCI_seoul_5m_PILOT_average.tif'), 'w', **profile) as dst:
    dst.write(avg.astype(np.float32), 1)

total_t = time.time() - t0
print(f"\n총 소요시간: {total_t:.1f}초 ({total_t/60:.2f}분)")
print("⚠️ 파일럿 결과 — 방법론 미확정(단일 기상값, URock/공간보간 미적용)")
