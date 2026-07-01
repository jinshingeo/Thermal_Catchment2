# Thorsson et al. (2007) — MRT 측정·산출 방법 비교 스터디노트

작성일: 2026-07-01  
버전: v1.0  
근거논문: Thorsson, S., Lindberg, F., Eliasson, I., & Holmer, B. (2007). Different methods for estimating the mean radiant temperature in an outdoor urban setting. *Int J Climatol*, 27, 1983–1993. DOI: 10.1002/joc.1537

---

## 1. 논문 기본 정보

- **저자**: Sofia Thorsson, Fredrik Lindberg, Ingegärd Eliasson, Björn Holmer (Göteborg University)
- **저널**: International Journal of Climatology (2007) 27:1983–1993
- **DOI**: 10.1002/joc.1537
- **측정 장소**: Göteborg, Sweden (57°42'N, 11°58'E) 대형 광장
- **측정 기간**: 2005년 10월, 2006년 7월~8월 (총 5일, 일출~일몰)

---

## 2. 비교 방법 3가지

### 방법 A — Integral radiation measurements (가장 정확, 비용 높음)

3차원 단파·장파 복사 플럭스 직접 측정 → 각도 인자 적용 → MRT 계산

**계산식 (Eq.1, p.1985):**
$$S_{str} = \alpha_k \sum_{i=1}^{6} K_i F_i + \varepsilon_p \sum_{i=1}^{6} L_i F_i$$

- K_i: 단파 복사 (i=1~6방향)
- L_i: 장파 복사 (i=1~6방향)
- α_k = **0.7** (단파 흡수계수, standard value)
- ε_p = **0.97** (인체 방사율, standard value)
- F_i = **0.22** (직립 보행자, 동서남북 4방위)
- F_i = **0.06** (직립 보행자, 위·아래)
- F_i = **0.167** (구, 6방향 균등)

**MRT 변환 (Eq.2, p.1986):**
$$T_{mrt} = \sqrt[4]{\frac{S_{str}}{\varepsilon_p \sigma}} - 273.15$$

- σ = **5.67 × 10⁻⁸ Wm⁻²K⁻⁴**

**측정 장비**: Kipp & Zonen CNR 1 (3개 net radiometer), 1.1m 높이

---

### 방법 B — 38 mm flat grey globe thermometer

간단한 현장 측정 도구. 글로브 온도에서 MRT 역산.

**계산식 (Eq.3, p.1986):**
$$T_{mrt} = \left[\left(T_g + 273.15\right)^4 + \frac{1.1 \times 10^8 V_a^{0.6}}{\varepsilon D^{0.4}} \left(T_g - T_a\right)\right]^{1/4} - 273.15$$

- T_g: 글로브 온도 (°C)
- V_a: 풍속 (ms⁻¹)
- T_a: 기온 (°C)
- D = **38 mm** (글로브 직경)
- ε = 글로브 방사율

**보정된 대류 계수 (Eq.4, p.1990):**
$$T_{mrt} = \left[\left(T_g + 273.15\right)^4 + \frac{1.335 \times 10^8 V_a^{0.71}}{\varepsilon D^{0.4}} \left(T_g - T_a\right)\right]^{1/4} - 273.15$$

→ 이 보정식 사용 시 Method A와 95% 신뢰구간 오차 ≈ **±3.5 K**

---

### 방법 C — Rayman 1.2 software (단순 모델)

Matzarakis(2000) 개발. 장소·시각·건물 기하학·기상 입력으로 T_mrt 계산.
- **입력**: 위치, 시각, 건물 기하학, 기상(전천복사, 기온, 습도), 알베도, Bowen비, 확산/전천복사 비율
- **기본값 사용**: 알베도 0.3, Bowen비 1.3, 확산/전천복사 비율 0.2
- **한계**: 건물 형태 정보 없으면 공간 변이 반영 불가

---

## 3. 비교 결과 — 논문 직접 확인 수치

### 3.1 방법 A vs B (Globe thermometer)

논문 Abstract:
> "Results show that the difference between Method A and Method B was generally relatively small."

- 5분 평균값 사용 시 차이 크게 감소
- 맑은 날, 5분 평균: 차이 **≈ 3.8 K** 이하 (Eq.4 적용 시)
- 그늘↔햇빛 전환 시 잠시 차이 증가 (응답 지연)
- 결론: "The 38 mm flat grey globe thermometer provides a good and cheap solution." (Abstract)

### 3.2 방법 A vs C (Rayman)

**여름 맑은 날 (26 July 2006)**:
- 정오: T_mrt(A) ≈ **58.8°C**, T_mrt(C) ≈ **57.5°C** → 차이 작음
- 오전/오후(저태양고도): Rayman 크게 과소평가

