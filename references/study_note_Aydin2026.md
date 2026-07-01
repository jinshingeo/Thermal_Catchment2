# Aydin et al. (2026) — UTCI-adjusted Pedestrian Accessibility

## 기본 정보
- **저자**: Elif Esra Aydin, Zebin Chen, F. Peter Ortner, Jing Zhi Tay, Kelvin Li, Ryan Chua
- **소속**: Singapore University of Technology and Design (SUTD) + Urban Redevelopment Authority (URA)
- **저널**: Sustainable Cities and Society, 143 (2026), 107335
- **DOI**: https://doi.org/10.1016/j.scs.2026.107335
- **투고/채택**: 2025-08-21 투고 → 2026-03-25 채택 → 2026-03-28 온라인 게재

---

## 연구 개요

열대 기후(싱가포르) 도시 설계 탐색을 위해, UTCI 기반 보행 접근성 지표를 생성 모델(Generative Model)과 결합한 방법론 제안. 핵심 기여는 **UTCI-adjusted reach**, **delta reach**, **RUCS(Reachable Urban Cool Spots)** 세 지표.

**연구 질문**: "보행 네트워크 성능(reach)이 열 스트레스 조건 하에서 얼마나 감소하는가?"

---

## 열환경 지표 및 산출 방법

### 사용 지표
- **UTCI (Universal Thermal Climate Index)**: 주 열환경 지표

### UTCI 계산 워크플로
1. **바람 (Wind)**: OpenFOAM v2112 CFD 시뮬레이션 (8방향 풍향, 초기 속도 1.0~1.3 m/s)
   - 112 ha 부지 전체를 Eddy3D로 메싱
   - NSCC 슈퍼컴퓨터에서 96 CPUs, 약 72시간 소요
   - 결과 1.2m 보행 높이에서 추출

2. **기온·습도 (Ta, RH)**: Urban Weather Generator (UWG) 도구 사용
   - EnergyPlus EPW 기준 기상 파일 + 건물 열 존 + 지표면 분류(포장/녹지) 입력
   - 사이트별 Ta, RH 생성

3. **MRT**: Ladybug Tools의 LB Outdoor Solar MRT 컴포넌트
   - UTCI 계산 시 T_mrt를 UTCI 시뮬레이션 setup으로 추정
   - 콘크리트 포장면 가정 (uniform albedo)
   - 부지 내 건물만 음영 요소로 포함 (주변 건물 제외)

4. **UTCI**: Ladybug(LB) 도구로 최종 계산
   - 2,000~4,000개 보행 경로 노드에서 계산 (2 m 간격)

### 시뮬레이션 시간
- **단시간**: 싱가포르 기준 가장 더운 날인 6월 4일 **17:00** 1시간
- **멀티일**: 극한 폭염 주간(6월 4~10일 중) 6월 8, 9, 10일 3일간 × 4시간대 (07:00, 12:00, 13:00, 17:00)
- 선정 근거: 싱가포르 보행 활동 피크 시간대 (Oh et al., 2020; Diao, 2019)

### UTCI 임계값
- **RUCS 기준**: UTCI < **32°C** (Moderate heat stress 하한 = No/Moderate heat stress 경계)
- 선정 근거: 싱가포르 112 ha 도시 설계 솔루션 32개에서 도출된 평균 UTCI가 32°C (Li et al., 2024)

---

## 공간적 범위 및 데이터

| 항목 | 내용 |
|------|------|
| 연구 지역 | 싱가포르 Punggol (동북쪽), 112 ha |
| 기후 | 열대우림기후 (Köppen Af) |
| 보행 네트워크 | 생성 모델로 자동 생성 (실제 OSM 아님, 가상 마스터플랜) |
| POI | 6개 외부 + 1개 내부 (총 7개): Neighbourhood Center, Precinct Center, Recreational Green Park |
| 베이스라인 도달 거리 (d⁰) | **1.2 km** (15분 걷기 기준, Wang et al., 2022) |
| 설계 솔루션 수 | 32개 (5개 파라미터 조합) |

---

## 접근성 반영 방식

### 3단계 계산 워크플로 (Fig. 7 참고)

**Step 0**: 보행 네트워크 결정 (Betweenness Centrality로 상위 50% 엣지 선택)

**Step 1**: UTCI 시뮬레이션 → 각 노드별 UTCI 값

**Step 2**: UTCI → PTT(Perceived Time Traveled) 변환
- Rakha(2015) PTT 차트 기반 (Jia & Wang 2021에서도 적용됨)
- UTCI 구간별 선형 공식:
  - No stress (9~26°C): ptt = 1
  - Moderate (26~32°C): ptt = 0.7 + (32 - utci)·(1/20)
  - Strong (32~38°C): ptt = 0.5 + (38 - utci)·(1/30)
  - Very strong (38~46°C): ptt = 0.1 + (46 - utci)·(1/20)
  - Extreme (>46°C): ptt = (50 - utci)·(1/40)

