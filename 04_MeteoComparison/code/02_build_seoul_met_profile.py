"""
서울 전체 5m 파일럿 — SOLWEIG 기상입력 06~19시 대표 프로파일 생성
================================================================
01_build_seongdong_met_profile.py와 동일한 방법론, 공간범위만 성동구→서울 전체.
⚠️ 서울 전체를 이 단일 met.txt로 균일 적용하는 예비 버전 — 공간적으로 기상이
균일하다는 단순화를 전제함(축2 기상입력 방식 비교 미확정 상태의 임시 조치).

기간: 2025-07-23~08-03 (폭염일 12일)
- Ta, RH : S-DoT 서울 전체 센서 단순평균
- 풍속    : AWS 서울 전체 관측소(27개) 단순평균
- 일사    : ASOS 서울(108) 전천일사 → Erbs et al.(1982) 직달/확산 분리

출력: 04_MeteoComparison/results/seoul_met_profile_06_19h.csv,
      04_MeteoComparison/results/seoul_solweig_met.txt
"""

import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.dirname(BASE)
RES_DIR = os.path.join(BASE, 'results')
os.makedirs(RES_DIR, exist_ok=True)

SDOT_DIR = os.path.join(
    PROJ, 'data', 'S-DoT_NATURE_2025년(2025.01.01~2026.01.04)')
AWS_PATH = os.path.join(PROJ, 'data', 'OBS_AWS_TIM_20260707154958.csv')
ASOS_PATH = os.path.join(PROJ, 'data', 'OBS_ASOS_TIM_20260702021244.csv')

START_DATE = '2025-07-23'
END_DATE = '2025-08-03'
HOURS = range(6, 20)  # 06~19시


# ── 1. S-DoT 서울 전체 Ta/RH ─────────────────────────────────────────────
def load_sdot_seoul():
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
                          usecols=['시리얼', '측정시간', '자치구', '온도 평균(℃)', '습도 평균(%)'])
        frames.append(df)
    wk = pd.read_csv(weekly_file, encoding='cp949', header=None, skiprows=1,
                      usecols=[1, 2, 4, 7, 10],
                      names=['시리얼', '측정시간', '자치구', '온도 평균(℃)', '습도 평균(%)'])
    wk['date'] = wk['측정시간'].str[:10]
    wk = wk[wk['date'] >= '2025-08-01']
    frames.append(wk.drop(columns='date'))

    sdot = pd.concat(frames, ignore_index=True)
    # ⚠️ 성동구 필터 제거 — 서울 전체 자치구 사용
    sdot['dt'] = pd.to_datetime(sdot['측정시간'], format='%Y-%m-%d_%H:%M:%S')
    sdot['hour'] = sdot['dt'].dt.hour
    sdot = sdot[sdot['hour'].isin(HOURS)]
    sdot = sdot.dropna(subset=['온도 평균(℃)', '습도 평균(%)'])

    profile = (sdot.groupby('hour')[['온도 평균(℃)', '습도 평균(%)']]
               .mean()
               .rename(columns={'온도 평균(℃)': 'Ta', '습도 평균(%)': 'RH'}))
    n_sensors = sdot['시리얼'].nunique()
    n_gu = sdot['자치구'].nunique()
    print(f"S-DoT 서울 전체: 자치구 {n_gu}개, 센서 {n_sensors}개, {len(sdot):,}행 사용")
    return profile


# ── 2. AWS 서울 전체(27개 관측소) 풍속 ────────────────────────────────────
def load_aws_seoul():
    aws = pd.read_csv(AWS_PATH, encoding='cp949')
    aws['일시'] = pd.to_datetime(aws['일시'])
    aws['hour'] = aws['일시'].dt.hour
    aws = aws[aws['hour'].isin(HOURS)]
    aws = aws.dropna(subset=['풍속(m/s)'])
    profile = (aws.groupby('hour')[['풍속(m/s)']]
               .mean()
               .rename(columns={'풍속(m/s)': 'wind'}))
    n_station = aws['지점명'].nunique()
    print(f"AWS 서울 전체: 관측소 {n_station}개, {len(aws):,}행 사용")
    return profile


