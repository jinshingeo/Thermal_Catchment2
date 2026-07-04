"""
Method A — Step 2: SVF + 수목 캐노피 기반 약식 MRT 보정 (링크별 UTCI 산출)
=============================================================================
작성일: 2026-07-04 | 연구: Thermal Catchment Area (파일럿: 성동구)

【방법론 요약】
기상관측(S-DoT IDW 보간) 기반 UTCI에 SVF·캐노피 보정을 적용하여
링크별 열환경 지표를 산출한다.

  UTCI_corrected = UTCI_idw − ΔUTCI_svf − ΔUTCI_canopy

  ΔUTCI_svf    = SVF_COEFF × (1 − SVF) × solar_factor(hour)
  ΔUTCI_canopy = CANOPY_COEFF × canopy_ratio × solar_factor(hour)

  SVF_COEFF    = 8.0°C  (Lindberg & Grimmond 2011 경험 계수)
  CANOPY_COEFF = 2.5°C  (Chen & Ng 2012 경험 계수)
  solar_factor : 서울 여름 태양 고도각 기반 시간별 가중치 (0~1)

【왜 "약식"인가】
  SOLWEIG 등 물리 기반 모델은 6방향 복사(K↓K↑L↓L↑K_side L_side)를
  DSM으로부터 직접 계산하여 MRT를 산출한다. 본 약식 방법은 MRT를 직접
  계산하지 않고, IDW 보간 UTCI를 경험 계수로 보정한다.
  장파 복사, 벽면 반사, 태양 동적 그늘 형상은 반영되지 않는다.

【입력 데이터】
  - link_utci_by_hour.csv : 링크별 시간대별 UTCI_idw (S-DoT IDW 보간 결과)
  - link_svf_canopy.csv   : Step 1 산출 SVF·캐노피 비율

【출력】
  - link_utci_corrected.csv : 링크별 시간대별 보정 UTCI

【참고문헌】
  Lindberg, F. & Grimmond, C.S.B. (2011). The influence of vegetation and
    building morphology on shadow patterns and mean radiant temperatures in
    urban areas. Theoretical and Applied Climatology, 105(3-4), 311-323.
    — SVF_COEFF=8.0°C 근거

  Chen, L. & Ng, E. (2012). Outdoor thermal comfort and outdoor activities:
    A review of research in the past decade. Cities, 29(2), 118-125.
    — CANOPY_COEFF=2.5°C 근거
"""

import os
import numpy as np
import pandas as pd

# ── 경로 설정 ────────────────────────────────────────────────────────────────
STP_BASE   = '/Users/jin/석사논문/성동구_STP연구'
UTCI_PATH  = os.path.join(STP_BASE, '04_분석결과/link_utci_by_hour_v3.csv')
SVF_PATH   = 'results/link_svf_canopy.csv'
OUT_PATH   = 'results/link_utci_corrected.csv'

# ── 보정 계수 (선행연구 기반) ────────────────────────────────────────────────
# Lindberg & Grimmond(2011): 완전 개활지(SVF=1) → 완전 협곡(SVF=0) 간 최대 MRT 차이 기반
SVF_COEFF    = 8.0   # °C

# Chen & Ng(2012): 수목 캐노피 완전 덮임(canopy_ratio=1) 시 추가 복사 차단 효과
CANOPY_COEFF = 2.5   # °C

# 서울 여름(7~8월) 태양 고도각 기반 일사 가중치
# 일출 약 05:20, 일몰 약 19:40, 정오 최대(12~13시)
# 야간(solar_factor=0): 보정 없음 — 단파 복사 없으므로 SVF·캐노피 효과 없음
SOLAR_FACTOR = {
    0: 0.00, 1: 0.00, 2: 0.00, 3: 0.00, 4: 0.00,
    5: 0.05, 6: 0.20, 7: 0.40, 8: 0.60, 9: 0.75,
    10: 0.88, 11: 0.95, 12: 1.00, 13: 1.00, 14: 0.95,
    15: 0.88, 16: 0.75, 17: 0.60, 18: 0.40, 19: 0.20,
    20: 0.05, 21: 0.00, 22: 0.00, 23: 0.00,
}

# ── 데이터 로드 ─────────────────────────────────────────────────────────────
print("UTCI 데이터 로드...")
utci_df = pd.read_csv(UTCI_PATH, encoding='utf-8-sig')
print(f"  {len(utci_df):,}행 | 링크 {utci_df[['u','v']].drop_duplicates().shape[0]:,}개")

