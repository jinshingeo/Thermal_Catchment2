# Geurs & van Wee (2004) — Accessibility Evaluation of Land-use and Transport Strategies

## 기본 정보
- **저자**: Karst T. Geurs, Bert van Wee
- **소속**: Netherlands Environmental Assessment Agency; Delft University of Technology
- **저널**: Journal of Transport Geography, 12 (2004) 127–140
- **DOI**: https://doi.org/10.1016/j.jtrangeo.2003.10.005
- **출판**: 2003년 12월 게재 (2004년 인쇄본)

---

## 연구 개요

접근성(accessibility) 측정 방법을 체계적으로 리뷰하고 분류하는 **고전 문헌**. 이론적 근거, 조작 가능성, 해석 가능성, 정책 평가 유용성 4대 기준으로 다양한 접근성 지표를 평가.

**핵심 기여**:
- 접근성 4대 구성요소 정의
- 4대 측정 관점 (infrastructure → location → person → utility)의 체계적 분류
- 각 접근성 지표의 이론적 타당성 + 실용성 평가 매트릭스

---

## 접근성 구성요소 (4대 Component)

### 1. Land-use component (토지이용 요소)
- 목적지의 양·질·공간 분포 (공급) + 수요 지점의 분포
- 공급과 수요의 경쟁 (예: 학교 정원 제한)

### 2. Transportation component (교통 요소)
- 원점~목적지 이동의 비효용(disutility)
- 이동 시간, 이동 비용(고정+변동), 노력(신뢰성, 편의, 안전 등)
- **수요↔공급 대립**: 인프라 공급 + 통행 수요

### 3. Temporal component (시간 요소)
- 하루 중 기회가 이용 가능한 시간대
- 개인이 특정 활동에 쓸 수 있는 가용 시간
- 예: 상점 영업시간, 출퇴근 시간

### 4. Individual component (개인 요소)
- 개인의 필요(소득, 나이, 성별), 능력(신체 조건, 차량 소유), 기회
- 접근성이 개인별로 크게 달라질 수 있음

---

## 접근성 측정 관점 (4대 Perspective)

### 1. Infrastructure-based measures
- 교통 인프라 수준: 혼잡도, 평균 통행 속도
- **우리 연구 연결**: Hard Cut = 인프라 제거 (열노출 = 인프라 붕괴)
- 단점: Land-use component 미반영

### 2. Location-based measures ← **우리 연구의 관점**
- 거시 수준에서 공간 분포된 활동에 대한 접근성
- **Contour measure (등시선 접근성)**:
  - 일정 이동 비용(시간·거리) 내 도달 가능한 기회 수
  - "30분 내 도달 가능한 일자리 수"
  - 단순하고 해석 용이 → 도시계획에서 널리 사용
- **Potential accessibility measure**:
  - Aᵢ = Σⱼ Dⱼ·e^(−β·cᵢⱼ)
  - 거리 감쇠 함수 포함 (더 복잡하고 이론적으로 우수)

### 3. Person-based measures
- 시공간 지리학(Hägerstrand 1970) 기반
- 개인별 시공간 제약을 고려한 접근성
- 데이터 요구량 높음, 집계 어려움

### 4. Utility-based measures
- 확률적 효용 이론(random utility theory) 기반
- Logsum benefit measure:
  - Aᵢ = ln(Σₖ e^(vₖ))
  - 경제적 해석 가능 (소비자 잉여)

---

## Contour Measure 특성 (우리 연구와 직결)

**정의**: 일정 이동 비용(시간·거리·비용) 내에서 도달 가능한 기회의 수 또는 면적

**장점**:
- 조작 용이 (GIS + 네트워크 분석)
- 해석 용이 → 정책 소통 가능
- 데이터 요구량 낮음 (교통+토지이용 기본 데이터)

**단점**:
- **임계값 내외 기회를 동등 취급** (경계 근처 불연속)
- 거리 감쇠 효과 미반영
- 경쟁 효과 미반영
- Temporal component 명시적 처리 어려움
- Individual component 미반영

