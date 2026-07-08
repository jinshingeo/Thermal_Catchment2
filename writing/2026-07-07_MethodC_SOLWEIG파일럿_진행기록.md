작성일: 2026-07-07
버전: v2 (전체 재확인·업데이트)
근거논문: Lindberg et al. (2008, 2011, 2016, 2018), Erbs et al. (1982), Colaninno et al. (2024), Basu et al. (2024), Jia et al. (2022)

> ⚠️ v1은 세션 초반 스냅샷이라 이후 발견사항(임상도 원본 HEIGHT, F_FAC_BUILDING 건물높이,
> 크로스워크 표 등)이 빠져있었음. v2에서 전체 업데이트. 상세 방법론 서술은
> [[writing/2026-07-07_2장선행연구검토_3장연구자료구축및방법론_v1]] 참고.

# Method C — 성동구 SOLWEIG 파일럿 진행 기록 (2026-07-07 세션)

> 목적: 오늘 세션에서 확정한 데이터 소스·처리방식·근거를 논문 방법론 작성 시 그대로
> 참조하기 위한 기록. 추정/할루시네이션 없이 실제 확인된 것만 적음.

## 1. 원칙 확정 사항

- **모든 데이터 수집·전처리는 서울 전체 기준**으로 하고, 성동구는 분석(SOLWEIG 실행)
  단계에서만 클립해서 사용한다. (반복 확인된 원칙 — [[feedback_seoul_wide_preprocessing]])
- 분석 시간대: 06~19시 시간별, **2025-07-23~08-03 폭염일 12일 평균** (대표 단일일 방식
  아님). Colaninno et al.(2024)의 아침(6-10)/낮(10-3)/저녁(3-7) 3구간과 비교 가능하도록
  전체 시간대를 다 산출해두고 이후 구간별로 묶어서 봄.
- SOLWEIG는 **도메인 전체에 적용되는 단일 시계열 기상입력만 받음** (격자 기상입력 불가,
  UMEP 공식문서 확인: "a single uniform time series applied across the spatial domain").
  → 링크별로 기상을 달리 주고 싶다면 SOLWEIG의 Tmrt(지오메트리 기반 공간변이)와 별도로
  구한 공간 보간 Ta/RH/wind를 **UTCI 계산 단계에서 사후 결합**해야 함 (Method A
  `39_utci_sdot_solweig.py`와 동일 구조). MRT 산출 자체엔 보간 불필요.

## 2. 기상 프로파일 (met.txt) 산출 방법

출처: `04_MeteoComparison/code/01_build_seongdong_met_profile.py`
결과: `04_MeteoComparison/results/seongdong_met_profile_06_19h.csv`,
`04_MeteoComparison/results/seongdong_solweig_met.txt`

| 변수 | 소스 | 근거 |
|---|---|---|
| 기온(Ta), 습도(RH) | S-DoT 성동구 내 64개 센서, 12일×06-19시 단순평균 | 역내 지점 다수라 공간대표성 확보, IDW 불필요(성동구 안에 있는 지점 평균이라 경계효과 없음) |
| 풍속(wind) | AWS 성동(지점번호 421), 12일×06-19시 평균 | S-DoT는 풍속 센서 결측(성동구 64개 센서 전부 NaN 확인됨) → AWS로 대체 |
| 전천일사(kdown) | ASOS 서울(108), 일사(MJ/m²)→W/m² 환산(×1,000,000/3600) | ASOS만 일사계 보유(AWS엔 없음) |
| 직달(kdir)/확산(kdiff) | ASOS GHI에 **Erbs et al.(1982)** 직산분리모델 적용 | ERA5 대신 실측 지상관측 사용 — Colaninno(2024)가 ERA5(direct/diffuse 분리 입력)를 쓴 건 LA에 지상관측 대안이 마땅치 않아서였을 가능성, 서울은 ASOS 실측이 있어 오히려 더 나은 선택 |
| 풍향(wdir) | **미사용(-999)** | (1) 각도(원형)변수라 산술평균 무의미(예: 350°/10° 평균→180°, 정반대) (2) SOLWEIG Tmrt·UTCI 공식 모두 풍속만 쓰고 풍향은 안 씀 |
| 강수(rain) | 0 | ASOS 확인 결과 12일×06-19시 전부 무강수(153/154행 결측=무강수 관례) |
| 기압(pres) 등 나머지 | -999 | ASOS 다운로드본에 기압 컬럼 없음(Tmrt 영향 미미) / qn·qh·qe·qs·qf·snow·ldown·fcld·wuh·xsmd·lai는 SUEWS 전용, SOLWEIG 미사용 |

**iy/id(연/DOY)**: 2025, DOY 209(2025-07-28, 12일 기간 중앙일) 고정 — 실제 날짜 의미가
아니라 SOLWEIG 내부 태양위치(그림자) 계산용 입력. 12일간 태양적위 변화 1도 미만이라
중앙일 고정에 따른 오차 무시 가능.

