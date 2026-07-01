# Bröde et al. (2012) — UTCI 운영 절차 스터디노트

작성일: 2026-07-01  
버전: v1.0  
근거논문: Bröde, P., Fiala, D., Błażejczyk, K., Holmér, I., Jendritzky, G., Kampmann, B., Tinz, B., & Havenith, G. (2012). Deriving the operational procedure for the Universal Thermal Climate Index (UTCI). *Int J Biometeorol*, 56, 481–494. DOI: 10.1007/s00484-011-0454-1

---

## 1. 논문 기본 정보

- **저자**: Peter Bröde, Dusan Fiala, Krzysztof Błażejczyk, Ingvar Holmér, Gerd Jendritzky, Bernhard Kampmann, Birger Tinz, George Havenith
- **저널**: International Journal of Biometeorology (2012) 56:481–494
- **DOI**: 10.1007/s00484-011-0454-1
- **Special Issue**: UTCI
- **배경**: COST Action 730 (EU 지원)

---

## 2. UTCI 핵심 정의

### 2.1 개념 정의

논문 p.481 Abstract:
> "UTCI aimed for a one-dimensional quantity adequately reflecting the human physiological reaction to the multi-dimensionally defined actual outdoor thermal environment."

> "UTCI for a given combination of wind speed, radiation, humidity and air temperature was defined as the air temperature of the reference environment, which according to the model produces an equivalent dynamic physiological response."

**수식 (Eq.1, p.483):**
$$UTCI(T_a, T_r, v_a, p_a) = T_a + Offset(T_a, T_r, v_a, p_a)$$

- T_a: 기온 (°C)
- T_r: 평균복사온도 (°C)
- v_a: 풍속 10m 높이 (m/s)
- p_a: 수증기압 (hPa)

---

### 2.2 참조 조건 (Reference Condition) — 논문 직접 확인 (p.483)

| 항목 | 값 | 비고 |
|------|-----|------|
| Activity | 보행 4 km/h | 135 W/m² (2.3 MET) |
| Wind speed (v_a) | **0.5 m/s** | 10m 높이 (≈1.1m 높이에서 0.3 m/s) |
| Humidity | **rH=50%** (T_a<29°C) | 또는 **p_a=20 hPa** (T_a>29°C) |
| Radiation | T_r = T_a | 복사와 기온 동일 |

논문 p.483:
> "The working group of COST Action 730 agreed upon the former suggestion of 4 km/h as a representative walking speed... The rate of metabolic heat production was assumed to be 2.3 MET (135 W m⁻²)."

---

## 3. ✅ UTCI 열스트레스 분류표 — Table 3, p.489 직접 확인

| UTCI 범위 (°C) | 스트레스 분류 |
|--------------|------------|
| Above +46 | **Extreme heat stress** |
| **+38 to +46** | **Very strong heat stress** ← Hard Cut 기준선 |
| +32 to +38 | Strong heat stress |
| +26 to +32 | Moderate heat stress |
| +9 to +26 | No thermal stress |
| +9 to 0 | Slight cold stress |
| 0 to −13 | Moderate cold stress |
| −13 to −27 | Strong cold stress |
| −27 to −40 | Very strong cold stress |
| Below −40 | Extreme cold stress |

**⚠️ 논문 각주**: "The UTCI subinterval +18 to +26°C within this category complies with the definition of the 'thermal comfort zone'"

**→ 우리 Hard Cut 기준: UTCI ≥ 38°C = Very Strong Heat Stress 하한 = 직접 확인 완료**  
**인용**: Bröde et al. (2012), Table 3, p.489

---

## 4. MRT와 UTCI의 관계

### 4.1 복사 민감도 (p.487, Fig.8)

논문 직접 인용:
> "UTCI increases linearly with radiation by about **3 K per 10 K increment in mean radiant temperature**, as indicated by the regression equation."

→ MRT 10°C 증가 → UTCI 약 3°C 증가

### 4.2 회귀식 (Fig.8 caption, p.488)

$$UTCI = 0.995 \times T_a + 0.27 \times (T_r - T_a), \quad R^2 = 0.99$$

(T_a: 20~50°C 범위, humidity와 wind는 참조 조건 고정)

---

## 5. UTCI 계산 방법 (운영 절차)

### 5.1 정확한 계산 (생리학 모델)
- UTCI-Fiala 다중노드 열조절 모델 실행
- 속도: ~1 calculations/s → 실용적이지 않음

