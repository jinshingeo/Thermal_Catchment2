# UMEP 공식 튜토리얼 — DSM/CDSM/토지피복 생성 도구 상세 정리
작성일: 2026-07-06
목적: Method B(합성 DSM) 구체화 전 UMEP 공식 도구의 정확한 입출력 사양 확보 (추측·할루시네이션 방지)
출처: UMEP 공식 튜토리얼 사이트 (umep-docs.readthedocs.io/projects/tutorial) — WebFetch로 직접 확인, 2026-07-06
관련 기존 노트: `references/study_note_Lindberg2018_UMEP_합성DSM검증.md` (Lindberg et al. 2018 논문 본문 자체엔 합성 DSM 방법 언급 없다는 걸 이미 확인해둔 파일 — 이번 튜토리얼 조사로 "논문엔 없지만 공식 튜토리얼 문서엔 있다"는 걸 보강함)

> ⚠️ 주의: 튜토리얼 사이트는 지속적으로 갱신될 수 있음. 아래는 2026-07-06 fetch 시점 스냅샷. 실제 QGIS 설치 후 도구 실행 화면과 다를 수 있으니 사용 직전 재확인 권장.

---

## 1. DSM Generator (건물 DSM 생성)

**튜토리얼 URL**: https://umep-docs.readthedocs.io/projects/tutorial/en/latest/Tutorials/DSMGenerator.html
**메뉴 경로(QGIS)**: `UMEP > Pre-Processor > Spatial Data > DSM Generator`

### 입력
| 항목 | 설명 | 튜토리얼 예시 파일명 |
|------|------|-------------------|
| DEM | 지형 래스터 | `DEM_KRbig.tif` |
| 건물 폴리곤 | OSM 또는 자체 벡터 건물 풋프린트 | (OSM 다운로드 or 기존 shapefile) |
| 높이 속성 필드 | 건물 폴리곤 속성테이블의 높이 컬럼 | `bld_height` |

- 높이 속성이 없거나 비어있는 건물이 있으면, **QGIS 필드 계산기(Field Calculator)로 기본값을 채워 넣으라**고 튜토리얼이 안내함 (예: 층수 정보가 있으면 층수×3m 같은 방식으로 채우는 것이 이 단계에 해당)

### 출력
- DSM 래스터 (튜토리얼 예시: `dsm_osm_v1`, `dsm_osm_v2` — v1/v2는 높이값 보강 전/후 비교용으로 두 번 생성한 것으로 보임)
- 처리된 건물 shapefile (예: `buildings_gothenburg.shp`)

### 사용 절차 (튜토리얼 기준)
1. QGIS Processing Toolbox에서 `DSM Generator` 실행
2. DEM 범위(extent) 지정
3. OSM 데이터를 새로 받거나 기존 건물 레이어 지정
4. 건물 속성테이블에서 높이값 누락분을 필드계산기로 보강
5. 보강된 데이터로 DSM Generator 재실행 → 최종 DSM 생성

### 명시된 한계
- **평지붕(flat roof) 가정** — 실제 지붕 형태(경사·옥탑구조물)는 반영 안 됨
- 정밀도가 중요하면 LiDAR 데이터를 대안으로 쓰라고 튜토리얼이 직접 언급

### 우리 프로젝트 적용 메모
- VWorld 실제 3D 건물 데이터(⚠️ 확보 여부 미정, `데이터 신청/` 폴더 참고)를 쓰면 층수 추정보다 정확한 높이값을 이 도구의 "높이 속성 필드"에 바로 넣을 수 있음
- 국토지리정보원 1m DEM(⚠️ 공개제한, 신청 진행 중) 확보 시 이 도구의 DEM 입력으로 바로 사용 가능

---

## 2. TreePlanter (식생 CDSM 생성)

**튜토리얼 URL**: https://umep-docs.readthedocs.io/projects/tutorial/en/latest/Tutorials/IntroductionToTreePlanter.html
**메뉴 경로(QGIS)**: `UMEP > Pre-Processor > ... > TreePlanter` (정확한 서브메뉴 경로는 SOLWEIG 계열과 함께 "Thermal Comfort" 카테고리로 분류된 것으로 보임 — 실행 시 재확인 필요)

### 입력
| 항목 | 설명 | 튜토리얼 예시 |
|------|------|--------------|
| 식재 영역(Planting area) | **벡터 폴리곤 레이어** | `planting_area.shp` |
| 나무 높이 | 파라미터 | 10m (기본값, 조정 가능) |
| 수관직경(canopy diameter) | 파라미터 | 5m (기본값, 조정 가능) |
| 수간고(trunk zone height) | 파라미터 | 3m (기본값, 조정 가능) |

### 출력
- **CDSM 래스터** — 기존 식생 + 새로 심는 나무를 통합해서 생성
- **나무 위치 벡터 포인트 파일** — 각 나무의 위치를 점으로 자동 배치한 결과물