**산출 결과 검증**: kdown 12~14시 737~797 W/m² — 기존 파일럿에서 쓰던 "Kdown=708W/m²
근거 미확보" 수치와 근접. 즉 그 수치의 실제 출처가 이 계열 ASOS 자료였을 가능성이 높고,
이번에 정식 출처(기상청 ASOS 서울 108, 일사 실측)로 명시 가능해짐.

## 3. 지오메트리 입력 데이터 확보 현황 (v2 업데이트)

| 데이터 | 상태 | 위치/출처 |
|---|---|---|
| DEM(지면) | GLO-30(30m, 오픈소스) 확보됨. 국토지리정보원 1m DEM은 신청 진행상황 미확인(서식만 준비됨) — 안 와도 진행, 오면 업그레이드 | `data/GLO30_DSM/` |
| 건물(DSM) | ✅ 확보 — **F_FAC_BUILDING**(건축물대장 통합정보)의 실측 `HEIGHT` 필드 우선 사용, 없으면 자체 `GRND_FLR`×3m, 그것도 없으면 `TL_SPBD_BULD`(도로명주소)의 `GRO_FLO_CO`를 `BD_MGT_SN` 키로 교차조인×3m, 전부 없으면 기본값 3m. 성동구 25,092개 기준 1단계 37.3%/2단계 30.4%/3단계 6.6%/4단계(기본값) 25.6% (직접 검산 완료, 합계 100% 확인) | `data/F_FAC_BUILDING_서울/`, `TAVI/03_건물데이터/(도로명주소)건물_서울/` |
| 토지피복도 | ✅ 확보+매핑 완료 — 환경부 세분류(L3, 37클래스 실측/41클래스 전체), 서울 전체 136타일 병합(EPSG:5186), **41→UMEP 5클래스(building/paved/grass/bare_soil/water) 크로스워크 표 작성 완료** | `data/landcover_seoul_L3_merged.gpkg`, `03_Method_C/code/landcover_crosswalk_L3_to_UMEP.csv` |
| 수목 캐노피(CDSM) | ✅ **확보** — 2SFCA의 병합 shp는 못 썼지만(v1 문제), **산림청 임상도 원본**(서울시, `녹지데이터 복사본/임상도/11_서울시/11.shp`, EPSG:5179)에 `HEIGHT`(임분고코드, 00~28m 2m간격 실측)와 `FRTP_NM`(임상명: 침엽수림/활엽수림/혼효림)이 그대로 있음. 성동구 산림 53개 결측 0%, 면적가중평균수고 10.5m. **임분수확표 변환 불필요** — 산림청이 이미 실측한 수고값 직접 사용 | `data/녹지데이터 복사본/임상도/11_서울시/11.shp` |
| 성동구 경계 | ✅ 확보 — 국토지리정보원 N3A_G0100000(시군구경계, EPSG:5179) 및 SGIS 통계지역경계(EPSG:5179, `_tmp_boundary/행정구역.shp`) |

**해상도 비교 설계**: 위 자료를 두 가지 격자 해상도로 각각 구축해 비교.
- 접근1: 지면·건물·수목 동일 자료를 **30m** 격자로 (자료 원해상도)
- 접근2: 동일 자료를 **1m**로 다운스케일링 (지면은 보간뿐이라 정보 추가 없음, 건물·수목은
  벡터속성이라 손실 없이 세밀하게 반영됨 — 진짜 디테일은 건물·수목 층에서만 생김)
- 목적: "데이터 유무"가 아니라 "해상도" 하나만 통제된 변수로 비교 (지난 2026-07-04
  GLO-30 단독 결과는 이번 비교와 역할이 달라 논문에 굳이 재인용할 필요 없음 — [[feedback_paper_lean_content]])

## 4. UMEP SOLWEIG 입력 포맷 확인 사항

met.txt는 UMEP 표준 24컬럼 포맷(iy,id,it,imin,qn,qh,qe,qs,qf,U,RH,Tair,pres,rain,kdown,
snow,ldown,fcld,wuh,xsmd,lai,kdiff,kdir,wdir). 공식문서로 컬럼 순서·의미 확인함
(umep-docs.readthedocs.io). 미사용 컬럼은 -999.

**landcover 기본 파라미터** (로컬 UMEP 플러그인 파일에서 확인,
`~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/UMEP/SOLWEIG/landcoverclasses_2016a.txt`
— 아스팔트/자갈/잔디/물 값은 **Lindberg et al.(2016) Table 1과 정확히 일치** 확인함,
즉 원출처는 Lindberg(2016)+Oke(1987)+예테보리 실측):

