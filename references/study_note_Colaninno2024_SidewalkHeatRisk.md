# Colaninno et al. (2024) — 보도 단위 열위험 평가 프레임워크

작성일: 2026-07-01  
버전: v1.0  
근거논문: Colaninno, N., Basu, R., Hosseini, M., Alhassan, A., Liu, L., & Sevtsuk, A. (2024). A sidewalk-level urban heat risk assessment framework using pedestrian mobility and urban microclimate modeling. *EPB: Urban Analytics and City Science*, 52(5), 1071–1090. DOI: 10.1177/23998083241280746

---

## 1. 논문 기본 정보

- **저자**: Nicola Colaninno (Politecnico di Milano + MIT), Rounaq Basu, Maryam Hosseini, Abdulaziz Alhassan, Liu Liu, Andres Sevtsuk (MIT)
- **저널**: EPB: Urban Analytics and City Science (2025) 52(5):1071–1090
- **DOI**: 10.1177/23998083241280746
- **연구지역**: Los Angeles, CA — Expo 지역 6km×6km (약 36 sq.km)
- **재정지원**: EU Horizon 2020 Marie Skłodowska-Curie, MultiCAST 프로젝트 (No. 101028035)

---

## 2. 핵심 프레임워크

**IPCC 리스크 3요소를 보도 단위로 구현**:

$$\text{Heat Risk} = \text{Hazard (UTCI)} \times \text{Exposure (보행자량)} \times \text{Vulnerability (연령)}$$

| 요소 | 측정 방법 | 해상도 |
|------|----------|--------|
| Hazard | UTCI (SOLWEIG) | 1m 픽셀 |
| Exposure | 보행자 이동량 (UNA) | 사이드워크 세그먼트 |
| Vulnerability | 연령 (5세 이하, 65세 이상) | 주소 단위 |

---

## 3. 방법론 — Hazard (UTCI)

### 3.1 SOLWEIG 설정
- **모델**: SOLWEIG (UMEP 플러그인) — Lindberg et al. (2008, 2018) 인용
- **공간해상도**: **1m**
- **기상입력**: ERA5 (Copernicus C3S, ECMWF) — 시간별
- **공간입력**: LiDAR DSM (건물+지면 + 수목 캐노피 분리), LULC 2016

### 3.2 분석 기간 및 시간 구분
- **폭염**: 2022년 9월 3일~9일 (7일, LA)
  - 폭염 판별: 일 최고기온이 1980~2022 기준기간 90th percentile 초과
- **시간 범위**: 6:00 AM ~ 7:00 PM (일조 시간)
- **시간대 3구분**:
  - 아침 peak: 6:00–10:00 AM
  - 낮(midday): 10:00 AM–3:00 PM
  - 저녁 peak: 3:00–7:00 PM

### 3.3 열위험 지도 산출
각 시간대별로:
1. UTCI 래스터 스택 생성 (시간별)
2. **mean + 95th percentile** 동시 계산 → 0–1 정규화
3. 정규화 mean × 95th percentile → 최종 heat hazard map
- 95th percentile 사용 이유: 극단값 이상치 영향 줄이면서 고빈도 고강도 구역 강조

---

## 4. 방법론 — Exposure (보행자량)

### 4.1 보행 네트워크
- **Tile2Net** (Hosseini et al., 2023): 항공영상 → 사이드워크 네트워크 자동 추출
- **사이드워크 네트워크** 사용 (도로 centerline ❌) — 이유: 같은 거리 양쪽이 그림자·폭 달라 서로 다른 열노출

### 4.2 보행 모델 (UNA Framework)
- **Madina** Python 라이브러리 (Alhassan & Sevtsuk, 2024)
- 5개 목적지: 버스정류장, 기차역, 공원, 공립학교, 상업시설
- **보행거리 임계값**: 800m (≈ half mile)
- **경로 배정**: 확률적 (최단경로의 1.15배 이내 모든 경로에 확률 할당)
- 출발지: 주거 주소 단위 (address point)

### 4.3 보행자량 Calibration
- Calibration 데이터: **Streetlight** 보행자 카운트 (foot traffic index)
- **OLS 회귀 결과 (Table 1 직접 확인)**:

| 목적지 | 아침(6-10am) | 낮(10am-3pm) | 저녁(3-7pm) |
|--------|------------|------------|------------|
| 버스정류장 | **0.493***  | **0.847*** | **0.945*** |
| 기차역    | **0.256*** | **0.336*** | **0.267*** |
| 공원·학교·상업시설 | 유의하지 않음 → **제외** | | |

- Adj. R²: 0.077 / 0.066 / 0.071 (낮지만 proof-of-concept으로 수용)

---

## 5. 방법론 — Vulnerability

