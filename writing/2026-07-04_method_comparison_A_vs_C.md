# Method A vs Method C — MRT 산출 방식 상세 비교 분석
작성일: 2026-07-04 | 버전: v1.0

---

## 1. 개요: 왜 MRT를 SOLWEIG로 계산하는가

UTCI(Universal Thermal Climate Index)는 6개 입력 변수(기온, 풍속, 상대습도, 평균복사온도)로 구성되며,
이 중 **평균복사온도(MRT, Mean Radiant Temperature)**가 보행 환경의 열환경을 가장 크게 좌우한다.
MRT는 인체가 모든 방향(6방향: 상·하·전·후·좌·우)에서 받는 단파·장파 복사의 합으로,
건물 그늘, 수목 캐노피, 바닥 반사율, 하늘 개방도(SVF)에 따라 수십 °C 차이가 발생한다.

SOLWEIG(Solar and LongWave Environmental Irradiance Geometry)는 Lindberg et al. (2008, 2018)이
개발한 물리 기반 복사 모델로, 래스터 단위로 MRT를 직접 산출한다. 이를 "정식" 방법으로 보는 이유는:
- 단파 6방향 복사(K↓, K↑, K_sw_side)와 장파 6방향 복사(L↓, L↑, L_lw_side)를 **분리 계산**
- DSM으로부터 Sky View Factor(SVF)를 픽셀 단위로 정밀 산출
- 태양 고도각·방위각 기반 **그늘 형상** 시뮬레이션
- 벽면 복사(Wall H&A) 반영

Method A(약식)는 위 계산을 **경험적 계수**로 대체한다.

---

## 2. Method A: 약식 MRT (Oke H/W Canyon SVF 기반)

### 2-1. 계산 파이프라인

```
S-DoT 기상 센서 데이터 (복수 관측소)
    → IDW 보간 → 링크별 UTCI_idw
    
건물 SHP (층수 × 3m = 높이 H)
    + 도로 유형별 표준 폭 W (국토부 도로설계기준)
    → Oke(1987) H/W Canyon 공식: SVF = 1 / √(1 + (H_eff/W)²)
    
도시숲 SHP (면 데이터)
    → 링크 버퍼 15m 내 캐노피 면적 비율 산출

→ 보정: UTCI_corrected = UTCI_idw − ΔUTCI_svf − ΔUTCI_canopy
    ΔUTCI_svf    = 8.0°C × (1 − SVF) × solar_factor(hour)
    ΔUTCI_canopy = 2.5°C × canopy_ratio × solar_factor(hour)

→ Hard Cut: UTCI_corrected ≥ 38°C 링크 제거
→ Thermal Catchment Area 산출
```

### 2-2. 왜 "약식"인가: Method A의 한계

| 항목 | SOLWEIG (정식) | Method A (약식) |
|------|---------------|----------------|
| SVF 산출 | 래스터 픽셀 단위, 360° 고려 | H/W 비율 단순 공식 (Oke 1987) |
| 그늘 형상 | 태양 위치·DSM 기반 동적 계산 | static — 시간별 solar_factor 경험 가중치 |
| MRT 직접 계산 | ✅ 물리 기반 6방향 복사 | ❌ MRT 미계산, UTCI 직접 보정 |
| 수목 캐노피 | CDSM 래스터 입력 (미적용 시 0) | SHP 기반 면적 비율 → 경험 계수(2.5°C) |
| 바닥 반사율 | 래스터 albedo 입력 가능 | 미반영 |
| 장파 복사(L) | ✅ 직접 계산 | ❌ 미반영 |
| 벽면 복사 | ✅ Wall H&A 포함 | ❌ 미반영 |
| 도로 폭 기준 | 불필요 (래스터 기반) | 유형별 표준폭 가정 — 실제 폭과 불일치 가능 |
| 기상 입력 | 공간적으로 단일 or 분포 | IDW 보간 (S-DoT 복수 센서) |

