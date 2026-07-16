"""서울 전체 5m Tmrt — 8타일 모자이크 (버퍼 크롭 후 병합)"""
import os
import json
import numpy as np
import rasterio
from rasterio.transform import from_origin

BASE = '/home/sj/thermal_catchment'
TILE_DIR = os.path.join(BASE, '03_Method_C', 'results', 'dsm_cdsm_seoul_5m_v2', 'tiles8')
SOLWEIG_BASE = os.path.join(BASE, '03_Method_C', 'results')
OUT_DIR = os.path.join(SOLWEIG_BASE, 'solweig_seoul_5m_v2_mosaic')
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(TILE_DIR, 'tile_ranges.json')) as f:
    meta = json.load(f)
tile_ranges = meta['tile_ranges']  # [core_start, core_end, buf_start, buf_end]
width, height = meta['width'], meta['height']

with rasterio.open(os.path.join(TILE_DIR, '..', 'DSM_seoul_5m_v2.tif')) as ref:
    ref_transform = ref.transform
    crs = ref.crs

HOURS = ['0600N','0700D','0800D','0900D','1000D','1100D','1200D','1300D',
         '1400D','1500D','1600D','1700D','1800D','1900D']

def mosaic_one(fname_suffix, out_name):
    """타일 8개에서 fname_suffix(예: 'Tmrt_2025_209_0600N.tif')를 읽어 코어만 잘라 병합"""
    full = np.full((height, width), np.nan, dtype=np.float32)
    for i, (cs, ce, bs, be) in enumerate(tile_ranges):
        tile_path = os.path.join(SOLWEIG_BASE, f'solweig_seoul_5m_v2_tile{i}', fname_suffix)
        with rasterio.open(tile_path) as src:
            arr = src.read(1).astype(np.float32)
        core_offset = cs - bs
        core_w = ce - cs
        core_data = arr[:, core_offset:core_offset + core_w]
        full[:, cs:ce] = core_data
    full[(full <= -100) | (full >= 200)] = np.nan
    profile = {'driver': 'GTiff', 'height': height, 'width': width, 'count': 1,
               'dtype': 'float32', 'crs': crs, 'transform': ref_transform, 'nodata': np.nan}
    out_path = os.path.join(OUT_DIR, out_name)
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(full, 1)
    print(f"저장: {out_path} (min={np.nanmin(full):.1f}, max={np.nanmax(full):.1f})", flush=True)
    return full

hourly_arrays = {}
for h in HOURS:
    hour_int = int(h[:2])
    arr = mosaic_one(f'Tmrt_2025_209_{h}.tif', f'Tmrt_seoul_5m_{h}.tif')
    hourly_arrays[hour_int] = arr

# 평균
avg = np.nanmean(list(hourly_arrays.values()), axis=0)
profile = {'driver': 'GTiff', 'height': height, 'width': width, 'count': 1,
           'dtype': 'float32', 'crs': crs, 'transform': ref_transform, 'nodata': np.nan}
with rasterio.open(os.path.join(OUT_DIR, 'Tmrt_seoul_5m_average.tif'), 'w', **profile) as dst:
    dst.write(avg.astype(np.float32), 1)
print("평균 저장 완료", flush=True)
print("전체 모자이크 완료.", flush=True)