| Name | Code | Alb | Emis |
|---|---|---|---|
| Roofs(buildings) | 2 | 0.18 | 0.95 |
| Dark_asphalt | 1 | 0.18 | 0.95 |
| Cobble_stone_2014a | 0 | 0.20 | 0.95 |
| Water | 7 | 0.05 | 0.98 |
| Grass_unmanaged | 5 | 0.16 | 0.94 |
| bare_soil | 6 | 0.25 | 0.94 |
| Walls | 99 | 0.20 | 0.90 |

**주의**: UMEP 공식문서에 "grass와 impervious surface만 파라미터화·검증됐고 나머지(나지·
수역 등)는 first order approximation"이라 명시됨. 우리 논문에 인용 시 이 한계를 같이
서술할 것.

**구조적으로 중요한 점**: 이 표에 산림(활엽수/침엽수) 클래스가 없음 — landcover는
지면(ground) 표면 재질용이고, 수목은 CDSM(캐노피 높이 래스터)으로 별도 처리되는 구조.
따라서 토지피복 37클래스 매핑 시 산림 폴리곤은 landcover 코드가 아니라 CDSM 수고값으로
반영해야 하며, 그 지점의 지면(landcover)은 grass_unmanaged 또는 bare_soil로 매핑하는
것이 구조적으로 맞음. (Basu et al. 2024는 이 실제 수치를 논문에 공개하지 않음 — "assign
different values of albedo and emissivity to different land cover classes"라는 방법론
서술만 있고 구체적 수치 없음. 방법론적 선례로만 인용 가능, 수치 출처는 아님.)

## 4.5 식생(CDSM) 복사 파라미터 및 처리 방식 (Lindberg & Grimmond 2011)

- 알베도 0.15, 방사율 0.90, 단파투과율(τ) 0.05(여름·완전히 잎이 달린 상태 권장값, 기본값 0.20 아님)
- 형태: 침엽수림=원뿔형, 활엽수림=구형. **혼효림**은 수종 구성비 정보가 없어(`KOFTR_NM`이
  "침활혼효림" 단일값뿐) 활엽수(구형)로 단순화 — 성동구 산림 53개 중 11개(21%)라 영향 제한적, 한계로 명시
- TDSM(수간부): 실측자료 없어 **UMEP 공식튜토리얼 권장값(CDSM 높이의 25%)**으로 근사
- CDSM은 rasterize(gdal:rasterize)로 임상도 HEIGHT를 직접 굽는 방식 채택 — TreePlanter는
  "신규 식재 최적위치 탐색" 도구라 기존 산림 반영에는 부적합하다고 판단(튜토리얼 확인:
  "will find optimal locations for three deciduous trees")
- CDSM은 **magl(지면 기준 상대높이)**, DSM은 **masl(절대표고)** — UMEP 공식문서로 확인.
  건물은 100% 불투명이라 지면과 합쳐도 되지만, 수목은 부분투과(τ=0.05)+수간/수관 구분이
  필요해 지면과 독립적인 상대값이어야 함

## 4.6 하늘방사율(Prata)·SVF — 우리가 구현할 필요 없음

Method A 파일럿 스크립트(`39_utci_sdot_solweig.py`)는 하늘방사율을 간이식(`0.575*ea^(1/7)`)
으로 자체 계산했으나, 이는 Lindberg(2008)의 실제 SOLWEIG 공식(Prata 1996 + Jonsson et al.
2006 보정 + Crawford & Duchon 1999 구름보정)과 다르다. **다만 오늘부터는 실제 UMEP/SOLWEIG
소프트웨어(QGIS 플러그인)를 돌리는 것이 목표이므로, 이 물리식은 소프트웨어가 이미 정확히
내장하고 있어 우리가 재구현할 필요가 없다.** SVF도 마찬가지로 UMEP 전용 SVF 산출 도구를
그대로 쓰면 됨 — Method A식 직접 계산 불필요.

## 5. 다음 액션 (v2 기준)

1. ✅ ~~토지피복 크로스워크 표 작성~~ → 완료 (`03_Method_C/code/landcover_crosswalk_L3_to_UMEP.csv`)
2. ✅ ~~원본 임상도(수고) 확보~~ → 완료
3. ✅ ~~건물 높이 확보~~ → 완료 (4단계 하이브리드)
4. ✅ ~~2장(일부)·3장 초안 작성~~ → 완료 ([[writing/2026-07-07_2장선행연구검토_3장연구자료구축및방법론_v1]])
5. **DSM·CDSM 실제 rasterize 코드 작성** (QGIS Python 콘솔용, 접근1=30m/접근2=1m 두 세트)
6. Wall height/aspect, SVF 산출 (UMEP 도구)
7. SOLWEIG 연속 실행 (06~19시 1시간 간격)
8. 출력 집계 및 Hard Cut 임계값 결정 (UTCI급간 vs MRT 56/58°C — 공간분화 결과 보고 판단)
