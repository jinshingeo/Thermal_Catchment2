# Wallenberg et al. (2026) — 벽 표면온도 step heating 방법 (SOLWEIG)

작성일: 2026-07-01  
버전: v1.0  
근거논문: Wallenberg, N., Holmer, B., Lindberg, F., Lönn, J., Maesel, E., & Rayner, D. (2026). A simple step heating approach for wall surface temperature estimation in the SOlar and LongWave Environmental Irradiance Geometry (SOLWEIG) model. *Geoscientific Model Development*, 19, 1321–1336. DOI: 10.5194/gmd-19-1321-2026

---

## 1. 논문 기본 정보

- **저자**: Nils Wallenberg, Björn Holmer, Fredrik Lindberg, Jessika Lönn, Erik Maesel, David Rayner (University of Gothenburg)
- **저널**: Geoscientific Model Development (2026) 19:1321–1336
- **DOI**: 10.5194/gmd-19-1321-2026
- **발표**: 2026년 2월 12일 (가장 최신 SOLWEIG 개발 논문)

---

## 2. 핵심 기여

### 2.1 기존 방법의 한계

기존 SOLWEIG (Lindberg et al., 2008/2016): 지면 T_s만 경험식으로 추정.  
**벽 표면온도(T_s,wall)는 T_air와 동일하게 가정** → 단순화 오류.

이 논문 지적 (p.1322):
> "Gál and Kántor (2020) found that T_mrt simulated with SOLWEIG was underestimated in sunlit areas and overestimated in shaded areas, and that these offsets could be related to its wall surface temperature parameterization."

### 2.2 새 방법: Step Heating Approach

**Dirac heat pulse 기반 step heating equation** (Eq.1):

$$T_s = \frac{2\omega}{e}\sqrt{\frac{t}{\pi}} + T_{air}$$

- ω: 벽 표면 수신 열플럭스 밀도 (W/m²) = 입사 단파 + 장파 - 반사 - 방출
- e: thermal effusivity (W s^0.5 m⁻² K⁻¹) = √(λρC)
- t: characteristic time (s) = L²/(π²κ), L=벽 두께, κ=열확산율
- T_air: 기온

**Thermal effusivity 계산 (Eq.2)**:
$$e = \sqrt{\lambda\rho C}$$

- λ: 열전도율 (W m⁻¹ K⁻¹)
- ρ: 밀도 (kg m⁻³)
- C: 비열 (J kg⁻¹ K⁻¹)

---

## 3. 벽 재료별 파라미터 (Table 1)

| 재료 | λ (W/mK) | ρ (kg/m³) | C (J/kgK) | κ (m²/s ×10⁻⁶) | e (J/m²s^0.5K) |
|-----|---------|---------|---------|-------------|-------------|
| Brick (outer leaf) | 0.84 | 1700 | 800 | 0.62 | 1068 |
| Dense plaster (brick) | 0.57 | 1300 | 1000 | 0.44 | 860 |
| Hardwood (dry) | 0.17 | 700 | 1880 | 0.13 | 472 |

---

## 4. 검증 결과 — 논문 직접 확인 수치

### 4.1 검증 장소: Gothenburg, Sweden (3층 건물 외벽)

- 관측 기간: 2023년 5월 15일 ~ 8월 31일 (107일, 10분 간격)
- 벽 재료: 목재(wooden, 1층)와 플라스터 벽돌(plaster brick, 2~3층)
- 방위: 154° (남남동)

### 4.2 전체 성능 (Fig.4f, Fig.5f — all data)

| 벽 종류 | R² | RMSE (°C) | MBE (°C) |
|---------|-----|----------|---------|
| **목재(wooden)** | **0.93** | **2.09** | -0.07 |
| **플라스터 벽돌** | **0.94** | **1.94** | -0.92 |

### 4.3 선행 연구 대비

- PALM-4U (벽돌 벽): RMSE 3.3°C (전통) / 7.4°C (현대 건물)
- ENVI-met (플라스터 벽): R²=0.98~0.99, RMSE=1.03~1.25°C (단일 건물, 더 유리)
- 이 논문: 실제 복잡한 도시 환경에서도 RMSE<2.1°C

