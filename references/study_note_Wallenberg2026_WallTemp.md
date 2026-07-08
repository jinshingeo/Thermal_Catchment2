# Wallenberg et al. (2026) — 벽 표면온도 step heating 방법 (SOLWEIG)

작성일: 2026-07-01 (2026-07-08 상세 재독·보강, v2.0)
버전: v2.0
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

⚠️ **출처 정정**: 이 값들은 논문이 직접 측정한 게 아니라 **CIBSE(2015)**(영국 건축설비기술자협회 핸드북, Table 1³·2³·3⁴⁶ — 원문엔 "Tables 1 3.37, 2 3.38 and 3 3.46"으로 표기)에서 그대로 인용한 것. 인용 시 "Wallenberg et al.(2026), Table 1(CIBSE 2015 인용)"으로 표기할 것.

| 재료 | λ (W/mK) | ρ (kg/m³) | C (J/kgK) | κ (m²/s ×10⁻⁶) | e (J/m²s^0.5K) |
|-----|---------|---------|---------|-------------|-------------|
| Brick (outer leaf) | 0.84 | 1700 | 800 | 0.62 | 1068 |
| Dense plaster (brick) | 0.57 | 1300 | 1000 | 0.44 | 860 |
| Hardwood (dry) | 0.17 | 700 | 1880 | 0.13 | 472 |

**Table 2 (센서티비티 테스트용 dummy wall, QGIS UMEP 플러그인 기본 3재질과 일치)**:

| 재료 | λ (W/mK) | ρ (kg/m³) | C (J/kgK) |
|---|---|---|---|
| Wood | 0.17 | 700 | 1880 |
| Brick | 0.84 | 1700 | 800 |
| Concrete | 1.17 | 2200 | 840 |

본문 명시: "**Three materials are available in the new publicly available SOLWEIG model: brick, concrete and wood. Other materials can simply be added to the parameter file in SOLWEIG.**" — ⚠️ **재질 미상일 때 무엇으로 대체할지에 대한 지침은 논문에 없음** (다른 재질 추가는 가능하다고만 언급, fallback 규정 없음).

**수식적 성질(Eq.1-3 결합)**: 밀도(ρ)·비열(C)은 e와 t 계산에서 상쇄되어 **최종 Ts에는 영향 없음** — 실제로는 열전도율(λ)과 벽 두께(L)만 Ts를 결정 (논문이 직접 도출·명시).

**검증 실험 실제 벽 두께**: 플라스터벽돌 L=0.1m, 목재 L=0.03m (⚠️ 이전 버전 노트에서 "브릭<0.3m/콘크리트 0.5-0.6m"라 적었던 건 **모델이 불안정해지는 한계두께**(Lmax, R비율 기반)이지 실제 검증 두께가 아님 — 혼동 주의).

**민감도 분석 순위 (Fig.8)**: **알베도·열전도율의 영향력이 가장 크고, 방사율의 영향력이 가장 작음.** 알베도↑→Ts↓(단파흡수 감소), 열전도율↑→Ts↓(열이 표면 안 쌓이고 재질 내부로 전달 — 목재<벽돌<콘크리트 순으로 열전도율이 높아 콘크리트가 표면온도 변화가 제일 적고 "관성적").

**타 모델 대비 성능**: PALM-4U(Resler et al. 2021, Prague) RMSE 3.3°C(전통건물)/7.4°C(현대건물); ENVI-met(Simon 2016) R²=0.98–0.99, RMSE=1.03–1.25°C(단, 통제된 실험실 조건 — 이 논문은 실제 도시환경이라 직접비교 불리한 조건에서도 RMSE 1.94–2.09°C 확보).

**추가 관련 인용**: Kim & Ham(2024) — 아스팔트·합판·토양(수평면) SOLWEIG Ts 시뮬레이션에서도 건축재료 물성 개선 필요성 지적 (이 논문과 같은 문제의식의 수평면 버전).

**그림자캐스팅 알고리즘 출처**: Ratti & Richens(2004) + Lindberg & Grimmond(2011a,b) — 기존에 Lindberg(2011)만 인용했었는데 Ratti & Richens(2004)도 원출처로 확인됨.

**코드·데이터 공개(재현성)**: 코드 https://doi.org/10.5281/zenodo.15309383, 검증데이터셋(DEM/DSM/CDSM/토지피복/기상/관측Ts) https://doi.org/10.5281/zenodo.15309444

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

---

## 10. 우리 프로젝트 적용 검토 (2026-07-08)

**성동구 STRCT_CD(건물구조) 분포 vs Wallenberg 3재질 매칭**:
- 벽돌(11): 32.3% → Brick 직접 매칭
- 철근콘크리트 등(21 등): ~27% → Concrete 직접 매칭 (Table 2)
- 목구조(51): 2.4% → Wood 직접 매칭
- 철골(31/32): ~1.6% → 매칭 없음
- **결측: 32.2%** → 매칭 없음, 논문에 fallback 규정 없음

서울 전체 기준으로는 결측 21.6%, 벽돌+콘크리트+목조 매칭률 74.2%로 더 양호함.

**판단(결론은 본문 대화 참고, 2026-07-08 세션 결정 확정 시 이 섹션 업데이트)**: 재질 미상 처리는 논문이 아니라 우리 자체 판단(예: 최빈값 대체)이 되므로, 사용 시 "이 부분은 자체 가정"이라고 명확히 분리해서 서술해야 함 — Wallenberg(2026)가 검증한 건 "재질을 알 때의 물리식"이지 "모를 때 뭘 가정할지"가 아님.
