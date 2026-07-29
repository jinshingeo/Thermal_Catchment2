"""성동구 5m/10m/30m(clean, 1mtrue 다운샘플 소스) 각각을 1mtrue(기준값)와 비교해 정밀도 산출
근거논문: 없음(자체 산출 비교). compare_v2v3_1mtrue_seongdong.py와 동일 방법(픽셀+링크 r/MAE,
HardCut38 일치율). 각 RES는 1mtrue와 지형/건물/수목 데이터가 완전히 동일(같은 소스를
다운샘플)하므로 순수한 해상도 효과만 측정한다.
"""
import os
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.warp import reproject, Resampling
from pythermalcomfort.models import utci
from rasterstats import zonal_stats

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TODAY = '2026-07-29'
TMRT1_DIR = os.path.join(BASE, '03_Method_C/results/solweig_seongdong_1mtrue_mosaic_local')
UTCI1_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_1mtrue_local')
LINK_SRC = os.path.join(BASE, '03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg')
STATS_DIR = os.path.join(BASE, '03_Method_C/results/compare_resolution_tradeoff')
os.makedirs(STATS_DIR, exist_ok=True)

HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}


def readclean(path):
    with rasterio.open(path) as src:
        arr = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None and not np.isnan(nodata):
            arr[arr == nodata] = np.nan
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        return arr, src.transform, src.crs, src.width, src.height


def reproject_1m_to_target(path1m, ref_transform, ref_crs, ref_w, ref_h):
    with rasterio.open(path1m) as src:
        src_arr = src.read(1).astype(np.float32)
        src_nodata = src.nodata
        if src_nodata is not None and not np.isnan(src_nodata):
            src_arr[src_arr == src_nodata] = np.nan
        dst_arr = np.full((ref_h, ref_w), np.nan, dtype=np.float32)
        reproject(source=src_arr, destination=dst_arr,
                  src_transform=src.transform, src_crs=src.crs,
                  dst_transform=ref_transform, dst_crs=ref_crs,
                  resampling=Resampling.average, src_nodata=np.nan, dst_nodata=np.nan)
        return dst_arr


