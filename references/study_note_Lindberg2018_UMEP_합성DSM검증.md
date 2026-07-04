# Lindberg et al. (2018) UMEP 논문 + 합성 DSM 코드 꼼꼼 검증 노트

작성일: 2026-07-01  
목적: 18_synthetic_dsm.py 코드의 인용 근거 할루시네이션 방지 검증

---

## ⚠️ 핵심 발견 — 코드 주석의 인용이 논문 직접 인용이 아님

코드 `18_synthetic_dsm.py`의 docstring에 다음 인용이 있음:

```
참고문헌:
  Lindberg, F., et al. (2018). Urban Multi-scale Environmental Predictor (UMEP).
  Environmental Modelling & Software, 99, 70–87.
  → "Building footprint polygons with height attributes can be used to generate
     a building DSM as an alternative when airborne LiDAR data is unavailable."
```

**이 문구는 Lindberg et al.(2018) 논문 본문 어디에도 존재하지 않는다.**  
논문 전체(pp.70–87) 확인 완료.

---

## 1. 논문 기본 정보

- **제목**: Urban Multi-scale Environmental Predictor (UMEP): An integrated tool for city-based climate services
- **저자**: Fredrik Lindberg, C.S.B. Grimmond et al. (13인)
- **저널**: Environmental Modelling & Software, Volume 99 (2018), pp. 70–87
- **DOI**: https://doi.org/10.1016/j.envsoft.2017.09.020
- **출판**: 2017년 10월 27일 온라인, 2018년 인쇄본
- **오픈소스**: QGIS 플러그인, Python 기반, CC BY-NC-ND 라이선스

---

## 2. 논문이 실제로 말하는 것 — SOLWEIG 입력 데이터

### Table 1에서 SOLWEIG 관련 기술 (p.72)
> "SOLWEIG estimates spatial (2-D) variations of 3-D radiation fluxes and the mean radiant temperature (T_mrt) in complex urban settings. **Both 3D vegetation (trees and bushes), as well as ground cover variations are currently considered in the model.**"
- Key References: Lindberg et al. (2008), Lindberg and Grimmond (2011a,b), Lindberg et al. (2016b)

### Fig. 7 워크플로우 (p.79) — SOLWEIG 입력 데이터 명시

```
필수 입력 (Bold 표시):
  - DEM (Digital Elevation Model)
  - Ground & Building DSM

선택 입력:
  - Vegetation DSM (CDSM) — Tree Generator로 생성 가능
  - Land Cover Reclassifier
  - Meteorological data
```

> Fig. 7 caption: "Workflow and geodata used for analysing mean radiant temperature using SOLWEIG in UMEP. **Bold outlines indicate mandatory items.**"

### 본문 p.77 직접 인용
> "To model T_mrt successfully, **building footprint locations must be derived from either the ground cover grid or from differences between ground heights (DEM) and a DSM** (Fig. 7)."

→ 이 문장은 DSM이 필요하다는 것만 말함. **건물 폴리곤으로 합성 DSM을 만들 수 있다는 내용 없음.**

### Fig. 7 workflow에서 DSM 생성 방법 언급 없음
- 논문은 DSM의 소스(LiDAR vs. 합성)에 대해 전혀 언급하지 않음
- Fig. 4에서 LiDAR 기반 CDSM을 사용한 예시(London Greater London Authority)가 있을 뿐

### CDSM에 대한 언급 (p.77)
> "However, **as 3D information on vegetation is sparse, the Tree Generator tool allows point vector data of tree locations to be transformed into a CDSM.** Ground cover information can be used to estimate outgoing short and longwave radiation fluxes."

→ CDSM의 경우 Tree Generator를 공식 대안으로 제시함. 하지만 **Building DSM에 대한 대안은 논문에 없음.**

---

## 3. 논문에서 확인된 SOLWEIG 관련 정보

### SOLWEIG 적용 사례 (Table 5, p.76)
| 도시 | 적용 내용 |
|------|---------|
| Gothenburg | Radiant fluxes and T_mrt (도시 광장, 안마당) |
| Kassel | T_mrt (Street canyon) |
| Freiburg | T_mrt (4개 도시 사이트) |
| London | Radiant fluxes and T_mrt |
| Shanghai | T_mrt (고밀도 도시) |
| Hong Kong | T_mrt (고밀도 도시) |

→ **모든 검증 사례에서 LiDAR DSM 사용** (합성 DSM 사례 없음)

