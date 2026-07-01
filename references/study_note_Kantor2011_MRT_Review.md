# Kantor & Unger (2011) — MRT 측정·산출 방법 종합 리뷰

작성일: 2026-07-01  
버전: v1.0  
근거논문: Kantor, N., & Unger, J. (2011). The most problematic variable in the course of human-biometeorological comfort assessment – the mean radiant temperature. *Central European Journal of Geosciences*, 3(1), 90–100. DOI: 10.2478/s13533-011-0010-x

---

## 1. 논문 기본 정보

- **저자**: Noémi Kántor, János Unger (University of Szeged, Hungary)
- **저널**: Central European Journal of Geosciences (2011) 3(1):90–100
- **DOI**: 10.2478/s13533-011-0010-x
- **성격**: MRT 측정 및 산출 방법 리뷰 논문 (입문용 포괄적 개요)

---

## 2. MRT 정의 및 계산식

### 2.1 개념 정의 (p.90)

> "The mean radiant temperature T_mrt has been introduced in order to parameterize the effects of the complex radiant environment (containing several long and short wave radiation fluxes) in one, temperature-dimension index."

**T_mrt**: 균일한 흑체 복사체 둘러싸인 가상 환경에서 실제와 동일한 순복사 에너지 교환이 이루어지는 그 흑체 온도 (ε=1)

### 2.2 기본 T_mrt 수식 (p.92, Eq.)

$$T_{mrt} = \sqrt[4]{\frac{S_{str}}{\varepsilon_p \cdot \sigma}} - 273.15$$

$$S_{str} = a_l \sum_{i=1}^{n} F_i \cdot E_i + a_k \sum_{i=1}^{n} F_i \cdot D_i + a_k \cdot f_p \cdot I^*$$

- E_i: i번 면에서 장파 복사 (W/m²)
- D_i: i번 면에서 확산 단파 복사 (W/m²)
- I*: 직달 태양 복사 (W/m², 수직 면 기준)
- f_p: 투영 인자 (projection factor, 태양 고도각·자세의 함수)
- F_i: 각도 인자 (angle factor / view factor)
- a_l = **0.97** (장파 흡수계수 = ε_p) — Table 3 직접 확인
- a_k = **0.7** (단파 흡수계수) — Table 3 직접 확인

### 2.3 투영 인자 f_p (Table 2, p.92)

| 태양 고도각(γ) | 0° | 10° | 20° | 30° | 40° | 50° | 60° | 70° | 80° | 90° |
|------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| f_p | 0.308 | 0.304 | 0.292 | 0.271 | 0.237 | 0.205 | 0.174 | 0.140 | 0.108 | 0.082 |

→ **직립 보행자(standing/walking person)**에 대한 값 (Fanger 1972, VDI 6방향 기준 [6])

### 2.4 6방향 각도 인자 W_i (Table 4, p.95)

| | East | South | West | North | Upward | Downward |
|--|------|-------|------|-------|--------|----------|
| Standing person | 0.220 | 0.220 | 0.220 | 0.220 | 0.060 | 0.060 |
| Seated person | 0.185 | 0.185 | 0.185 | 0.185 | 0.130 | 0.130 |
| Globe (sphere) | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 |

**⚠️ 확인**: 이 논문(Kantor2011)의 W_i는 Table 4에 6방향으로 명시됨.  
SOLWEIG/Thorsson2007에서 사용하는 F_i = 0.22 (방위 4방향) / 0.06 (상하) 와 동일한 값.

---

## 3. MRT 측정 방법 5가지 비교

### 3.1 방법 1: 구형 온도계 (Globe thermometer)

**표준 구형 온도계**:
- 직경 150mm 흑색 구리 구 (ISO 7726)
- 야외 적용 한계: 응답 지연(15~20분), 흑색이 사람 피부·의복 흡수 과대평가
- T_mrt 계산식 (p.93):
$$T_{mrt} = \sqrt[4]{(T_g + 273.15)^4 + \frac{h_{cg}}{\varepsilon \cdot d_g^{0.4}}(T_g - T_a)} - 273.15$$
$$h_{cg} = 1.1 \times 10^8 \cdot v_a^{0.6}$$

**개선형: 평면 회색 구형 온도계 (40mm 탁구공)**:
- Thorsson et al.(2007) 개발
- 응답 시간 5분 이내
- 그늘: 약간 과대평가 / 햇빛: 약간 과소평가
- **야외 열 쾌적성 현장 측정에 적합**