**핵심 한계**: UTCI_corrected는 물리량이 아닌 경험적 보정값이다.
SVF_COEFF=8.0°C, CANOPY_COEFF=2.5°C는 문헌(Lindberg & Grimmond 2011, Chen & Ng 2012)에서 도출된
경험 계수이나, 실제 복사 조건에 따라 오차가 크다. 특히 비대칭 건물 협곡이나 특수 지형에서
H/W 단순화는 실제 SVF를 과대/과소 추정한다.

### 2-3. 선행연구 근거

| 구성 요소 | 적용 공식/계수 | 근거 |
|-----------|--------------|------|
| SVF | SVF = 1/√(1+(H/W)²) | Oke, T.R. (1987). *Boundary Layer Climates* (2nd ed.). Routledge |
| 도로 폭(W) | 유형별 표준폭 | 국토부 도로설계기준 / OSM 실측 통계 |
| SVF_COEFF | 8.0°C | Lindberg, F. & Grimmond, C.S.B. (2011). *IJCL* 25(1):51-62 |
| CANOPY_COEFF | 2.5°C | Chen, L. & Ng, E. (2012). *Landscape and Urban Planning* 105(3):350-360 |
| 수목 높이 | 10.0m | UMEP TreePlanter Tutorial (Lindberg et al.) |

---

## 3. Method C: SOLWEIG + GLO-30 30m DSM

### 3-1. 계산 파이프라인

```
GLO-30 30m DSM (Copernicus, 서울)
+ GLO-30 30m DEM
    → QGIS UMEP: Wall Height & Aspect 산출
    → QGIS UMEP: Sky View Factor (ANISO=True, 360° 방향) 산출
    → QGIS UMEP: SOLWEIG → Tmrt 래스터 (°C)

단일 기상 입력 (S-DoT 평균 + ASOS 풍속):
  Tair=35.2°C, RH=54.0%, U=1.9m/s, Kdown=708W/m², UTC=9

→ MRT 래스터에서 링크별 샘플링 (Buo et al. 2026, 5m 간격 평균)
→ Hard Cut: MRT ≥ 56°C (UTCI 42°C 역산) 링크 제거
→ Thermal Catchment Area 산출
```

### 3-2. SOLWEIG의 6방향 복사 계산 원리

Lindberg et al. (2008)의 SOLWEIG는 인체 주변 6방향 복사를 다음과 같이 분리 계산한다:

```
MRT = [(1/σ) × (0.5 × (fsvf×K_dif + fsvf×K_ref + SVF_walls×K_walls)
       + Fp(K_dir + K_dif_sun) + 0.5 × (fsvf×L_dif + ...)]^(1/4) - 273.15
```

- **K↓ (단파 하향)**: 직달 + 확산일사 합산 → 태양 고도각, DSM 그늘 반영
- **K↑ (단파 상향)**: 바닥 반사 (albedo 반영)
- **K_side (단파 측면)**: 벽면 반사 (Wall H&A 반영)
- **L↓ (장파 하향)**: 대기 방출 복사 (Tair, RH → Stefan-Boltzmann)
- **L↑ (장파 상향)**: 지면 방출 복사
- **L_side (장파 측면)**: 벽면 방출 복사

각 방향은 SVF(하늘 개방도) 가중치로 합산된다.

### 3-3. 이번 실행에서 반영한 것 vs 반영 안 한 것

#### ✅ 반영한 것

| 항목 | 내용 | 파라미터 |
|------|------|---------|
| 건물 형상 (DSM) | GLO-30 30m 해상도 | `INPUT_DSM` |
| 지형 기복 (DEM) | GLO-30 30m | `INPUT_DEM` |
| Sky View Factor | 360° 방향, Anisotropic | `ANISO=True` |
| Wall H&A | 벽면 높이·방위 | `INPUT_HEIGHT`, `INPUT_ASPECT` |
| 태양 위치 | 날짜(DOY=206, 7월25일) + 시각(14시) | `INPUTMET` iy/id/it |
| UTC 시간대 | KST = UTC+9 | `UTC=9` |
| 기상 입력 | Tair, RH, U, Kdown (단일값) | `INPUTMET` |
| 전천일사 | Kdown만 입력 (직달/확산 미분리) | `ONLYGLOBAL=True` |

