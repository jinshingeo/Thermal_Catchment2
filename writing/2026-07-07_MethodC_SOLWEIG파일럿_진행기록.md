작성일: 2026-07-07 (2026-07-09 SOLWEIG 실행·링크부여·시각화 결과 추가 v3, 2026-07-12 접근2 5m 파일럿 추가 v4)
버전: v4
근거논문: Lindberg et al. (2008, 2011, 2016, 2018), Erbs et al. (1982), Colaninno et al. (2024), Basu et al. (2024), Jia et al. (2022), Wallenberg et al. (2026)

> ⚠️ v1은 세션 초반 스냅샷이라 이후 발견사항(임상도 원본 HEIGHT, F_FAC_BUILDING 건물높이,
> 크로스워크 표 등)이 빠져있었음. v2에서 전체 업데이트. v3은 2026-07-09 SOLWEIG 실행
> 성공(접근1, 30m) 및 링크 부여·시각화 결과 추가. v4는 2026-07-11~12 접근2(1m) 메모리
> 위기 발견 및 5m 파일럿 실행·비교 결과 추가. 모든 산출 요소의 상세 근거는
> [[writing/2026-07-09_MRT산출_기술노트_전체요소정리]] 참고(이게 정본, 이 문서는 진행 로그).
> 상세 방법론 서술은 [[writing/2026-07-07_2장선행연구검토_3장연구자료구축및방법론_v1]] 참고.

## 0. 2026-07-09 추가 — SOLWEIG 실행 성공 및 링크 부여·시각화

**서버 발견**: 로컬 QGIS가 접근2(1m) SVF 계산 중 85.57GB 메모리 사용으로 크래시함
(맥 강제종료 필요). 사용자 리눅스 서버(163.180.10.188, Rocky Linux 9.6, RAM 124GB/
가용115GB, 24코어) 확인 — 접근2는 이쪽으로 이전 예정, QGIS/UMEP 설치 필요.

**접근1(30m) SOLWEIG 실행 성공**: `umep:Outdoor Thermal Comfort: SOLWEIG` 정상 실행,
06~19시 Tmrt 래스터 14장 + 일평균 1장 산출 (`03_Method_C/results/dsm_cdsm_seongdong/
solweig_approach1_30m/`). 실행 시 `INPUT_DEM`이 사실상 필수 파라미터였음(순수 지면
DEM 별도 저장 필요, `DEM_approach1_30m.tif`/`DEM_approach2_1m.tif` 추가 생성).

**결과 검증 — 핵심 발견**: 13시 기준 링크 표준편차 4.62°C, 최소~최대 34.9~68.2°C로
**뚜렷한 공간분화 확인**. 2026-07-04에 발견했던 "GLO-30 단독 30m는 공간분화 실패"
문제가, 오늘은 **같은 30m 해상도인데도** 건물·수목·토지피복 정보를 제대로 반영하니
해결됨 — 문제의 원인이 해상도 자체가 아니라 지오메트리 정보의 유무였음을 실증.

**링크 단위 Tmrt 부여**: SOLWEIG는 네트워크 개념이 없어 별도 후처리 필요.
Colaninno et al.(2024)의 "세그먼트 버퍼+zonal mean" 방식 채택(Buo et al. 2026은
버퍼 없는 선-래스터 교차 방식이나 구현 디테일 불명확해 재현성 낮다고 판단).
버퍼 폭은 OSM width 태그(0.9%) 또는 도로유형별 통상값(⚠️근거논문 미확보).
`all_touched=True` 필요(안 그러면 30m 격자 대비 좁은 버퍼가 픽셀 중심점을 못 잡아
72%가 결측되는 문제 실제 확인함). 16,316개 링크 전부 결측 없이 부여 완료
(`03_Method_C/results/2026-07-09_link_tmrt_approach1_30m.gpkg`/`.csv`).

**시각화**: 래스터·링크 각각 (1) 06~19시 14장 그리드, (2) Colaninno 3구간(아침/낮/
저녁) 평균 지도, (3) 링크 Tmrt 분포 KDE(3구간 비교 + 시간대별 능선그래프) —
전부 공통 컬러스케일/축으로 시간대 간 비교 가능하게 제작 (`03_Method_C/results/
figures/2026-07-09_*.png`).

**모든 산출 요소(SOLWEIG 정식방식 vs 문헌기반 vs 자체가정 구분)는
[[writing/2026-07-09_MRT산출_기술노트_전체요소정리]]에 체계적으로 정리함.**

## 0.1 UTCI 탐색 산출 (⚠️ 탐색적 기록 — 논문에 바로 쓰기로 확정한 것 아님)