### ⚠️ 확인 안 된 부분 (직접 테스트 필요)
- 튜토리얼 문서는 "식재 영역 = 폴리곤"이라고만 나와 있고, **넓은 면적(공원·숲 전체)을 하나의 폴리곤으로 넣었을 때 정확히 어떻게 처리되는지**는 명시 안 됨:
  - (가설 A) 폴리곤 내부에 나무를 알고리즘으로 자동 배치(개수·간격 계산)하는 방식인지
  - (가설 B) 폴리곤 전체를 그냥 균일한 캐노피 높이로 채우는 방식인지
  - → **둘 중 무엇인지에 따라 우리 "산/공원/가로수 SHP + 유형별 대표 수고" 아이디어를 그대로 쓸 수 있는지가 갈림**. QGIS에서 소규모 테스트로 직접 확인 필요

### 우리 프로젝트 적용 메모
- 가로수(선형/점형에 가까움)와 공원·산림(면형)을 다르게 처리해야 할 수도 있음 — 가설 확인 후 결정
- 수간고(trunk zone) 파라미터가 공식적으로 존재한다는 게 확인됨 — 지난번 논의한 "캐노피 높이 하나만" 아이디어보다 한 단계 더 정확하게, 수간고까지 반영한 CDSM 제작 가능

---

## 3. SOLWEIG 본체 — 입력 전체 목록 및 토지피복 처리 방식

**튜토리얼 URL**: https://umep-docs.readthedocs.io/projects/tutorial/en/latest/Tutorials/IntroductionToSolweig.html

### 입력 전체 목록 (R=필수, O=선택, R*=조건부 필수)
| 구분 | 항목 |
|------|------|
| R (필수) | DSM, DEM, 위도, 경도, UTC, 기상데이터(기온·습도·단파복사) |
| O (선택) | CDSM, **TDSM**(Trunk-zone DSM — CDSM과 별도 레이어), 토지피복 |
| R* (조건부) | **토지피복이 없으면 DEM이 건물 식별 용도로 대신 필요** |

- **TDSM이 CDSM과 별도 레이어로 명시적으로 존재함**을 확인 — 앞서 우리가 "수간고 있으면 더 정확"이라고 얘기했던 게, 실제로는 완전히 분리된 입력 파일(TDSM)로 요구된다는 뜻. TreePlanter가 이걸 자동 생성해주는지, 별도로 만들어야 하는지는 추가 확인 필요

### 토지피복(Land Cover) 처리
- SOLWEIG 인터페이스에 "Use land cover scheme (Lindberg et al. 2016)" 체크박스 존재 → 켜면 토지피복 반영
- **딱 5개 클래스만 지원**: `building`, `paved`, `grass`, `bare soil`, `water` (Lindberg et al. 2016 scheme)
- 시각화용 스타일 파일 `landcoverstyle.qml` 제공됨
- **알베도·방사율 지정 방식**: 튜토리얼 문서상 "모델 인터페이스에서 설정(Set in the interface of the model)"이라고만 나와 있고, 5개 클래스별 기본 알베도값이 자동 내장되어 있는지 사용자가 직접 입력해야 하는지는 이 문서만으로 확정 불가 — **QGIS 설치 후 SOLWEIG 패널 직접 열어서 확인 필요**

### 우리 프로젝트 적용 메모 (중요)
- **환경부 EGIS 토지피복지도(원래 세분류 40여개 클래스)를 이 5개 클래스(building/paved/grass/bare soil/water)로 재분류해야 함** — 이전에 "토지피복지도 전처리" 작업 범위가 이제 구체적으로 확정됨
- Basu et al.(2024)이 MassGIS LULC를 재분류해 알베도 지정한 것도 결국 이런 소수 클래스 체계로 압축했을 가능성이 높음(원문에 몇 개 클래스인지까지는 안 나왔음 — Basu 논문엔 "포장재/잔디/나지/수역"까지만 명시, building 포함 5개인지 4개인지 재확인 필요)

---

## 4. 추가로 확인된(아직 안 읽은) 관련 튜토리얼 — 다음에 참고

- **LiDAR 처리**: https://umep-docs.readthedocs.io/projects/tutorial/en/latest/Tutorials/LidarProcessing.html — "Generating UMEP input data from a LiDAR point cloud" — 국토지리정보원 1m DEM/라이다 확보 시 이 튜토리얼이 직접 도움될 것
- **Spatial Thermal Comfort**: https://umep-docs.readthedocs.io/projects/tutorial/en/latest/Tutorials/SpatialTC.html
- **SOLWEIG+URock+SpatialTC 통합(ICUC12 학회버전)**: https://umep-docs.readthedocs.io/projects/tutorial/en/latest/Tutorials/IntroductionToSolweigICUC12.html

---

## 5. 다음 액션 (Method B 구체화 시 확인할 것)
1. QGIS에 UMEP 설치 후 `DSM Generator`, `TreePlanter`, `SOLWEIG` 패널을 직접 열어서:
   - TreePlanter가 폴리곤(공원/숲)을 어떻게 처리하는지 소규모 테스트
   - SOLWEIG의 토지피복 알베도값이 기본 내장인지 직접 입력인지 확인
   - TDSM을 TreePlanter가 자동 생성하는지, 별도 제작이 필요한지 확인
2. 환경부 EGIS 토지피복지도를 5개 클래스(building/paved/grass/bare soil/water)로 재분류하는 매핑표 작성
3. 국토지리정보원 DEM + VWorld 건물데이터 확보되면 `DSM Generator`에 바로 투입해 실제 테스트
