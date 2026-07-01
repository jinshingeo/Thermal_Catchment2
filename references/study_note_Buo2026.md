# Buo et al. (2026) — Cool Routes: Real-time Human Thermal Exposure Routing

## 기본 정보
- **저자**: Isaac Buo, Waqar Hassan Khan, Evan Crabtree, Fletcher Emmott, Devbrat Hariyani, Ariane Middel
- **소속**: The GAME School, Arizona State University; School of Computing and Augmented Intelligence, ASU; School of Geographical Sciences and Urban Planning, ASU
- **저널**: Building and Environment, 298 (2026) 114622
- **DOI**: https://doi.org/10.1016/j.buildenv.2026.114622
- **투고/채택**: 2026-02-13 투고 → 2026-04-11 수정 → 2026-04-13 채택 → 2026-04-18 온라인 게재

---

## 연구 개요

피닉스(Arizona) ASU 캠퍼스에서 **MRT를 임피던스(impedance)로** 직접 사용하는 실시간 보행 라우팅 시스템 *Cool Routes* 개발. SOLWEIG 1m 해상도 MRT를 사전 계산하고 Dijkstra 알고리즘으로 최소 누적 MRT 경로 탐색.

**핵심 기여**:
- 최초의 실시간 MRT 기반 보행 내비게이션 시스템
- SOLWEIG + LiDAR DSM + weather API 완전 파이프라인
- 모바일 센서(MaRTy)로 MRT 예측 검증 (d=0.73)

---

## 핵심 모델

### 누적 열 노출 (Cumulative Thermal Exposure)
```
C(P) = Σₑ∈P Tₑ · lₑ          ...(1)
```
- Tₑ: 엣지 e의 평균 MRT (°C)
- lₑ: 엣지 e의 길이 (m)
- **임피던스 = 거리 가중 MRT 합산**

### 최적 경로 탐색
```
P* = argmin C(P)          ...(2)
```
- Dijkstra 알고리즘 적용 (MRT × 길이를 edge weight로 사용)

### 평균 경로 MRT
```
T(P) = C(P) / Σₑ lₑ          ...(3)
```

### MRT 계산 (SOLWEIG 출력)
```
R_str = ζₖ Σᵢ₌₁⁶ KᵢFᵢ + εₚ Σᵢ₌₁⁶ LᵢFᵢ          ...(4)
MRT = ⁴√(R_str / (εₚ·σ)) − 273.15          ...(5)
```
- Kᵢ: 단파 복사 플럭스, Lᵢ: 장파 복사 플럭스
- Fᵢ: 인체 각도 계수 (6방향)
- ζₖ = 0.70 (단파 흡수율), εₚ = 0.97 (방사율)
- σ = 5.67×10⁻⁸ Wm⁻²K⁻⁴ (Stefan-Boltzmann 상수)

---

## 데이터 및 시스템 구조

### 시스템 아키텍처 (Cool Routes)
- **Frontend**: 웹 앱 (사용자: O-D 입력 + 날짜/시간 선택)
- **Backend**: Flask 서버
  1. DSM bucket (건물 + 나무 + DEM)
  2. Weather API (Ta, RH, wind, solar radiation — 72시간 예보)
  3. SOLWEIG model → 1m MRT 래스터 (매시간 사전 계산)
  4. MRT bucket (GeoTIFF 저장)
  5. Walkable paths bucket (OSMnx 기반 GraphML)
  6. Routing algorithm (Dijkstra)

### 입력 데이터
| 데이터 | 소스 | 해상도 |
|--------|------|-------|
| 건물 Surface Model (BSM) | LiDAR 2020 | 1m |
| 나무 캐노피 Surface Model (CDSM) | LiDAR 2020 | 1m |
| DEM | LiDAR 2020 | 1m |
| 기상 | Weather API (실시간) | 사이트별 |
| 보행 네트워크 | OSMnx | 링크 단위 |

### 공간 범위
- ASU Tempe 캠퍼스 + Downtown Tempe
- 7.01 km² (−111.9178°~−111.941°E, 33.4294°~33.4097°N)
- 기후: 건조 아열대 (Köppen Bwh), 여름 최고 38°C (MRT 76.2°C 가능)

---

## 검증

### MaRTy 모바일 센서 검증
- 3개 net-radiometers → 6방향 복사 측정 (2초 간격)
- 핫 서머 데이터 (July 5, 6, 9, 2025) — Ta ≈ 40°C
- 5개 경로, 319개 엣지 검증

### 검증 결과
| 지표 | 값 |
|------|-----|
| Index of Agreement (d) | **0.73** |
| MAE | 6.2 °C |
| MBE | −2.0 °C (과소추정) |
| RMSE | 8.4 °C |
| 오차 5°C 이하 엣지 비율 | 72% (228/319개) |

---

## 주요 결과

