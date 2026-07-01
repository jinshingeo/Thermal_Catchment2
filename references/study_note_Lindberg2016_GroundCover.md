# Lindberg et al. (2016) — 지표면 특성이 MRT에 미치는 영향 (SOLWEIG ground cover scheme)

작성일: 2026-07-01  
버전: v1.0  
근거논문: Lindberg, F., Onomura, S., & Grimmond, C. S. B. (2016). Influence of ground surface characteristics on the mean radiant temperature in urban areas. *International Journal of Biometeorology*, 60, 1439–1452. DOI: 10.1007/s00484-016-1135-x

---

## 1. 논문 기본 정보

- **저자**: Fredrik Lindberg, Shiho Onomura, C. S. B. Grimmond (Gothenburg + Reading)
- **저널**: International Journal of Biometeorology (2016) 60:1439–1452
- **DOI**: 10.1007/s00484-016-1135-x
- **주요 기여**: SOLWEIG에 지표면(ground cover) 유형별 T_s 추정 스킴 추가

---

## 2. 핵심 연구 목적

기존 SOLWEIG는 지표면 온도(T_s)를 단일 경험식으로 추정. 이 논문은 **지표면 재료(아스팔트/잔디/물 등)에 따라 T_s를 차별화**하여 T_mrt 정확도 개선.

---

## 3. 모델 방법론

### 3.1 SOLWEIG 기본 MRT 계산 (Eq.2)

$$R = \xi_k \sum_{i=1}^{6} K_i F_i + \varepsilon_p \sum_{i=1}^{6} L_i F_i$$

- F_i = **0.22** (동서남북 방위), **0.06** (상하) — Fanger 1970, VDI 1994
- ξ_k = **0.7**, ε_p = **0.97**
- T_mrt 산출: Stefan-Boltzmann law (Lindberg et al., 2008 Eq.2)

### 3.2 신규 Ground Cover Scheme

**지표면 T_s 추정 (outgoing shortwave)**:

$$K_{\uparrow} = \Psi_{g\_sunlit(\alpha)} I \sin\eta + \Psi_{g\_All(\alpha)}\left(\alpha_w\left[1 - \left(\Psi_{sky,b} - (1-\Psi_{sky,v})(1-\tau)\right)\right](G(1-f_s) + Df_s)\right) \quad \text{(Eq.16)}$$

**장파 복사 (지표면에서)**:

$$L_{\uparrow} = \Psi_g \left[\varepsilon_{ground}(i)\sigma T_a + (S_b - (1-S_v)(1-\tau))(T_s - T_a)^4\right] \quad \text{(Eq.17)}$$

### 3.3 지표면별 파라미터 (Table 1 직접 확인)

| 지표면 | 방사율(ε) | 알베도(α) | T_diffmax/η_max (°C/°) | T_start (°C) | T_diffmax 최대 시각 |
|--------|---------|---------|----------------------|------------|-----------------|
| **아스팔트** | 0.95 | 0.18 | **0.59** | -10.12 | 15:00 (local) |
| Cobble stones | 0.95 | 0.20 | 0.37 | -3.41 | 14:00 |
| **잔디** | 0.94 | 0.16 | **0.21** | -3.38 | 14:00 |
| 물 | 0.98 | 0.05 | 0.00 | 0.00 | NA |

※ 값은 Oke (1987) 및 현지 측정에서 도출

**선형 회귀 (T_diffmax vs η_max)**:
- 아스팔트: R²=**0.93**, y = 0.59x − 10.12 (n=71)
- 잔디: R²=**0.67**, y = 0.21x − 3.38

---

## 4. 검증 결과

### 4.1 Gothenburg, Sweden (측정 기간 2011-07~2012-12)

- 아스팔트 표면 온도 피크: **45.6°C** (오후 2시, 맑은 날)
- 잔디 표면 온도 피크: **31.6°C** (오후 2시)
- 그늘 구역: T_s = T_a (주간)

### 4.2 London Barbican Estate (검증, 2014 여름)

**잔디 사이트 (Site 1)**:
- 관측 vs 모델 T_mrt: 전반적으로 일치
- 잔디 스킴 적용 시 잔디 미적용 대비 T_mrt **-5.2°C** (오후 4시, sunlit 위치)