#### ❌ 반영 안 한 것 (한계)

| 항목 | 미반영 이유 | 영향 |
|------|-----------|------|
| **수목 캐노피 (CDSM)** | 서울 전역 CDSM 데이터 미확보 | 나무 그늘 효과 0으로 처리 → MRT 과대추정 |
| **바닥 재질 공간 변화** | 래스터 albedo 미입력 → 기본값(0.2) | 아스팔트/콘크리트/잔디 구분 불가 |
| **공간적으로 다양한 기상** | 단일 관측소 값 사용 | 성동구 전체 동일 기상 조건 → 공간 분화 제한 |
| **직달/확산 분리** | ONLYGLOBAL=True | 구름 조건 반영 부정확 (맑은 날 가정) |
| **인체 파라미터** | 기본값 적용 | 직립, 흡수율 0.7, 임의 방향 평균 |

#### ONLYGLOBAL=True 설명

기상 파일에 Kdown(전천일사, W/m²)만 제공하고 `ONLYGLOBAL=True`로 설정하면,
SOLWEIG는 내부적으로 전천일사를 직달(beam)과 확산(diffuse)으로 분리하지 않고
단순화된 방식으로 처리한다. 이는 일반 기상 관측소 데이터(Kdown만 제공)를 사용할 때의
표준 설정이다.
선행연구(Buo et al. 2026, Jia et al. 2022)에서도 동일하게 사용됐으며,
직달/확산 분리 데이터가 없는 경우 불가피한 타협점이다.

### 3-4. 고정 파라미터 선행연구 근거

| 파라미터 | 값 | 근거 |
|---------|---|------|
| `ONLYGLOBAL=True` | 전천일사만 입력 | Buo et al. (2026). *Building and Environment* 298:114622 — 동일 설정 사용; Lindberg et al. (2018) UMEP manual |
| `ANISO=True` | 비등방성 SVF | Lindberg, F. et al. (2018). *Urban Climate* 24:516-525 — SOLWEIG 2018a |
| `INPUT_LIMIT=3.0` | 벽면 탐지 최소 높이(m) | UMEP 기본값 (Lindberg et al. 2018) |
| `UTC=9` | KST | — |
| `Tair=35.2°C, RH=54.0%` | S-DoT 폭염일 평균 | 서울 S-DoT 센서 2025-07-23~08-02 평균 |
| `U=1.9 m/s` | 성동구 풍속 | ASOS 서울 관측소 폭염일 평균 |
| `Kdown=708 W/m²` | 단파 복사 | ⚠️ 근거 논문 미확보 — Open-Meteo 또는 기상청 자료 확인 필요 |
| MRT 임계값 56°C | UTCI 42°C 역산 | pythermalcomfort 역산 (Tair=36.3, RH=51.9, U=2.17) |

---

## 4. 핵심 결과 비교

### 4-1. MRT 분포

| 지표 | Method A | Method C |
|------|----------|---------|
| 공간 단위 | 링크별 UTCI_corrected (°C) | 링크별 MRT 샘플링 평균 (°C) |
| 범위 | 다양 (그늘 링크 ↓) | 58.4~61.6°C (균일하게 높음) |
| 공간 분화 | 가능 (SVF, 캐노피에 따라 링크마다 다름) | **매우 제한적** — 30m 해상도에서 건물 그늘 뭉개짐 |
| Hard Cut 비율 | 시간대에 따라 다름 (예: 13시 ~99%) | **100%** (전 링크 ≥ 56°C) |

