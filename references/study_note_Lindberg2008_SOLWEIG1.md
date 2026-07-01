# Lindberg et al. (2008) — SOLWEIG 1.0 스터디노트

작성일: 2026-06-23  
버전: v1.0  
근거논문: Lindberg, F., Holmer, B., & Thorsson, S. (2008). SOLWEIG 1.0 – Modelling spatial variations of 3D radiant fluxes and mean radiant temperature in complex urban settings. *Int J Biometeorol*, 52, 697–713. DOI: 10.1007/s00484-008-0162-7

---

## 1. 논문 기본 정보

- **저자**: Fredrik Lindberg, Björn Holmer, Sofia Thorsson (Göteborg University)
- **저널**: International Journal of Biometeorology (2008) 52:697–713
- **DOI**: 10.1007/s00484-008-0162-7
- **키워드**: Digital elevation model, Integral radiation modelling, Mean radiant temperature, Outdoor thermal comfort

---

## 2. SOLWEIG 모델 구조 — 논문 직접 확인 수치

### 2.1 모델 차원

논문 p.698 직접 인용:
> "SOLWEIG 1.0 is a 2.5-dimensional model in the sense that it applies a 2.5-dimensional DEM (i.e. x and y coordinates with height attributes) in the calculation of T_mrt. However, the output from the current version of SOLWEIG is represented in two dimensions (x and y)."

→ **2.5D 모델**: x,y 좌표 + 높이 속성. 출력은 2D 래스터.

---

### 2.2 MRT 계산 수식 (Eq.1, Eq.2, p.699)

**Mean radiant flux density (S_str):**

$$S_{str} = \zeta_k \sum_{i=1}^{6} K_i F_i + \varepsilon_p \sum_{i=1}^{6} L_i F_i \quad \text{(Eq.1)}$$

- K_i: 단파 복사 플럭스 (i=1~6)
- L_i: 장파 복사 플럭스 (i=1~6)
- F_i: 사람과 주변 면 사이의 각도 인자

**Angular factor F_i (Fanger 1972, VDI 1994):**
- 직립 보행자: F_i = **0.22** (동서남북 4방위), **0.06** (위아래)
- 구(sphere): F_i = 0.167 (6방향 균등)

**흡수·방사 계수:**
- ζ_k = **0.7** (단파 흡수계수, standard value)
- ε_p = **0.97** (인체 방사율, standard value)

**MRT 변환 (Stefan-Boltzmann):**

$$T_{mrt} = \sqrt[4]{\frac{S_{str}}{\varepsilon_p \sigma}} + 273.15 \quad \text{(Eq.2)}$$

- σ = Stefan-Boltzmann constant = **5.67 × 10⁻⁸ Wm⁻²K⁻⁴**

---

### 2.3 단파 복사 계산 (Eq.3, p.699)

수직 방향 단파 복사 (도시 내 하나의 픽셀):

$$K_{1ij} = K_{dir} \times Sh_{ij} \times \sin\eta + K_{diff} \times \Psi_{ij} + G \times \alpha \times (1 - \Psi_{ij}) \times \sin\eta \quad \text{(Eq.3)}$$

- K_dir, K_diff, G: 직달·산란·전천 복사
- Sh_ij: 그늘 유무 Boolean (0=그늘, 1=햇빛)
- η: 태양 고도각 (altitude angle)
- Ψ_ij: SVF (Sky View Factor) — 특정 픽셀에서의 천공률
- α: 반사율 = **0.15** (전체 연구 지역 평균값 — 논문 직접 확인)

---

### 2.4 장파 복사 계산 (Eq.7, p.699)

$$L_{1ij} = \Psi_{ij} \varepsilon_{sky} \sigma T_a^4 + (1 - \Psi_{ij}) \varepsilon_w \sigma T_s^4 + (1 - \Psi_{ij})(1 - \varepsilon_w) \varepsilon_{sky} \sigma T_a^4$$

- ε_sky: 하늘 방사율 (Prata 1996 공식 사용)
- ε_w: 벽·지면 방사율
- T_s: 건물 벽·지면 평균 온도

**Prata 공식 (clear sky):**
$$\varepsilon_{sky} = 1 - \left(1 + 46.5\frac{e_a}{T_a}\right) \exp\left(-\left(1.2 + 3.0 \times 46.5\frac{e_a}{T_a}\right)^{0.5}\right) \quad \text{(Eq.8)}$$

→ 논문에서 "Jonsson et al.(2006): Prata 공식이 낮 시간 방사율을 0.04 과대추정" → L_↓ 25 Wm⁻² 감소 보정

---

### 2.5 SVF 계산 방법

논문 p.699:
> "Spatial variations of the sky view factor and shadow patterns are calculated using an urban raster DEM. This technique was developed by Ratti and Richens (1999)."

> "The main advantage of using raster images is that the spatial extension can be increased due to the much faster computing time."

---

### 2.6 지면 온도 T_s 추정 (Eq.12, p.700)

맑은 날 조건에서:
$$T_{diffmax} = 0.37 \times \eta_{max} - 3.41 \quad \text{(Eq.12, R²=0.90)}$$

- η_max: 최대 태양고도
- T_diffmax = 최대 (T_s − T_a) 온도차
- T_s 초기값 = −3.41K 낮게 설정 (태양고도 0° 시 T_s ≈ T_a − 3.41)

---

## 3. 필수 입력 데이터 — 논문 확인

### 입력 기상 데이터 (p.702, "Model domain and data")
- **직달 복사 (K_dir)**
- **산란 복사 (K_diff)**
- **전천 복사 (G, global shortwave)**
- **기온 (T_a)**
- **상대습도 (RH)**

