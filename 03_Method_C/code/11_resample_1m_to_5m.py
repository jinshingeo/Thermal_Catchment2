"""
성동구 파일럿 — Approach 2(1m) 래스터를 5m로 리샘플링
================================================================
목적: 1m SVF가 메모리(107GB)/시간(며칠) 문제로 비현실적이라
5m 해상도로 먼저 파이프라인을 검증하기 위한 단계.
- DSM/CDSM/DEM(연속형): average 리샘플링
- LandCover(범주형): mode(최빈값) 리샘플링
"""
import os
os.environ.setdefault('PROJ_DATA', '/opt/miniconda3/lib/python3.13/site-packages/rasterio/proj_data')
import rasterio
from rasterio.enums import Resampling

SRC_DIR = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/dsm_cdsm_seongdong'
FACTOR = 5  # 1m -> 5m

CONTINUOUS = ['DSM_approach2_1m.tif', 'CDSM_approach2_1m.tif', 'DEM_approach2_1m.tif']
CATEGORICAL = ['LandCover_approach2_1m.tif']


def resample(src_path, dst_path, resampling):
    with rasterio.open(src_path) as src:
        new_width = src.width // FACTOR
        new_height = src.height // FACTOR
        data = src.read(
            out_shape=(src.count, new_height, new_width),
            resampling=resampling
        )
        new_transform = src.transform * src.transform.scale(
            src.width / new_width, src.height / new_height
        )
        profile = src.profile.copy()
        profile.update(height=new_height, width=new_width, transform=new_transform)
        with rasterio.open(dst_path, 'w', **profile) as dst:
            dst.write(data)
        print(f"  {os.path.basename(dst_path)}: {new_width}x{new_height}")


for fname in CONTINUOUS:
    src = os.path.join(SRC_DIR, fname)
    dst = os.path.join(SRC_DIR, fname.replace('approach2_1m', 'approach2_5m'))
    resample(src, dst, Resampling.average)

for fname in CATEGORICAL:
    src = os.path.join(SRC_DIR, fname)
    dst = os.path.join(SRC_DIR, fname.replace('approach2_1m', 'approach2_5m'))
    resample(src, dst, Resampling.mode)

print("완료")