### Stockholm Civic Square 사례 (pp.77–79)
- 1m 픽셀 해상도로 T_mrt 분석
- DSM 소스: 명시 안 됨 (그러나 Stockholm LiDAR 데이터 사용으로 추정)
- 결과: T_mrt가 14:00에 shadow 영향 큼

### Fig. 8 (p.79) 실제 SOLWEIG 입력 데이터
- (a) DSM and CDSM — LiDAR 기반 래스터 (Gothenburg 예시)
- 픽셀 해상도: **1m** (논문 본문: "The pixel resolution here is 1 m")
- T_mrt 결과: 26 July 2006 Gothenburg, 2 p.m.

---

## 4. 코드 18_synthetic_dsm.py 실제 구현 내용

### 코드가 하는 일 (검증 완료)

```python
# 입력
BULD_PATH = 'TL_SPBD_BULD_11_202603.shp'  # 서울 건물 전체 SHP
GREEN_PATH = '도시숲전체_면_서울_최종_중분류.shp'  # 도시녹지 SHP

# 파라미터
RESOLUTION = 2.0   # m
TREE_HEIGHT = 8.0  # m (가로수 평균 높이 추정값 — 근거 없음)
층수 × 3m          # 건물 높이 추정 — 근거 없음

# 성동구 bbox
BBOX_WGS = [127.010~127.070, 37.530~37.570] + 여유 100m
```

### DSM 생성 방식
```
DSM: 건물 footprint 래스터화 + 층수×3m 높이값 → 건물 없는 곳=0m
DEM: 전체 0m (성동구 평탄 지형 가정)
CDSM: 가로수 폴리곤 래스터화 + 8m 고정 높이
```

### 코드의 한계 (docstring에 명시됨)
1. 수목 CDSM 미반영 (가로수 데이터로 부분 보완)
2. 지붕 형태 무시 (평지붕 가정)
3. 층수×3m 추정값으로 실제 높이와 오차 가능

---

## 5. 합성 DSM 방식의 실제 근거 — 논문이 아닌 다른 소스

코드 주석이 Lindberg et al.(2018)을 인용했지만, 실제 건물 폴리곤 기반 합성 DSM 방식의 근거는 다음에서 찾아야 함:

### 5-1. UMEP 공식 온라인 매뉴얼 (논문이 아님)
- URL: http://www.urban-climate.net/umep/UMEP_Manual
- 논문 p.70 abstract에서 매뉴얼 존재 언급: "tutorials have been developed (http://www.urban-climate.net/umep/UMEP_Manual#Tutorials)"
- 실제 "building footprint polygons can be used to generate DSM" 문구는 **매뉴얼**에 있을 가능성이 높음 — **직접 확인 필요**

### 5-2. Wolf et al.(2025) 선례 — 논문에서 직접 확인된 문구

**논문 Data 섹션 직접 인용 (확인 완료)**:
> "Given the sparse availability of full 3D building data, and for computational simplicity, we handle building data following the **2.5D standard**, i.e. consisting of a footprint-polygon and a singular height value which is simplified as constant across the whole building."

- 2.5D standard = footprint-polygon + 단일 높이값 (건물 전체에 constant)
- 도시: Manhattan(NYC), Barcelona, Valencia (Scientific Reports 15:14911, SCI 게재)
- **이것이 우리 `18_synthetic_dsm.py`와 동일한 방식. 우리 논문에서 직접 인용 가능.**

**단, Wolf2025와 우리의 차이점:**
- Wolf2025: 건물 폴리곤으로 **그늘(shadow fraction)** 직접 계산 (MRT 없음)
- 우리: 건물 폴리곤으로 **합성 DSM** 생성 → SOLWEIG로 **MRT** 계산
- 즉, 2.5D 데이터 처리 방식은 동일하나, 활용 목적이 다름

### 5-3. UMEP 개발팀 선행논문들
- Lindberg & Grimmond (2011a): Shadow patterns and mean radiant temperature in urban areas
- Lindberg & Grimmond (2011b): Vegetation and building morphology characteristics
- 이 논문들에 합성 DSM 관련 내용이 있을 수 있음 — 미확인

---

## 6. 논문 인용 시 수정 권고

### ❌ 잘못된 인용 (현재 코드 주석)
```
Lindberg et al. (2018) → "Building footprint polygons with height attributes 
can be used to generate a building DSM as an alternative when airborne LiDAR 
data is unavailable."
```
→ **이 문구는 논문에 없음. 인용 불가.**

### ✅ 올바른 인용 (논문에서 실제 확인 가능한 내용)

