"""성동구 v2(30m DEM소스,5m) vs v3(1m DEM소스,5m) vs 1mtrue(1m DEM소스,1m,9타일) 3자 비교
근거논문: 없음(자체 산출 비교 검증). v2/v3는 서울 전체 파이프라인에서 성동구만 클립한 것 —
2026-07-28_성동구_5m_1mtrue_비교결과.md의 approach2_5m(구버전) 대신 사용하는 올바른 기준선.
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

mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

BASE = '/Users/jin/석사논문/Thermal_Catchment'
TODAY = '2026-07-28'

V2_TMRT_DIR = os.path.join(BASE, '03_Method_C/results/clip_seongdong_v2_tmrt')
V2_UTCI_DIR = os.path.join(BASE, '03_Method_C/results/clip_seongdong_v2_utci')
V3_TMRT_DIR = os.path.join(BASE, '03_Method_C/results/clip_seongdong_v3_tmrt')
V3_UTCI_DIR = os.path.join(BASE, '03_Method_C/results/clip_seongdong_v3_utci')
TMRT1_DIR = os.path.join(BASE, '03_Method_C/results/solweig_seongdong_1mtrue_mosaic_local')
UTCI1_DIR = os.path.join(BASE, '03_Method_C/results/utci_seongdong_1mtrue_local')
LINK5_PATH = os.path.join(BASE, '03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg')
MET_CSV = os.path.join(BASE, '04_MeteoComparison/results/seongdong_met_profile_06_19h.csv')

FIG_DIR = os.path.join(BASE, '03_Method_C/results/figures/compare_v2v3_1mtrue_seongdong')
os.makedirs(FIG_DIR, exist_ok=True)
STATS_DIR = os.path.join(BASE, '03_Method_C/results/compare_v2v3_1mtrue_seongdong')
os.makedirs(STATS_DIR, exist_ok=True)

HOURS = list(range(6, 20))
HCODE = {h: (f'{h:02d}00N' if h == 6 else f'{h:02d}00D') for h in HOURS}
met = pd.read_csv(MET_CSV).set_index('hour')


def readclean(path):
    with rasterio.open(path) as src:
        arr = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None and not np.isnan(nodata):
            arr[arr == nodata] = np.nan
        arr[(arr <= -100) | (arr >= 200)] = np.nan
        return arr, src.transform, src.crs, src.width, src.height


def reproject_1m_to_5m(path1m, ref_transform, ref_crs, ref_w, ref_h):
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


# ---------- 픽셀 단위: 시간대별 스택 적재 ----------
v2t_stack, v3t_stack, m1t_stack = [], [], []
v2u_stack, v3u_stack, m1u_stack = [], [], []
rows = []
ref_tr = ref_crs = ref_w = ref_h = None

for h in HOURS:
    hc = HCODE[h]
    v2t, tr, crs, w, hh = readclean(os.path.join(V2_TMRT_DIR, f'Tmrt_seoul_5m_{hc}.tif'))
    v3t, _, _, _, _ = readclean(os.path.join(V3_TMRT_DIR, f'Tmrt_seoul_5m_{hc}.tif'))
    v2u, _, _, _, _ = readclean(os.path.join(V2_UTCI_DIR, f'UTCI_seoul_5m_PILOT_{h:02d}.tif'))
    v3u, _, _, _, _ = readclean(os.path.join(V3_UTCI_DIR, f'UTCI_seoul_5m_v3_{h:02d}.tif'))
    m1t = reproject_1m_to_5m(os.path.join(TMRT1_DIR, f'Tmrt_seongdong_1mtrue_{hc}.tif'), tr, crs, w, hh)
    m1u = reproject_1m_to_5m(os.path.join(UTCI1_DIR, f'UTCI_seongdong_1mtrue_{h:02d}.tif'), tr, crs, w, hh)

    ref_tr, ref_crs, ref_w, ref_h = tr, crs, w, hh
    v2t_stack.append(v2t); v3t_stack.append(v3t); m1t_stack.append(m1t)
    v2u_stack.append(v2u); v3u_stack.append(v3u); m1u_stack.append(m1u)

    def stat_pair(a, b):
        valid = ~(np.isnan(a) | np.isnan(b))
        d = b[valid] - a[valid]
        mae = np.mean(np.abs(d)); rmse = np.sqrt(np.mean(d**2))
        r = np.corrcoef(a[valid], b[valid])[0, 1]
        return mae, rmse, r, int(valid.sum())

    mae_v2v3t, rmse_v2v3t, r_v2v3t, _ = stat_pair(v2t, v3t)
    mae_v2m1t, rmse_v2m1t, r_v2m1t, _ = stat_pair(v2t, m1t)
    mae_v3m1t, rmse_v3m1t, r_v3m1t, n = stat_pair(v3t, m1t)
    mae_v2v3u, rmse_v2v3u, r_v2v3u, _ = stat_pair(v2u, v3u)
    mae_v2m1u, rmse_v2m1u, r_v2m1u, _ = stat_pair(v2u, m1u)
    mae_v3m1u, rmse_v3m1u, r_v3m1u, _ = stat_pair(v3u, m1u)

    valid_u = ~(np.isnan(v2u) | np.isnan(v3u) | np.isnan(m1u))
    hc_v2 = v2u[valid_u] >= 38; hc_v3 = v3u[valid_u] >= 38; hc_m1 = m1u[valid_u] >= 38
    agree_v2v3 = np.mean(hc_v2 == hc_v3) * 100
    agree_v2m1 = np.mean(hc_v2 == hc_m1) * 100
    agree_v3m1 = np.mean(hc_v3 == hc_m1) * 100

    rows.append(dict(hour=h,
                      Tmrt_MAE_v2v3=mae_v2v3t, Tmrt_r_v2v3=r_v2v3t,
                      Tmrt_MAE_v2_1mtrue=mae_v2m1t, Tmrt_r_v2_1mtrue=r_v2m1t,
                      Tmrt_MAE_v3_1mtrue=mae_v3m1t, Tmrt_r_v3_1mtrue=r_v3m1t,
                      UTCI_MAE_v2v3=mae_v2v3u, UTCI_r_v2v3=r_v2v3u,
                      UTCI_MAE_v2_1mtrue=mae_v2m1u, UTCI_r_v2_1mtrue=r_v2m1u,
                      UTCI_MAE_v3_1mtrue=mae_v3m1u, UTCI_r_v3_1mtrue=r_v3m1u,
                      HardCut38_v2v3=agree_v2v3, HardCut38_v2_1mtrue=agree_v2m1,
                      HardCut38_v3_1mtrue=agree_v3m1, n_valid=n))
    print(f'{h:02d}시 | v2vs v3: Tmrt r={r_v2v3t:.3f} UTCI r={r_v2v3u:.3f} HC={agree_v2v3:.1f}% '
          f'| v2 vs 1mtrue: Tmrt r={r_v2m1t:.3f} UTCI r={r_v2m1u:.3f} HC={agree_v2m1:.1f}% '
          f'| v3 vs 1mtrue: Tmrt r={r_v3m1t:.3f} UTCI r={r_v3m1u:.3f} HC={agree_v3m1:.1f}%', flush=True)

df_stats = pd.DataFrame(rows)
df_stats.to_csv(os.path.join(STATS_DIR, f'{TODAY}_hourly_stats_v2v3_1mtrue.csv'), index=False)

# ---------- 평균 기준 ----------
v2t_avg = np.nanmean(np.stack(v2t_stack), axis=0)
v3t_avg = np.nanmean(np.stack(v3t_stack), axis=0)
m1t_avg = np.nanmean(np.stack(m1t_stack), axis=0)
v2u_avg = np.nanmean(np.stack(v2u_stack), axis=0)
v3u_avg = np.nanmean(np.stack(v3u_stack), axis=0)
m1u_avg = np.nanmean(np.stack(m1u_stack), axis=0)


def summarize(a, b, label):
    valid = ~(np.isnan(a) | np.isnan(b))
    d = b[valid] - a[valid]
    mae = np.mean(np.abs(d)); rmse = np.sqrt(np.mean(d**2))
    r = np.corrcoef(a[valid], b[valid])[0, 1]
    print(f'[평균, {label}] MAE={mae:.3f} RMSE={rmse:.3f} r={r:.4f}')
    return mae, rmse, r


with open(os.path.join(STATS_DIR, f'{TODAY}_summary_stats.txt'), 'w') as f:
    f.write('[픽셀 평균 기준 — 3자 비교]\n')
    for label, a, b in [('Tmrt v2-v3', v2t_avg, v3t_avg), ('Tmrt v2-1mtrue', v2t_avg, m1t_avg),
                         ('Tmrt v3-1mtrue', v3t_avg, m1t_avg),
                         ('UTCI v2-v3', v2u_avg, v3u_avg), ('UTCI v2-1mtrue', v2u_avg, m1u_avg),
                         ('UTCI v3-1mtrue', v3u_avg, m1u_avg)]:
        mae, rmse, r = summarize(a, b, label)
        f.write(f'{label}: MAE={mae:.3f} RMSE={rmse:.3f} r={r:.4f}\n')
    valid_u = ~(np.isnan(v2u_avg) | np.isnan(v3u_avg) | np.isnan(m1u_avg))
    hc_v2 = v2u_avg[valid_u] >= 38; hc_v3 = v3u_avg[valid_u] >= 38; hc_m1 = m1u_avg[valid_u] >= 38
    f.write(f'HardCut38 일치(평균): v2-v3={np.mean(hc_v2==hc_v3)*100:.2f}% '
            f'v2-1mtrue={np.mean(hc_v2==hc_m1)*100:.2f}% v3-1mtrue={np.mean(hc_v3==hc_m1)*100:.2f}%\n')

print('픽셀 단위 3자 비교 완료', flush=True)

# ---------- 평균 비교맵 (Tmrt/UTCI 3단) ----------
vmin, vmax = np.nanpercentile(v3t_avg, 2), np.nanpercentile(v3t_avg, 98)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, arr, label in zip(axes, [v2t_avg, v3t_avg, m1t_avg], ['v2(30m소스,5m)', 'v3(1m소스,5m)', '1mtrue(1m소스,1m)']):
    im = ax.imshow(arr, cmap='inferno', vmin=vmin, vmax=vmax)
    ax.set_title(f'Tmrt 평균 - {label}'); ax.axis('off')
fig.colorbar(im, ax=axes, shrink=0.7, label='Tmrt (°C)')
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_Tmrt_avg_v2v3_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

vminu, vmaxu = np.nanpercentile(v3u_avg, 2), np.nanpercentile(v3u_avg, 98)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, arr, label in zip(axes, [v2u_avg, v3u_avg, m1u_avg], ['v2(30m소스,5m)', 'v3(1m소스,5m)', '1mtrue(1m소스,1m)']):
    im = ax.imshow(arr, cmap='inferno', vmin=vminu, vmax=vmaxu)
    ax.set_title(f'UTCI 평균 - {label}'); ax.axis('off')
fig.colorbar(im, ax=axes, shrink=0.7, label='UTCI (°C)')
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_UTCI_avg_v2v3_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

# ---------- 차이맵: v3 vs 1mtrue (가장 중요 — DEM소스 동일, 해상도만 다름) ----------
diff_t = m1t_avg - v3t_avg
diff_u = m1u_avg - v3u_avg
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
lim_t = np.nanpercentile(np.abs(diff_t), 98)
im0 = axes[0].imshow(diff_t, cmap='RdBu_r', vmin=-lim_t, vmax=lim_t)
axes[0].set_title('Tmrt 차이 (1mtrue - v3)'); axes[0].axis('off')
fig.colorbar(im0, ax=axes[0], shrink=0.8)
lim_u = np.nanpercentile(np.abs(diff_u), 98)
im1 = axes[1].imshow(diff_u, cmap='RdBu_r', vmin=-lim_u, vmax=lim_u)
axes[1].set_title('UTCI 차이 (1mtrue - v3)'); axes[1].axis('off')
fig.colorbar(im1, ax=axes[1], shrink=0.8)
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_diff_map_v3_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

# ---------- 산점도: v3 vs 1mtrue ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
valid_t = ~(np.isnan(v3t_avg) | np.isnan(m1t_avg))
samp = np.random.choice(np.where(valid_t.ravel())[0], size=min(50000, valid_t.sum()), replace=False)
x = v3t_avg.ravel()[samp]; y = m1t_avg.ravel()[samp]
axes[0].scatter(x, y, s=1, alpha=0.2)
lims = [min(x.min(), y.min()), max(x.max(), y.max())]
axes[0].plot(lims, lims, 'r--', lw=1)
axes[0].set_xlabel('Tmrt v3(5m)'); axes[0].set_ylabel('Tmrt 1mtrue(1m)')
r_t = np.corrcoef(v3t_avg[valid_t], m1t_avg[valid_t])[0, 1]
axes[0].set_title(f'Tmrt v3 vs 1mtrue r={r_t:.4f}')

valid_u = ~(np.isnan(v3u_avg) | np.isnan(m1u_avg))
sampu = np.random.choice(np.where(valid_u.ravel())[0], size=min(50000, valid_u.sum()), replace=False)
xu = v3u_avg.ravel()[sampu]; yu = m1u_avg.ravel()[sampu]
axes[1].scatter(xu, yu, s=1, alpha=0.2, color='darkorange')
limsu = [min(xu.min(), yu.min()), max(xu.max(), yu.max())]
axes[1].plot(limsu, limsu, 'r--', lw=1)
axes[1].set_xlabel('UTCI v3(5m)'); axes[1].set_ylabel('UTCI 1mtrue(1m)')
r_u = np.corrcoef(v3u_avg[valid_u], m1u_avg[valid_u])[0, 1]
axes[1].set_title(f'UTCI v3 vs 1mtrue r={r_u:.4f}')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_compare_scatter_v3_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

print('평균 비교맵/산점도 완료', flush=True)

# ---------- 링크 단위 (평균 기준, in-memory 배열 zonal_stats — 빠른 방식) ----------
links = gpd.read_file(LINK5_PATH)
links_buf = links.buffer(5.0)

for name, arrT, arrU in [('v2', v2t_avg, v2u_avg), ('v3', v3t_avg, v3u_avg), ('m1', m1t_avg, m1u_avg)]:
    st = zonal_stats(links_buf, arrT, affine=ref_tr, stats=['mean'], nodata=np.nan)
    links[f'Tmrt_{name}_avg'] = [s['mean'] for s in st]
    su = zonal_stats(links_buf, arrU, affine=ref_tr, stats=['mean'], nodata=np.nan)
    links[f'UTCI_{name}_avg'] = [s['mean'] for s in su]

for name in ['v2', 'v3', 'm1']:
    links[f'HardCut38_{name}'] = links[f'UTCI_{name}_avg'] >= 38

link_valid = links.dropna(subset=[f'Tmrt_{n}_avg' for n in ['v2', 'v3', 'm1']] +
                                  [f'UTCI_{n}_avg' for n in ['v2', 'v3', 'm1']])

with open(os.path.join(STATS_DIR, f'{TODAY}_summary_stats.txt'), 'a') as f:
    f.write(f'\n[링크 단위, n={len(link_valid)}]\n')
    for a, b, label in [('v2', 'v3', 'v2-v3'), ('v2', 'm1', 'v2-1mtrue'), ('v3', 'm1', 'v3-1mtrue')]:
        dT = link_valid[f'Tmrt_{b}_avg'] - link_valid[f'Tmrt_{a}_avg']
        maeT = np.mean(np.abs(dT)); rmseT = np.sqrt(np.mean(dT**2))
        rT = np.corrcoef(link_valid[f'Tmrt_{a}_avg'], link_valid[f'Tmrt_{b}_avg'])[0, 1]
        dU = link_valid[f'UTCI_{b}_avg'] - link_valid[f'UTCI_{a}_avg']
        maeU = np.mean(np.abs(dU)); rmseU = np.sqrt(np.mean(dU**2))
        rU = np.corrcoef(link_valid[f'UTCI_{a}_avg'], link_valid[f'UTCI_{b}_avg'])[0, 1]
        agree = np.mean(link_valid[f'HardCut38_{a}'] == link_valid[f'HardCut38_{b}']) * 100
        n_dis = (link_valid[f'HardCut38_{a}'] != link_valid[f'HardCut38_{b}']).sum()
        f.write(f'{label}: Tmrt MAE={maeT:.3f} RMSE={rmseT:.3f} r={rT:.4f} | '
                f'UTCI MAE={maeU:.3f} RMSE={rmseU:.3f} r={rU:.4f} | '
                f'HardCut38 일치={agree:.2f}% (불일치 {n_dis}/{len(link_valid)})\n')
        print(f'[링크, {label}] Tmrt MAE={maeT:.3f} r={rT:.4f} | UTCI MAE={maeU:.3f} r={rU:.4f} | '
              f'HardCut38 일치={agree:.2f}% (불일치 {n_dis})', flush=True)

links.to_file(os.path.join(STATS_DIR, f'{TODAY}_link_compare_v2v3_1mtrue_seongdong.gpkg'), driver='GPKG')

# v3 vs 1mtrue Hard Cut 불일치 지도(가장 중요한 쌍)
fig, ax = plt.subplots(figsize=(10, 10))
link_valid.plot(ax=ax, color='lightgray', linewidth=0.5)
disagree_v3m1 = link_valid[link_valid['HardCut38_v3'] != link_valid['HardCut38_m1']]
disagree_v3m1.plot(ax=ax, color='red', linewidth=1.5)
ax.set_title(f'Hard Cut(UTCI≥38°C) v3 vs 1mtrue 불일치 링크 ({len(disagree_v3m1)}개, 빨강)')
ax.axis('off')
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_link_hardcut38_disagreement_v3_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

# 링크 산점도 v3 vs 1mtrue
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].scatter(link_valid['Tmrt_v3_avg'], link_valid['Tmrt_m1_avg'], s=3, alpha=0.3)
lims = [link_valid['Tmrt_v3_avg'].min(), link_valid['Tmrt_v3_avg'].max()]
axes[0].plot(lims, lims, 'r--', lw=1)
axes[0].set_xlabel('링크 Tmrt v3(5m)'); axes[0].set_ylabel('링크 Tmrt 1mtrue(1m)')
r_link_t = np.corrcoef(link_valid['Tmrt_v3_avg'], link_valid['Tmrt_m1_avg'])[0, 1]
axes[0].set_title(f'링크 Tmrt r={r_link_t:.4f}')
axes[1].scatter(link_valid['UTCI_v3_avg'], link_valid['UTCI_m1_avg'], s=3, alpha=0.3, color='darkorange')
limsu = [link_valid['UTCI_v3_avg'].min(), link_valid['UTCI_v3_avg'].max()]
axes[1].plot(limsu, limsu, 'r--', lw=1)
axes[1].set_xlabel('링크 UTCI v3(5m)'); axes[1].set_ylabel('링크 UTCI 1mtrue(1m)')
r_link_u = np.corrcoef(link_valid['UTCI_v3_avg'], link_valid['UTCI_m1_avg'])[0, 1]
axes[1].set_title(f'링크 UTCI r={r_link_u:.4f}')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, f'{TODAY}_link_scatter_v3_1mtrue.png'), dpi=150, bbox_inches='tight')
plt.close()

print('\n링크 단위 3자 비교 완료. 전체 완료.', flush=True)