- **대상**: 5세 이하 어린이 + 65세 이상 노인
- **데이터**: 미국 Decennial Census 2020 블록그룹 → 주소 단위로 비례 배분
- **한계 (저자 직접 인정)**: 연령만 고려 — 소득, 인종, 녹지 접근성 등 미포함 (proof-of-concept)

---

## 6. 지수 산출

### 6.1 Heat Exposure Index (HEI) — 세그먼트 단위
$$\text{HEI} = \text{norm}(\text{UTCI hazard}) \times \text{norm}(\text{보행자량})$$
- UTCI: 세그먼트 버퍼로 픽셀 평균
- 버스정류장·기차역 통행만 포함 (calibration 유의 항목만)

### 6.2 Home-based Heat Risk — 주거 출발지 단위
$$\text{Risk}_{origin} = \text{norm}(\text{hazard}) \times \text{norm}(\text{exposure}) \times \text{norm}(\text{vulnerability})$$
- 경로별 세그먼트 길이 가중 평균 UTCI 집계
- 최종 0–1 정규화

---

## 7. 주요 결과

- **가장 위험한 시간대**: 낮(10am–3pm) — HEI·Risk 모두 최대
- **공간 패턴**: 주거 밀집 지역 인근에서 HEI 높음 (버스/기차역 접근 보행량 많음)
- **사이드워크 비대칭**: 같은 거리 양쪽 사이드워크에서 그림자·보행자량 차이로 비대칭적 HEI — **centerline 대신 사이드워크 네트워크 필수 근거**
- **UTCI 수준**: study area 전반 >29°C, extreme heat(46°C↑) 없음

---

## 8. 우리 연구와의 비교 (Discussion 인용 핵심)

| 항목 | Colaninno et al. (2024) | 우리 연구 (TCA) |
|------|------------------------|----------------|
| 목적 | 열위험 평가 (어디가 더 위험한가) | 접근성 범위 변화 (얼마나 못 가게 되나) |
| 임계값 처리 | 없음 — 연속 지수(HEI) | Hard Cut ≥38°C 링크 완전 제거 |
| 공간 단위 | 사이드워크 세그먼트 수준 | 보행자 catchment area 수준 |
| DSM | LiDAR 1m | GLO-30 30m (오픈소스) |
| 취약성 | 연령 포함 | 미포함 (접근성 감소 자체가 주제) |
| 연구 규모 | 6km×6km (LA) | 서울 전역 |
| 기상 데이터 | ERA5 (글로벌) | S-DoT (도시 센서 네트워크) |

**우리 연구의 차별성 강조 포인트**:
1. Colaninno는 리스크 평가 → 우리는 **접근 가능 공간 범위의 정량적 변화** (새로운 공간 단위 TCA 제안)
2. Colaninno는 소프트 접근(연속 지수) → 우리는 **Hard Cut이라는 보수적 시나리오**
3. Colaninno는 LiDAR → 우리는 **오픈소스 30m DSM으로 확장성 검토**
4. Colaninno는 취약성 포함 → 우리는 **감소율([검증 지표])로 공간 형평성 논의 가능**

---

## 9. 논문에서 직접 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| SOLWEIG 공간해상도 | **1m** | p.1074 |
| 분석기간 | 2022년 9월 3~9일 (7일) | p.1078 |
| 보행거리 임계값 | **800m** | p.1075 |
| detour ratio | ≤1.15 | p.1076 |
| 버스정류장 계수(낮) | **0.847*** | Table 1 |
| 기차역 계수(낮) | **0.336*** | Table 1 |
| Adj. R² | 0.066~0.077 | Table 1 |
| 최위험 시간대 | 10am–3pm | p.1081 |
| 연구면적 | 6km×6km ≈ 36 sq.km | p.1077 |

---

## 10. 핵심 인용 형식

```
Colaninno, N., Basu, R., Hosseini, M., Alhassan, A., Liu, L., & Sevtsuk, A. (2024).
A sidewalk-level urban heat risk assessment framework using pedestrian mobility
and urban microclimate modeling.
EPB: Urban Analytics and City Science, 52(5), 1071–1090.
https://doi.org/10.1177/23998083241280746
```

**인용 가능 문구 (Discussion 비교)**:
> "Colaninno et al.(2024)는 SOLWEIG와 보행 이동량을 결합하여 사이드워크 단위 열위험 지수(HEI)를 제안하였으나, 연속적 지수를 통한 상대적 위험 순위 파악에 초점을 맞춘다. 이에 반해 본 연구는 열환경 임계값(UTCI ≥38°C) 초과 링크를 완전 제거하는 Hard Cut을 적용하여, 보행 가능 공간 범위 자체의 변화를 Thermal Catchment Area라는 새로운 공간 단위로 정량화한다."
