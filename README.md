# Thermal Catchment Area

**열노출을 반영한 보행 환경 접근성 공간 단위 제안**

> 석사 논문 연구 | 서울특별시 | 경희대학교 기후사회과학융합학과

---

## 연구 개요

보행 네트워크에서 열환경 임계값 초과 링크를 제거했을 때 실질적으로 접근 가능한 공간 범위가 어떻게 변화하는가를 분석하여, **Thermal Catchment Area**를 새로운 보행 환경 접근성 공간 단위로 제안한다.

---

## 연구 구성

### 축 1 — MRT 산출 방식 비교
| 방법 | 내용 |
|------|------|
| Baseline | UTCI 직접 사용 (선행연구 재현) |
| A | 약식 MRT (Oke 1987 H/W Canyon SVF) |
| B | DSM 없이 SOLWEIG 약식 |
| C | 오픈소스 30m DSM + SOLWEIG |

### 축 2 — 링크 단위 기상 입력 비교
단일값 / IDW / 크리깅

---

## 폴더 구조

```
Thermal_Catchment/
├── 00_Baseline_UTCI/
├── 01_Method_A/
├── 02_Method_B/
├── 03_Method_C/
├── 04_MeteoComparison/
├── references/          # 선행연구 마스터 목록
└── writing/             # 논문 초안
```

---

*Note: `archive/`, `data/` 폴더는 .gitignore 처리 (대용량 데이터)*
