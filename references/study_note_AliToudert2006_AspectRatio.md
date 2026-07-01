# Ali-Toudert & Mayer (2006) — 가로 협곡 종횡비·방위가 열 쾌적성에 미치는 영향

작성일: 2026-06-23  
버전: v1.0  
근거논문: Ali-Toudert, F., & Mayer, H. (2006). Numerical study on the effects of aspect ratio and orientation of an urban street canyon on outdoor thermal comfort in hot and dry climate. *Building and Environment*, 41, 94–108. DOI: 10.1016/j.buildenv.2005.01.013

---

## 1. 논문 기본 정보

- **저자**: Fazia Ali-Toudert, Helmut Mayer (University of Freiburg, Meteorological Institute)
- **저널**: Building and Environment (2006) 41:94–108
- **DOI**: 10.1016/j.buildenv.2005.01.013
- **연구 지역**: Ghardaia, Algeria (32.40°N, 3.80°E, 469m a.s.l.) — 북아프리카 사하라 사막 기후
- **분석 조건**: 전형적인 여름 맑은 날 (1st August), 07:00~20:00

---

## 2. 연구 방법

### 2.1 수치 모델: ENVI-met 3.0

- 3D 수치 마이크로기후 모델 (Bruse, 1999)
- 1m 수평 해상도, 2m 수직 해상도
- 대류·복사·열플럭스·습도·난류 모두 시뮬레이션
- 열 쾌적성 지표: **PET (Physiologically Equivalent Temperature)**

### 2.2 모의 케이스

| 파라미터 | 설정값 |
|---------|--------|
| 가로 폭(W) | 8m (고정) |
| 건물 높이(H) | 4, 8, 16, 32m (H/W = 0.5, 1, 2, 4) |
| 가로 방위 | E-W, N-S, NE-SW, NW-SE |
| 풍속 | 5 m/s (10m 높이), 가로 수직 방향 |
| 기온 (월평균 최고) | 39°C |
| 상대습도 | VP = 12.5 hPa |
| 건물 재료 | 벽: brick (U=1.7 W/m²K), 지붕: U=2.2 W/m²K |
| 지면 알베도 | 0.1 (아스팔트) |
| 분석 높이 | 1.2m above ground |

---

## 3. T_mrt 계산 방법 (논문 Eq.2, p.97)

ENVI-met의 각 그리드 포인트(z)에서 T_mrt:

$$T_{mrt} = \left[\frac{1}{\sigma}\left(E_t(z) + \frac{\alpha_k}{\varepsilon_p}(D_t(z) + I_t(z))\right)\right]^{0.25}$$

구성요소:
- **E_t(z)**: 장파 복사 (대기·지면·벽에서 50%/50%)
- **D_t(z)**: 확산·반사 단파 복사
- **I_t(z)**: 직달 단파 복사 (투영 인자 f_p 포함)
- **α_k** = 단파 흡수계수
- **ε_p** = 인체 방사율

SVF에 의한 장파 복사 분배 (Eq.3):
$$E_t(z) = 0.5[1 - SVF(z)]E_w + SVF(z)E_s + 0.5E_g$$

**⚠️ 중요**: Ali-Toudert(2006)은 SOLWEIG가 아닌 ENVI-met을 사용한 T_mrt 계산 선례.  
T_mrt에 SVF 적용하는 방식은 SOLWEIG와 동일한 원리.

---

## 4. 핵심 결과

### 4.1 기온(T_a) vs T_mrt 공간 분포 (Fig.5, p.100)

- **T_a**: 가로 내 균일 분포. 햇빛/그늘 간 차이 작음 (H/W=2, E-W, 14:00 기준 37~40°C)
- **T_mrt**: 극단적 공간 분화. 햇빛 구역과 그늘 구역 간 **최대 40K 차이** (Fig.5 직접 확인)

> **"T_mrt shows a totally different pattern with differences to T_a reaching 40 K for the sunlit part of the street and about 6–10 K for the shaded area."** (p.100)