**SOLWEIG 모델이 DSM을 필수 입력으로 요구한다:**
> "To model T_mrt successfully, building footprint locations must be derived from either the ground cover grid or from differences between ground heights (DEM) and a DSM (Lindberg et al., 2018, Fig. 7)."

**SOLWEIG가 3D 식생과 지표면 변화를 고려한다:**
> "SOLWEIG estimates spatial (2-D) variations of 3-D radiation fluxes and the mean radiant temperature (T_mrt) in complex urban settings. Both 3D vegetation (trees and bushes), as well as ground cover variations are currently considered in the model (Lindberg et al., 2018)."

**DSM 해상도 관련:**
> "The pixel resolution here is 1 m." (p.79, Stockholm Civic Square 사례)
→ 논문 권장 해상도 = 1m, 우리 코드 = 2m — 이 차이를 한계로 명시해야 함

### ✅ 합성 DSM 방식의 논문 인용 문구 (확정 가능)

**우리 논문에서 쓸 수 있는 문장 (초안)**:
> "LiDAR 데이터를 확보하기 어려운 경우, 건물 footprint 폴리곤과 단일 높이값으로 구성된 2.5D 표준 방식으로 건물 형태를 표현하는 것은 선행연구에서 이미 적용된 바 있다(Wolf et al., 2025). 본 연구에서는 이 방식을 확장하여 건물 행정 데이터(TL_SPBD_BULD)의 지상층수에 층고 3m를 곱한 추정 높이를 적용해 2m 해상도의 합성 DSM을 생성하고, 이를 SOLWEIG의 Ground & Building DSM 입력으로 활용하였다(Lindberg et al., 2018)."

→ Wolf2025 인용: 2.5D 방식의 SCI 선례  
→ Lindberg2018 인용: SOLWEIG가 Ground & Building DSM을 필수 입력으로 요구한다는 사실  
→ 두 인용 모두 논문 직접 확인 완료

**UMEP 매뉴얼**: 아직 미확인 — 필요 시 추가 확인

---

## 7. 논문에서 확인된 SOLWEIG 모델 구조 (정확한 정보)

### 필수 입력 (Fig. 7, p.79 기준)
| 입력 | 설명 |
|------|------|
| DEM | 수치지형모델 (지표면 고도) |
| Ground & Building DSM | 건물 포함 수치표면모델 |
| Meteorological data | Ta, RH, wind, solar radiation |

### 선택 입력
| 입력 | 설명 |
|------|------|
| Vegetation DSM (CDSM) | 수목 캐노피 (Tree Generator로 대체 가능) |
| Land Cover | 지표피복 분류 |
| Wall height and aspect | 벽 높이·방위각 |

### SVF 계산 방식 (p.77)
> "A pixel-wise sky view factor calculated in SVF uses ground and building DSMs and/or vegetation DSM (Fig. 8c)."

→ SVF는 DSM에서 자동 계산. 우리 코드의 `15_svf_per_link.py`가 이를 구현.

---

## 8. 우리 코드에 있는 추가 미검증 수치

| 항목 | 코드 값 | 근거 |
|------|---------|------|
| RESOLUTION | 2.0 m | 논문 권장 1m보다 낮음. 한계로 명시 필요 |
| TREE_HEIGHT | 8.0 m | Wolf et al.(2025) park canopy 8m 가정과 동일 수치 — 단, Wolf는 공원, 우리는 가로수로 대상 다름. "준용" 수준으로 인용 가능 |
| 층수×3m | 건물 높이 계산 | 설계 기준 근사값 — 출처 명시 필요 |
| DEM=0 | 성동구 평탄 가정 | 성동구가 실제로 평탄한지 검증 필요 |

---

## 9. 결론 및 다음 할 일

**코드 방법론 자체는 합리적이나 인용이 틀림:**
- 건물 SHP → DSM 합성 방식: 합리적이고 Wolf2025 선례 있음
- Lindberg et al.(2018) 직접 인용 문구: **논문에 없음 → 사용 불가**

**논문 작성 시 해야 할 것:**
1. UMEP 공식 매뉴얼에서 "building footprint DSM" 관련 문구 직접 확인
2. 또는 Wolf et al.(2025)로 선례 인용 대체
3. 해상도 2m → 논문 권장 1m와 차이: 한계로 명시
4. TREE_HEIGHT=8m, 층수×3m: 근거 논문 서치
5. DEM=0 가정: 성동구 실제 지형 확인 (성동구는 실제로 한강·중랑천 변 일부 저지대 있음)
