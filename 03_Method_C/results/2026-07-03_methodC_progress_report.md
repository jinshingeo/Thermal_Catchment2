# Method C (SOLWEIG 30m DSM) 진행 현황 및 파일럿 비교
작성일: 2026-07-03 | 버전: v1.0

---

## 1. 현재 진행 상황 요약

| 단계 | 상태 | 비고 |
|------|------|------|
| SOLWEIG 실행 | **완료** (MRT 산출 성공) | 단, DSM 좌표 오류 있음 (아래 참조) |
| MRT 링크 집계 | **차단 중** | DSM 재투영 오류로 MRT 래스터 위치 엉뚱 |
| 응봉/성수역 지도 | **대기** | 집계 완료 후 자동 생성 가능 |
| 서울 전체 파이프라인 | **코드 준비 완료** | 데이터 준비 필요 |

---

## 2. 발견된 문제: DSM 재투영 오류

### 문제 내용
- **원본 DSM**: `DSM_seongdong_2m.tif` (CRS: `LOCAL_CS["KGD2002/Central Belt 2010"]`)
- **실제 CRS**: EPSG:5186 (KGD2002 중앙 자오선 127°E)
- **QGIS 재투영 결과**: UTM52N(EPSG:32652) 좌표가 성동구에서 **서쪽 ~10km 오차**

### 증거
| 항목 | 값 |
|------|----|
| MRT 래스터 실제 위치 (UTM→WGS84) | 126.88~126.95°E, 37.57~37.61°N |
| 성동구 실제 위치 | 126.99~127.09°E, 37.52~37.59°N |
| 거리 오차 | ~10km |

### 원인
QGIS가 `LOCAL_CS` 태그를 가진 DSM을 EPSG:5186으로 인식 못 하고 다른 CRS로 처리.

### 해결 방법 (다음 실행 시)
QGIS Python Console에서 실행:
```python
exec(open('/scratchpad/run_solweig_correct_dsm.py').read())
```
→ GDAL Warp로 EPSG:5186 명시 재투영 → SOLWEIG 재실행 → 올바른 MRT 래스터 생성

---

## 3. 파일럿(Method A) vs Method C 비교 프레임

### 방법론 차이
| 항목 | Method A (파일럿) | Method C (현재) |
|------|-----------------|----------------|
| MRT 산출 | 약식 MRT (H/W Canyon + SVF) | SOLWEIG + 30m DSM |
| 데이터 | OSM + 건물 폴리곤 | DSM + DEM + 기상 |
| 해상도 | 링크 단위 직접 계산 | 30m 래스터 → 샘플링 |
| 기상 입력 | IDW or 단일값 (S-DoT) | 단일 기상관측소 |
| UTCI 임계값 | 38°C | 42°C (MRT 56°C) |
| 검토 날짜 | 2025-07-28~08-03 (7일 평균) | 2025-07-25 14:00 KST |

### 파일럿 결과 (Method A, h13 — 13시)

| 역 | Classic (노드) | Thermal (노드) | 감소율 |
|----|--------------|--------------|--------|
| 응봉역 (경의중앙선) | 891 | 1 | **99.9%** |
| 성수역 (2호선) | 644 | 1 | **99.8%** |

> ⚠️ 파일럿 임계값 UTCI 38°C는 현재 확정 기준(42°C)과 다름 — 직접 수치 비교 시 주의

### Method C 예상 결과
- 임계값을 UTCI 42°C (MRT 56°C)로 높이면 파일럿보다 Hard Cut 수가 적을 것으로 예상
- 하지만 SOLWEIG MRT는 약식 MRT보다 일반적으로 높게 나오므로 실제 결과는 실행 후 확인 필요

---

## 4. 다음 실행 순서

### ① SOLWEIG 재실행 (QGIS Console, 약 15분)
```python
exec(open('/private/tmp/claude-501/-Users-jin------TAVI/11a7aa5d-485a-4d32-8032-faf31923985e/scratchpad/run_solweig_correct_dsm.py').read())
```

### ② mrt_link_aggregation.py의 MRT 경로 수정
완료 후 아래 라인 변경:
```python
# 현재 (잘못된 래스터)
MRT_TIF = SCRATCH + "/umep_output_seongdong/solweig_out/Tmrt_2025_206_1400D.tif"
# 변경 후 (올바른 래스터)
MRT_TIF = SCRATCH + "/umep_output_seongdong_v2/solweig_out/Tmrt_2025_206_1400D.tif"
```

### ③ 파이프라인 전체 실행
```bash
export PROJ_LIB="/opt/miniconda3/lib/python3.13/site-packages/pyproj/proj_dir/share/proj"
cd /Users/jin/석사논문/Thermal_Catchment/03_Method_C/code
bash run_all_method_c.sh
```

---

## 5. 파일 목록

### 완성된 코드
| 파일 | 역할 |
|------|------|
| `code/mrt_link_aggregation.py` | MRT → 링크 집계 + Hard Cut (v3) |
| `code/catchment_contrast_map.py` | 응봉역/성수역 비교 지도 (v2) |
| `code/mrt_link_aggregation_seoul.py` | 서울 전체 파이프라인 |
| `code/download_seoul_network.py` | 서울 전체 보행 네트워크 다운로드 |
| `code/run_all_method_c.sh` | 전체 실행 스크립트 |
| `/scratchpad/run_solweig_correct_dsm.py` | QGIS Console용 DSM 수정 + SOLWEIG 재실행 |

### 생성될 결과물
| 파일 | 생성 조건 |
|------|---------|
| `results/2026-07-03_catchment_contrast_eungbong_methodC.png` | 집계 완료 후 |
| `results/2026-07-03_catchment_contrast_sungsoo_methodC.png` | 집계 완료 후 |
| `results/2026-07-03_catchment_summary_method_c.csv` | 집계 완료 후 |

---

## 6. 서울 전체 확장 준비 사항

### 필요한 데이터
1. **서울 전체 보행 네트워크**: `download_seoul_network.py` 실행 (osmnx)
2. **서울 전체 DSM (30m)**: QGIS에서 서울 전체 범위로 SOLWEIG 실행
   - 성동구와 동일한 방법: DSM(EPSG:5186) → UTM52N → Wall H&A → SVF → SOLWEIG
   - 서울 전체는 구 단위로 나눠 실행 후 mosaic 권장
3. **서울 전체 MRT 래스터**: SOLWEIG 출력 → `mrt_link_aggregation_seoul.py`

### 예상 소요 시간
- 서울 전체 SOLWEIG: 구 단위 25개 × 약 20분 = ~8시간 (또는 병렬 처리)
- 서울 전체 링크 집계: ~30분 (약 100만 링크 예상)