---

## 5. 단파 복사 계산 (Eqs. 4-7)

$$K_{dir} = (1 - \alpha_{wall}) \times I \times Sh \times \zeta$$
$$K_{diff} = (1 - \alpha_{wall}) \times D \times \psi$$
$$K_{ref} = (1 - \alpha_{wall}) \times (G \times \alpha_{wall} \times F_b + G \times \alpha_g \times F_g)$$

- I: 직달 복사, D: 산란 복사, G: 전천 복사
- Sh: 그늘 Boolean, ζ: 벽에 대한 태양 입사각의 코사인
- ψ: SVF at wall surface (≤0.5, 상반구의 절반만 봄)

**벽의 입사각 계산 (Eq.7)**:
$$\zeta = \cos\eta\cos\theta\cos\varphi + \sin\eta\sin\theta\sin\varphi$$

- η: 태양 고도, θ: 태양 방위각, φ: 벽 방위각 (0°=북향)

---

## 6. T_mrt에 미치는 영향

새 방법으로 T_mrt가 기존 대비 최대 **±2.5°C** 차이:

- 09:00 (낮은 태양 고도): 북서쪽 코너 T_mrt 최대 **+2.5°C** (직달복사 수직 입사)
- 12:00 (정오): 차이 소폭
- 15:00 (서쪽 태양): 북동 코너 ~+2.0°C
- 18:00 (서쪽 태양): ~+1.0°C
- 21:00 (해질녘): ~-0.6°C

---

## 7. 우리 연구와의 관련성

### 7.1 방법 C에서 SOLWEIG 버전 명시

이 논문은 2026년 발표된 최신 SOLWEIG 업데이트. 우리 연구에서 사용하는 SOLWEIG 버전에 따라 이 새 T_s 스킴 포함 여부 결정됨.

- **만약 UMEP/SOLWEIG v2022a 이상 사용**: Wallenberg et al.(2026) 언급 가능
- 이전 버전 사용 시: "기존 T_s 경험식 사용" 명시 + 이 논문 한계 인용

### 7.2 벽 표면온도의 T_mrt 영향 ±2.5°C

우리 연구의 T_mrt 불확실성 구간 설정 시 참조 가능:
> "Wallenberg et al.(2026)에 따르면, SOLWEIG의 벽 표면온도 파라미터화 개선으로 T_mrt가 최대 2.5°C 달라질 수 있다."

### 7.3 아스팔트 vs 벽 재료: 어느 쪽이 T_mrt에 더 중요?

Lindberg2016: 지표면 재료 효과 < 그림자 효과  
Wallenberg2026: 벽 재료가 T_mrt에 ±2.5°C 영향

→ 고층 건물이 밀집한 서울 도심에서 벽 표면온도가 중요한 요소임을 논문에서 논의 필요

---

## 8. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| 검증 R² (목재) | 0.93 | Fig.4f |
| 검증 R² (플라스터 벽돌) | 0.94 | Fig.5f |
| 검증 RMSE (목재) | 2.09°C | Fig.4f |
| 검증 RMSE (플라스터 벽돌) | 1.94°C | Fig.5f |
| T_mrt 영향 (신구 방법 차이) | 최대 ±2.5°C | Fig.6, p.1327 |
| 벽돌 열전도율 | 0.84 W/mK | Table 1 |
| 벽돌 thermal effusivity | 1068 J/m²s^0.5K | Table 1 |
| 목재 thermal effusivity | 472 J/m²s^0.5K | Table 1 |
| SOLWEIG 공간해상도 | 0.5m (이 논문) | p.1324 |

---

## 9. 핵심 인용 형식

```
Wallenberg, N., Holmer, B., Lindberg, F., Lönn, J., Maesel, E., & Rayner, D. (2026). 
A simple step heating approach for wall surface temperature estimation 
in the SOlar and LongWave Environmental Irradiance Geometry (SOLWEIG) model. 
Geoscientific Model Development, 19, 1321–1336.
https://doi.org/10.5194/gmd-19-1321-2026
```