→ 모두 시간 단위(hourly) 수집, 인근 기상관측소 (연구지 서쪽 1km)에서 취득

### 입력 지형 데이터
- **DEM (Digital Elevation Model)**: 지표 고도
- **Ground & Building DSM**: 건물 포함 수치표면모델
- 식생(수목) 미포함: "Trees and bushes are not included in the current DEM (Fig. 1)." (p.702)

**⚠️ 주의**: 이 논문(Lindberg2008)은 SOLWEIG 1.0 원본. 식생 처리는 이후 버전(Lindberg & Grimmond 2011)에서 추가됨.

---

## 4. 검증 결과 — 논문 직접 확인 수치

### 전체 검증 (n=95, 7일 × 2 사이트)
- **R² = 0.94** (p<0.01)
- **RMSE = 4.8 K**
- 저온 범위(T_mrt < 10°C): 약 2.5K 과대평가
- 고온 범위: 약 2.5K 과대평가

### 사이트별 T_mrt 오차
| 날짜 | 사이트 | 평균 차이 |
|------|--------|---------|
| 맑은 여름날 (26 July 2006) | SITE 1 (광장) | **2.3 K** |
| 맑은 가을날 (11 Oct 2005) | SITE 1 (광장) | **1.7 K** |
| 흐린 날 (1 Aug 2006) | SITE 1 (광장) | **3.1 K** |
| 맑은 가을날 | SITE 2 (안마당) | **6.5 K** (과대평가) |

SITE 2 오차 원인: 장파 복사 방향성 계산 한계 (SOLWEIG는 비방향성 계산)

### 복사 플럭스 검증
- 전체 단파 복사: R²=0.96, RMSE=152.2 Wm⁻²
- 전체 장파 복사: R²=0.93, RMSE=70.6 Wm⁻²
- K↓: R²=0.97, RMSE=42.1 Wm⁻²; K↑: R²=0.97, RMSE=7.0 Wm⁻²
- L_down: R²=0.73, RMSE=17.5 Wm⁻²; L_up: R²=0.94, RMSE=15.6 Wm⁻²; L_side: R²=0.92, RMSE=48.9 Wm⁻²

---

## 5. 연구 지역 설명

- **위치**: Göteborg, Sweden (57°42'N, 11°58'E)
- **모델 도메인**: 1400 × 1400m (도심 중심부)
- **DEM 범위**: 지표 0~35m a.s.l., 건물 1~100m a.s.l.
- **평균 건물 높이**: **16.5m** (표준편차 6.0m)
- **픽셀 해상도**: **1m** ("The pixel resolution here is 1 m", p.702)
- **측정 높이**: 1.1m above ground (성인 중심 무게 높이 기준)

---

## 6. 우리 연구와의 관련성

### 방법 C (30m DSM + SOLWEIG) 인용 근거
SOLWEIG 모델 자체의 원본 논문 → 반드시 인용

**인용 가능 문구 (논문에서 직접 확인)**:
> "SOLWEIG 1.0 is a 2.5-dimensional model in the sense that it applies a 2.5-dimensional DEM (i.e. x and y coordinates with height attributes) in the calculation of T_mrt." (p.698)

> "Spatial variations of the sky view factor and shadow patterns are calculated using an urban raster DEM." (p.699)

### 해상도 이슈
- 논문 사용: **1m** 해상도
- GLO-30 DSM: **30m** 해상도 → 우리 연구 한계로 명시 필요
- 비교: Lindberg2008 권장 1m vs 우리 30m → 30배 차이

### 식생 처리
- Lindberg2008 (SOLWEIG 1.0): 식생 미포함
- 이후 버전에서 CDSM(Canopy DSM) 추가 — Lindberg & Grimmond (2011) 참조

---

## 7. 논문에서 확인된 파라미터 정리

| 파라미터 | 값 | 근거 |
|---------|-----|------|
| ζ_k (단파 흡수계수) | 0.7 | p.699, "standard value" |
| ε_p (인체 방사율) | 0.97 | p.699, "standard value" |
| F_i (cardinal 방위) | 0.22 | p.699, Fanger (1972) |
| F_i (상하) | 0.06 | p.699, Fanger (1972) |
| α (반사율) | 0.15 | p.699, "average value for the albedo" |
| σ (Stefan-Boltzmann) | 5.67×10⁻⁸ Wm⁻²K⁻⁴ | p.699 |
| 픽셀 해상도 | 1m | p.702 |
| 측정 높이 | 1.1m above ground | p.702 |
| 검증 R² | 0.94 | p.706 |
| 검증 RMSE | 4.8 K | p.706 |

---

## 8. 우리 논문 방법론 섹션 인용 초안

> "MRT는 SOLWEIG 1.0(Lindberg et al., 2008)을 사용하여 계산하였다. SOLWEIG는 6방향 단파 및 장파 복사 플럭스와 SVF를 기반으로 T_mrt를 픽셀 단위로 산출하는 2.5D 복사 모델로, 입력 데이터로 DEM과 Ground & Building DSM, 그리고 직달·산란·전천 복사, 기온, 상대습도 기상 데이터를 요구한다. 본 연구에서는 Copernicus GLO-30 오픈소스 DSM(30m)을 SOLWEIG의 Ground & Building DSM 입력으로 활용하였으며, 논문 권장 해상도(1m; Lindberg et al., 2008)보다 낮은 30m 해상도를 사용한 것은 본 연구의 공간 범위(서울 전역)를 고려한 타협점임을 명시한다."
