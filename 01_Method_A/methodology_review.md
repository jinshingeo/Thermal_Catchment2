---
작성일: 2026-06-23
버전: v1.0
방법: Method A — 약식 MRT (Oke 1987 H/W Canyon SVF)
상태: 파일럿(성동구) 완료 / 서울 전체 확장 예정
---

# Method A — 약식 MRT 방법론 정리

## 파이프라인 요약

```
01_download_network.py   → OSM 보행 네트워크 구축
15_svf_per_link.py       → SVF + 캐노피 비율 계산 (링크별)
39_utci_sdot_solweig.py  → 기상 IDW 보간 + MRT 산출
40_catchment_mrt.py      → Hard Cut → Thermal Catchment 계산
```

## 핵심 파라미터
| 파라미터 | 값 | 근거 |
|---------|-----|------|
| WALK_SPEED | 4.5 km/h | ⚠️ 근거 논문 미확보 — 서치 필요 |
| TIME_BUDGET | 15분 | ⚠️ 근거 논문 미확보 — 서치 필요 |
| MRT 임계값 | 55°C | UTCI 38°C 역산 (Bröde et al. 2012) |
| ξ_k (인체 단파 흡수율) | 0.70 | Fanger (1970) |
| ε_p (인체 장파 방사율) | 0.97 | ISO 7726 (1998) |
| FP (투영면적계수) | 0.308 | Höppe (1992) |
| ε_w (도시 표면 방사율) | 0.90 | Oke (1987) |
| σ | 5.67×10⁻⁸ W/m²K⁴ | Stefan-Boltzmann 상수 |
| 나무 높이 | 10.0m | ⚠️ 근거 논문 미확보 — 서치 필요 |
| CANOPY_COEFF | 2.5 | ⚠️ 경험값, 근거 논문 없음 |
| 벽면 온도 오프셋 | +10K (일사 시) | ⚠️ 근거 논문 미확보 — 서치 필요 |

## SVF 계산 방식
**Oke (1987) H/W Street Canyon 공식**:
```
SVF = 1 / √(1 + (H_eff / W)²)
H_eff = H_building + 10.0 × canopy_ratio
```
- H_building: 링크 주변 20m 버퍼 내 건물 평균 높이 (지상층수 × 3m)
- W: 도로 유형별 표준 폭 (국토부 도로설계기준)
- canopy_ratio: 링크 주변 15m 버퍼 내 도시숲 면적 비율

**풀 SOLWEIG 대비 한계**: DSM fisheye 투영 없음, 그림자 계산 없음, 2D Canyon 근사

## MRT 계산 수식
```
K_abs = K_dir × FP + K_dif × SVF × 0.5
L_mean = L_sky × SVF + L_wall × (1 − SVF)
T_mrt (K) = ((ξ_k × K_abs + L_mean) / (ε_p × σ))^0.25
```
- 직산 분리: Erbs et al. (1982)
- 대기 장파: Brutsaert (1975)
- 방향성 없음, 그림자 없음

## 기상 입력
- 기온·습도: S-DoT 57개소 → IDW 보간 (power=2) → 링크별 할당
- 일사량(GHI): Open-Meteo archive, 폭염일 7일 평균 (2025.07.28–08.03)
- 분석 시각: 13시 기준

## 파일럿 결과 (성동구, 7개역)
- MRT 범위: 42–63°C (13시 기준)
- MRT ≥ 55°C 링크 비율: 30.1%
- 결과 파일: `results/catchment_mrt_summary.json`

## 풀 SOLWEIG 대비 한계 요약
| 항목 | 풀 SOLWEIG | Method A |
|------|-----------|----------|
| SVF | DSM fisheye 투영 | Oke H/W Canyon 공식 |
| 그림자 | DSM 기반 pixel-level | 없음 |
| 단파복사 | 6방향 개별 계산 | 직달+산란 단순 합산 |
| 장파복사 | 하늘·식생·벽·지면 6방향 | 하늘+벽 SVF 가중 평균 |
| 계산 단위 | 픽셀 (1m×1m) | 링크 중심점 |

근거: Lindberg & Grimmond (2011), Lindberg et al. (2016)