# ── 3. ASOS 서울(108) 일사 → Erbs 직달/확산 분리 (기존과 동일) ────────────
def cos_solar_zenith(hour, lat=37.5714, lon=126.9658, doy=200):
    lat_r = np.radians(lat)
    decl = np.radians(23.45 * np.sin(np.radians(360 / 365 * (284 + doy))))
    solar_time = hour + (lon - 135.0) / 15.0
    hour_angle = np.radians(15.0 * (solar_time - 12.0))
    cos_z = (np.sin(lat_r) * np.sin(decl) +
             np.cos(lat_r) * np.cos(decl) * np.cos(hour_angle))
    return float(max(cos_z, 0.0))


def split_radiation(ghi, cos_z):
    """Erbs et al. (1982) 직산분리모델"""
    if ghi <= 10 or cos_z < 0.01:
        return 0.0, float(ghi)
    kt = min(ghi / (1367.0 * cos_z), 1.0)
    if kt <= 0.22:
        kd = 1.0 - 0.09 * kt
    elif kt <= 0.80:
        kd = max(0.9511 - 0.1604 * kt + 4.388 * kt ** 2
                 - 16.638 * kt ** 3 + 12.336 * kt ** 4, 0.1)
    else:
        kd = 0.165
    return float(ghi * (1 - kd)), float(ghi * kd)


def load_asos_seoul():
    asos = pd.read_csv(ASOS_PATH, encoding='cp949')
    asos['일시'] = pd.to_datetime(asos['일시'])
    mask = (asos['일시'] >= START_DATE) & (asos['일시'] < pd.to_datetime(END_DATE) + pd.Timedelta(days=1))
    asos = asos[mask].copy()
    asos['hour'] = asos['일시'].dt.hour
    asos = asos[asos['hour'].isin(HOURS)]
    asos['GHI_Wm2'] = asos['일사(MJ/m2)'] * 1_000_000 / 3600

    ghi_profile = asos.groupby('hour')['GHI_Wm2'].mean()
    doy_mid = pd.Timestamp('2025-07-28').dayofyear

    rows = []
    for hour, ghi in ghi_profile.items():
        cos_z = cos_solar_zenith(hour, doy=doy_mid)
        kdir, kdiff = split_radiation(ghi, cos_z)
        rows.append({'hour': hour, 'kdown': ghi, 'kdir': kdir, 'kdiff': kdiff})
    print(f"ASOS 서울(108): {len(asos)}행 사용, DOY 기준일={doy_mid}")
    return pd.DataFrame(rows).set_index('hour')


# ── 4. 통합 ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    sdot_p = load_sdot_seoul()
    aws_p = load_aws_seoul()
    asos_p = load_asos_seoul()

    profile = sdot_p.join(aws_p, how='outer').join(asos_p, how='outer')
    profile = profile.round(2)
    profile.index.name = 'hour'

    out_path = os.path.join(RES_DIR, 'seoul_met_profile_06_19h.csv')
    profile.to_csv(out_path, encoding='utf-8-sig')

    print(f"\n저장: {out_path}")
    print(profile.to_string())

    IY, ID = 2025, pd.Timestamp('2025-07-28').dayofyear
    UNUSED = -999

    umep_rows = []
    for hour, row in profile.iterrows():
        umep_rows.append({
            'iy': IY, 'id': ID, 'it': int(hour), 'imin': 0,
            'qn': UNUSED, 'qh': UNUSED, 'qe': UNUSED, 'qs': UNUSED, 'qf': UNUSED,
            'U': row['wind'], 'RH': row['RH'], 'Tair': row['Ta'],
            'pres': UNUSED, 'rain': 0, 'kdown': row['kdown'],
            'snow': UNUSED, 'ldown': UNUSED, 'fcld': UNUSED,
            'wuh': UNUSED, 'xsmd': UNUSED, 'lai': UNUSED,
            'kdiff': row['kdiff'], 'kdir': row['kdir'], 'wdir': UNUSED,
        })
    umep_df = pd.DataFrame(umep_rows)
    met_path = os.path.join(RES_DIR, 'seoul_solweig_met.txt')
    umep_df.to_csv(met_path, sep=' ', index=False)
    print(f"\nSOLWEIG met.txt 저장: {met_path}")
    print(umep_df.to_string(index=False))