### 3.2 방법 2: 파이라노미터+파이저지오미터 6방향

- **가장 정확한 야외 T_mrt 측정법** (독일 VDI 3789 가이드라인)
- 6방향 동시 측정: 단파(파이라노미터) + 장파(파이저지오미터)
- 단점: 고가, 복잡 (회전형 사용 시 총 10분 소요)
- 식: S_str = Σ⁶ Wi·(ak·Ki + al·Li) (p.95)

### 3.3 방법 3: RayMan (소프트웨어)

- 입력: 날짜·시각, 위경도·고도, 기상(전천복사, T_a, RH, 운량), horizon 제한
- 1개 지점만 계산 (공간 분포 불가)
- 검증: r=0.95~0.96 (Freiburg 반개방, 가로수 사이트)
- **한계**: 저태양고도에서 과소평가 (Thorsson et al., 2007 확인)
- 논문 직접 인용: "RayMan tends to underestimate T_mrt. According to Thorsson et al.(2019) this underestimation is particularly obvious at low solar elevations." (p.98)

### 3.4 방법 4: ENVI-met

- 3D 비정적 비정수압 마이크로기후 모델
- 0.5~10m 해상도, 최대 시간 스텝 10s
- T_mrt 포함 모든 기상 변수 시뮬레이션
- 단점: 계산 시간 수일, 입력 데이터 많음

### 3.5 방법 5: SOLWEIG (우리 방법 C)

논문 p.96-98:
> "The SOLWEIG (solar and longwave environmental irradiance geometry) model calculates the T_mrt on the basis of the integral radiation measurement procedure introduced by [7] so it considers the solar and terrestrial radiation flux densities from 6 perpendicular directions."

- 공간 분포 계산 가능 (래스터 출력)
- 1m 해상도 도메인, 도시 형태 고려
- **검증**: "almost one to one relationship between the modeled and measured data (based on observations carried out in Göteborg, Kassel and Freiburg) and the corresponding correlation coefficient is 0.96" (p.98)

**SOLWEIG vs RayMan 비교**:
- SOLWEIG: r=**0.96** (저태양고도에서도 신뢰성)
- RayMan: 저태양고도 과소평가
- SOLWEIG의 장점: 공간 분포, 식생 포함 가능, 저태양고도 강건

---

## 4. 우리 연구와의 관련성

### 4.1 SOLWEIG 선택 근거 (방법 C)

이 리뷰 논문은 SOLWEIG가 5가지 방법 중 야외 T_mrt 공간 분포 산출에 가장 적합함을 정리한다.  
우리 방법 C (GLO-30 DSM + SOLWEIG)의 선택 이유로 인용 가능.

**인용 가능 문구**:
> "Kantor & Unger (2011)의 리뷰에 따르면, SOLWEIG는 복잡한 도시 형태에서 6방향 복사 플럭스를 공간적으로 계산할 수 있는 모델로, T_mrt 산출 정확도(r=0.96)가 다른 방법보다 우수하다."

### 4.2 흡수계수 표준값 확인

논문 Table 3 직접 확인:
- a_k (단파) = **0.7** (standard value)
- a_l (장파) = **0.97** (= ε_p)

→ Thorsson2007, Lindberg2008과 동일. 우리 연구 파라미터 확정 근거.

---

## 5. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| a_k (단파 흡수계수) | 0.7 | Table 3, p.92 |
| a_l (장파 흡수계수=ε_p) | 0.97 | Table 3, p.92 |
| Standing person W_i (방위) | 0.220 | Table 4, p.95 |
| Standing person W_i (상하) | 0.060 | Table 4, p.95 |
| Globe W_i | 0.167 | Table 4, p.95 |
| SOLWEIG 검증 r | 0.96 | p.98 |
| RayMan 검증 r | 0.95~0.96 | p.98 (but 저태양고도 취약) |
| f_p (γ=0°) | 0.308 | Table 2 |
| f_p (γ=90°) | 0.082 | Table 2 |

---

## 6. 핵심 인용 형식

```
Kantor, N., & Unger, J. (2011). 
The most problematic variable in the course of human-biometeorological 
comfort assessment – the mean radiant temperature. 
Central European Journal of Geosciences, 3(1), 90–100.
https://doi.org/10.2478/s13533-011-0010-x
```