def run_for_resolution(res_label, tmrt_dir, utci_dir, tmrt_prefix, utci_prefix):
    """res_label: '5m','10m','30m'. tmrt_prefix/utci_prefix: 파일명 접두어"""
    t_stack, u_stack, m1t_stack, m1u_stack = [], [], [], []
    ref_tr = ref_crs = ref_w = ref_h = None
    for h in HOURS:
        hc = HCODE[h]
        t, tr, crs, w, hh = readclean(os.path.join(tmrt_dir, f'{tmrt_prefix}_{hc}.tif'))
        u, _, _, _, _ = readclean(os.path.join(utci_dir, f'{utci_prefix}_{h:02d}.tif'))
        m1t = reproject_1m_to_target(os.path.join(TMRT1_DIR, f'Tmrt_seongdong_1mtrue_{hc}.tif'), tr, crs, w, hh)
        m1u = reproject_1m_to_target(os.path.join(UTCI1_DIR, f'UTCI_seongdong_1mtrue_{h:02d}.tif'), tr, crs, w, hh)
        ref_tr, ref_crs, ref_w, ref_h = tr, crs, w, hh
        t_stack.append(t); u_stack.append(u); m1t_stack.append(m1t); m1u_stack.append(m1u)

    t_avg = np.nanmean(np.stack(t_stack), axis=0)
    u_avg = np.nanmean(np.stack(u_stack), axis=0)
    m1t_avg = np.nanmean(np.stack(m1t_stack), axis=0)
    m1u_avg = np.nanmean(np.stack(m1u_stack), axis=0)

    valid_t = ~(np.isnan(t_avg) | np.isnan(m1t_avg))
    dT = m1t_avg[valid_t] - t_avg[valid_t]
    mae_t = np.mean(np.abs(dT)); rmse_t = np.sqrt(np.mean(dT**2))
    r_t = np.corrcoef(t_avg[valid_t], m1t_avg[valid_t])[0, 1]

    valid_u = ~(np.isnan(u_avg) | np.isnan(m1u_avg))
    dU = m1u_avg[valid_u] - u_avg[valid_u]
    mae_u = np.mean(np.abs(dU)); rmse_u = np.sqrt(np.mean(dU**2))
    r_u = np.corrcoef(u_avg[valid_u], m1u_avg[valid_u])[0, 1]
    hc_agree_px = np.mean((u_avg[valid_u] >= 38) == (m1u_avg[valid_u] >= 38)) * 100

    # 링크 단위
    links = gpd.read_file(LINK_SRC)
    links_buf = links.buffer(links['width_final'] / 2)
    st_t = zonal_stats(links_buf, t_avg, affine=ref_tr, stats=['mean'], nodata=np.nan, all_touched=True)
    links['Tmrt_res'] = [s['mean'] for s in st_t]
    st_u = zonal_stats(links_buf, u_avg, affine=ref_tr, stats=['mean'], nodata=np.nan, all_touched=True)
    links['UTCI_res'] = [s['mean'] for s in st_u]
    st_t1 = zonal_stats(links_buf, m1t_avg, affine=ref_tr, stats=['mean'], nodata=np.nan, all_touched=True)
    links['Tmrt_1mtrue'] = [s['mean'] for s in st_t1]
    st_u1 = zonal_stats(links_buf, m1u_avg, affine=ref_tr, stats=['mean'], nodata=np.nan, all_touched=True)
    links['UTCI_1mtrue'] = [s['mean'] for s in st_u1]

    lv = links.dropna(subset=['Tmrt_res', 'Tmrt_1mtrue', 'UTCI_res', 'UTCI_1mtrue'])
    link_mae_t = np.mean(np.abs(lv['Tmrt_1mtrue'] - lv['Tmrt_res']))
    link_r_t = np.corrcoef(lv['Tmrt_res'], lv['Tmrt_1mtrue'])[0, 1]
    link_mae_u = np.mean(np.abs(lv['UTCI_1mtrue'] - lv['UTCI_res']))
    link_r_u = np.corrcoef(lv['UTCI_res'], lv['UTCI_1mtrue'])[0, 1]
    hc_res = lv['UTCI_res'] >= 38
    hc_1m = lv['UTCI_1mtrue'] >= 38
    link_hc_agree = np.mean(hc_res == hc_1m) * 100
    n_disagree = int((hc_res != hc_1m).sum())

    result = dict(resolution=res_label,
                  pixel_Tmrt_MAE=mae_t, pixel_Tmrt_r=r_t,
                  pixel_UTCI_MAE=mae_u, pixel_UTCI_r=r_u, pixel_HardCut38_agree_pct=hc_agree_px,
                  link_Tmrt_MAE=link_mae_t, link_Tmrt_r=link_r_t,
                  link_UTCI_MAE=link_mae_u, link_UTCI_r=link_r_u,
                  link_HardCut38_agree_pct=link_hc_agree, link_n_disagree=n_disagree,
                  link_n_total=len(lv))
    print(f'[{res_label}] 픽셀 Tmrt r={r_t:.4f} MAE={mae_t:.3f} | UTCI r={r_u:.4f} MAE={mae_u:.3f} '
          f'HC={hc_agree_px:.2f}% || 링크 Tmrt r={link_r_t:.4f} | UTCI r={link_r_u:.4f} '
          f'HC={link_hc_agree:.2f}%({n_disagree}/{len(lv)})', flush=True)
    return result


if __name__ == '__main__':
    results = []
    results.append(run_for_resolution(
        '1m', TMRT1_DIR, UTCI1_DIR,
        'Tmrt_seongdong_1mtrue', 'UTCI_seongdong_1mtrue'))
    results.append(run_for_resolution(
        '5m', os.path.join(BASE, '03_Method_C/results/solweig_seongdong_5m_clean_local'),
        os.path.join(BASE, '03_Method_C/results/utci_seongdong_5m_clean_local'),
        'Tmrt_2025_209', 'UTCI_seongdong_5m_clean'))
    results.append(run_for_resolution(
        '15m', os.path.join(BASE, '03_Method_C/results/solweig_seongdong_15m_clean_local'),
        os.path.join(BASE, '03_Method_C/results/utci_seongdong_15m_clean_local'),
        'Tmrt_2025_209', 'UTCI_seongdong_15m_clean'))
    results.append(run_for_resolution(
        '10m', os.path.join(BASE, '03_Method_C/results/solweig_seongdong_10m_clean_local'),
        os.path.join(BASE, '03_Method_C/results/utci_seongdong_10m_clean_local'),
        'Tmrt_2025_209', 'UTCI_seongdong_10m_clean'))
    results.append(run_for_resolution(
        '30m', os.path.join(BASE, '03_Method_C/results/solweig_seongdong_30m_clean_local'),
        os.path.join(BASE, '03_Method_C/results/utci_seongdong_30m_clean_local'),
        'Tmrt_2025_209', 'UTCI_seongdong_30m_clean'))

    df = pd.DataFrame(results)
    out_csv = os.path.join(STATS_DIR, f'{TODAY}_precision_vs_1mtrue_v3.csv')
    df.to_csv(out_csv, index=False)
    print(f'\n저장: {out_csv}')
    print(df.to_string(index=False))
