# Wolf et al. (2025) — CoolWalks for Active Mobility in Urban Street Networks

## 기본 정보
- **저자**: Henrik Wolf, Ane Rahbek Viero, Michael Szell
- **소속**: IT University of Copenhagen (NERDS); TU Dresden; ISI Foundation, Turin; Complexity Science Hub, Vienna
- **저널**: Scientific Reports, 15:14911 (2025)
- **DOI**: https://doi.org/10.1038/s41598-025-97200-2
- **투고/채택**: 2025년 게재

---

## 연구 개요

Manhattan, Barcelona, Valencia 3개 도시의 가로 네트워크와 건물 형태를 결합하여 보행자가 그늘 속에서 걷는 잠재력을 정량화. **CoolWalkability** 지표를 개발해 도시별·시간대별 그늘 보행 기회를 체계적으로 분석.

**핵심 기여**:
- 태양 회피 파라미터 α를 포함한 경로 선택 모델 수립
- CoolWalkability C^α(t) 지표: 도시 전체의 그늘 보행 잠재력을 0~1로 정량화
- 격자형(Manhattan) vs 불규칙형(Barcelona, Valencia) 가로망의 그늘 기회 차이 실증

---

## 핵심 모델

### 경험 길이 (Experienced Length) — 경로 선택 모델

```
λᵢⱼ = α·l^sun_ij + l^shade_ij          ...(1)
```

- l^sun_ij: 햇빛 노출 구간 거리
- l^shade_ij: 그늘 구간 거리
- **α ∈ [1,∞)**: 태양 회피 파라미터 (sun aversion)
  - α=1: 햇빛과 그늘 동등 → 최단거리 선호
  - α=1.5: 햇빛 100m = 그늘 150m로 인식
  - α≫1: 극단적 그늘 선호

경로 P의 최적화: Π*ᵢ→ⱼ = argmin Λ^α_i→j(Πᵢ→ⱼ)

### CoolWalkability (전체 도시)

```
C^α(t) = Σ (Λ^α,*(i→j)(0) − Λ^α,*(i→j)({Sab(t)})) 
          ────────────────────────────────────────────
          Σ (Λ^α,*(i→j)(0) − Λ^α,*(i→j)(1))
```

- Λ*(0): 그늘 없을 때 경험 거리
- Λ*({S}): 실제 그늘 분포에서 경험 거리
- Λ*(1): 완전 그늘일 때 경험 거리
- C^α → 0: 그늘 없거나 효과 없음 / C^α → 1: 완벽한 그늘 제공

### Shadow fraction (링크 단위)

```
Sᵢⱼ(t) = l^shade_ij(t) / lᵢⱼ          ...(4)
```

### Local CoolWalkability (노드 단위)

```
C^α_i(t) = Σⱼ(Λ^α,*(i→j)(0) − Λ^α,*(i→j)({Sab}))
            ────────────────────────────────────────
            Σⱼ(Λ^α,*(i→j)(0) − Λ^α,*(i→j)(1))
```

---

## 데이터 및 공간 범위

| 항목 | 내용 |
|------|------|
| 도시 | Manhattan, Barcelona, Valencia |
| 네트워크 | OSM (bicycle network → centerline proxy) |
| 건물 | Manhattan: NYC OOTI, Barcelona/Valencia: Spanish Cadastre |
| 건물 처리 | 2.5D (footprint polygon + 단일 높이값) |
| 해상도 | 그늘 시뮬레이션: 건물별 태양 위치 기반 |
| 분석 날짜 | 2023년 7월 21일 (여름 대표일) |
| 보행 속도 | **5 km/h** |
| 반경 | 800m (≒10분 보행) |
| α 범위 | α ∈ {1.1, 1.25, 1.5, 2, 4, 10} |

**네트워크 크기 (Table 1)**:
| 도시 | Nodes (ctrl) | Edges (ctrl) |
|------|------------|------------|
| Manhattan | 1,506 | 4,114 |
| Barcelona | 2,780 | 8,572 |
| Valencia | 3,156 | 9,456 |

---

## 주요 결과

### 격자형 도시 (Manhattan)
- **CoolWalkability는 α와 무관**: 규칙적 격자 + 균일 건물 높이 → 그늘 경로 선택지 없음
- 이론적 유도: C^α ≠ f(α) for symmetric grid
- 실증: 4가지 α 값에서 diurnal profile 거의 일치