### 계절별 라우팅 성능
- 500개 OD 쌍 × 12 맑은 날 (계절별 1일/월)
- **70% 이상**: 최단 경로와 다른 경로 권장 (재경로 발생)

| 계절 | 평균 우회 거리 | 평균 MRT 감소 |
|------|--------------|--------------|
| 냉월 (11~3월) | +5.0% | **−3.8°C** (−11.8%) |
| 어깨철 (4, 10월) | +32.2m | **−3.2°C** (−6.8%) |
| 열월 (5~9월) | +22.3m (평균) | **−2.5°C** (−4.4%) |

- 우회 거리: 주로 8~60m (중앙값 50m 이하)
- 정오(10:00~18:00) 최대 효과

### MRT 범위 (ASU 캠퍼스, 열월)
- 완전 햇빛: max MRT **76.2°C**
- 완전 그늘: −20~40°C 감소 가능
- 최저 MRT: 37.4°C (7월 오전)

---

## 우리 연구에서 따라할 수 있는 부분

### 1. SOLWEIG 1m 해상도 MRT 계산 파이프라인 ← A5 해결
- **완전한 파이프라인**: LiDAR DSM + CDSM + DEM + weather API → SOLWEIG → MRT
- 우리도 동일 파이프라인 사용 (단, LiDAR 없으면 DSM 대안 필요)
- **인용 가능**: "Buo et al.(2026)은 SOLWEIG와 1m LiDAR DSM을 결합하여 캠퍼스 규모 실시간 MRT를 산출하고 보행 라우팅에 적용하였다"

### 2. MRT를 임피던스로 직접 사용 ← E1 보완
- 우리 Hard Cut: UTCI ≥38°C 초과 링크 제거 = 해당 링크를 통행 불가로 설정하는 것
- Buo는 MRT를 연속적 비용으로 사용 (소프트) → 우리는 UTCI 임계값 초과 시 제거 (하드)
- **비교 서술**: "Buo et al.(2026)은 MRT를 연속적 임피던스로 사용해 누적 열노출을 최소화하는 경로를 탐색한 반면, 본 연구는 UTCI ≥38°C(Very Strong Heat Stress) 초과 링크를 완전 제거하는 Hard Cut 접근을 채택한다"

### 3. SOLWEIG 검증 정확도 수치 참고
- d=0.73, MAE=6.2°C, RMSE=8.4°C
- 우리 SOLWEIG 적용 시 모델 불확실성 논의에 인용 가능
- "Buo et al.(2026)의 검증 결과(d=0.73, MAE=6.2°C)는 SOLWEIG가 도시 보행 맥락에서 MRT를 합리적으로 추정함을 시사한다"

### 4. Dijkstra 알고리즘으로 MRT 최소 경로 탐색
- 우리도 Hard Cut 후 Dijkstra 재실행 → 동일 알고리즘 사용
- Buo의 edge weight = Tₑ×lₑ / 우리 edge weight = 기존 이동 시간

### 5. 우회 거리 10m~60m, +3~5% 수준
- 열 최적 경로 선택 시 실제 우회 거리 매우 작음 → 현실적
- 우리 연구 Hard Cut이 더 극단적 (도달 불가 = ∞ 우회)이지만 보수적 시나리오 명시

### 6. MRT 최대 76.2°C (피닉스 여름)
- 우리 Hard Cut 기준 UTCI ≥38°C: 서울 폭염 조건에 적합한 임계값 (Bröde et al., 2012 Very Strong Heat Stress 하한)
- **한국 폭염 MRT 범위 산출 필요** (분석 단계에서 확인)

---

## 우리 연구와의 차별점

| 항목 | Buo2026 | 우리 연구 |
|------|---------|----------|
| 목적 | 실시간 개인 내비게이션 | 역세권 접근권 분석 |
| 열 지표 | MRT (직접) | MRT → UTCI (생리 지표) |
| 패널티 방식 | 소프트 (누적 MRT 최소화) | **Hard Cut** (UTCI≥38°C 링크 제거) |
| 스케일 | 캠퍼스 (~7km²) | 서울 전역 (성동구 파일럿 기반) |
| 기후 | 건조 아열대 (피닉스) | 온대 계절풍 (서울) |
| 결과 | 개별 OD쌍 최적경로 | 보행권 감소율([검증 지표]) |
| 실시간 여부 | 실시간 MRT 예보 반영 | 특정 폭염일 단일 시점 분석 |

---

## 한계 (논문 명시)
- 단일 사용자 요청 처리 (동시 세션 불가)
- 정적 지면 모델 (식생 성장, 계절 낙엽 미반영)
- LiDAR 취득 비용 + 항공 허가 제약
- 열대·습윤 기후 적용 가능성 미검증 (현재는 건조 아열대 한정)
- MaRTy 이동 중 측정 vs SOLWEIG 정지 추정 간 방법론적 차이