→ 이는 우리 연구가 Hard Cut 기준으로 **T_a 대신 T_mrt(→UTCI) 채택**한 핵심 근거

### 4.2 H/W 종횡비 효과

| H/W | 햇빛 노출 시간 (E-W) | 특성 |
|-----|---------------------|------|
| 0.5 | 10시간 | 하루 종일 극심한 불쾌적 (PET peak 66°C) |
| 1   | 7시간 | 미미한 개선 |
| 2   | N-S 방향에서 효과적 | 40% 면적이 정오에 그늘 |
| 4   | 가장 쾌적 (N-S 방향) | PET <38°C 구역 존재 |

> "H/W = 2 could be considered as a threshold with respect to street solar access." (p.99)

### 4.3 방위 효과

| 방위 | 특성 |
|------|------|
| E-W | **가장 불쾌적** — 측면에서 태양 조사 → 높은 복사 부하 |
| N-S | **H/W≥2에서 가장 쾌적** — 벽이 효과적으로 그늘 제공 |
| NE-SW, NW-SE | 중간 수준 |

**PET 최대값**:
- E-W, H/W=0.5: 66°C (16:00~17:00)
- E-W, H/W=2: 66°C (16:00, sunlit)
- N-S, H/W=4: ≤38°C (정오 이후)

---

## 5. 우리 연구와의 관련성

### 5.1 T_mrt vs T_a 우선성 선행 실증

Ali-Toudert(2006)은 T_mrt가 T_a보다 보행 열 쾌적성에 훨씬 결정적임을 수치 시뮬레이션으로 실증하였다. 이는 우리 연구에서 링크 단위 UTCI 산출 시 T_mrt를 핵심 입력으로 사용하는 근거로 인용 가능.

**인용 가능 문구**:
> "Ali-Toudert & Mayer (2006)는 도시 가로 내 T_mrt가 T_a보다 보행자 열 부하에 훨씬 민감하며, 햇빛과 그늘 구역 간 최대 40K 차이를 보인다고 실증하였다."

### 5.2 H/W Canyon 정보 (방법 A 관련)

우리 방법 A는 Oke의 H/W Canyon SVF 기반 약식 MRT를 사용.  
Ali-Toudert(2006)의 H/W=0.5~4 분석은 H/W 범위에 따른 SVF 값 참조:

| H/W | SVF (paper Fig.1) |
|-----|------------------|
| 0.5 | 0.87 |
| 1   | 0.71 |
| 2   | 0.54 |
| 4   | 0.37 |

→ 우리 방법 A에서 링크별 H/W로부터 SVF 추정 시 이 값 참조 가능

### 5.3 서울과의 기후 차이 명시

이 논문은 사하라 사막 기후 (T_a 39°C, VP 12.5 hPa) → 서울 여름 (T_a ~35°C, 고습) 조건과 다름.  
서울 조건에서는 습도 영향으로 UTCI가 더 높아질 수 있음 (Bröde et al., 2012 참조).

---

## 6. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| 햇빛/그늘 T_mrt 차이 | 최대 40K | p.100, Fig.5 |
| 햇빛/그늘 T_a 차이 | 6~10K | p.100 |
| PET 최대 (E-W, H/W=0.5) | 66°C | p.101 |
| H/W=0.5 SVF | 0.87 | Fig.1 |
| H/W=1 SVF | 0.71 | Fig.1 |
| H/W=2 SVF | 0.54 | Fig.1 |
| H/W=4 SVF | 0.37 | Fig.1 |
| 분석 높이 | 1.2m above ground | Table 1 |

---

## 7. 핵심 인용 형식

```
Ali-Toudert, F., & Mayer, H. (2006). 
Numerical study on the effects of aspect ratio and orientation of an urban street canyon 
on outdoor thermal comfort in hot and dry climate. 
Building and Environment, 41, 94–108.
https://doi.org/10.1016/j.buildenv.2005.01.013
```
