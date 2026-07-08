"""
성동구 파일럿 — SOLWEIG 기상입력 06~19시 대표 프로파일 생성
================================================================
기간: 2025-07-23~08-03 (폭염일 12일)
- Ta, RH : S-DoT 성동구 전체 센서 단순평균 (역내 지점이라 보간 불필요)
- 풍속    : AWS 성동(421) 지점 (S-DoT는 풍속 센서 결측이라 사용 불가)
- 일사    : ASOS 서울(108) 전천일사 → Erbs et al.(1982) 직달/확산 분리

참고문헌:
  Erbs, D.G., Klein, S.A., Duffie, J.A. (1982). Estimation of the diffuse
  radiation fraction for hourly, daily and monthly-average global radiation.
  Solar Energy, 28(4), 293-302.

출력: 04_MeteoComparison/results/seongdong_met_profile_06_19h.csv
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


# ── 1. S-DoT 성동구 Ta/RH ────────────────────────────────────────────────
def load_sdot_seongdong():
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
    # 주간 병합파일: 데이터행이 헤더(58컬럼)보다 필드 6개 더 많음(끝에 빈 컬럼 6개 추가됨) →
    # 이름 대신 위치(index)로 읽어서 컬럼 밀림 방지
    wk = pd.read_csv(weekly_file, encoding='cp949', header=None, skiprows=1,
                      usecols=[1, 2, 4, 7, 10],
                      names=['시리얼', '측정시간', '자치구', '온도 평균(℃)', '습도 평균(%)'])
    # 주간 병합파일에서 07-28~07-31 중복분 제외, 08-01~08-03만 사용
    wk['date'] = wk['측정시간'].str[:10]
    wk = wk[wk['date'] >= '2025-08-01']
    frames.append(wk.drop(columns='date'))

    sdot = pd.concat(frames, ignore_index=True)
    sdot = sdot[sdot['자치구'] == 'Seongdong-gu'].copy()
    sdot['dt'] = pd.to_datetime(sdot['측정시간'], format='%Y-%m-%d_%H:%M:%S')
    sdot['hour'] = sdot['dt'].dt.hour
    sdot = sdot[sdot['hour'].isin(HOURS)]

    profile = (sdot.groupby('hour')[['온도 평균(℃)', '습도 평균(%)']]
               .mean()
               .rename(columns={'온도 평균(℃)': 'Ta', '습도 평균(%)': 'RH'}))
    n_sensors = sdot['시리얼'].nunique()
    print(f"S-DoT 성동구: 센서 {n_sensors}개, {len(sdot):,}행 사용")
    return profile


# ── 2. AWS 성동(421) 풍속 ────────────────────────────────────────────────
def load_aws_seongdong():
    """풍향(deg)은 제외: (1) 원형 변수라 산술평균이 무의미(350도·10도 평균→180도로
    정반대 값이 나옴, 벡터평균 필요) (2) SOLWEIG Tmrt·UTCI 공식 모두 풍속만 쓰고
    풍향은 쓰지 않아 애초에 met.txt에 넣을 이유가 없음 → -999 처리"""
    aws = pd.read_csv(AWS_PATH, encoding='cp949')
    aws['일시'] = pd.to_datetime(aws['일시'])
    aws = aws[aws['지점명'] == '성동'].copy()
    aws['hour'] = aws['일시'].dt.hour
    aws = aws[aws['hour'].isin(HOURS)]
    profile = (aws.groupby('hour')[['풍속(m/s)']]
               .mean()
               .rename(columns={'풍속(m/s)': 'wind'}))
    print(f"AWS 성동(421): {len(aws)}행 사용")
    return profile


# ── 3. ASOS 서울(108) 일사 → Erbs 직달/확산 분리 ─────────────────────────
def cos_solar_zenith(hour, lat=37.5714, lon=126.9658, doy=200):
    """DOY=200은 폭염기간(7/23~8/3) 대략 중앙일(7/19경)에 가까운 절기값 근사가 아니라
    실제 분석기간 중앙일(2025-07-28 -> DOY 209)로 맞춤"""
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
    return float(ghi * (1 - kd)), float(ghi * kd)  # (직달, 확산)


def load_asos_seoul():
    asos = pd.read_csv(ASOS_PATH, encoding='cp949')
    asos['일시'] = pd.to_datetime(asos['일시'])
    mask = (asos['일시'] >= START_DATE) & (asos['일시'] < pd.to_datetime(END_DATE) + pd.Timedelta(days=1))
    asos = asos[mask].copy()
    asos['hour'] = asos['일시'].dt.hour
    asos = asos[asos['hour'].isin(HOURS)]
    asos['GHI_Wm2'] = asos['일사(MJ/m2)'] * 1_000_000 / 3600  # MJ/m2/h -> W/m2

    ghi_profile = asos.groupby('hour')['GHI_Wm2'].mean()
    doy_mid = pd.Timestamp('2025-07-28').dayofyear  # 분석기간 중앙일 근사

    rows = []
    for hour, ghi in ghi_profile.items():
        cos_z = cos_solar_zenith(hour, doy=doy_mid)
        kdir, kdiff = split_radiation(ghi, cos_z)
        rows.append({'hour': hour, 'kdown': ghi, 'kdir': kdir, 'kdiff': kdiff})
    print(f"ASOS 서울(108): {len(asos)}행 사용, DOY 기준일={doy_mid}")
    return pd.DataFrame(rows).set_index('hour')


# ── 4. 통합 ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    sdot_p = load_sdot_seongdong()
    aws_p = load_aws_seongdong()
    asos_p = load_asos_seoul()

    profile = sdot_p.join(aws_p, how='outer').join(asos_p, how='outer')
    profile = profile.round(2)
    profile.index.name = 'hour'

    out_path = os.path.join(RES_DIR, 'seongdong_met_profile_06_19h.csv')
    profile.to_csv(out_path, encoding='utf-8-sig')

    print(f"\n저장: {out_path}")
    print(profile.to_string())

    # ── UMEP SOLWEIG met.txt (24컬럼) 조립 ────────────────────────────────
    # 12일 평균으로 만든 "가상의 대표일"이므로 iy/id는 분석기간 중앙일(2025-07-28,
    # DOY 209)로 고정 — 실제 날짜가 아니라 SOLWEIG 내부 태양위치(그림자) 계산용 입력값.
    # 12일간 태양적위 변화는 1도 미만이라 중앙일 고정에 따른 오차는 무시 가능.
    IY, ID = 2025, pd.Timestamp('2025-07-28').dayofyear
    UNUSED = -999

    umep_rows = []
    for hour, row in profile.iterrows():
        umep_rows.append({
            'iy': IY, 'id': ID, 'it': int(hour), 'imin': 0,
            'qn': UNUSED, 'qh': UNUSED, 'qe': UNUSED, 'qs': UNUSED, 'qf': UNUSED,
            'U': row['wind'], 'RH': row['RH'], 'Tair': row['Ta'],
            'pres': UNUSED,   # ASOS 다운로드본에 기압 컬럼 없음, Tmrt/UTCI 영향 미미
            'rain': 0,        # ASOS 강수량 확인 결과 12일×06-19시 전부 무강수
            'kdown': row['kdown'],
            'snow': UNUSED, 'ldown': UNUSED, 'fcld': UNUSED,
            'wuh': UNUSED, 'xsmd': UNUSED, 'lai': UNUSED,
            'kdiff': row['kdiff'], 'kdir': row['kdir'],
            'wdir': UNUSED,   # 원형변수라 산술평균 불가 + Tmrt/UTCI 공식에 미사용
        })
    umep_df = pd.DataFrame(umep_rows)
    met_path = os.path.join(RES_DIR, 'seongdong_solweig_met.txt')
    umep_df.to_csv(met_path, sep=' ', index=False)
    print(f"\nSOLWEIG met.txt 저장: {met_path}")
    print(umep_df.to_string(index=False))
