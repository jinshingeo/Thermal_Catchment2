# Method C (GLO-30 DSM + SOLWEIG) 진행 현황
작성일: 2026-07-04 | 버전: v2.0

---

## 현재 상태: SOLWEIG 실행 대기

| 단계 | 상태 |
|------|------|
| DSM/DEM clip (성동구, 올바른 좌표) | ✅ 완료 |
| QGIS SOLWEIG 실행 | ⏳ **실행 필요** |
| MRT 링크 집계 | 대기 |
| 응봉/성수역 비교 지도 | 대기 |
| 서울 전체 overnight 실행 | 이후 |

---

## 지금 당장 할 것: QGIS Console에서 아래 1줄 실행

```python
exec(open('/private/tmp/claude-501/-Users-jin------TAVI/11a7aa5d-485a-4d32-8032-faf31923985e/scratchpad/run_solweig_seongdong_v2.py').read())
```

**예상 소요 시간**: 성동구 v1 (233×167px)과 유사한 수 분
**출력 경로**: `/scratchpad/umep_output_seongdong_v2/solweig_out/Tmrt_2025_206_1400D.tif`

스크립트 안에 **좌표 자동 검증** 포함 — 마지막에 `✅ OK` 뜨면 다음 단계 진행.

---

## SOLWEIG 완료 후 바로 실행 (터미널)

```bash
export PROJ_LIB="/opt/miniconda3/lib/python3.13/site-packages/pyproj/proj_dir/share/proj"
bash /Users/jin/석사논문/Thermal_Catchment/03_Method_C/code/run_all_method_c.sh
```

→ 자동으로:
1. MRT → 링크별 집계 (Buo et al. 2026 방식)
2. Hard Cut (MRT ≥ 56°C)
3. 응봉역 / 성수역 비교 지도 PNG 생성
4. 감소율 요약 CSV 생성

---

## 이전 실패 원인 (다시는 반복 안 함)

| 문제 | 원인 | 해결 |
|------|------|------|
| MRT 링크 유효 0% | DSM_Seongdong_UTM52N.tif가 성동구에서 ~10km 서쪽으로 잘못 투영 | 서울 DSM(올바른 좌표)에서 clip |
| `ox.load_graphml` OSM 재다운로드 | osmnx 2.x 호환성 변경 | `nx.read_graphml`로 교체 |
| `CRS.to_epsg()` → None | PROJ 버전 충돌 | `to_epsg() or 32652` fallback |

---

## DSM/DEM 파일 현황

| 파일 | 크기 | 좌표(UTM52N) | 용도 |
|------|------|------------|------|
| `DSM_Seoul_UTM52N.tif` | 1496×1140px | ✅ 296418~341298E | 서울 전체 (원본) |
| `DEM_Seoul_UTM52N.tif` | 1496×1140px | ✅ 296418~341298E | 서울 전체 (원본) |
| `DSM_Seongdong_v2.tif` | 273×233px | ✅ 322848~331038E | 성동구 clip (v2, 올바름) |
| `DEM_Seongdong_v2.tif` | 273×233px | ✅ 322848~331038E | 성동구 clip (v2, 올바름) |
| `DSM_Seongdong_UTM52N.tif` | 233×167px | ❌ 잘못된 위치 | 폐기 |

성동구 보행 네트워크 UTM 범위: E 324059~329850, N 4155663~4160242
→ v2 clip 범위(E 322848~331038, N 4154478~4161468) 내에 완전 포함 ✅

---

## 성공 후: 서울 전체 overnight 실행

성동구 검증 완료되면 `run_solweig_seongdong_v2.py`를 서울 전체용으로 확장:

```python
DSM = SCRATCH + "/DSM_Seoul_UTM52N.tif"   # 1496×1140px
DEM = SCRATCH + "/DEM_Seoul_UTM52N.tif"
OUT = SCRATCH + "/umep_output_seoul"
```

- 예상 시간: 성동구 약 3~5분 × 44배 → **2~4시간** (SVF 포함)
- 실행: 자리 비울 때 overnight으로 돌리기
