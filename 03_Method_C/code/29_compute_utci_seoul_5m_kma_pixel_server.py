"""
서울 전체 5m — 픽셀 단위 KMA 격자기상 반영 UTCI 산출, 서울 경계 클리핑판 (서버용)
================================================================
18b_compute_utci_seoul_5m_v3.py(도메인 단일 기상값)를 픽셀 단위 KMA 500m
격자 최근접 기상으로 대체. 08b_build_pixel_kma_grid_index_seoulclip.py가
만든 인덱스(서울 행정경계 안쪽 픽셀만, 기존 캐시된 2,300개 격자셀 중
최근접 — API 재호출 없음, 근거는 2026-08-17 거리 검증 참고)를 사용.

Tmrt는 그대로(solweig_seoul_5m_v3_mosaic), 기상요소만 픽셀마다 다르게 배정해
pythermalcomfort.utci()로 픽셀별 UTCI를 직접 계산한다(평균 후 계산이 아님).
서울 경계 바깥 픽셀은 nodata로 남긴다(어차피 최종 결과물도 경계로 클리핑).
"""
import os
import glob
import time
import numpy as np
import pandas as pd
import rasterio
from pythermalcomfort.models import utci

BASE = '/home/sj/thermal_catchment'
TMRT_DIR = os.path.join(BASE, '03_Method_C', 'results', 'solweig_seoul_5m_v3_mosaic')
IDX_ROW = os.path.join(BASE, '04_MeteoComparison', 'data', 'kma_grid_cache', 'pixel_grid_row_seoulclip.npy')
IDX_COL = os.path.join(BASE, '04_MeteoComparison', 'data', 'kma_grid_cache', 'pixel_grid_col_seoulclip.npy')
IDX_MASK = os.path.join(BASE, '04_MeteoComparison', 'data', 'kma_grid_cache', 'pixel_seoul_mask.npy')
MET_CSV = os.path.join(BASE, '04_MeteoComparison', 'data', 'kma_grid_cache', 'kma_grid_met_12day_avg.csv')
OUT_DIR = os.path.join(BASE, '03_Method_C', 'results', 'utci_seoul_5m_kma_pixel')
os.makedirs(OUT_DIR, exist_ok=True)

NATIONAL_GRID_NCOL = 2049  # grid_row*NCOL+grid_col 인코딩 기준 (03/08b번 스크립트와 동일 전국격자)

t0 = time.time()
print("픽셀->KMA격자 인덱스(서울 경계 클리핑) 로드 중...", flush=True)
grid_row = np.load(IDX_ROW)
grid_col = np.load(IDX_COL)
seoul_mask = np.load(IDX_MASK)
print(f"  픽셀 배열 크기: {grid_row.shape}, 경계 안쪽 픽셀 {seoul_mask.sum():,}개", flush=True)

print("KMA 격자 기상(12일 평균, 기존 링크 기반 2,300셀) 로드 중...", flush=True)
met = pd.read_csv(MET_CSV)
cells = met[['grid_row', 'grid_col']].drop_duplicates().reset_index(drop=True)
cell_keys = (cells['grid_row'].values.astype(np.int64) * NATIONAL_GRID_NCOL
             + cells['grid_col'].values.astype(np.int64))
order = np.argsort(cell_keys)
sorted_keys = cell_keys[order]

# 경계 안쪽 픽셀에 대해서만 키 매칭 (바깥은 grid_row/col=-1 sentinel이라 제외)
flat_mask = seoul_mask.ravel()
flat_row = grid_row.ravel()
flat_col = grid_col.ravel()
flat_keys_valid = (flat_row[flat_mask].astype(np.int64) * NATIONAL_GRID_NCOL
                    + flat_col[flat_mask].astype(np.int64))
pos = np.searchsorted(sorted_keys, flat_keys_valid)
assert np.array_equal(sorted_keys[pos], flat_keys_valid), "픽셀->격자 키 매칭 불일치 — 인덱스 재확인 필요"

local_idx = np.full(flat_mask.shape, -1, dtype=np.int32)
local_idx[flat_mask] = order[pos]
local_idx = local_idx.reshape(grid_row.shape)
print("  검증 완료: 경계 안쪽 픽셀 전부 대응 격자셀과 정확히 매칭됨", flush=True)

tmrt_files = sorted(glob.glob(os.path.join(TMRT_DIR, 'Tmrt_seoul_5m_*.tif')))
tmrt_files = [f for f in tmrt_files if 'average' not in f]
print(f"\nTmrt 래스터 {len(tmrt_files)}개 시간대 처리 시작", flush=True)

utci_arrays = {}
for f in tmrt_files:
    th = time.time()
    hour = int(os.path.basename(f).split('_')[-1][:2])

    h_met = met[met['hour'] == hour].set_index(['grid_row', 'grid_col'])
    ta_by_cell = cells.join(h_met, on=['grid_row', 'grid_col'])['ta'].values
    rh_by_cell = cells.join(h_met, on=['grid_row', 'grid_col'])['hm'].values
    ws_by_cell = cells.join(h_met, on=['grid_row', 'grid_col'])['ws_10m'].values

    ta_sorted = ta_by_cell[order]
    rh_sorted = rh_by_cell[order]
    ws_sorted = ws_by_cell[order]

    safe_idx = np.where(local_idx >= 0, local_idx, 0)
    ta_pixel = ta_sorted[safe_idx]
    rh_pixel = rh_sorted[safe_idx]
    ws_pixel = ws_sorted[safe_idx]

    with rasterio.open(f) as src:
        tmrt = src.read(1).astype(float)
        profile = src.profile
        bad_tmrt = (tmrt <= -100) | (tmrt >= 200)
        tmrt[bad_tmrt] = np.nan

    valid = seoul_mask & ~np.isnan(tmrt) & ~np.isnan(ta_pixel) & ~np.isnan(rh_pixel) & ~np.isnan(ws_pixel)
    result = utci(tdb=ta_pixel[valid].tolist(), tr=tmrt[valid].tolist(),
                  v=ws_pixel[valid].tolist(), rh=rh_pixel[valid].tolist(),
                  limit_inputs=False, round_output=False)
    utci_flat = np.array(result.utci)

    utci_grid = np.full(tmrt.shape, np.nan, dtype=np.float32)
    utci_grid[valid] = utci_flat
    utci_arrays[hour] = utci_grid

    out_path = os.path.join(OUT_DIR, f'UTCI_seoul_5m_kma_pixel_{hour:02d}.tif')
    profile.update(dtype='float32', nodata=np.nan)
    with rasterio.open(out_path, 'w', **profile) as dst:
        dst.write(utci_grid, 1)

    print(f"  {hour:02d}시 완료 (유효 {valid.sum():,}/{seoul_mask.sum():,}, "
          f"UTCI {np.nanmin(utci_grid):.1f}~{np.nanmax(utci_grid):.1f}degC, "
          f"{time.time()-th:.1f}초)", flush=True)

avg = np.nanmean(list(utci_arrays.values()), axis=0)
with rasterio.open(os.path.join(OUT_DIR, 'UTCI_seoul_5m_kma_pixel_average.tif'), 'w', **profile) as dst:
    dst.write(avg.astype(np.float32), 1)

print(f"\n총 소요시간: {time.time()-t0:.1f}초 ({(time.time()-t0)/60:.1f}분)", flush=True)
print("픽셀 단위 KMA 격자기상 UTCI 산출 완료(서울 경계 클리핑)", flush=True)