**가을 맑은 날 (11 Oct 2005)**:
- 정오: T_mrt(A) ≈ **46.9°C**, T_mrt(B) ≈ **43.5°C**, T_mrt(C) ≈ **34.3°C**
- Method C가 정오에도 **약 12.6°C** 과소평가

논문 Abstract 직접 인용:
> "Method C works very well during the middle of the day in July, i.e. at high sun elevations. However, the model considerably underestimates the T_mrt in the morning and evening in July and during the whole day in October, i.e. at low sun elevations."

### 3.3 T_mrt 피크 시각 (여름 맑은 날)

논문 p.1987:
> "T_mrt standing man (Method A) and T_mrt (Tg) (Method B) reached their highest values in the afternoon, between **2 and 3 p.m.** These were **58.8°C** and **60.2°C** respectively."

→ **여름 맑은 날 MRT 피크는 13시가 아닌 14~15시** (태양고도 최대 시각보다 1~2시간 늦음)  
→ 13시는 태양고도 최대(남중)이지만, MRT 피크는 열 축적으로 14~15시에 발생

---

## 4. 방법별 한계 정리

| 방법 | 장점 | 한계 |
|------|------|------|
| A (integral) | 가장 정확 | 비용·설치 복잡, 대규모 공간 적용 불가 |
| B (globe thermo) | 간단·저비용 | 5분 이상 응답 지연, ±3.5K 오차 |
| C (Rayman) | 소프트웨어 사용 편리 | **저태양고도(오전/오후/가을)에서 심각한 과소평가** |

---

## 5. 우리 연구와의 관련성

### 5.1 "방법 A" 명칭 혼동 주의

**⚠️ 중요**: 우리 연구의 "방법 A (약식 MRT)"는 Thorsson2007의 "Method A"와 다르다.

| 항목 | Thorsson2007 Method A | 우리 연구 방법 A |
|------|---------------------|----------------|
| 내용 | 3D 복사 직접 측정 + 각도 인자 | Oke H/W Canyon SVF 기반 약식 근사 |
| 정확도 | 가장 정확 (ground truth) | 근사 방법 |
| 적용 규모 | 단일 포인트 측정 | 도시 전체 링크 단위 |

### 5.2 SOLWEIG vs Rayman

우리 방법 C는 SOLWEIG (Lindberg et al., 2008)를 사용하며, 이는 Thorsson2007의 Rayman(Method C)보다 발전된 모델:
- SOLWEIG: 도시 래스터 DEM 기반, SVF 픽셀 단위 계산, 공간 분포 산출
- Rayman: 단일 포인트, 건물 기하학 단순화

**인용 가능**: "Thorsson et al.(2007)은 단순 모델(Rayman)이 저태양고도 조건에서 T_mrt를 크게 과소평가함을 보고하였으며, 이후 개발된 SOLWEIG(Lindberg et al., 2008)는 도시 래스터 DEM 기반의 픽셀 단위 계산으로 이러한 한계를 개선하였다."

### 5.3 13시 선택 근거 재검토

Thorsson2007 결과: **여름 맑은 날 MRT 피크 = 14~15시** (방법 A 기준)

우리 연구에서 13시를 선택한 경우:
- 13시 = 태양남중(단파복사 피크) 근방
- MRT 피크는 14~15시이나, 13시도 상위권 (열축적 시작 직후)
- 분석 시각 선택 시 이 점 논의 필요

### 5.4 측정 높이 통일

- Thorsson2007: **1.1m above ground** (성인 중심 무게 높이 기준)
- Lindberg2008: 동일 1.1m
- 우리 연구: 동일 기준 적용

---

## 6. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| α_k (단파 흡수계수) | 0.7 | p.1985, "standard value" |
| ε_p (인체 방사율) | 0.97 | p.1985, "standard value" |
| F_i (보행자, 방위) | 0.22 | p.1985, Fanger (1972) |
| F_i (보행자, 상하) | 0.06 | p.1985 |
| F_i (구) | 0.167 | p.1985 |
| σ | 5.67×10⁻⁸ Wm⁻²K⁻⁴ | p.1986 |
| 측정 높이 | 1.1m above ground | p.1984 |
| 여름 MRT 피크 (Method A) | 58.8°C | p.1987 |
| 여름 MRT 피크 시각 | 14~15시 (오후 2~3시) | p.1987 |
| A vs B 오차 (95% CI) | ±3.5 K | p.1990 |

---

## 7. 핵심 인용 형식

```
Thorsson, S., Lindberg, F., Eliasson, I., & Holmer, B. (2007). 
Different methods for estimating the mean radiant temperature in an outdoor urban setting. 
International Journal of Climatology, 27, 1983–1993.
https://doi.org/10.1002/joc.1537
```