**산출 방법**: Ta/RH는 S-DoT 서울 전체 지점(1,011개, 결측 제거 후) 기반 IDW 보간
(leave-one-out CV로 power=1 선정, RMSE=1.045), 풍속은 met.txt의 AWS 균일값 그대로
사용(별도 보간 인프라 없음). Tmrt는 기존 링크 산출값. `pythermalcomfort`로 UTCI 계산
(`03_Method_C/code/07_build_idw_utci_links.py`). IDW 검증: 13시 Ta_idw 평균 35.6°C,
기존 단순평균(35.77°C)과 근접해 일관성 확인됨.

**탐색적 발견 (Hard Cut 임계값 논의 참고용, 결정 아님)**:
- 시간대별 UTCI≥38°C/42°C, Tmrt≥56°C/58°C 초과 링크 비율을 06~19시 전체로 확인한 결과,
  **UTCI≥38°C는 09~19시(10시간) 거의 내내 80~100%로 포화**되어 시간대 구분력이 약함.
  반면 **UTCI≥42°C(또는 Tmrt≥56/58°C)는 10~17시에만 높고 그 앞뒤(06-09시, 18-19시)는
  급격히 낮아지는 뚜렷한 "위험 시간대" 패턴**을 보임.
- **3구간(Colaninno) 집계 vs 시간대별(14장) 집계 비교**: UTCI 열스트레스 급간(Bröde 2012)
  으로 시각화했을 때, 3구간으로 평균 내면 각 구간이 거의 단일 급간(아침 99.8% Strong,
  낮 99.7%/저녁 99.3% Very strong)으로 뭉개져 정보량이 거의 없음. 시간대별(14장)로 보면
  09시·18-19시의 전환이 뚜렷하게 살아남 — **집계 단위에 따라 UTCI 급간의 유용성이 달라짐**.
- 이 두 관찰 다 "UTCI를 최종적으로 채택할지, MRT 임계값을 쓸지"를 판단하는 데 참고할
  근거 자료로만 기록. 최종 Hard Cut 지표·임계값·집계단위는 아직 미확정.

**시각화**: UTCI 연속값(래스터 아님, 링크만) 시간대별 14장·3구간·분포(3구간 비교+
능선그래프) 4종, UTCI 급간(Bröde 2012) 범주형 지도 2종(3구간·시간대별)
(`03_Method_C/results/figures/2026-07-09_*UTCI*.png`, 결과 데이터
`2026-07-09_link_utci_approach1_30m.gpkg`/`.csv`).

## 0.2 2026-07-11~12 추가 — 접근2(1m) 메모리 위기 발견 및 5m 파일럿 실행·비교

**로컬 크래시 재확인**: 접근2(1m) SVF는 Wall Height/Aspect까지는 로컬에서 성공했으나
(`wallheight_approach2_1m.tif`/`wallaspect_approach2_1m.tif`), SVF 단계에서 크래시하여
결과물 없음(폴더 비어있음 확인). SOLWEIG는 SVF 선행 필요라 시작도 못 함.

**서버 이전 중 겪은 문제 4가지(순차 해결)**: (1) pip pyproj의 번들 libproj가 시스템
libproj와 충돌 → pip pyproj 제거 후 시스템 RPM `python3-pyproj`로 교체, (2) 헤드리스
서버에 디스플레이가 없어 Qt 초기화 실패 → `QT_QPA_PLATFORM=offscreen`, (3) `netCDF4`
모듈 누락 → pip 설치, (4) **Rocky Linux 9 AppStream의 시스템 `gdal-libs` 자체가 GTiff
드라이버를 포함하지 않는 최소 빌드임을 발견**(`nm -D`로 `GDALRegister_GTiff` 심볼 부재
확인, 재설치해도 동일 — 손상이 아니라 원래 이런 구성). → **conda-forge QGIS(3.44.11,
GDAL 3.13.1 full build)로 완전히 전환**하여 해결(신규 conda env `qgis_umep`).

