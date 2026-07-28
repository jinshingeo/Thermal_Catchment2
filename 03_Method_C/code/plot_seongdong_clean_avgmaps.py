"""성동구 5m/30m(clean) — Tmrt/UTCI 평균맵만 간단히(1mtrue/10m 수준 풀세트 아님)"""
import os
import numpy as np
import rasterio
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TODAY = '2026-07-29'
HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}


def make_avg_maps(res_label, tmrt_dir, utci_dir, tmrt_prefix, utci_prefix, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    tmrt_list, utci_list = [], []
    for h in HOURS:
        with rasterio.open(os.path.join(tmrt_dir, f'{tmrt_prefix}_{HCODE[h]}.tif')) as src:
            a = src.read(1).astype(np.float32)
            a[(a <= -100) | (a >= 200)] = np.nan
            tmrt_list.append(a)
        with rasterio.open(os.path.join(utci_dir, f'{utci_prefix}_{h:02d}.tif')) as src:
            a = src.read(1).astype(np.float32)
            a[(a <= -100) | (a >= 200)] = np.nan
            utci_list.append(a)
    tmrt_avg = np.nanmean(tmrt_list, axis=0)
    utci_avg = np.nanmean(utci_list, axis=0)

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(tmrt_avg, cmap='inferno')
    ax.axis('off'); ax.set_title(f'성동구 {res_label}(clean) — Tmrt 평균(06-19시)', fontsize=13)
    fig.colorbar(im, ax=ax, shrink=0.8, label='Tmrt (°C)')
    p = os.path.join(out_dir, f'{TODAY}_Tmrt_average_seongdong_{res_label}.png')
    fig.savefig(p, dpi=150, bbox_inches='tight'); plt.close(fig)
    print('저장:', p)

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(utci_avg, cmap='inferno')
    ax.axis('off'); ax.set_title(f'성동구 {res_label}(clean) — UTCI 평균(06-19시)', fontsize=13)
    fig.colorbar(im, ax=ax, shrink=0.8, label='UTCI (°C)')
    p = os.path.join(out_dir, f'{TODAY}_UTCI_average_seongdong_{res_label}.png')
    fig.savefig(p, dpi=150, bbox_inches='tight'); plt.close(fig)
    print('저장:', p)


make_avg_maps('5m', os.path.join(BASE, '03_Method_C/results/solweig_seongdong_5m_clean_local'),
              os.path.join(BASE, '03_Method_C/results/utci_seongdong_5m_clean_local'),
              'Tmrt_2025_209', 'UTCI_seongdong_5m_clean',
              os.path.join(BASE, '03_Method_C/results/figures/seongdong_5m_clean_standalone'))

make_avg_maps('30m', os.path.join(BASE, '03_Method_C/results/solweig_seongdong_30m_clean_local'),
              os.path.join(BASE, '03_Method_C/results/utci_seongdong_30m_clean_local'),
              'Tmrt_2025_209', 'UTCI_seongdong_30m_clean',
              os.path.join(BASE, '03_Method_C/results/figures/seongdong_30m_clean_standalone'))

print('\n5m/30m 평균맵 완료')