### 4-2. Thermal Catchment Area 결과

| 역 | Method A (13시, UTCI≥38°C) | Method C (14시, MRT≥56°C) |
|----|--------------------------|--------------------------|
| 응봉역 | Classic 891, Thermal 1 (−99.9%) | Classic 809, Thermal 1 (−99.9%) |
| 성수역 | Classic 644, Thermal 1 (−99.8%) | Classic 575, Thermal 1 (−99.8%) |

두 방법 모두 **13~14시 폭염 조건에서 동일한 결론**을 도출한다.
이는 두 방법의 Hard Cut 비율이 모두 ~100%이기 때문이다.

### 4-3. 왜 Method C에서 공간 분화가 안 되는가

GLO-30 30m 해상도에서:
- 한 픽셀 = 30m × 30m → 서울 도심 평균 건물 1~3개 포함
- 건물 모서리, 처마 그늘, 1~5m 폭의 가로수 그늘은 픽셀 내부에서 평균화됨
- 결과: 건물 그늘 링크와 직사광 링크의 MRT 차이가 사라짐 → 전 링크 균일 고온

**Method A 성수역 발표자료의 초록(Thermal Catchment) 면적**:
→ 파일럿 발표 자료(slide10_contrast_sungsoo.png)에서 초록이 많은 이유:
→ 해당 지도는 **전체 역(성수역 포함) 공통 base UTCI로 보정 후**의 결과였거나,
   **h10(오전 10시) 기준**의 결과일 가능성이 높음.
→ h13 기준 결과도 99.8% 감소로, 비슷하게 Thermal ≈ 1이었음.

---

## 5. 논문 Methods 서술 포인트

### Method A 서술 시 주의사항

```
"약식 MRT 접근 방식을 적용하였다. 건물 층수와 도로 유형별 표준 폭을 이용하여
Oke(1987)의 도시 협곡(H/W) 공식으로 링크별 Sky View Factor를 산출하고,
Lindberg & Grimmond(2011)의 경험 계수를 적용하여 S-DoT 기상 관측 기반
UTCI를 공간적으로 보정하였다."
```

명시해야 할 한계:
- 물리 기반 MRT 계산이 아닌 경험적 보정
- H/W 공식의 대칭 협곡 가정 → 비대칭 도시 형태 표현 한계
- 장파 복사, 벽면 반사 미반영

### Method C 서술 시 주의사항

```
"UMEP SOLWEIG 모델(Lindberg et al. 2008, 2018)을 적용하여 Copernicus GLO-30 
30m 해상도 DSM을 입력으로 링크별 MRT를 산출하였다. 수목 캐노피(CDSM)는 서울 
전역 데이터 미확보로 미반영하였으며, 기상 입력은 S-DoT 폭염일 평균 단일값을 
적용하였다(ONLYGLOBAL=True). 30m 해상도의 한계로 인해 도시 미기후 스케일 
복사 환경의 공간 분화가 제한적이었으며, 이는 방법론 비교 결과에서 확인되었다."
```

명시해야 할 한계:
- 30m 해상도 → 도시 스케일 공간 분화 제한
- 수목 캐노피 미반영 → MRT 과대추정
- 단일 기상값 → 공간적 기상 변동성 미반영
- ⚠️ Kdown=708 W/m² 근거 논문 확인 필요

---

## 6. 향후 과제

- [ ] `Kdown=708 W/m²` 근거 논문/데이터 확인 (Open-Meteo or 기상청 자료 명시)
- [ ] Method A 성수역 발표자료 초록 면적의 정확한 시간대/임계값 확인
- [ ] 고해상도(2m급) DSM 또는 건물 폴리곤 기반 합성 DSM(Method B) 검토
- [ ] CDSM 확보 가능성 검토 (서울시 공개 데이터 또는 항공 LiDAR)
- [ ] Monte Carlo 민감도 분석 (MRT 임계값 54°C ± 4°C)