**진짜 병목 발견 — 속도가 아니라 메모리**: `svfForProcessing153`(153 patch, ANISO=True)는
SOLWEIG 비등방성 하늘 모델용으로 153개 patch 전체의 그림자 행렬(`shmat`/`vegshmat`/
`vbshvegshmat`, `Solweig_run.py` 401~403줄에서 실제로 로드해 사용 — 선택사항 아님)을
전부 메모리에 들고 있다가 `shadowmats.npz`로 저장함. 성동구 bbox(5820×5010px, 1m) 기준
계산하면 3개 행렬 합쳐 **float64 기준 약 107GB** — 로컬 85GB 크래시와 서버 재현 시도 중
112GB까지 치솟은 것의 정확한 원인. 코드 확인 결과(`shadowingfunctions.py` 내
`shadow.shadowingfunction_20`은 numpy/matplotlib 의존성뿐이라 이론상 patch 단위
multiprocessing 병렬화는 수학적으로 안전(각 patch 독립 계산 후 단순 가중합)하나,
최종적으로 이 107GB 행렬 자체를 어차피 다 들고 있어야 해서 **병렬화만으로는 메모리
문제가 해결 안 됨** → 병렬 구현 시도 중단, 해상도 축소로 방향 전환.

**5m 파일럿 결정 및 정확한 리샘플링 방법**: 1m 픽셀 수(2900만) 대비 5m는 1/25
(약 117만)이라 시간·메모리 모두 25배 감소 추정(→ 메모리 약 4.3GB, 시간 몇시간대 예상).
⚠️ **이 5m은 접근2(1m)와 다른 방식으로 만들어짐** — 벡터에서 직접 rasterize한 게
아니라, 이미 구축된 `DSM/CDSM/DEM_approach2_1m.tif`를 `rasterio.warp.reproject`로
**연속형(DSM/CDSM/DEM)은 `Resampling.average`, 범주형(LandCover)은 `Resampling.mode`**
로 다운샘플링(`03_Method_C/code/11_resample_1m_to_5m.py`). 반면 접근1(30m)은 벡터
(건물 폴리곤+높이속성)에서 `rasterio.features.rasterize()`로 **직접** 30m 격자를
만드는데, 이 함수는 각 셀의 **중심점이 어느 건물 폴리곤 안에 드는지만** 보고 그 건물
높이를 그대로 대입함(평균도 최댓값도 아님) — 그 결과 30m 셀보다 작은 건물은 격자
정렬에 따라 전체 반영되거나(중심점이 안에 들면) 전체 누락되는(중심점이 밖이면)
"복불복 point-sampling" 특성을 가짐(`01_build_dsm_cdsm_seongdong.py` 125~136줄
확인). 즉 30m는 원천 rasterize 단계에서 정보가 소실되고, 5m(오늘 것)는 이미 세밀한
1m 데이터를 성실하게 면적평균한 것이라 **구축 경로 자체가 다름** — 향후 논문에서
"해상도만 통제된 순수 비교"라고 서술하면 안 되고 이 차이를 명시해야 함.

**CRS 손상 발견 및 수정**: 리샘플링 스크립트에서 로컬 PROJ 충돌 회피용으로 넣어둔
`PROJ_DATA` 환경변수가 EPSG:5186을 제대로 못 써서, 리샘플된 5m 파일들의 CRS가
`LOCAL_CS["KGD2002 / Central Belt 2010", ...]`라는 손상된 형태로 저장됨(SOLWEIG의
`xy2latlon_fromraster`가 위경도 변환 실패로 크래시). 서버의 정상 GDAL로 `rasterio.crs.
CRS.from_epsg(5186)`을 직접 대입해 수정, 이를 상속한 Wall Height/Aspect·SVF 출력도
재계산.

**5m 파이프라인 결과**: Wall Height/Aspect(수초) → SVF(9분, 메모리 안정적으로 5GB
내외 유지, ANISO=True 153patch) → SOLWEIG(45분, UTC=9) 순서로 전부 성공. Tmrt 14개
시간대+평균 산출, 값 정상 범위(13시 34.6~69.3°C). 링크 부여도 30m와 동일 방식
(Colaninno 버퍼+zonal mean, `all_touched=True`, 동일 네트워크·버퍼폭 가정)으로 수행,
16,316개 링크 결측 0개(`03_Method_C/results/2026-07-12_link_tmrt_approach2_5m.gpkg`/
`.csv`).

**30m vs 5m 비교 결과**: 3구간 평균 차이는 작음(아침 -1.17°C, 낮 -0.51°C, 저녁
-2.07°C, 링크 단위 기준) — 그러나 **링크×시간 단위(228,424개 조합)로 보면 절대 차이
평균 2.55°C, 최대 27.2°C**까지 벌어짐. 즉 전체 평균은 비슷해도 개별 링크·시간대에서는
해상도에 따라 결과가 크게 달라질 수 있음 — Hard Cut 임계값 적용 시 특정 링크의
포함/제외 여부가 해상도에 따라 뒤집힐 수 있다는 뜻으로, 축 1(MRT 산출방식 비교)의
근거로 활용 가능. 시각화 6종(래스터 3+링크 3, 전부 30m/5m 공통 컬러스케일)
`03_Method_C/results/figures/2026-07-12_*compare_30m_5m.png`.

**다음 단계**: 5m 결과를 기준선으로 두고, 접근2 원래 목표인 1m 실행을 서버에서
시간이 걸리더라도 진행 예정. ⚠️ **단순 픽셀수 비례(25배)로는 5m의 9분×25=3.75시간
정도로 예상되지만, 실제 서버에서 1m를 시도했을 때(2026-07-10) py-spy로 실측한 결과
90분 동안 153 patch 중 겨우 1~2개만 진행되어 전체 5~10일로 추정된 바 있음** —
5m 대비 32~64배나 더 느려, 단순 CPU 연산량 비례를 크게 벗어남. 가장 유력한 원인은
1m의 107GB 요구량이 서버 RAM(124GB)에 근접해 스와핑·캐시미스 등 **메모리 압박으로
인한 비선형적 성능 저하**로 추정(확정된 원인 규명은 아님). 따라서 1m 실행 시
소요시간은 3.75시간이 아니라 **5~10일 범위를 기본 가정**으로 두고, 실행하며 실측
재확인 필요.

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

## 4.7 DSM·CDSM은 Python(rasterize+merge)으로 직접 생성 — ⚠️ 지도교수 확인 필요

`03_Method_C/code/01_build_dsm_cdsm_seongdong.py`로 DSM(건물높이+DEM)·CDSM(수목높이)을
QGIS 없이 Python(rasterio)으로 직접 생성함(접근1 30m/접근2 1m 완료, 결과는
`03_Method_C/results/dsm_cdsm_seongdong/`).

**판단 근거**: UMEP의 DSM Generator도 "건물폴리곤 높이를 래스터화해서 DEM에 더하는" 동일한
연산이라, SOLWEIG 고유의 검증된 알고리즘(그림자 캐스팅, SVF, 하늘복사 등)과 달리 특별한
물리모델이 들어있지 않음 — GUI로 감싼 것뿐이라 결과가 같아야 한다고 판단.

**⚠️ 다만 이건 우리 판단이고, 지도교수님께 확인 시 "그래도 정식 프로그램(UMEP DSM
Generator)으로 돌린 게 방어(defense)에 유리하다"는 의견이 나올 수 있음 — 그때는 동일
입력자료로 UMEP DSM Generator를 QGIS에서 실제로 돌려 본 결과와 대조 검증하거나, 아예
그쪽으로 대체할 수 있음. 논문 심사 전에 이 판단을 재확인할 것.**

