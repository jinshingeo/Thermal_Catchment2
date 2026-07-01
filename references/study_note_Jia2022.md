# Jia et al. (2022) — Thermal Environment Influences on Pedestrian Thermal Perception and Travel Behavior

## 기본 정보
- **저자**: Siqi Jia, Yuhong Wang, Nyuk Hien Wong, Wu Chen, Xiaoli Ding
- **소속**: 홍콩 폴리텍 대학교 토목환경공학과 + 국립싱가포르대학교 건축환경학과
- **저널**: Building and Environment, 226 (2022), 109687
- **DOI**: https://doi.org/10.1016/j.buildenv.2022.109687
- **투고/채택**: 2022-08-04 투고 → 2022-10-07 채택 → 2022-10-12 온라인 게재

---

## 연구 개요

홍콩 Kowloon Peninsula 4개 조사지점에서 337명의 보행자를 대상으로 야외 열환경과 열 인지(TSV, TCV) 및 **보행 속도** 간의 관계를 정량화. PET와 UTCI 모두 적용하여 비교.

**핵심 발견**: 열 스트레스 증가 → 보행 속도 감소 (Strong heat stress에서 10~20% 감소)

---

## 열환경 지표 및 산출 방법

### 사용 지표
- **PET (Physiologically Equivalent Temperature)**: 주 예측 지표
- **UTCI (Universal Thermal Climate Index)**: 비교 검증용
- **TSV (Thermal Sensation Vote)**: 주관적 열 감각 (-1~3)
- **TCV (Thermal Comfort Vote)**: 주관적 열 쾌적도 (-2~2)

### 측정 및 계산

**현장 기상 관측**
- Kestrel 5400 (Nielsen-Kellerman) 기상 관측 기기
- 지상 1.5m 높이 설치, 1초 간격 측정
- 측정 항목: 기온 (Ta), 구형 온도 (Tg), 상대습도 (RH), 풍속 (Va), 풍향
- 범위: Ta 26~38°C, Tg 29~70°C, RH 53~85%, Va 0~4 m/s

**Tmrt 계산 (야외용)**
글로브 온도계법 (경험식) 적용:
```
Tmrt = [(Tg + 273.15)⁴ + (1.1×10⁸ × Va⁰·⁶) / (ε × D⁰·⁴) × (Tg - Ta)]^0.25 - 273.15
```
- Tg: 구형 온도, Va: 풍속, D: 구형 직경, ε: 방사율

**SVF 계산**
- Fish-eye 사진 → RayMan 1.2 소프트웨어로 자동 계산
- Site 1,2 (저SVF, 0.45~0.50): 나무 그늘, 협소한 도로
- Site 3,4 (고SVF, 0.82~0.91): 개방 공간, 직사광선 노출

**PET, UTCI 계산**
- SOLWEIG 1.0 마이크로 기상 모델링 소프트웨어
- 입력: Ta, Tmrt, RH, Va + 현장 SVF 데이터
- Kuehn 등의 글로브 온도계법으로 Tmrt 결정

---

## 데이터 및 공간 범위

| 항목 | 내용 |
|------|------|
| 연구 지역 | 홍콩 Kowloon Peninsula, 4개 야외 보도 |
| 기후 | 아열대 고온다습 (여름 극심한 폭염) |
| 조사 기간 | 2021년 4월 30일 ~ 6월 15일 (10회 현장 조사) |
| 조사 시간 | **14:00~17:00** (일반 여름 더운 시간대) |
| 조사 대상 | 337명 (남 168명/여 169명) |
| 사이트 | 4곳: Nathan Rd (SVF↓), Chatham Rd (SVF↓), Cheong Wan Rd (SVF↑), Fat Kwong St (SVF↑) |
| 보도 너비 | 3~5m |

### 현장 기상 조건 요약 (Table 2 기반)
| 조건 | 범위 |
|------|------|
| UTCI 최대값 | 29.4~46.4°C |
| UTCI 평균 | 27.0~40.2°C |
| PET 최대값 | 26.4~50.3°C |
| Tmrt 최대값 | 36.1~52.8°C |