print("SVF/캐노피 데이터 로드...")
svf_df = pd.read_csv(SVF_PATH, encoding='utf-8-sig')
print(f"  링크 {len(svf_df):,}개 | SVF 평균 {svf_df['svf'].mean():.3f}")

# ── SVF 딕셔너리 구축 (양방향 매칭) ─────────────────────────────────────────
# SVF는 무방향 링크, UTCI는 양방향 링크이므로 역방향도 동일값으로 매핑
svf_dict = {}
for _, row in svf_df.iterrows():
    key_fwd = (int(row['u']), int(row['v']))
    key_bwd = (int(row['v']), int(row['u']))
    svf_dict[key_fwd] = (row['svf'], row['canopy_ratio'])
    svf_dict[key_bwd] = (row['svf'], row['canopy_ratio'])

def lookup_svf(u, v):
    return svf_dict.get((int(u), int(v)), (np.nan, np.nan))

utci_df[['svf', 'canopy_ratio']] = pd.DataFrame(
    [lookup_svf(u, v) for u, v in zip(utci_df['u'], utci_df['v'])],
    index=utci_df.index
)

# 미매칭 링크: SVF 평균값으로 대체 (보행 접근 불가 지역 등 edge case)
n_missing = utci_df['svf'].isna().sum()
utci_df['svf']          = utci_df['svf'].fillna(svf_df['svf'].mean())
utci_df['canopy_ratio'] = utci_df['canopy_ratio'].fillna(0.0)
print(f"  SVF 매칭률: {(1 - n_missing/len(utci_df))*100:.1f}%")

# ── 보정 계산 ────────────────────────────────────────────────────────────────
utci_df['solar_factor']   = utci_df['hour'].map(SOLAR_FACTOR)

# 건물 협곡 그늘 보정: SVF 낮을수록(협곡) 보정량 큼
utci_df['delta_svf']      = (SVF_COEFF    * (1 - utci_df['svf'])
                              * utci_df['solar_factor']).round(2)

# 수목 캐노피 차폐 보정: 캐노피 비율 높을수록 보정량 큼
utci_df['delta_canopy']   = (CANOPY_COEFF * utci_df['canopy_ratio']
                              * utci_df['solar_factor']).round(2)

utci_df['utci_corrected'] = (utci_df['utci_idw']
                              - utci_df['delta_svf']
                              - utci_df['delta_canopy']).round(2)

# 물리적 하한 적용: UTCI < 20°C는 현실적으로 불가한 여름 폭염 조건
utci_df['utci_corrected'] = utci_df['utci_corrected'].clip(lower=20.0)

# ── 저장 ─────────────────────────────────────────────────────────────────────
cols_out = ['u', 'v', 'hour', 'utci_idw', 'svf', 'canopy_ratio',
            'solar_factor', 'delta_svf', 'delta_canopy', 'utci_corrected',
            'bridge', 'highway']
utci_df[cols_out].to_csv(OUT_PATH, index=False, encoding='utf-8-sig')

# ── 결과 요약 (13시 기준) ────────────────────────────────────────────────────
h13 = utci_df[utci_df['hour'] == 13]
print(f"\n=== 결과 요약 (13시) ===")
print(f"원본 UTCI_idw:    {h13['utci_idw'].min():.1f}~{h13['utci_idw'].max():.1f}°C (평균 {h13['utci_idw'].mean():.1f}°C)")
print(f"보정 UTCI:        {h13['utci_corrected'].min():.1f}~{h13['utci_corrected'].max():.1f}°C (평균 {h13['utci_corrected'].mean():.1f}°C)")
print(f"SVF 보정량:       평균 -{h13['delta_svf'].mean():.1f}°C")
print(f"캐노피 보정량:    평균 -{h13['delta_canopy'].mean():.1f}°C")
n_hot_orig = (h13['utci_idw'] >= 38).sum()
n_hot_corr = (h13['utci_corrected'] >= 38).sum()
print(f"\n임계값(UTCI≥38°C) 링크: {n_hot_orig:,}개 → 보정 후 {n_hot_corr:,}개")
print(f"그늘·캐노피로 구제된 링크: {n_hot_orig - n_hot_corr:,}개")
print(f"\n저장: {OUT_PATH}")