## 4.8 WALL_SCHEME(Wallenberg et al. 2026 벽면온도 파라미터화) — 이번 파일럿엔 미적용

SOLWEIG SVF 알고리즘의 `WALL_SCHEME` 옵션을 켜면 벽 재질별(벽돌/콘크리트/목조) 열물성
기반 벽 표면온도 계산(Wallenberg et al. 2026, [[references/study_note_Wallenberg2026_WallTemp]])이
가능하다는 걸 확인했으나, **이번 파일럿에서는 미적용(WALL_SCHEME=False)으로 확정.**

**사유**: 건물 구조코드(STRCT_CD) 결측이 성동구 32.2%(서울 전체 21.6%)이고, 재질 미상일
때 무엇으로 대체할지에 대한 논문상 규정이 없어(확인됨) 별도의 자체 가정이 추가로 필요함.
현재도 건물높이·수목높이 등에서 이미 여러 자체 가정을 쌓은 상태라, 여기에 결측 처리
가정을 하나 더 얹는 것은 투고 일정(8월) 대비 리스크 대비 이득이 작다고 판단.

**대응 문구(심사·질의 대비)**: "건물 구조(재질) 정보 결측률이 높아(성동구 32.2%) 이번
분석에서는 벽면온도 파라미터화 스킴(Wallenberg et al., 2026)을 적용하지 않았으며, 향후
재질 데이터가 보완되면 반영 가능하다." — **지도교수님이 반영을 요청하면 그때 STRCT_CD
매칭표(벽돌/콘크리트/목조, 결측은 최빈값 대체)를 만들어 재실행.**

## 5. 다음 액션 (v2 기준)

1. ✅ ~~토지피복 크로스워크 표 작성~~ → 완료 (`03_Method_C/code/landcover_crosswalk_L3_to_UMEP.csv`)
2. ✅ ~~원본 임상도(수고) 확보~~ → 완료
3. ✅ ~~건물 높이 확보~~ → 완료 (4단계 하이브리드)
4. ✅ ~~2장(일부)·3장 초안 작성~~ → 완료 ([[writing/2026-07-07_2장선행연구검토_3장연구자료구축및방법론_v1]])
5. **DSM·CDSM 실제 rasterize 코드 작성** (QGIS Python 콘솔용, 접근1=30m/접근2=1m 두 세트)
6. Wall height/aspect, SVF 산출 (UMEP 도구)
7. SOLWEIG 연속 실행 (06~19시 1시간 간격)
8. 출력 집계 및 Hard Cut 임계값 결정 (UTCI급간 vs MRT 56/58°C — 공간분화 결과 보고 판단)
