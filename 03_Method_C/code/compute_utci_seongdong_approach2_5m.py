"""성동구 approach2(5m) Tmrt -> UTCI 산출 (로컬)
기상요인 단일값(도메인 전체, 시간대별) + MRT만 공간화, 1mtrue와 동일 met.
"""
import os, glob, time
import numpy as np
import pandas as pd
import rasterio
from pythermalcomfort.models import utci

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TMRT_DIR = os.path.join(BASE, '03_Method_C', 'results', 'solweig_approach2_5m')
MET_CSV = os.path.join(BASE, '04_MeteoComparison', 'results', 'seongdong_met_profile_06_19h.csv')
OUT_DIR = os.path.join(BASE, '03_Method_C', 'results', 'utci_seongdong_5m_approach2')
os.makedirs(OUT_DIR, exist_ok=True)

met = pd.read_csv(MET_CSV)
met = met.set_index('hour')

t0 = time.time()
tmrt_files = sorted(glob.glob(os.path.join(TMRT_DIR, 'Tmrt_2025_209_*.tif')))
print(f'Tmrt 파일 {len(tmrt_files)}개 발견', flush=True)

utci_arrays = {}
for f in tmrt_files:
    hour = int(os.path.basename(f).split('_')[-1][:2])
    Ta = met.loc[hour, 'Ta']
    RH = met.loc[hour, 'RH']
    wind = met.loc[hour, 'wind']

    with rasterio.open(f) as src:
        tmrt = src.read(1).astype(float)
        profile = src.profile
        nodata = src.nodata
        mask = (tmrt <= -100) | (tmrt >= 200)
        if nodata is not None:
            mask = mask | (tmrt == nodata)
        tmrt[mask] = np.nan

    valid = ~np.isnan(tmrt)
    flat_tmrt = tmrt[valid]

    result = utci(tdb=Ta, tr=flat_tmrt.tolist(), v=wind, rh=RH,
                  limit_inputs=False, round_output=False)
    utci_flat = np.array(result.utci)

    utci_grid = np.full(tmrt.shape, np.nan, dtype=np.float32)
    utci_grid[valid] = utci_flat

    utci_arrays[hour] = utci_grid
    out_path = os.path.join(OUT_DIR, f'UTCI_seongdong_5m_approach2_{hour:02d}.tif')
    profile.update(dtype='float32', nodata=np.nan)
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(utci_grid, 1)
    print(f'  {hour:02d}시 (Ta={Ta}, RH={RH}, wind={wind}) -> '
          f'UTCI {np.nanmin(utci_grid):.1f}~{np.nanmax(utci_grid):.1f}degC', flush=True)

avg = np.nanmean(list(utci_arrays.values()), axis=0)
with rasterio.open(os.path.join(OUT_DIR, 'UTCI_seongdong_5m_approach2_average.tif'), 'w', **profile) as dst:
    dst.write(avg.astype(np.float32), 1)

print(f'\n총 소요시간: {time.time()-t0:.1f}초', flush=True)
print('성동구 5m(approach2) UTCI 산출 완료', flush=True)
