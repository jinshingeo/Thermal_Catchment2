# Dong et al. (2024) — Measuring Urban Thermal Environment from Accessibility-based Perspective

## 기본 정보
- **저자**: Xinyu Dong, Xiaoya Li, Yanmei Ye, Dan Su, Runjia Yang, Angela Lausch
- **소속**: Zhejiang University; Helmholtz Centre UFZ; Humboldt-Universität zu Berlin; Martin Luther University Halle-Wittenberg; Anhalt University of Applied Sciences
- **저널**: Geography and Sustainability, 5 (2024) 329–342
- **DOI**: https://doi.org/10.1016/j.geosus.2024.02.004
- **투고/채택**: 2023-09-07 투고 → 2024-02-06 채택 → 2024-02-20 온라인 게재

---

## 연구 개요

접근성 프레임워크(2SFCA)를 활용해 정저우(郑州, 중국) 도시 열환경을 공간적으로 평가. UGS(Urban Green Space) 냉각 서비스 접근성과 HIA(Hot Island Area) 열노출 위험을 동시에 정량화하고, 공간 클러스터링으로 취약 지역 식별.

**핵심 기여**:
- 도시 열환경 평가에 접근성(2SFCA) 개념 통합
- 냉각 서비스 공급↔열 노출 위험 공간 불일치 지역 식별
- 2010→2015→2020 시공간 변화 분석

---

## 방법론

### 전체 프레임워크
1. **데이터 준비**: Landsat 위성영상으로 UGS(NDVI>0.4) + LST → HIA 추출
2. **2SFCA 접근성 계산**: UGS 냉각 서비스 접근성 + HIA 열노출 위험
3. **공간 클러스터링**: Bivariate Local Moran's I로 H-H/L-L 비정상 클러스터 식별

### UGS 및 HIA 추출

**UGS (Urban Green Space)**:
```
NDVI = (NIR − RED) / (NIR + RED)          ...(4)
```
- Landsat 7 Band 4&3, Landsat 8 Band 5&4
- NDVI > 0.4 → UGS 분류

**HIA (Hot Island Area)**:
- LST Radiative Transfer Equation (RTE)
- Getis-Ord Gi* 공간통계 → H-H 군집 = HIA

**NDBI (Normalized Difference Built-up Index)**:
```
NDBI = (SWIR − NIR) / (SWIR + NIR)       ...(7)
```
- NDBI: HIA 품질 지표 (고밀 건축 = 고열 노출)

### 개선 2SFCA (Improved 2SFCA) 접근성

**1단계: 공급-수요 비율 계산 (공급 포인트 = UGS 또는 HIA)**

냉각 서비스 접근성:
```
A^CS_i = Σⱼ [S^UGS_j · (1 + NDVI̅_j) · f(dᵢⱼ)] / [Σₖ Dₖ · f(dₖⱼ)]     ...(5)
```
- S^UGS_j: j번째 UGS 면적
- NDVI̅_j: 냉각 품질 (NDVI 평균)
- f(dᵢⱼ): Gaussian 거리 감쇠 함수
- Dₖ: 인구 (WorldPop)

열노출 위험:
```
A^HIA_i = Σⱼ [S^HIA_j · (1 + NDBI̅_j) · Σₖ Dₖ f(dₖⱼ)]^(1/2) · f(dᵢⱼ)     ...(8)
```

**Gaussian 감쇠 함수**:
```
f(dᵢⱼ) = e^(-1/2·(dᵢⱼ/d₀)²) / (1 - e^(-1/2)), dᵢⱼ ≤ d₀
        = 0, dᵢⱼ > d₀
```
- d₀ = 1,000m (냉각 효과 최대 거리)

