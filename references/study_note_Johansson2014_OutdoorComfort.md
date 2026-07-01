# Johansson et al. (2014) — 야외 열 쾌적성 측정기기·방법 표준화 리뷰

작성일: 2026-07-01  
버전: v1.0  
근거논문: Johansson, E., Thorsson, S., Emmanuel, R., & Krüger, E. (2014). Instruments and methods in outdoor thermal comfort studies – The need for standardization. *Urban Climate*, 10, 346–366. DOI: 10.1016/j.uclim.2013.12.002

---

## 1. 논문 기본 정보

- **저자**: Erik Johansson (Lund), Sofia Thorsson (Gothenburg), Rohinton Emmanuel (Glasgow), Eduardo Krüger (Brazil)
- **저널**: Urban Climate (2014) 10:346–366
- **DOI**: 10.1016/j.uclim.2013.12.002
- **성격**: 26편 선행연구 기기·방법 리뷰 + 표준화 필요성 제안

---

## 2. T_mrt 측정 방법

### 2.1 가장 정확한 방법: 6방향 적분 복사 측정

ISO 7726:1998 및 독일 VDI 3787 권장:

$$T_{mrt} = \sqrt[4]{(S_{str}/(\varepsilon_p\sigma))} - 273.15 \quad \text{(Eq.1)}$$

$$S_{str} = \alpha_k \sum_{i=1}^{6} K_i F_i + \varepsilon_p \sum_{i=1}^{6} L_i F_i \quad \text{(Eq.2)}$$

- K_i: 단파 복사 플럭스 (파이라노미터)
- L_i: 장파 복사 플럭스 (파이저지오미터)
- F_i: 각도 인자 (standing person: 0.22 방위, 0.06 상하)
- α_k = 0.7, ε_p = 0.97

6방향 동시 측정 장비: Kipp & Zonen CNR 1 3개 사용 (Fig. 1) → Thorsson et al.(2007) 방법

### 2.2 Globe thermometer 방법

**40mm 평면 회색 글로브 (Table tennis ball)**:
$$T_{mrt} = \left[(T_g + 273.15)^4 + \frac{1.335 \times 10^8 V_a^{0.71}}{\varepsilon D^{0.4}}(T_g - T_a)\right]^{1/4} - 273.15 \quad \text{(Eq.3)}$$

- D = 0.04m (40mm 탁구공)
- ε = 글로브 방사율
- V_a: 풍속 (m/s)
- 참고: Thorsson et al.(2007)에서 검증, RAL 7001 (flat grey) 색상

**장단점**:
- 장점: 저렴, 이동 간편, 응답 시간 5분 이내
- 단점: 6방향 측정법 대비 불확실성 (햇빛: 과소, 그늘: 과대)

### 2.3 소프트웨어 모델링

SOLWEIG (Lindberg et al., 2008), ENVI-met (Bruse, 2011), RayMan (Matzarakis et al., 2010)

---

## 3. T_mrt 측정 기준 (ISO 7726:1998)

| 측정 파라미터 | 편안한 환경 | 스트레스 환경 |
|------------|-----------|------------|
| T_mrt 범위 | +10~+40°C | -40~+150°C |
| 요구 정확도 | ±2°C | ±5.8°C (−40°C) |
| 바람직한 정확도 | ±0.2°C | ±0.9°C |

**측정 높이**: ISO 7726:1998 → **앉은 사람: 0.6m, 선 사람: 1.1m** (Table 2)

---

## 4. 열 쾌적성 지표 비교 (Table 4, p.353)

| 지표 | 주요 참고 | 설명 |
|------|---------|------|
| PMV | ASHRAE 55 | 실내용. 의복·활동 표준화 실내 |
| SET* | ASHRAE 2001 | 실내용 기원, 야외 적용 |
| PET | VDI 3787 | 야외용. 4변수만 사용 (T_a와 동일 단위) |
| **UTCI** | Blazejczyk 2012 | **야외용.** 의복 정보 불필요. 참조활동: 135W/m², 1.1m/s |

**UTCI 참조 조건** (논문 직접 확인, p.353):
- 보행 활동: 135 W/m² (2.3 MET에 해당)
- 보행 속도: **1.1 m/s ≈ 4 km/h**

---

## 5. 26편 연구 분석 결과 요약

### 5.1 실험 설계

- 21편(84%): 횡단연구 (transversal) — 사람이 한 번만 참여
- 4편(16%): 종단연구 (longitudinal) — 소수 인원 여러 마이크로기후 경험

### 5.2 측정 지점 및 사이트

- 도심 광장, 보행자 거리, 공원이 가장 일반적
- **Local Climate Zone (LCZ)** 분류 (Stewart & Oke, 2012) 활용 권장

### 5.3 열 지수 사용 현황

- 26편 중 PET, UTCI, PMV 가장 많이 사용
- UTCI: 2010년 이후 급증

---

## 6. 표준화 권고안

논문의 주요 제안:
1. **측정 높이**: 1.1m (선 사람 기준) — 모든 연구 일관 적용
2. **T_mrt 최적 방법**: 파이라노미터+파이저지오미터 6방향 (또는 calibrated globe)
3. **기후대별 현지 검증**: globe 온도계 변환식은 현지 조건에서 검증 필요
4. **설문 표준화**: ISO 10551(1995) 권장 — 7단계 열 감각 척도

---

## 7. 우리 연구와의 관련성

### 7.1 UTCI 사용 정당성

Johansson et al.(2014)는 UTCI를 야외 열 쾌적성 평가에 적합한 지표로 권장함.  
특히 의복 데이터 없이도 적용 가능하다는 점이 도시 전역 스케일 분석에 유리.

**인용 가능 문구**:
> "Johansson et al.(2014)의 리뷰에서 UTCI는 야외 열 쾌적성 평가의 표준화 지표로 권장되며, 의복 정보 없이 적용 가능한 참조 활동(135 W/m², 4 km/h)을 채택한다."

### 7.2 측정 높이 1.1m 표준 확인

우리 연구에서 SOLWEIG 출력 높이 1.1m above ground 선택의 표준 근거:
- ISO 7726:1998 → 선 사람 기준 1.1m
- Lindberg2008, Thorsson2007 모두 동일

### 7.3 UTCI 참조 보행속도 4km/h

우리 WALK_SPEED = **4.5 km/h** vs UTCI 참조 **4 km/h**:
- 차이 소폭 (0.5 km/h) → 동일 MET(2.3) 적용 가능
- 방법론 섹션에서 이 근사 명시 필요

---

## 8. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| T_mrt 측정 표준 높이 (선 사람) | 1.1m | ISO 7726:1998 (Table 1) |
| UTCI 참조 보행속도 | 1.1 m/s ≈ 4 km/h | p.353, Table 4 |
| UTCI 참조 대사량 | 135 W/m² (2.3 MET) | p.353 |
| α_k (단파 흡수계수) | 0.7 | Eq.2, p.349 |
| ε_p (인체 방사율) | 0.97 | Eq.2, p.349 |
| F_i (방위) | 0.22 | Eq.2 |
| F_i (상하) | 0.06 | Eq.2 |

---

## 9. 핵심 인용 형식

```
Johansson, E., Thorsson, S., Emmanuel, R., & Krüger, E. (2014). 
Instruments and methods in outdoor thermal comfort studies – 
The need for standardization. 
Urban Climate, 10, 346–366.
https://doi.org/10.1016/j.uclim.2013.12.002
```
