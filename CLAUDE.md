# 프로젝트 CLAUDE.md — Thermal Catchment Area 연구
> 최종 수정: 2026-07-01

## 연구 개요
- **핵심 제안**: Thermal Catchment Area — 열노출을 반영한 보행 환경 접근성 공간 단위 제안
- **핵심 아이디어**: 보행 네트워크에서 열환경 임계값 초과 링크를 제거(Hard Cut)했을 때 실질적으로 접근 가능한 공간 범위가 어떻게 변화하는가
- **연구 지역**: 서울특별시 전체 (성동구는 파일럿 스터디 지역 — 방법론 검증 완료 후 서울 전역 확장)
- **시설 검증 대상**: 지하철역·버스 정류장 등은 접근성 감소를 수치화하기 위한 검증 수단이며 연구의 주제가 아님

## 타임라인 (절대 준수)
- **2026-08-xx**: SCI 투고 완료
- **2026-09-15**: 석사논문 원고 제출
- **2026-09-말**: 중간발표

## 연구의 두 축 (방법론 기여)

### 축 1 — MRT 산출 방식 비교 (3가지)
| ID | 방법 | 핵심 내용 | 데이터 요구 |
|----|------|----------|-----------|
| A | 약식 MRT (Oke H/W Canyon SVF) | OSM 네트워크 + 건물 SHP만 사용 | 최소 |
| B | 합성 DSM + SOLWEIG | 건물 폴리곤+층수 → UMEP 합성 DSM | 중간 |
| C | 오픈소스 30m DSM + SOLWEIG | 오픈소스 DSM 활용 | 중간 |

비교 목적: 서울 도보 링크 평가에서 데이터 비용 대비 어떤 MRT 산출 방식이 적합한가 실증적으로 제안

### 축 2 — 링크 단위 기상 입력 방식 비교 (미확정, 전체 검토 중)
| 방식 | 내용 |
|------|------|
| 단일값 | 단일 기상관측소 대표값 |
| IDW | 복수 S-DoT 센서 역거리가중 보간 |
| MQ | Modified Quadratic 보간 |
| 크리깅 | 공간 자기상관 반영 보간 |

기여 포인트: 링크 단위 보행 분석에서 기상 입력을 어떻게 처리할 것인가 (기후학이 아닌 보행 분석 목적)
축 2는 메인 연구는 아니나, 방법론 신뢰성 확보를 위해 병행 수행

## 핵심 파라미터 (확정)
- **WALK_SPEED** = 4.5 km/h
- **TIME_BUDGET** = 15분 (→ 반경 약 1,125m)
- **HARD_CUT 기준**: UTCI ≥38°C (Bröde et al., 2012 — Very Strong Heat Stress 하한)
- **MRT 선택 근거**: 파일럿(성동구)에서 폭염 조건 적용 시 전체 링크의 **98.9%**가 UTCI 38°C 이상 구간 집중 → 링크 단위 공간 분화 불가 → MRT 채택

## 분석 날짜 및 시각 (⚠️ 두 방식 모두 미확정 — 초안 단계)
- **방식 1**: 2025년 7월 28일–8월 3일 폭염일 7일 평균 × **13시** 단일 시각
  - 13시 후보 근거: 태양 남중 직후 = 단파 복사 최대 = MRT 피크 시간대
  - 이 방식은 파일럿 초안에서 사용된 것이며, 확정 아님
- **방식 2 (추가)**: 2025년 폭염일 중 맑은 날 하루 × **시간대별(일출~일몰)**
  - Wolf et al.(2025) diurnal profile 분석 방식 참고 (08:00~17:00)
  - 시간대별 Thermal Catchment Area 변화 패턴 파악 목적

## 검증 지표
- **[검증 지표명 미확정]**: (Classic Catchment − Thermal Catchment) / Classic Catchment × 100
- **TARR** 표현 사용 금지 — 확정 전까지 "[검증 지표]" 또는 "감소율(%)"로 표기

## 선행연구 핵심 수치 (서론·방법론 인용용)

### Hard Cut 행동 근거
- **Melnikov et al. (2022)**: 그늘 경로 이동 비용이 햇볕 경로의 **0.86** 수준 (abstract); β̄=1.16 — 햇볕 100m를 그늘 116m로 인식 (Discussion)
- **Azegami et al. (2023)**: 보행자 **28.2%**가 최단경로보다 그늘 경로 우선 선택; 일부는 신호 대기까지 감수

### 소프트 패널티 선행연구 (우리와 차별화 대상)
- **Basu et al. (2024)**: UTCI 1°C 증가 → 인지 보행거리 **80.8m** 증가 (소프트 패널티)
- **Jia et al. (2022)**: Strong heat stress 조건(PET>32°C)에서 보행속도 **10~20%** 감소
- **Aydin et al. (2026)**: PTT(인지이동시간) 방식 소프트 패널티, 싱가포르

### 접근성 이론
- **Geurs & van Wee (2004)**: location-based contour measure — 우리 TCA의 이론적 위치
- **Bröde et al. (2012)**: UTCI ≥38°C = Very Strong Heat Stress (Table 3, p.489)

