지도 제목: SEAR 감소율(%) 공간분포 — 집계구/행정동/구 3단계, 대표 시각(09/14/18시)

범례: 별도 파일(`legend_sear_{jibgyegu,dong,gu}_barsonly.png`) — 라벨 없음(PPT에서
직접 입력 예정). 6급간 자연분류(Jenks) 색상 6단 + 결측(회색+빗금) 1단, 총 7단.
레벨별로 09·14·18시 3개 시각 값을 풀링해 breaks 산출(같은 레벨 내에서는 시각 간
비교 가능하도록 공통 classification 사용, 결측은 breaks 계산에서 제외).

방위표: 없음(PPT에서 직접 추가)

축척: 5km 축척바 포함, 우하단 고정 위치. `figure_UTCI래스터_전시간대/서울/
utci_raster_seoul_clip_18h_축척.png`를 픽셀 단위로 실측(가로 83.9~97.5%,
세로 하단 3.2~4.1%)해 동일 위치·스타일(검정 막대, 흰배경 없음)로 맞춤.

경계·결측: 모든 레이어(집계구/행정동/구/하천)를 서울 행정경계(행정구역.shp
dissolve)로 클립 — 경계 밖으로 하천이 삐져나가는 문제 해소. opp_CA=0(기회
도달 자체가 불가해 감소율이 정의되지 않는 경우)은 회색+빗금(hatch)으로 표시하고
자연분류 계산에서 제외(집계구 레벨 285건, 행정동·구는 합산 후 0건).

경계선 스타일·구 슬리버 처리(2026-08-17 최종 확정 — KHU_GIS_Project 강의노트
jparkgeo/Geospatial_Data_Visualization.ipynb 방식 채용): 집계구는 흰색 경계선
유지. 구는 dissolve 직후 발생하는 내부 슬리버("지렁이" 라인)를 양수
buffer(5m) 한 번으로 해소 — 처음엔 buffer(+10).buffer(-10)(부풀렸다 깎기)
방식을 썼으나 이 "깎는" 단계에서 구멍·스프링 모양 부작용이 생겨(예: 구로구)
폐기, 노트북 방식(디졸브 → 양수 buffer만, 깎지 않음)으로 교체. 서울 경계
클립(clip) 자체도 미세한 새 구멍을 만들 수 있어(2026-08-17 확인, 클립 후
금천구 28개·관악구 1개 구멍 발생) 클립 뒤에 같은 양수 buffer(5m)를 한 번 더
적용. 잔여 구멍은 최대 900㎡ 내외로 렌더링 해상도(픽셀당 약 180m)보다
작아 시각적으로 보이지 않음(직접 확인). 행정동은 애초에 디졸브를 안 해서
슬리버가 없었는데 같은 buffer 처리를 걸었다가 오히려 멀쩡한 경계가
뭉개지는 부작용만 생겨 제거함(원본 그대로 사용) — 경계선 색만 회색으로 변경.

하천 처리(최종): 하천은 land와 완전히 무관한 별도 레이어로만 취급(표시
zorder=3), land geometry는 전혀 건드리지 않음(difference로 지우려던 시도는
하천 폴리곤이 1,871개 조각이라 구 내부에 최대 805개의 구멍을 만드는 부작용이
있어 폐기, 표시용 버퍼도 마찬가지로 하천 내부 섬 주변에서 렌더링 부작용을
일으켜 폐기 — 최종적으로는 가공 없이 원본 그대로 얹기만 함). 하천 자체에
한강 교량 구간(다리 밑은 원본에서 "물" 아님으로 제외됨) 등 실제 빈틈이
일부 있으나 land를 건드리지 않으므로 지도 전체 판단에는 영향 없음.

구성:
- `sear_reduction_{level}_{hour}h_{river|norriver}.png` — level=jibgyegu/dong/gu,
  hour=09/14/18, 한강(seoul_water.gpkg) 레이어 유/무 각각 별도 저장(18장)
- `legend_sear_{level}_barsonly.png` — 레벨별 6급간 색상 스와치(3장)

자연분류 breaks(2026-08-18 최종, 시각 풀링 기준):
- 집계구: [13.5, 34.4, 55.6, 75.4, 92.2, 100.0]
- 행정동: [15.8, 36.6, 57.0, 75.8, 92.1, 100.0]
- 구: [18.3, 38.1, 56.8, 71.3, 93.7, 100.0]

집계 방식: 집계구 원자료(opp_CA, opp_SEAR)를 ADM_CD(행정동)·SIGUNGU_CD(구) 기준으로
sum한 뒤 reduction_pct = (ΣCA − ΣSEAR)/ΣCA × 100 재계산(개별 집계구 reduction_pct의
단순평균이 아님 — 집계구별 CA 크기가 다르므로 sum 기반이 통계적으로 올바름).

경계 데이터: `data/_tmp_boundary/집계구.shp`(집계구, ADM_CD 포함),
`data/_tmp_boundary/행정구역.shp`(행정동 424개, SIGUNGU_CD로 구 25개 dissolve),
`data/_tmp_boundary/seoul_water.gpkg`(하천, EPSG:5179)

데이터: `03_Method_C/results/2026-08-18_seoul_jibgyegu_contour_CA_vs_SEAR_api_network_nobuffer.csv`
(픽셀 우선계산·버퍼 없음 + 서울시 도보 네트워크 API 기준 — 마스터 값은 이 파일)

⚠️ 2026-08-18 정정: 2026-08-17에 만든 첫 버전(`2026-08-17_seoul_jibgyegu_
contour_CA_vs_SEAR_allhours_kma_pixel_nobuffer.csv`)은 "API 기반"이라고
캡션에 적어놨었지만 실제로는 스크립트가 OSM 네트워크(`seoul_walk_network.
graphml`)를 잘못 참조하고 있었음 — 이 실수는 2026-08-06 원본 파이프라인부터
있던 것으로 추정. 정정된 API 네트워크(`2026-08-02_seoul_walk_api_network.
gpkg`, TbTraficWlkNet, 279,016개 링크) 기준으로 픽셀 UTCI 래스터부터
재집계(`32_assign_utci_links_api_network_nobuffer_server.py`)·SEAR 재계산
(`33_seoul_wide_api_native_contour_nobuffer.py`) 완료. 이전 OSM 기반 결과는
폐기하지 않고 §3.3 네트워크 선택 강건성 비교(메인 API vs 검증 OSM)의 OSM쪽
데이터로 재활용함.

네트워크: 서울시 도보 네트워크 API 기반(TbTraficWlkNet, OSM 아님) — 실제로 확인됨

생성 스크립트: `03_Method_C/code/31_plot_sear_reduction_maps_3levels.py`

09시 지도 상단(노원구 등 일부 구)이 옅은 살구색으로 나오는 건 결측이 아니라
실제로 감소율이 낮은 지역(해당 시각 열환경 영향이 상대적으로 적음)임 —
결측(회색+빗금)과는 색상으로 명확히 구분됨. 고정 지도범위(FULL_BOUNDS) 적용
확인 완료, 3단계 모두 동일한 서울 전체 경계로 렌더링됨.