**우리 연구에서의 적용**:
- Classic Catchment = 15분(시간 예산) + 4.5km/h 기준 등시선 → 전형적인 contour measure
- Thermal Catchment = Hard Cut 후 재계산한 contour measure
- **[검증 지표] = (Classic − Thermal)/Classic**: 열환경 적용 전후 contour measure 면적 변화율 (지표명 미확정)

---

## 주요 인용 가능 내용

### 접근성 정의
- Hansen (1959): "the potential of opportunities for interaction" (상호작용 기회의 잠재력)
- Dalvi and Martin (1976): "the ease with which any land-use activity can be reached from a location using a particular transport system"
- Burns (1979): "the freedom of individuals to decide whether or not to participate in different activities"

### Contour measure 문헌
- Ingram 1971, Wickstrom 1971, Wachs and Kumagai 1973, Black and Conroy 1977, Guy 1983

---

## 우리 연구에서 따라할 수 있는 부분

### 1. 우리 연구의 이론적 위치 정립 ← D1 해결
- **"우리 Classic Catchment는 location-based contour measure"**
- Geurs & van Wee (2004) 분류 체계에서 정확히 위치 지정 가능
- **인용 방식**: "본 연구의 Classic Catchment Area는 Geurs & van Wee (2004)가 제시한 location-based contour measure에 해당하며, 일정 시간 예산(15분) 내 도달 가능한 보행 공간의 면적을 정량화한다"

### 2. Temporal component 반영 = 우리 연구의 혁신 ← G1 서술 근거
- Geurs & van Wee: 전통적 contour measure는 temporal 요소 미반영
- 우리 연구: 폭염 시간대(13시) × 폭염일 → temporal 제약 명시적 반영
- **차별화 논거**: "전통적 contour measure(Geurs & van Wee, 2004)는 temporal component를 명시적으로 다루지 않으나, 본 연구는 폭염 발생 시간대(13시)를 고정하여 열환경의 시간적 변동성을 반영한다"

### 3. 개인 요소(Individual component) → 취약계층 논의
- 나이, 건강, 소득 등 개인 특성에 따라 접근성 달라짐
- 우리 연구가 집계 수준(역세권 면적)을 다루지만, 취약계층 논의 시 활용 가능

### 4. 접근성 지표의 이론적 기준 제시
- 이론적 타당성, 조작 가능성, 해석 가능성, 정책 유용성
- 우리 [검증 지표]가 이 기준에서 어떻게 평가받는지 서술 가능
  - 이론적 타당성: contour measure (검증된 방법)
  - 조작 가능성: 높음 (GIS + 네트워크 분석)
  - 해석 가능성: 높음 (%, 직관적)
  - 정책 유용성: 높음 (TCA 면적 기반)

---

## 우리 연구와의 관계

| 항목 | Geurs2004 (이론) | 우리 연구 (실증) |
|------|----------------|----------------|
| 접근성 유형 | Location-based, Contour | Location-based, Contour |
| 시간 요소 | 명시적 다루지 않음 | **폭염 시간대 반영** (혁신) |
| 개인 요소 | 이론적 기술 | 집계 수준 (미반영, 한계) |
| 교통 비용 | 이동 시간/거리 | 이동 시간 + **열환경 제약** |
| 스케일 | 이론 리뷰 | 서울 전역 (성동구 파일럿 기반) |

---

## 핵심 인용 문구

**서론 접근성 정의**:
> "접근성은 토지이용-교통 시스템이 개인(집단)에게 활동 참여 기회를 제공하는 정도를 나타낸다(Geurs & van Wee, 2004). 이 중 location-based contour measure는 일정 이동 시간 내 도달 가능한 기회의 수 또는 면적으로 접근성을 정량화하며(Geurs & van Wee, 2004; Ingram, 1971), 본 연구에서 열환경 반영 역세권 접근성 측정의 이론적 근거가 된다."

**Temporal component 확장**:
> "전통적 contour 접근성 지표는 temporal component를 암묵적으로만 다루어왔으나(Geurs & van Wee, 2004), 본 연구는 폭염 발생 시간대(14시)와 UTCI 임계값을 명시적으로 적용하여 temporal 및 individual 요소가 내포된 열환경 제약을 반영한다."