**Step 3**: PDS(Perceived Distance Shortened) 계산
- PDS = (1.0 - PTT) × d⁰

**Step 4**: UTCI-adjusted 도달 거리 계산
- d^utci = d⁰ - PDS = d⁰ × PTT

**Step 5**: POI.reach^utci 계산 (각 노드에서 d^utci 내 도달 가능 POI 수)
- P.reach^utci(G) = Σ POI.reach^utci[i]

### 핵심 지표
- **UTCI-adjusted reach**: 열 스트레스 하에서 재계산된 도달 가능 POI 수
- **ΔP.reach** (delta reach): Baseline reach - UTCI-adjusted reach (POI 수 차이)
- **RUCS**: 전체 노드 중 UTCI < 32°C AND ΔP.reach = 0인 노드 비율(%)

---

## 주요 결과

| 지표 | 값 |
|------|-----|
| RUCS 범위 (단시간, 32개 설계안) | 0.08% ~ 18.0% |
| RUCS 범위 (멀티일) | 6.45% ~ 25.6% |
| 평균 UTCI 범위 | 32.35°C ~ 33.3°C |
| deltaReach0 범위 | 10.4% ~ 29.3% |

### 설계 파라미터 상관관계 (Spearman)
- 공원 위치 ↔ RUCS: **-0.77** (가장 강한 상관)
- 필지 방향 ↔ RUCS: **+0.39**
- 평균 풍속 ↔ UTCI: **-0.81** (풍속이 높을수록 UTCI 낮음)
- 도로 비율 ↔ deltaReach0: **+0.78**

---

## 우리 연구에서 따라할 수 있는 부분

1. **PTT 방식 (소프트 패널티)**
   - Rakha(2015) PTT 차트 → 인지 이동 거리 단축 계산 방식
   - 우리는 현재 Hard Cut 방식 사용. PTT 방식과 비교 실험으로 쓸 수 있음 (Track 2)

2. **UTCI 임계값 32°C**
   - RUCS 기준 32°C 설정 근거 제공 (moderate heat stress 상한)
   - 우리 연구의 MRT ≥55°C (UTCI ≥38°C, Very Strong) 임계값과 비교 서술 가능
   - "Aydin et al.(2026)은 UTCI 32°C를 기준으로 보수적 Cool Spots를 정의한 반면, 본 연구는 Very Strong Heat Stress(UTCI ≥38°C)를 Hard Cut으로 적용하는 보수적 플래닝 시나리오를 채택"

3. **검색 반경 1.2 km**
   - 15분 걷기 = 1.2 km로 설정 (Wang et al., 2022 기반)
   - 우리 연구 TIME_BUDGET=15분, WALK_SPEED=4.5 km/h → 1.125 km ≈ 1.2 km와 유사 → 인용 가능

4. **멀티시간대 분석 필요성**
   - 17:00 단시간 → RUCS 거의 0%가 되는 문제 지적
   - 07:00이 RUCS 가장 높음 → 시간대 선택이 결과에 크게 영향
   - 우리 연구에서 "14:00 폭염 피크 시간대 선정" 근거로 활용

5. **민감도 분석 (Morris SA)**
   - RUCS는 POI 수 > 베이스라인 도달 거리 > 포장재 순으로 민감
   - 우리 연구에서 MRT 임계값 민감도 분석 필요성 지지

---

## 우리 연구와의 차별점

| 항목 | Aydin2026 | 우리 연구 |
|------|-----------|----------|
| 공간 | 싱가포르 112 ha 가상 마스터플랜 | 서울 성동구 실제 역세권 |
| 네트워크 | 생성 모델 자동 생성 | OSM 실제 도로망 |
| 열 패널티 방식 | 소프트 (PTT 기반 거리 단축) | **Hard Cut** (임계 초과 링크 제거) |
| 접근성 종점 | POI (POI count) | 지하철역 (역세권 면적/인구) |
| UTCI 임계값 | 32°C (moderate) | 38°C (very strong) |
| 기후 | 열대우림 (고온다습 연중) | 온대 계절풍 (여름 폭염) |
| 목적 | 도시 설계 최적화 | 취약성 공간 분포 분석 |

---

## 한계 (논문 명시)
- 계산 비용 (CFD: 72h × 96 CPUs)
- 작은 샘플 (32개 설계안)
- 자동 생성 보행로가 도로 비율 높아질 수 있어 결과 편향 가능
- 나무 캐노피, 아케이드, 차양 등 소규모 개입 제외
- 단일 도시·기후에 국한
