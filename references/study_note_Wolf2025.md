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

| 항목 | 내용 | 논문 직접 확인 |
|------|------|--------------|
| 도시 | Manhattan, Barcelona, Valencia | ✅ |
| 네트워크 | OSM bicycle network (centerline proxy) | ✅ Data 섹션 |
| 건물(Manhattan) | NYC Office of Technology and Innovation | ✅ Data 섹션 |
| 건물(Barcelona/Valencia) | General Directorate for Cadastre of Spain | ✅ Data 섹션 |
| 건물 처리 방식 | **2.5D standard** — footprint-polygon + singular height value (건물 전체 constant) | ✅ Data 섹션 직접 인용 |
| 분석 날짜 | 2023년 7월 21일 단일 날짜, 시간대별 분석 | ✅ "fixed times during the 21st of July 2023" |
| 보행 속도 | **5 km/h** | ✅ "average speed of 5km/h" |
| 반경 | V_dst(i) = {j ∈ V \| Λ¹ < 800m} → 약 10분 보행 | ✅ 수식 및 본문 |
| α 범위 | α ∈ {1.1, 1.25, 1.5, 2, 4, 10} | ✅ |

### ✅ 2.5D 표준 문구 — 논문 Data 섹션 직접 인용

> "Given the sparse availability of full 3D building data, and for computational simplicity, we handle building data following the **2.5D standard**, i.e. consisting of a footprint-polygon and a singular height value which is simplified as **constant across the whole building**."

→ 이것이 우리 `18_synthetic_dsm.py`의 방식(건물 footprint + 층수×3m 단일 높이)과 동일. **우리 논문의 합성 DSM 방식 정당화에 인용 가능.**

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

### 녹지(공원) 포함 시 — ✅ 논문 직접 확인 (p.10 "Incorporating green spaces")

> "We used this data to re-run our simulations, modeling each park in our study areas as a **canopy of 8m height**, assuming a park to be fully covered and shaded by trees and able to cast a shadow on surrounding streets."

- OSM의 park 데이터를 활용 → 각 공원을 8m 높이 캐노피로 모델링
- park = 완전 그늘 처리, 주변 거리에 그림자 투영
- 결과: 정오 전후 CoolWalkability 소폭 향상 (Figs. SI7-9)
- Wolf2025도 8m에 대한 별도 인용 논문 없음 — 가정값으로 사용

**우리 코드와의 관계 (TREE_HEIGHT=8m)**:
- 공통점: urban tree canopy 8m 가정
- 차이점: Wolf는 **공원(park)** 캐노피, 우리는 **가로수(street tree)** 높이
- 인용 가능 범위: "Wolf et al.(2025)의 도시 수목 캐노피 8m 가정을 준용" 정도

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
- 우리 [검증 지표]와 개념 유사 (지표명 미확정)
- 차이: Wolf는 그늘 라우팅 잠재력, 우리는 Thermal Catchment 면적 감소율
- **인용 방식**: "Wolf et al.(2025)이 제안한 CoolWalkability가 도시의 그늘 보행 잠재력을 집계하는 것과 달리, 본 연구는 Thermal Catchment Area의 감소율([검증 지표])을 지표로 활용한다"

### 4. 건물 그늘 기반 분석 → 우리 MRT 기반과 비교
- Wolf는 건물 그늘(shade fraction)을 직접 사용 → MRT 없음
- 우리는 SOLWEIG MRT → UTCI 변환 → Hard Cut → 더 생리학적으로 근거 있음
- **차별점 서술**: "Wolf et al.(2025)은 그늘 분율(shadow fraction)을 라우팅 비용으로 활용했으나, 본 연구는 SOLWEIG로 계산한 MRT를 기반으로 UTCI를 산출하여 생리학적으로 더 타당한 열 스트레스 지표를 활용한다"

### 5. 격자형 vs 불규칙 가로망 논의
- 서울 가로망 특성 논의 시 참고
- 격자형이면 그늘 경로 대안이 적다는 논리 → Hard Cut 영향이 더 클 수 있음

---

## 우리 연구와의 차별점

| 항목 | Wolf2025 | 우리 연구 |
|------|----------|----------|
| 열 지표 | 건물 그늘 비율 (물리적) | MRT → UTCI (생리학적) |
| 패널티 방식 | 소프트 (α 경험 거리) | **Hard Cut** (링크 제거) |
| 목적 | 그늘 라우팅 잠재력 | 역세권 접근권 감소 정량화 |
| 결과 지표 | CoolWalkability (0~1) | [검증 지표] (%) |
| 도시 | Manhattan, Barcelona, Valencia | 서울 전역 |
| 스케일 | 도시 전체 | 서울 전역 |
| 시간 분석 | 하루 diurnal profile | 폭염 특보 발효일 단일 시점 |

---

## 한계 (논문 명시)
- 2.5D 건물 모델 (3D 복잡성 미반영)
- 나무 그늘: 공원 단순 처리 (실제 캐노피 구조 미반영)
- 시간적 다이나믹스 미고려 (이동 중 그늘 변화)
- 보행자 개인 특성 (나이, 건강, 열 민감도) 미반영
- centerline network의 accuracy 한계
