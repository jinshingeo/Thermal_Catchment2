작성일: 2026-07-07
버전: v1
근거논문: Lindberg et al. (2008, 2018), Erbs et al. (1982), Colaninno et al. (2024), Basu et al. (2024)

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

## 3. 지오메트리 입력 데이터 확보 현황

| 데이터 | 상태 | 위치/출처 |
|---|---|---|
| DEM | GLO-30(30m, 오픈소스) 확보됨, 국토지리정보원 1m DEM 신청 진행상황 미확인(서식만 준비됨) | `data/GLO30_DSM/` |
| 건물 폴리곤+층수 | ✅ 확보 — `GRO_FLO_CO`(지상층수)/`UND_FLO_CO`(지하층수) 필드 있음, 도로명주소 공식자료, EPSG:5179 | `/Users/jin/석사논문/TAVI/03_건물데이터/(도로명주소)건물_서울/TL_SPBD_BULD_11_202603.shp` |
| 토지피복도 | ✅ 확보 — 환경부 세분류(L3, 37클래스), 서울 전체 136타일 병합 완료, EPSG:5186(ITRF2000/TM, 기존 Method A와 동일 CRS) | `data/landcover_seoul_L3_merged.gpkg` (105만 피처, 640MB) |
| 수목 캐노피(CDSM) | ❌ 미확보 — 2SFCA 프로젝트의 `도시숲전체_면_서울_최종_중분류.shp`, `임상도_병합.geojson`은 수종/영급/수고 속성이 없음(병합 과정에서 손실 추정). **원본 임상도(영급 필드 포함) 재확보 필요** — 산림청 표준 임분수확표로 영급→수고 매핑하면 "대표값 임의 부여"보다 방어력 있는 근거 확보 가능 |
| 성동구 경계 | ✅ 확보 — 국토지리정보원 N3A_G0100000(시군구경계, 1:5,000, EPSG:5179) 및 SGIS 통계지역경계(readme 기준 EPSG:5179) 두 소스 확보 |

## 4. UMEP SOLWEIG 입력 포맷 확인 사항

met.txt는 UMEP 표준 24컬럼 포맷(iy,id,it,imin,qn,qh,qe,qs,qf,U,RH,Tair,pres,rain,kdown,
snow,ldown,fcld,wuh,xsmd,lai,kdiff,kdir,wdir). 공식문서로 컬럼 순서·의미 확인함
(umep-docs.readthedocs.io). 미사용 컬럼은 -999.

**landcover 기본 파라미터** (로컬 설치된 UMEP 플러그인 실제 파일에서 확인,
`~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/UMEP/SOLWEIG/landcoverclasses_2016a.txt`):

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

## 5. 다음 액션

1. 토지피복 37클래스 → UMEP landcover 7클래스 매핑표 작성 (산림류는 CDSM으로 분리)
2. 원본 임상도(영급 포함) 재확보 → 산림청 임분수확표 기반 수고 매핑
3. 건물 데이터로 합성 DSM 생성 (UMEP DSM Generator, GLO-30 ground + 층수)
4. QGIS Python 콘솔 실행용 코드 작성 (사용자가 QGIS에 붙여넣어 실행하는 워크플로우)
