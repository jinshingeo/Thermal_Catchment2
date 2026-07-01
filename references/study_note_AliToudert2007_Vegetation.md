# Ali-Toudert & Mayer (2007) — 갤러리·비대칭·식생의 열 쾌적성 효과

작성일: 2026-07-01  
버전: v1.0  
근거논문: Ali-Toudert, F., & Mayer, H. (2007). Effects of asymmetry, galleries, overhanging façades and vegetation on thermal comfort in urban street canyons. *Solar Energy*, 81, 742–754. DOI: 10.1016/j.solener.2006.10.007

---

## 1. 논문 기본 정보

- **저자**: Fazia Ali-Toudert, Helmut Mayer (University of Freiburg)
- **저널**: Solar Energy (2007) 81:742–754
- **DOI**: 10.1016/j.solener.2006.10.007
- **배경**: Ali-Toudert & Mayer (2006) 후속 연구 — 단순 대칭 캐니언 → 복잡 형태 확장
- **연구 지역**: Ghardaia, Algeria (32.40°N, 3.80°E) — 동일 조건

---

## 2. 연구 케이스 (Table 1)

| Case | 설명 | H/W |
|------|------|-----|
| I | 갤러리(gallery) 포함 대칭 캐니언 | H/W=2, 4m 높이 갤러리 |
| II | 비대칭 캐니언 (H₁=16m, H₂=8m) | 가변 |
| III | 비대칭 + 오버행 파사드 (H₁=16m, H₂=12m) | 가변 |
| IV | E-W 가로 + 가로수 행 (H/W=2) | H/W=2 |
| V | N-S 가로 + 큰 중앙 가로수 (H/W=1) | H/W=1 |

**기상 설정**: 동일 (알제리 사하라, 1 August, ENVI-met 3.0)

---

## 3. 핵심 결과

### 3.1 갤러리(Gallery) 효과 (Case I)

**E-W 방향**:
- 갤러리 내부 PET: 34~42°C (그늘 확보)
- 주 도로 공간: PET 여전히 66°C 도달 (E-W 방향 한계)
- 갤러리의 효율: E-W 방향에서는 제한적

**N-S 방향** (가장 효과적):
- 정오에 주 도로 전체가 그늘
- 갤러리 PET <34°C
- 논문 직접 인용: "the gallery on the north-facing side is as expected shaded..." (p.748)

**갤러리 PET 역설**:
- 일부 갤러리는 인접 개방 공간보다 PET 최대 4K **높음** 발생 (p.747)
- 원인: SVF 낮음(0.12) → 확산 반사 복사 증가 → T_mrt 과대

### 3.2 비대칭 캐니언 효과 (Case II)

- 좁은 SKY VIEW (SVF=0.39) → 확산 복사 감소하지만 직달 복사 증가
- 비대칭: H/W=1과 H/W=2 사이 열적 상황
- **E-W 방향**: H/W=2보다 약 1/8 면적 추가로 햇빛 노출 (더 불쾌적)
- **N-S 방향**: H/W=2 대비 14:00~17:00 사이 T_mrt 최대 24K 감소 (p.749)

### 3.3 오버행 파사드 효과 (Case III)

- PET 최대값 낮아짐: 66°C → **58°C** (H/W=2 대비)
- N-S 방향에서 가장 효과적
- E-W 방향: 덜 효과적 (태양 측면 조사로 오버행 효율 낮음)

### 3.4 식생(Vegetation) 효과 (Cases IV, V)

**E-W + 가로수 행 (Case IV)**:
- 수관(tree crown) 바로 아래: PET 최대 **22K 감소** (p.751)
- 그러나 냉각 효과는 tree crown 아래에만 집중, 주변부로 퍼지지 않음
- 논문 직접 인용: "leads to a decrease of PET up to 22 K directly under the tree crowns" (p.750)
- 간접 복사 감소(ΔS): 200~850 W/m² 범위

**N-S + 큰 가로수 + 갤러리 (Case V)**:
- PET 최대 **24K 감소** (tree 없는 가로 대비)
- 최적 조합: N-S + H/W=1 + 가로수 + 갤러리

### 3.5 T_a 변화 (Fig. 2c)

- 가로수 있는 캐니언: T_a 최대 1.5K 낮음 (가로수 없는 경우 대비)
- 잎 면적 밀도(LAD) 밀함/가볍함 간 차이 ~0.8K (p.744)

---

## 4. SVF 관련 핵심 내용

비대칭 캐니언(Case II): SVF = 0.46 (Case I 대칭 H/W=2, SVF=0.39 대비 더 큼)

→ SVF 증가: 더 많은 확산 복사 수신 + 더 빠른 야간 냉각

---

## 5. 우리 연구와의 관련성

### 5.1 MRT > T_a: 복사 환경 우세 재확인

논문 p.744:
> "The following analysis focuses on PET which summarizes all these factors and highlights the effects of T_mrt."
> "T_mrt shows larger spatial variation compared to T_a"

→ Ali-Toudert(2007)도 동일하게 T_mrt가 결정적 변수임을 확인

### 5.2 방법 A 약식 MRT의 현실적 한계 인식

이 논문은 ENVI-met 3D 시뮬레이션 기반. 갤러리, 오버행 등 복잡한 기하학적 요소가 T_mrt에 큰 영향을 미침.  
우리 방법 A(약식 SVF 기반 MRT)는 이런 복잡성을 단순화함 — 한계로 명시 필요.

### 5.3 하드 컷 배경으로서 복사 공간 이질성 강조

방법론 섹션에서:
> "Ali-Toudert & Mayer(2006, 2007)는 도시 가로 내 T_mrt의 공간적 이질성이 T_a보다 훨씬 크며, 보행자 열 쾌적성에 결정적 영향을 미침을 실증하였다. 이는 링크 단위 MRT 평가를 통한 Hard Cut 기준 적용의 공간적 타당성을 뒷받침한다."

---

## 6. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| 가로수 아래 PET 감소 | 최대 22K (E-W) | p.750 |
| 가로수+갤러리 조합 PET 감소 | 최대 24K (N-S) | p.751 |
| T_a 감소 (가로수) | 최대 1.5K | p.744 |
| 오버행 PET 최대 | 58°C (vs 66°C) | p.750 |
| 비대칭 캐니언 SVF | 0.46 | p.748 |
| 대칭 H/W=2 SVF | 0.39 | p.748 |

---

## 7. 핵심 인용 형식

```
Ali-Toudert, F., & Mayer, H. (2007). 
Effects of asymmetry, galleries, overhanging façades and vegetation on thermal comfort 
in urban street canyons. 
Solar Energy, 81, 742–754.
https://doi.org/10.1016/j.solener.2006.10.007
```
