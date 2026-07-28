"""성동구 5m(approach2) vs 1mtrue(진짜 1m DEM, 9타일) 해상도 비교
근거논문: 없음(자체 산출 비교 검증 — 외부 문헌 인용 아님)
picles/link 단위 통계 + 시각화. compare_v2_v3_seoul.py 구조를 성동구 데이터에 맞춰 재구성.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.warp import reproject, Resampling
import matplotlib as mpl
import matplotlib.pyplot as plt
from pythermalcomfort.models import utci
from rasterstats import zonal_stats
import subprocess

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TODAY = subprocess.run(['date', '+%Y-%m-%d'], capture_output=True, text=True).stdout.strip()

TMRT5_DIR = os.path.join(BASE, '03_Method_C/results/solweig_approach2_5m')
UTCI5_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_5m_approach2')
TMRT1_DIR = os.path.join(BASE, '03_Method_C/results/solweig_seongdong_1mtrue_mosaic_local')
UTCI1_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_1mtrue_local')
LINK5_PATH = os.path.join(BASE, '03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg')
MET_CSV = os.path.join(BASE, '04_MeteoComparison/results/seongdong_met_profile_06_19h.csv')

FIG_DIR = os.path.join(BASE, '03_Method_C/results/figures/compare_5m_1mtrue_seongdong')
os.makedirs(FIG_DIR, exist_ok=True)
STATS_DIR = os.path.join(BASE, '03_Method_C/results/compare_5m_1mtrue_seongdong')
os.makedirs(STATS_DIR, exist_ok=True)

HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}

met = pd.read_csv(MET_CSV).set_index('hour')


def read5(path):
    with rasterio.open(path) as src:
        arr = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None and not np.isnan(nodata):
            arr[arr == nodata] = np.nan
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        return arr, src.profile, src.transform, src.crs, src.width, src.height


def reproject_to_5m(path1m, ref_transform, ref_crs, ref_w, ref_h):
    with rasterio.open(path1m) as src:
        src_arr = src.read(1).astype(np.float32)
        src_nodata = src.nodata
        if src_nodata is not None and not np.isnan(src_nodata):
            src_arr[src_arr == src_nodata] = np.nan
        dst_arr = np.full((ref_h, ref_w), np.nan, dtype=np.float32)
        reproject(
            source=src_arr, destination=dst_arr,
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=ref_transform, dst_crs=ref_crs,
            resampling=Resampling.average, src_nodata=np.nan, dst_nodata=np.nan,
        )
        return dst_arr


# ---------- 1. 픽셀 단위 시간대별 통계 ----------
rows = []
diff_tmrt_sum = None
diff_utci_sum = None
tmrt5_avg_arr = None
tmrt1_avg_arr = None
utci5_avg_arr = None
utci1_avg_arr = None
n_hours = 0

for h in HOURS:
    hc = HCODE[h]
    t5, prof5, tr5, crs5, w5, h5_ = read5(os.path.join(TMRT5_DIR, f'Tmrt_2025_209_{hc}.tif'))
    u5, _, _, _, _, _ = read5(os.path.join(UTCI5_DIR, f'UTCI_seongdong_5m_approach2_{h:02d}.tif'))
    t1_on5 = reproject_to_5m(os.path.join(TMRT1_DIR, f'Tmrt_seongdong_1mtrue_{hc}.tif'), tr5, crs5, w5, h5_)
    u1_on5 = reproject_to_5m(os.path.join(UTCI1_DIR, f'UTCI_seongdong_1mtrue_{h:02d}.tif'), tr5, crs5, w5, h5_)

    valid = ~(np.isnan(t5) | np.isnan(t1_on5))
    dt = t1_on5[valid] - t5[valid]
    valid_u = ~(np.isnan(u5) | np.isnan(u1_on5))
    du = u1_on5[valid_u] - u5[valid_u]

    mae_t = np.mean(np.abs(dt)); rmse_t = np.sqrt(np.mean(dt**2))
    r_t = np.corrcoef(t5[valid], t1_on5[valid])[0, 1]
    mae_u = np.mean(np.abs(du)); rmse_u = np.sqrt(np.mean(du**2))
    r_u = np.corrcoef(u5[valid_u], u1_on5[valid_u])[0, 1]

    hc38_5 = u5[valid_u] >= 38
    hc38_1 = u1_on5[valid_u] >= 38
    agree38 = np.mean(hc38_5 == hc38_1) * 100

    rows.append(dict(hour=h, MAE_Tmrt=mae_t, RMSE_Tmrt=rmse_t, r_Tmrt=r_t,
                      MAE_UTCI=mae_u, RMSE_UTCI=rmse_u, r_UTCI=r_u,
                      HardCut38_agree_pct=agree38, n_valid_px=int(valid.sum())))
    print(f'{h:02d}시: Tmrt MAE={mae_t:.3f} r={r_t:.4f} | UTCI MAE={mae_u:.3f} r={r_u:.4f} '
          f'| HardCut38 일치 {agree38:.2f}%', flush=True)

    if tmrt5_avg_arr is None:
        tmrt5_stack = []; tmrt1_stack = []; utci5_stack = []; utci1_stack = []
    tmrt5_stack.append(t5); tmrt1_stack.append(t1_on5)
    utci5_stack.append(u5); utci1_stack.append(u1_on5)
    n_hours += 1

# 픽셀별로 유효한 시간대만 평균(np.nanmean) — 그리드 경계에서 유효 시간대 수가
# 서로 다른 문제를 회피(이전 nansum 누적 방식의 버그 수정, 2026-07-28)
tmrt5_avg_arr = np.nanmean(np.stack(tmrt5_stack), axis=0)
tmrt1_avg_arr = np.nanmean(np.stack(tmrt1_stack), axis=0)
utci5_avg_arr = np.nanmean(np.stack(utci5_stack), axis=0)
utci1_avg_arr = np.nanmean(np.stack(utci1_stack), axis=0)

df_stats = pd.DataFrame(rows)
df_stats.to_csv(os.path.join(STATS_DIR, f'{TODAY}_hourly_stats_5m_vs_1mtrue.csv'), index=False)

# 평균 기준 종합 통계
valid_avg = ~(np.isnan(tmrt5_avg_arr) | np.isnan(tmrt1_avg_arr))
mae_t_avg = np.mean(np.abs(tmrt1_avg_arr[valid_avg] - tmrt5_avg_arr[valid_avg]))
rmse_t_avg = np.sqrt(np.mean((tmrt1_avg_arr[valid_avg] - tmrt5_avg_arr[valid_avg])**2))
r_t_avg = np.corrcoef(tmrt5_avg_arr[valid_avg], tmrt1_avg_arr[valid_avg])[0, 1]
valid_avg_u = ~(np.isnan(utci5_avg_arr) | np.isnan(utci1_avg_arr))
mae_u_avg = np.mean(np.abs(utci1_avg_arr[valid_avg_u] - utci5_avg_arr[valid_avg_u]))
rmse_u_avg = np.sqrt(np.mean((utci1_avg_arr[valid_avg_u] - utci5_avg_arr[valid_avg_u])**2))
r_u_avg = np.corrcoef(utci5_avg_arr[valid_avg_u], utci1_avg_arr[valid_avg_u])[0, 1]
hc38_avg_agree = np.mean((utci5_avg_arr[valid_avg_u] >= 38) == (utci1_avg_arr[valid_avg_u] >= 38)) * 100

print(f'\n[평균 기준] Tmrt MAE={mae_t_avg:.3f} RMSE={rmse_t_avg:.3f} r={r_t_avg:.4f}')
print(f'[평균 기준] UTCI MAE={mae_u_avg:.3f} RMSE={rmse_u_avg:.3f} r={r_u_avg:.4f} HardCut38일치={hc38_avg_agree:.2f}%')

with open(os.path.join(STATS_DIR, f'{TODAY}_summary_stats.txt'), 'w') as f:
    f.write(f'[픽셀 평균 기준]\nTmrt: MAE={mae_t_avg:.3f} RMSE={rmse_t_avg:.3f} r={r_t_avg:.4f}\n')
    f.write(f'UTCI: MAE={mae_u_avg:.3f} RMSE={rmse_u_avg:.3f} r={r_u_avg:.4f} HardCut38(pixel)={hc38_avg_agree:.2f}%\n')

# ---------- 2. 평균 비교맵 + 차이맵 + 산점도 (픽셀) ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
vmin, vmax = np.nanpercentile(tmrt5_avg_arr, 2), np.nanpercentile(tmrt5_avg_arr, 98)
im0 = axes[0].imshow(tmrt5_avg_arr, cmap='inferno', vmin=vmin, vmax=vmax)
axes[0].set_title('Tmrt 평균 - 5m(approach2)'); axes[0].axis('off')
im1 = axes[1].imshow(tmrt1_avg_arr, cmap='inferno', vmin=vmin, vmax=vmax)
axes[1].set_title('Tmrt 평균 - 1mtrue(5m격자 리샘플)'); axes[1].axis('off')
fig.colorbar(im1, ax=axes, shrink=0.8, label='Tmrt (°C)')
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_Tmrt_avg_5m_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
vminu, vmaxu = np.nanpercentile(utci5_avg_arr, 2), np.nanpercentile(utci5_avg_arr, 98)
im0 = axes[0].imshow(utci5_avg_arr, cmap='inferno', vmin=vminu, vmax=vmaxu)
axes[0].set_title('UTCI 평균 - 5m(approach2)'); axes[0].axis('off')
im1 = axes[1].imshow(utci1_avg_arr, cmap='inferno', vmin=vminu, vmax=vmaxu)
axes[1].set_title('UTCI 평균 - 1mtrue(5m격자 리샘플)'); axes[1].axis('off')
fig.colorbar(im1, ax=axes, shrink=0.8, label='UTCI (°C)')
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_UTCI_avg_5m_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

diff_t = tmrt1_avg_arr - tmrt5_avg_arr
diff_u = utci1_avg_arr - utci5_avg_arr
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
lim_t = np.nanpercentile(np.abs(diff_t), 98)
im0 = axes[0].imshow(diff_t, cmap='RdBu_r', vmin=-lim_t, vmax=lim_t)
axes[0].set_title('Tmrt 차이 (1mtrue - 5m)'); axes[0].axis('off')
fig.colorbar(im0, ax=axes[0], shrink=0.8)
lim_u = np.nanpercentile(np.abs(diff_u), 98)
im1 = axes[1].imshow(diff_u, cmap='RdBu_r', vmin=-lim_u, vmax=lim_u)
axes[1].set_title('UTCI 차이 (1mtrue - 5m)'); axes[1].axis('off')
fig.colorbar(im1, ax=axes[1], shrink=0.8)
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_diff_map_5m_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
samp = np.random.choice(np.where(valid_avg.ravel())[0], size=min(50000, valid_avg.sum()), replace=False)
x = tmrt5_avg_arr.ravel()[samp]; y = tmrt1_avg_arr.ravel()[samp]
axes[0].scatter(x, y, s=1, alpha=0.2)
lims = [min(x.min(), y.min()), max(x.max(), y.max())]
axes[0].plot(lims, lims, 'r--', lw=1)
axes[0].set_xlabel('Tmrt 5m'); axes[0].set_ylabel('Tmrt 1mtrue')
axes[0].set_title(f'Tmrt r={r_t_avg:.4f}, MAE={mae_t_avg:.2f}')
sampu = np.random.choice(np.where(valid_avg_u.ravel())[0], size=min(50000, valid_avg_u.sum()), replace=False)
xu = utci5_avg_arr.ravel()[sampu]; yu = utci1_avg_arr.ravel()[sampu]
axes[1].scatter(xu, yu, s=1, alpha=0.2, color='darkorange')
limsu = [min(xu.min(), yu.min()), max(xu.max(), yu.max())]
axes[1].plot(limsu, limsu, 'r--', lw=1)
axes[1].set_xlabel('UTCI 5m'); axes[1].set_ylabel('UTCI 1mtrue')
axes[1].set_title(f'UTCI r={r_u_avg:.4f}, MAE={mae_u_avg:.2f}')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_scatter_5m_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

print('픽셀 단위 비교 완료', flush=True)

# ---------- 3. 링크 단위 비교 ----------
# 주의(2026-07-28): 시간대별 zonal_stats를 1m 원본 래스터 28회(14시간×2변수) 파일
# 단위로 돌리는 최초 버전은 1시간 넘게 걸려 중단 — 대신 이미 메모리에 있는
# "5m 격자로 리샘플된 평균 배열"(픽셀 비교 단계에서 계산됨)을 배열째로 zonal_stats에
# 전달하는 방식으로 교체(파일 재오픈 없음, 평균 기준만 — 시간대별 링크값은 생략).
links = gpd.read_file(LINK5_PATH)
Ta_avg = met['Ta'].mean(); RH_avg = met['RH'].mean(); wind_avg = met['wind'].mean()
links['Tmrt5_avg'] = links[[f'Tmrt_{h:02d}' for h in HOURS]].mean(axis=1)
r_avg = utci(tdb=Ta_avg, tr=links['Tmrt5_avg'].tolist(), v=wind_avg, rh=RH_avg,
             limit_inputs=False, round_output=False)
links['UTCI5_avg'] = np.array(r_avg.utci)

BUFFER_M = 5.0
links_buf = links.buffer(BUFFER_M)
stats_t = zonal_stats(links_buf, tmrt1_avg_arr, affine=tr5, stats=['mean'], nodata=np.nan)
links['Tmrt1_avg'] = [s['mean'] for s in stats_t]
stats_u = zonal_stats(links_buf, utci1_avg_arr, affine=tr5, stats=['mean'], nodata=np.nan)
links['UTCI1_avg'] = [s['mean'] for s in stats_u]
links['HardCut38_5'] = links['UTCI5_avg'] >= 38
links['HardCut38_1'] = links['UTCI1_avg'] >= 38
links['HardCut38_agree'] = links['HardCut38_5'] == links['HardCut38_1']

link_valid = links.dropna(subset=['Tmrt5_avg', 'Tmrt1_avg', 'UTCI5_avg', 'UTCI1_avg'])
link_mae_t = np.mean(np.abs(link_valid['Tmrt1_avg'] - link_valid['Tmrt5_avg']))
link_rmse_t = np.sqrt(np.mean((link_valid['Tmrt1_avg'] - link_valid['Tmrt5_avg'])**2))
link_r_t = np.corrcoef(link_valid['Tmrt5_avg'], link_valid['Tmrt1_avg'])[0, 1]
link_mae_u = np.mean(np.abs(link_valid['UTCI1_avg'] - link_valid['UTCI5_avg']))
link_rmse_u = np.sqrt(np.mean((link_valid['UTCI1_avg'] - link_valid['UTCI5_avg'])**2))
link_r_u = np.corrcoef(link_valid['UTCI5_avg'], link_valid['UTCI1_avg'])[0, 1]
link_hc_agree = link_valid['HardCut38_agree'].mean() * 100
n_disagree = (~link_valid['HardCut38_agree']).sum()

print(f'\n[링크 단위, n={len(link_valid)}] Tmrt MAE={link_mae_t:.3f} RMSE={link_rmse_t:.3f} r={link_r_t:.4f}')
print(f'[링크 단위] UTCI MAE={link_mae_u:.3f} RMSE={link_rmse_u:.3f} r={link_r_u:.4f} '
      f'HardCut38일치={link_hc_agree:.2f}% (불일치 {n_disagree}개)')

with open(os.path.join(STATS_DIR, f'{TODAY}_summary_stats.txt'), 'a') as f:
    f.write(f'\n[링크 단위, n={len(link_valid)}]\n')
    f.write(f'Tmrt: MAE={link_mae_t:.3f} RMSE={link_rmse_t:.3f} r={link_r_t:.4f}\n')
    f.write(f'UTCI: MAE={link_mae_u:.3f} RMSE={link_rmse_u:.3f} r={link_r_u:.4f} '
            f'HardCut38(link)={link_hc_agree:.2f}% (불일치 {n_disagree}/{len(link_valid)})\n')

links.to_file(os.path.join(STATS_DIR, f'{TODAY}_link_compare_5m_1mtrue_seongdong.gpkg'), driver='GPKG')

# 링크 Hard Cut 불일치 지도
fig, ax = plt.subplots(figsize=(10, 10))
link_valid.plot(ax=ax, color='lightgray', linewidth=0.5)
link_valid[~link_valid['HardCut38_agree']].plot(ax=ax, color='red', linewidth=1.5)
ax.set_title(f'Hard Cut(UTCI≥38°C) 5m vs 1mtrue 불일치 링크 ({n_disagree}개, 빨강)')
ax.axis('off')
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_link_hardcut38_disagreement.png'), dpi=150, bbox_inches='tight')
plt.close()

# 링크 평균 Tmrt/UTCI 비교 산점도
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].scatter(link_valid['Tmrt5_avg'], link_valid['Tmrt1_avg'], s=3, alpha=0.3)
lims = [link_valid['Tmrt5_avg'].min(), link_valid['Tmrt5_avg'].max()]
axes[0].plot(lims, lims, 'r--', lw=1)
axes[0].set_xlabel('링크 Tmrt 5m'); axes[0].set_ylabel('링크 Tmrt 1mtrue')
axes[0].set_title(f'링크 Tmrt r={link_r_t:.4f}')
axes[1].scatter(link_valid['UTCI5_avg'], link_valid['UTCI1_avg'], s=3, alpha=0.3, color='darkorange')
limsu = [link_valid['UTCI5_avg'].min(), link_valid['UTCI5_avg'].max()]
axes[1].plot(limsu, limsu, 'r--', lw=1)
axes[1].set_xlabel('링크 UTCI 5m'); axes[1].set_ylabel('링크 UTCI 1mtrue')
axes[1].set_title(f'링크 UTCI r={link_r_u:.4f}')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_link_scatter_5m_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

print('\n링크 단위 비교 완료. 전체 완료.', flush=True)