### 불규칙 가로망 (Barcelona, Valencia)
- α에 따른 CoolWalkability 변화 존재
- 좁은 가로 + 높은 건물 → 그늘 선택 기회 더 많음

### Diurnal Profile
- Manhattan: 11:05(MH1)·13:25(MH2) 두 개 최저점 (Manhattanhenge 현상)
- 실측 Manhattan > 이론 Grid: 건물 높이 이질성 때문

### 공간 클러스터링 (DBSCAN + k-means)
- 도시 내 지역별 CoolWalkability 이질성 존재
- 불규칙 가로망 도시에서 클러스터 차이가 더 뚜렷
- 좁은 가로 + 높은 건물 지역: CoolWalkability 높음

### 녹지(공원) 포함 시
- 8m 캐노피 높이 가정, park를 완전 그늘로 처리
- 정오 전후 CoolWalkability 소폭 향상

---

## 우리 연구에서 따라할 수 있는 부분

### 1. α 파라미터 → 소프트 패널티 설계 참고
- α는 Melnikov2022의 β̄=1.16과 같은 맥락 (햇빛 경로를 더 길게 인식)
- 우리 Track 2 (소프트 패널티) 설계 시 α 개념 응용 가능
- **인용 가능**: "Wolf et al.(2025)은 보행자의 태양 회피 성향을 α ∈ [1.1, 10] 범위로 정량화하는 경로 선택 모델을 제시하였다"

### 2. OSM 자전거 네트워크 → 보행 네트워크 proxy
- OSM bicycle network가 sidewalk network와 98%(Manhattan)/75%(Barcelona)/80%(Valencia) 중복
- 우리 서울 OSM walk network 사용 정당성 확인 (centerline approach 선례)

### 3. CoolWalkability 지표 개념
- 우리 TARR (Thermal Area Reduction Rate)과 개념 유사
- 차이: Wolf는 그늘 라우팅 잠재력, 우리는 역세권 면적 감소율
- **인용 방식**: "Wolf et al.(2025)이 제안한 CoolWalkability가 도시의 그늘 보행 잠재력을 집계하는 것과 달리, 본 연구는 역세권 Thermal Catchment Area의 면적 감소율(TARR)을 지표로 활용한다"

### 4. 건물 그늘 기반 분석 → 우리 MRT 기반과 비교
- Wolf는 건물 그늘(shade fraction)을 직접 사용 → MRT 없음
- 우리는 SOLWEIG MRT → UTCI 변환 → Hard Cut → 더 생리학적으로 근거 있음
- **차별점 서술**: "Wolf et al.(2025)은 그늘 분율(shadow fraction)을 라우팅 비용으로 활용했으나, 본 연구는 SOLWEIG로 계산한 MRT를 기반으로 UTCI를 산출하여 생리학적으로 더 타당한 열 스트레스 지표를 활용한다"

### 5. 격자형 vs 불규칙 가로망 논의
- 서울 성동구 가로망 특성 논의 시 참고
- 격자형이면 그늘 경로 대안이 적다는 논리 → Hard Cut 영향이 더 클 수 있음

---

## 우리 연구와의 차별점

| 항목 | Wolf2025 | 우리 연구 |
|------|----------|----------|
| 열 지표 | 건물 그늘 비율 (물리적) | MRT → UTCI (생리학적) |
| 패널티 방식 | 소프트 (α 경험 거리) | **Hard Cut** (링크 제거) |
| 목적 | 그늘 라우팅 잠재력 | 역세권 접근권 감소 정량화 |
| 결과 지표 | CoolWalkability (0~1) | TARR (%) |
| 도시 | Manhattan, Barcelona, Valencia | 서울 성동구 |
| 스케일 | 도시 전체 | 행정구 전역 (역 7개) |
| 시간 분석 | 하루 diurnal profile | 폭염 특보 발효일 단일 시점 |

---

## 한계 (논문 명시)
- 2.5D 건물 모델 (3D 복잡성 미반영)
- 나무 그늘: 공원 단순 처리 (실제 캐노피 구조 미반영)
- 시간적 다이나믹스 미고려 (이동 중 그늘 변화)
- 보행자 개인 특성 (나이, 건강, 열 민감도) 미반영
- centerline network의 accuracy 한계