### MRT/SOLWEIG 방법론 선례
- **Buo et al. (2026)**: SOLWEIG 1m + Dijkstra MRT 임피던스 라우팅, 검증 d=0.73 / MAE=6.2°C
- **Basu et al. (2024)**: SOLWEIG + LiDAR DSM + ERA5 → UTCI 파이프라인 (보스턴)
- **Wolf et al. (2025)**: OSM 네트워크 + 건물 그늘 → CoolWalkability diurnal profile (08:00~17:00)

## 완독 선행연구 9편 목록
| 논문 | 역할 |
|------|------|
| Geurs & van Wee (2004) | 접근성 contour measure 이론 위치 |
| Melnikov et al. (2022) | Hard Cut 행동 근거 (0.86) |
| Azegami et al. (2023) | Hard Cut 행동 근거 (28.2%) |
| Jia et al. (2022) | 소프트 패널티 선례, 13시 근거, SOLWEIG 방법론 |
| Basu et al. (2024) | 소프트 패널티 선례, walkshed 감소 프레임 |
| Aydin et al. (2026) | 소프트 패널티 선례, PTT 방식 |
| Wolf et al. (2025) | CoolWalkability diurnal profile, OSM 활용 선례 |
| Dong et al. (2024) | 접근성 기반 열환경 평가, NDVI/NDBI 변수 |
| Buo et al. (2026) | MRT 임피던스 라우팅, SOLWEIG 1m 검증 |

스터디노트: `references/study_note_*.md`
이슈 매핑: `references/study_note_이슈매핑_해결방안.md`

## 폴더 구조
```
Thermal_Catchment/
├── CLAUDE.md
├── README.md
├── references/
│   ├── all_papers/          ← 선행연구 PDF
│   ├── study_note_*.md      ← 논문별 스터디노트 (9편 완독)
│   └── reference_list.csv   ← EndNote 연동 마스터 목록
├── 01_Method_A/             ← 약식 MRT (H/W Canyon SVF)
├── 02_Method_B/             ← 합성 DSM + SOLWEIG
├── 03_Method_C/             ← 30m DSM + SOLWEIG
├── 04_MeteoComparison/      ← 기상 입력 방식 비교
├── archive/                 ← 파일럿(성동구) 코드 보존 — 수정·참조 금지
├── writing/                 ← 논문 초안 (YYYY-MM-DD_섹션명_vN.md)
├── data/                    ← 원본 데이터
└── figures/                 ← 최종 출력 그림
```

## 선행연구 관리 규칙 (절대 원칙)
- 모든 수치·수식·방법론에는 SCI 논문 인용 필수
- 인용 없는 수치는 코드에도, 글에도 쓰지 않음
- Claude가 수치를 제안할 때: 반드시 "저자 연도, 논문 제목, DOI" 명시 — 추정 금지
- 확인되지 않은 경우 반드시 **"⚠️ 근거 논문 미확보 — 서치 필요"** 로 표시
- `references/reference_list.csv`: EndNote 가져오기용 마스터 목록 유지

## 버전 관리 규칙
- 파일럿(성동구) 코드는 `archive/pilot_seongdong/`에 보존 — **절대 수정·참조 금지**
- 새 코드는 방법별 폴더 `code/`에서 독립 관리
- 결과 파일 명명: `results/YYYY-MM-DD_설명.csv`
- md 파일 상단 필수 항목: `작성일`, `버전`, `근거논문`
- Git 커밋 시 대용량 데이터 파일 포함 금지

## 글쓰기 원칙
- 분석과 글 작성 **동시 진행** — 분석 완료 후 글쓰기 시작 금지
- 수정이 적은 섹션부터 초안 작성: Introduction → Study Area → Related Work → Methods
- 모든 초안 파일: `writing/YYYY-MM-DD_섹션명_vN.md`
- 글에 인용된 선행연구는 `reference_list.csv`에 즉시 추가

## 세션 시작 프로토콜
사용자가 **"오늘 시작"** 또는 **"/브리핑"** 입력 시:
memory 파일과 최근 변경 파일을 확인하고 아래 형식으로 응답:

> **[날짜] 연구 현황 브리핑**
> - 마지막 작업: [날짜 / 내용 / 결과]
> - 현재 부족한 점 또는 미완료 사항
> - 오늘 권장 작업 + 목표 완료선 (타임라인 기준)

## 용어 사용 규칙
- **Thermal Catchment Area (TCA)**: 이 연구에서 제안하는 핵심 용어
- **TAVI**: 사용 금지 (구 파일럿 연구의 잔재)
- **TARR**: 사용 금지 — 확정 전까지 "[검증 지표]" 또는 "감소율(%)"로 표기
- **Hard Cut**: 열환경 임계값(UTCI ≥38°C) 초과 링크를 네트워크에서 완전 제거하는 방식

## 절대 하지 말 것
- 출처 없는 수치 인용 또는 생성
- archive/ 내 구 코드 참조해 새 코드 작성
- 대용량 데이터 파일 Git 커밋
- 검증 안 된 방법을 확정된 것처럼 기술
- 기존 결과 파일 덮어쓰기 (날짜 포함 새 파일명으로 저장)
- "대중교통 접근성"을 연구의 주제로 표현 (검증 수단임)
- 성동구를 주요 연구 지역으로 표현 (파일럿 지역임)
- TARR 용어 사용 (미확정)
