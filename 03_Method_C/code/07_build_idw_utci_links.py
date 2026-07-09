"""
성동구 파일럿 — UTCI 산출 (IDW 보간 Ta/RH + 균일 풍속 + 링크별 Tmrt)
================================================================
- Ta/RH: S-DoT 서울 전체 지점(성동구만 아님) 기반 IDW 보간, leave-one-out CV로 최적
  power 선정 후 성동구 링크 위치에서 추출 (서울 전체로 보간 후 성동구만 보는 방식 —
  경계효과 방지)
- 풍속: AWS 성동(421) 균일값(met.txt와 동일, 보간 안 함 — 관련 인프라 없음)
- Tmrt: 이미 산출된 링크별 값(2026-07-09_link_tmrt_approach1_30m.csv)
- UTCI: pythermalcomfort (Bröde et al. 2012)
"""
import os
import glob
import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer
from pythermalcomfort.models import utci

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
SDOT_DIR = os.path.join(PROJ, 'data', 'S-DoT_NATURE_2025년(2025.01.01~2026.01.04)')
LOC_PATH = os.path.join(PROJ, 'data', '서울시 도시데이터 센서(S-DoT) 환경정보 설치 위치정보.xlsx')
LINK_TMRT_PATH = os.path.join(PROJ, '03_Method_C', 'results',
                              '2026-07-09_link_tmrt_approach1_30m.gpkg')
MET_PATH = os.path.join(PROJ, '04_MeteoComparison', 'results',
                        'seongdong_met_profile_06_19h.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results')

TARGET_CRS = 'EPSG:5186'
HOURS = list(range(6, 20))
wgs_to_5186 = Transformer.from_crs('EPSG:4326', TARGET_CRS, always_xy=True)


# ── 1. S-DoT 서울 전체 지점별 시간별 Ta/RH (12일 평균) ────────────────────
def load_sdot_seoul_by_station():
    daily_dir = os.path.join(SDOT_DIR, 'S-DoT_NATURE_2025.07')
    daily_files = [
        os.path.join(daily_dir, f'120_서울시 IOT 복합 센서(환경정보)_PUBDATA_{d}.csv')
        for d in ['20250723', '20250724', '20250725', '20250726',
                  '20250727', '20250728', '20250729', '20250730', '20250731']
    ]
    weekly_file = os.path.join(SDOT_DIR, 'S-DoT_NATURE_2025.07.28-08.03.csv')

    frames = []
    for path in daily_files:
        df = pd.read_csv(path, encoding='cp949',
                          usecols=['시리얼', '측정시간', '온도 평균(℃)', '습도 평균(%)'])
        frames.append(df)
    wk = pd.read_csv(weekly_file, encoding='cp949', header=None, skiprows=1,
                      usecols=[1, 2, 7, 10],
                      names=['시리얼', '측정시간', '온도 평균(℃)', '습도 평균(%)'])
    wk['date'] = wk['측정시간'].str[:10]
    wk = wk[wk['date'] >= '2025-08-01'].drop(columns='date')
    frames.append(wk)

    sdot = pd.concat(frames, ignore_index=True)
    sdot['dt'] = pd.to_datetime(sdot['측정시간'], format='%Y-%m-%d_%H:%M:%S')
    sdot['hour'] = sdot['dt'].dt.hour
    sdot = sdot[sdot['hour'].isin(HOURS)]

    station_hourly = (sdot.groupby(['시리얼', 'hour'])[['온도 평균(℃)', '습도 평균(%)']]
                       .mean().reset_index()
                       .rename(columns={'온도 평균(℃)': 'Ta', '습도 평균(%)': 'RH'}))
    print(f"  S-DoT 서울 전체: 지점 {station_hourly['시리얼'].nunique()}개, "
          f"{len(station_hourly)}행(지점x시간)")
    return station_hourly


print("S-DoT 서울 전체 지점별 시간별 Ta/RH 산출 중...")
station_hourly = load_sdot_seoul_by_station()

loc = pd.read_excel(LOC_PATH, sheet_name=0)
loc = loc.rename(columns={'모델 시리얼(*)': '시리얼', '위도': 'lat', '경도': 'lon'})[['시리얼', 'lat', 'lon']]
station_hourly = station_hourly.merge(loc, on='시리얼', how='inner')
print(f"  좌표 매칭 후: {station_hourly['시리얼'].nunique()}개 지점")