**2단계: 공간 자기상관 (Bivariate Local Moran's I)**:
```
Iₖₗ = (x^k_i - x̄_k)/S²_k × Σⱼ wᵢⱼ × (x^l_j - x̄_l)/S²_l
```
- x^k: 냉각 서비스 접근성, x^l: 열노출 위험

---

## 데이터 및 공간 범위

| 항목 | 내용 |
|------|------|
| 연구 지역 | 정저우(郑州), 5개 핵심 구역, 1,080 km² |
| 기후 | 온난 온대 대륙성 계절풍 (여름 기온 40°C 초과) |
| 분석 기간 | 2010, 2015, 2020년 (3개 시점) |
| 계절 | 4~10월 (비교적 더운 기간) |
| 위성 | Landsat 7 ETM+(2010), Landsat 8 OLI/TIRS(2015, 2020) |
| 인구 | WorldPop 100m 해상도 → 500m 집계 |
| 격자 단위 | 500m × 500m 격자 |
| 반경 | 1,000m (냉각 효과 최대 거리) |
| 검증 | GEE 200개 랜덤 샘플 kappa coefficient (0.82~0.83) |

---

## 주요 결과

### 시공간 변화 (2010→2020)
- UGS 전체 증가: 도심 내부 최저 10% → 29% (3rd ring 기준)
- HIA: 도심 밀집 (2nd ring 최고 35.3%) → 일부 감소

### 냉각 서비스 접근성
- 외곽(Zone IV) > 도심(Zone I): 반대 직관적 결과
- Zone IV 최고 접근성: 4,608~8,382 (2010→2020)
- Zone I(도심) 최저 → UGS 부족, 인구 과밀

### 열노출 위험
- Zone I(도심): 전 기간 최고 위험 (0% non-exposure)
- Zone IV: 51.7%(2020) 지역 → 열 위험 없음

### 공간 클러스터 (BiLISA)
- **H-H cluster** (이상 군집): 높은 냉각 접근성 + 높은 열위험 → 3rd ring 인근
  - UGS 냉각이 공급되어도 주민이 열에 노출 → 실제 효과 의문
- **L-L cluster** (이상 군집): 낮은 냉각 접근성 + 낮은 열위험 → 4th ring 외곽
- **H-L cluster** (정상): 낮은 냉각 접근성 + 높은 열위험 → 도심 핵심 취약 지역

---

## 우리 연구에서 따라할 수 있는 부분

### 1. 접근성 기반 열환경 평가 프레임 → 개념적 정당화
- "열환경을 접근성 관점에서 평가한다"는 연구 프레임 자체 참고
- 우리 연구도 열환경(UTCI)이 보행 접근성에 영향을 미친다는 동일 관점
- **인용 가능**: "Dong et al.(2024)은 접근성 기반 열환경 평가 프레임워크를 제안하여 UGS 냉각 서비스 접근성과 열노출 위험 간의 공간 불일치를 정량화하였다"

### 2. NDVI → 녹지 냉각 효과 지표
- NDVI가 UGS 냉각 품질 대리변수로 사용됨
- 우리 연구 NDVI를 TARR 설명변수로 쓰는 근거
- "NDVI는 UGS의 냉각 서비스 품질과 밀접하게 관련되어 있으며(Dong et al., 2024)"

### 3. 불투수면 → 열 위험 지표
- NDBI(건축밀도 지수)를 HIA 품질 지표로 사용
- 우리 연구 불투수면 비율을 TARR 설명변수로 쓰는 근거
- 불투수면 → 열 노출 증가 → Thermal Catchment 감소

### 4. 500m 격자 + 1km 반경 설계
- 격자 기반 평가 단위 참고 (우리는 역 중심 catchment)
- 1km 냉각 감쇠 반경 → 우리 검색 반경 1.125km와 유사한 스케일

### 5. 형평성 분석 → G 이슈
- 도심(고밀도, 낮은 UGS) vs 외곽(고 UGS, 낮은 열위험) 불평등
- 우리 연구의 역별 TARR 공간 불균형 해석 참고

---

## 우리 연구와의 차별점

| 항목 | Dong2024 | 우리 연구 |
|------|----------|----------|
| 열 지표 | LST (land surface temperature) | MRT → UTCI |
| 접근성 방법 | 2SFCA | 등시선 기반 Catchment (contour) |
| 대상 | UGS 냉각 서비스 접근성 | 역세권 보행 접근성 |
| 주요 결과 | 냉각-열위험 공간 불일치 | 역세권 Thermal Catchment 감소율 |
| 도시 | 정저우 (중국) | 서울 성동구 (한국) |
| 스케일 | 도시권 전체 (1,080km²) | 행정구 (역 7개) |
| 해상도 | 500m 격자 | 도로 링크 단위 (~10m) |

---

## 한계 (논문 명시)
- LST (지표 온도) vs 공기온도 차이 미고려
- WorldPop 인구 데이터 정확도 한계
- 비성수기(4~10월 중 봄·가을 포함) 날짜 혼재
- 단일 도시 사례 (정저우)