---

## 분석 모델

### 회귀 모델 (보행 속도 예측)
- 다항 회귀: R² = 0.719
- 최종 방정식:
```
y = 1.300 - 0.045TSV - 0.003TSV³ + 0.023air_ac - 0.108gender_female
    + 0.202age - 0.043age² - 0.140clo
```
- 유의 변수: TSV, 에어컨 사용 여부, 성별, 나이, 의복 단열

### 신경망 모델
| 모델 | 테스트 R² | 전체 R² |
|------|----------|---------|
| Stage 1 ANN | 0.669 | 0.817 |
| Stage 2 ANN (TSV 추가) | 0.762 | 0.907 |
| DNN (3 hidden layers) | **0.791** | **0.931** |

### UTCI-TSV 관계
```
MTSV = -7.068 + 0.276 × UTCI   (R² = 0.860)
```
→ UTCI 37°C 이상에서 TSV 포화 (절단됨)

### PET-TSV 관계
```
MTSV = -5.218 + 0.245 × PET    (R² = 0.921)
```
→ PET로 더 높은 설명력

### 속도 감소 구간 (Fig. 13 기반)
- No heat stress (PET < 23°C): baseline
- Slight heat stress (23~27°C): ~3~5% 감소
- Moderate heat stress (27~32°C): ~5~10% 감소
- Strong heat stress (PET > 32°C): **10~20% 감소**

---

## 우리 연구에서 따라할 수 있는 부분

### 1. SOLWEIG + 글로브 온도계 Tmrt 공식
- 야외 현장 Tmrt 계산 경험식 → 우리 현장 데이터가 없으면 SOLWEIG로 대체
- SOLWEIG 사용 방법론적 정당화에 활용

### 2. 조사 시간대 14:00~17:00
- 폭염 최고 시간대 → 우리 연구 14시 기준 선정과 일치
- **인용 가능**: "Jia et al.(2022)은 14:00~17:00를 여름 조사 시간대로 설정하였으며, 이는 보행자의 열 스트레스가 최대에 달하는 시간대와 일치한다"

### 3. UTCI 기반 TSV 관계식 인용
- MTSV = -7.068 + 0.276 × UTCI (R²=0.860) → UTCI가 주관적 열감과 선형 관계 실증
- UTCI 지표의 타당성 입증에 활용 가능

### 4. SVF와 열 스트레스 관계
- SVF 낮은 곳(나무/건물 그늘) → UTCI 낮고 보행 속도 변화 더 완만
- 우리 연구의 SVF 변수를 TARR 설명변수로 쓰는 근거

### 5. 보행 속도 감소 → Hard Cut 정당화 우회 논거
- UTCI Strong heat stress에서 10~20% 보행 속도 감소 실증
- Very Strong (UTCI ≥38°C)에서는 더 극적인 영향 예측 가능
- Hard Cut(보행 포기)이 현실적 반응을 단순화한 보수적 시나리오임을 설명하는 근거

---

## 우리 연구와의 차별점

| 항목 | Jia2022 | 우리 연구 |
|------|---------|----------|
| 방법 | 현장 실험 (N=337) | 공간 모델링 |
| 종속변수 | 보행 속도 | 역세권 면적 감소율 |
| 지표 | PET (주), UTCI (보조) | MRT (SOLWEIG 계산) |
| 공간 | 4개 지점 (소규모) | 서울 전역 |
| 임계값 | PET 35°C (포화), UTCI 37°C | UTCI ≥38°C → 역산 MRT 임계값 (Hard Cut) |
| 시간 | 2021년 봄-여름 | 폭염 특보 발효일 |

---

## 한계 (논문 명시)
- 현장 조사 4개 지점만 → 일반화 한계
- 라이프스타일·보행 습관 미통제
- 홍콩 한정 → 기후가 다른 도시 적용 시 보정 필요