**아스팔트(포장 podium) 사이트 (Site 2)**:
- 아스팔트 스킴 적용으로 outgoing longwave radiation(L_up) 개선
- 새 스킴이 기존 스킴보다 잔디 L_up 성능 향상 (오후 13:00, 71→5 W/m² 오차 감소)

---

## 5. 핵심 결과: 그림자 vs 지표면 재료 영향 비교

논문 Abstract 직접 인용:
> "The influence of ground surface materials on T_mrt is **small compared to the effects of shadowing**. Nevertheless, altering ground surface materials could contribute to a reduction in T_mrt to reduce the radiant load during heat-wave episodes in locations where shadowing is not an option."

**수치 근거**:
- sunlit 위치: 아스팔트 vs 잔디 T_mrt 차이 = **~1.5°C** (오후 4시)
- shadowed 위치: 아스팔트 vs 잔디 T_mrt 차이 = **-38.2°C** (그늘 내에서 차이 반전)
  - → 그늘이 되면 잔디가 오히려 더 높은 T_mrt (long-wave 때문)

**결론**: T_mrt의 공간 분포는 그림자 패턴이 지배적. 지표면 재료는 보조적 역할.

---

## 6. SOLWEIG 기상 입력 요구 사항

논문 p.1440 직접 확인:
> "The model requires weather time-series (> 1 minute) for ambient air temperature (T_a), relative air humidity (RH), global (G), direct (I) and diffuse (D) solar radiation, together with a digital surface model (DSM) and site geographical information (i.e. latitude, longitude, and altitude)."

**→ 필수 기상 입력**: T_a, RH, G(전천복사), I(직달복사), D(산란복사)  
**→ 필수 공간 입력**: DSM (+ 식생 있으면 CDSM)

---

## 7. 우리 연구와의 관련성

### 7.1 방법 C (GLO-30 + SOLWEIG) 기상 입력 파이프라인 근거

논문에서 확인된 SOLWEIG 필수 기상 입력은 우리 S-DoT 데이터로 일부 대체 필요:
- T_a, RH: S-DoT 직접 제공
- G, I, D: S-DoT에 있으면 직접, 없으면 T_a + RH로 추정 (Reindl et al., 1990)

### 7.2 지표면 파라미터 선택

우리 연구는 서울 보행 링크 분석 → 주요 지표면은 **아스팔트**:
- ε = 0.95, α = 0.18 (Lindberg2016 Table 1 직접 인용 가능)

### 7.3 그림자가 T_mrt를 지배한다는 결론 인용

Hard Cut 정당성 강화:
> "Lindberg et al.(2016)에 따르면, 도시 T_mrt의 공간 분포는 그림자 패턴이 지배적이며(ground cover 효과 < shadowing 효과), 이는 보행 링크에서의 일조/그늘 여부가 열 부하 평가의 핵심 요소임을 지지한다."

---

## 8. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| 아스팔트 방사율 | 0.95 | Table 1 |
| 아스팔트 알베도 | 0.18 | Table 1 |
| 잔디 방사율 | 0.94 | Table 1 |
| 잔디 알베도 | 0.16 | Table 1 |
| 아스팔트 T_diffmax/η_max | 0.59 | Table 1, R²=0.93 |
| 잔디 T_diffmax/η_max | 0.21 | Table 1, R²=0.67 |
| 아스팔트 T_diffmax 최대 시각 | 15:00 (local) | Table 1 |
| sunlit 아스팔트 vs 잔디 T_mrt 차이 | ~1.5°C | Fig.5c, p.1447 |
| shadowing vs ground cover 효과 비교 | shadowing 압도적 지배 | Abstract |
| SOLWEIG 필수 기상 입력 | T_a, RH, G, I, D | p.1440 |

---

## 9. 핵심 인용 형식

```
Lindberg, F., Onomura, S., & Grimmond, C. S. B. (2016). 
Influence of ground surface characteristics on the mean radiant temperature in urban areas. 
International Journal of Biometeorology, 60, 1439–1452.
https://doi.org/10.1007/s00484-016-1135-x
```