### 5.2 간소화 계산 (실용)

**방법 a: Polynomial regression (6차)** (p.489)
- 속도: >100,000 calculations/s
- RMSE: 약 0.5 K
- 최대 오차: 약 1 K (일부 고풍속 조건에서 더 큼)
- 입력: T_a, T_r-T_a, v_a, p_a (또는 rH)
- **실무에서 가장 많이 사용되는 방법 (pythermalcomfort 라이브러리 등)**

**방법 b: Look-up table (선형 보간)**
- 속도: ~70~80 calculations/s
- RMSE < 0.1 K

---

## 6. UTCI의 습도·풍속·복사 민감도

### 6.1 습도 효과 (p.487)
- 저온(T_a<20°C): 습도 영향 작음
- 고온(T_a>30°C): 습도 증가 → UTCI 증가 (더 더워짐)
- 폭염 조건(T_a~35°C)에서 rH 100%는 rH 50%보다 UTCI 수°C 더 높음

### 6.2 풍속 효과 (p.487, Fig.7)
- T_a > 35°C: 풍속 증가 → 열스트레스 가중 (냉각 효과보다 열전달 효과 우세)
- T_a < 35°C: 풍속 증가 → 열스트레스 감소
- **→ 폭염(T_a~37°C) 조건에서 v_a는 UTCI에 양(+)의 영향**

### 6.3 복사 효과
- MRT = T_a(참조 조건)에서 UTCI ≈ T_a (by definition)
- MRT > T_a일수록 UTCI > T_a
- 10 K MRT 상승 → UTCI 약 3 K 상승

---

## 7. 우리 연구에서의 활용

### 7.1 Hard Cut 기준 인용 근거

```
UTCI ≥ 38°C = Very Strong Heat Stress 하한
출처: Bröde et al. (2012), Table 3, p.489
인용 형식: (Bröde et al., 2012)
```

**논문 초안 문구:**
> "본 연구의 Hard Cut 임계값으로 UTCI 38°C를 채택하였다. 이는 Bröde et al.(2012)의 UTCI 열스트레스 분류 기준에서 Very Strong Heat Stress 범주의 하한(Table 3, p.489)으로, 인체 생리학적 반응이 강력한 열 부하를 나타내는 임계점이다."

### 7.2 UTCI 계산 파라미터

우리 연구에서 UTCI 계산 시 참조 조건과의 차이:
- **우리 보행속도**: 4.5 km/h (참조 조건 4 km/h와 근접, 동일 MET 적용 가능)
- **기상 입력**: S-DoT 센서 (T_a, RH), 풍속 별도 처리
- **복사 입력**: SOLWEIG 산출 MRT (방법 C) 또는 약식 MRT (방법 A)

### 7.3 UTCI 계산 도구

**pythermalcomfort** 라이브러리 활용 (polynomial regression 방법):
- 입력: tdb(기온), tr(MRT), v(1.1m 높이 풍속), rh(상대습도)
- 출력: utci (°C)
- ⚠️ v_a 높이 변환 필요: S-DoT 풍속 → 1.1m 환산

---

## 8. 논문에서 확인된 주요 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| 참조 보행속도 | 4 km/h | p.483 |
| 참조 대사량 | 135 W/m² (2.3 MET) | p.483 |
| 참조 풍속 | 0.5 m/s (10m 높이) | p.483 |
| 참조 습도 | rH=50% (T_a<29°C) / p_a=20 hPa (T_a>29°C) | p.483 |
| Very Strong Heat Stress 하한 | **38°C** | Table 3, p.489 |
| Extreme Heat Stress 하한 | 46°C | Table 3, p.489 |
| MRT 복사 민감도 | 3K per 10K Tr 상승 | p.487 |
| 회귀식 | UTCI ≈ 0.995×Ta + 0.27×(Tr-Ta) | Fig.8, p.488 |
| Polynomial RMSE | ~0.5K | p.489 |

---

## 9. 핵심 인용 형식

```
Bröde, P., Fiala, D., Błażejczyk, K., Holmér, I., Jendritzky, G., 
Kampmann, B., Tinz, B., & Havenith, G. (2012). 
Deriving the operational procedure for the Universal Thermal Climate Index (UTCI). 
International Journal of Biometeorology, 56, 481–494.
https://doi.org/10.1007/s00484-011-0454-1
```