sx, sy = wgs_to_5186.transform(station_hourly['lon'].values, station_hourly['lat'].values)
station_hourly['sx'] = sx
station_hourly['sy'] = sy


# ── 2. IDW + Leave-one-out CV로 최적 power 선정 ───────────────────────────
def idw_predict(qx, qy, sx, sy, vals, power, exclude_idx=None):
    dx, dy = sx - qx, sy - qy
    dist = np.sqrt(dx**2 + dy**2)
    if exclude_idx is not None:
        dist = dist.copy()
        dist[exclude_idx] = np.inf
    if dist.min() < 1.0:
        return vals[dist.argmin()]
    w = 1.0 / dist**power
    return np.sum(w * vals) / np.sum(w)


n_before = len(station_hourly)
station_hourly = station_hourly.dropna(subset=['Ta', 'RH']).reset_index(drop=True)
print(f"  Ta/RH 결측 제거: {n_before} -> {len(station_hourly)}행")

print("\nIDW power leave-one-out 교차검증 중 (Ta 기준)...")
h_sample = station_hourly[station_hourly['hour'] == 13].reset_index(drop=True)
sx_a, sy_a, val_a = h_sample['sx'].values, h_sample['sy'].values, h_sample['Ta'].values
best_power, best_rmse = None, np.inf
for power in [1, 2, 3, 4]:
    preds = np.array([idw_predict(sx_a[i], sy_a[i], sx_a, sy_a, val_a, power, exclude_idx=i)
                       for i in range(len(sx_a))])
    rmse = np.sqrt(np.mean((preds - val_a)**2))
    print(f"  power={power}: RMSE={rmse:.3f}")
    if rmse < best_rmse:
        best_rmse, best_power = rmse, power
print(f"  선정된 power = {best_power} (RMSE={best_rmse:.3f})")


# ── 3. 성동구 링크 중심점에서 Ta/RH IDW 추출 (서울 전체 지점 사용) ─────────
print("\n성동구 링크 위치에서 Ta/RH 추출 중...")
links = gpd.read_file(LINK_TMRT_PATH)
links['cx'] = links.geometry.centroid.x
links['cy'] = links.geometry.centroid.y

met = pd.read_csv(MET_PATH)  # 균일 풍속(및 kdown 등) 참고용
wind_by_hour = met.set_index('hour')['wind'].to_dict()

result_rows = []
for h in HOURS:
    h_df = station_hourly[station_hourly['hour'] == h]
    sx_h, sy_h = h_df['sx'].values, h_df['sy'].values
    ta_h, rh_h = h_df['Ta'].values, h_df['RH'].values
    ta_link = np.array([idw_predict(cx, cy, sx_h, sy_h, ta_h, best_power)
                        for cx, cy in zip(links['cx'], links['cy'])])
    rh_link = np.array([idw_predict(cx, cy, sx_h, sy_h, rh_h, best_power)
                        for cx, cy in zip(links['cx'], links['cy'])])
    wind_h = wind_by_hour[h]
    tmrt_link = links[f'Tmrt_{h:02d}'].values

    utci_vals = []
    for ta, tr, rh_v in zip(ta_link, tmrt_link, rh_link):
        try:
            utci_vals.append(float(utci(tdb=ta, tr=tr, v=max(wind_h, 0.5), rh=rh_v)['utci']))
        except Exception:
            utci_vals.append(np.nan)

    links[f'Ta_idw_{h:02d}'] = ta_link
    links[f'RH_idw_{h:02d}'] = rh_link
    links[f'UTCI_{h:02d}'] = utci_vals
    print(f"  {h:02d}시 완료 (Ta_idw 평균={ta_link.mean():.1f}, UTCI 평균={np.nanmean(utci_vals):.1f})")

out_gpkg = os.path.join(OUT_DIR, '2026-07-09_link_utci_approach1_30m.gpkg')
links.drop(columns=['cx', 'cy']).to_file(out_gpkg, driver='GPKG')
out_csv = os.path.join(OUT_DIR, '2026-07-09_link_utci_approach1_30m.csv')
links.drop(columns=['cx', 'cy', 'geometry']).to_csv(out_csv, index=False, encoding='utf-8-sig')
print(f"\n저장: {out_gpkg}\n저장: {out_csv}")
