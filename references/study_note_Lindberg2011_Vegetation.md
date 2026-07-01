# Lindberg & Grimmond (2011) — SOLWEIG 2.0: 식생 스킴 추가

작성일: 2026-07-01  
버전: v1.0  
근거논문: Lindberg, F., & Grimmond, C. S. B. (2011). The influence of vegetation and building morphology on shadow patterns and mean radiant temperatures in urban areas: model development and evaluation. *Theoretical and Applied Climatology*, 105, 311–323. DOI: 10.1007/s00704-010-0382-8

---

## 1. 논문 기본 정보

- **저자**: Fredrik Lindberg, C. S. B. Grimmond (University of Gothenburg / King's College London)
- **저널**: Theoretical and Applied Climatology (2011) 105:311–323
- **DOI**: 10.1007/s00704-010-0382-8
- **핵심 기여**: SOLWEIG 1.0(Lindberg2008) → **SOLWEIG 2.0**: 식생(vegetation) 스킴 추가

---

## 2. SOLWEIG 2.0 개선 사항

기존 SOLWEIG 1.0 대비 신규 추가:
1. **식생 스킴** — 독립적인 식생 DEM 2종 (canopy DEM + trunk zone DEM)
2. **Ground view factor (Ψ_ground)** 추가 — outgoing longwave radiation 개선
3. Nocturnal longwave radiation 추정 (Offerle et al., 2003 기반)
4. Diffuse & direct shortwave radiation 모델링 개선
5. 장파 복사의 방향성(anisotropic) 추정 개선

---

## 3. 식생 스킴 (Vegetation Scheme)

### 3.1 식생 DEM 2종 (Fig.2)

```
Canopy DEM: 캐노피(수관) 높이 래스터
Trunk zone DEM: 수간부(줄기 공간) 높이 래스터
```

- 수목 3D 형태: 원뿔형(침엽수) 또는 구형(활엽수)
- 수목·관목 처리: 투명 장애물 (바람·복사 투과)
- 복사 투과율(τ) 기본값: **0.20** (Oke 1987, Robitu et al. 2006)

### 3.2 식생 그림자 계산 알고리즘 (Fig.4)

Shadow volume 방법:
1. 캐노피 DEM을 태양 방위각으로 이동
2. 각 이동마다 태양 고도각에 맞게 높이 감소
3. 최대값을 취해 shadow volume 빌드
4. Shadow volume과 원본 DEM 비교 → boolean 그림자 맵

**Trunk zone 처리**: 저태양고도에서 수간부 그림자 중요 (Fig.5)

### 3.3 식생 복사 플럭스 계산 (Eq.3, 상향 단파)

$$K_{\downarrow} = I[S_b - (1-S_v)(1-\tau)]\sin\eta + D[\Psi_{sky,b} - (1-\Psi_{sky,v})(1-\tau)] + G\alpha[1 - (\Psi_{sky,b} - (1-\Psi_{sky,v})(1-\tau))](1-f_s)$$

- S_b: 건물 그림자 (Boolean), S_v: 식생 그림자 (Boolean)
- τ: 단파 복사 투과율 (기본값 0.20)
- Ψ_sky_b: 건물에 의한 SVF, Ψ_sky_v: 식생에 의한 SVF

---

## 4. 검증 결과 — 논문 직접 확인 수치

### 4.1 전체 검증 (n=205, 6개 사이트)

- **R² = 0.91** (p<0.01)
- **RMSE = 3.1 K**
- 회귀식: y = 1.021x − 1.170

(SOLWEIG 1.0 대비 개선: RMSE 8.63→6.79°C, v1.0→v2.0)

### 4.2 식생 스킴 효과

τ=0.20 (기본값) 적용 시:
- 관측 대비 개선, 그러나 T_mrt 여전히 약 11°C 과대평가 (식생 그늘 아래)
- MAE = 5.5°C

τ=0.05 적용 시:
- MAE 감소: 5.5°C → **2.74°C** (추가 0.4°C)

**→ 권장값**: τ = **0.05** (완전히 잎 달린 단독 수목에서)

### 4.3 사이트별 SVF 범위

| SVF 범위 | 사이트 |
|---------|--------|
| 0.91 | 개방 공간 (Göteborg) |
| 0.65 | 중간 (Göteborg) |
| 0.50 | 반폐쇄 (Kassel) |
| 0.63+ | KLIMES (Freiburg) |

---

## 5. SOLWEIG 파라미터 확인 (Eq.1, p.312)

$$R = \xi_k \sum_{i=1}^{6} K_i F_i + \varepsilon_p \sum_{i=1}^{6} L_i F_i$$

- F_i = **0.22** (동서남북), **0.06** (위아래) — Fanger 1970, VDI 1994
- ξ_k = **0.70** (단파 흡수계수)
- ε_p = **0.97** (인체 방사율)
- 수목 알베도: **0.15**, 방사율: **0.90**
- 수목 단파 투과율(τ): 기본 0.20 → 권장 **0.05** (여름, 완전한 잎)

---

## 6. 식생의 T_mrt 영향 공간 패턴 (Fig.12)

논문의 흥미로운 결과:
- 수관 바로 아래: T_mrt 상대적으로 **높음** (하늘 대신 상온 수관이 장파 복사 방출)
- 수관 아래가 열스트레스 지점은 아님 (PET 등으로 판단 필요)

---

## 7. SOLWEIG 2.0 vs 1.0 비교

| 항목 | SOLWEIG 1.0 (2008) | SOLWEIG 2.0 (2011) |
|------|-------------------|-------------------|
| 식생 처리 | 없음 | 캐노피+수간 DEM |
| Ground view factor | 없음 | 포함 |
| 검증 R² | 0.94 | 0.91 |
| 검증 RMSE | 4.8K | 3.1K (전체) |
| 식생 투과율 τ | - | 0.05 (권장) |

---

## 8. 우리 연구와의 관련성

### 8.1 SOLWEIG 버전 선택

우리 방법 C에서 SOLWEIG 사용 시:
- SOLWEIG 2.0 이상 사용 → 식생 효과 포함 가능
- 서울 도시 링크 분석에서 가로수는 T_mrt에 중요한 영향
- 그러나 GLO-30 DSM(30m)은 캐노피 DEM 분리 어려움 → 버전별 입력 데이터 제약 명시 필요

### 8.2 식생 투과율 τ=0.05 사용 근거

실제 가로수 시뮬레이션 시 τ=0.05 권장 (여름 잎이 달린 경우).  
τ 과대 설정 시 T_mrt 과대평가.

**⚠️ 주의**: 우리 GLO-30 DSM 30m 해상도에서는 개별 수목 구분 불가.  
식생 DEM 미포함 또는 별도 CDSM(Canopy DSM) 필요 → 한계로 명시.

### 8.3 검증 R²=0.91, RMSE=3.1K

우리 방법 C 한계 기술 시 선행연구 검증 수치로 인용 가능.

**인용 가능 문구**:
> "Lindberg & Grimmond(2011)는 SOLWEIG 2.0에 식생 스킴을 추가하여 R²=0.91, RMSE=3.1K의 검증 성능을 보고하였으며, 완전히 잎이 달린 수목의 단파 복사 투과율(τ)은 0.05를 권장하였다."

---

## 9. 논문에서 확인된 핵심 수치 정리

| 항목 | 값 | 출처 |
|------|-----|------|
| 검증 R² | 0.91 (p<0.01) | p.311 Abstract |
| 검증 RMSE | 3.1K | p.311 Abstract |
| 식생 단파 투과율 τ (기본) | 0.20 | Eq.3, p.313 |
| 식생 단파 투과율 τ (권장, 여름) | **0.05** | p.320 |
| τ=0.05 시 MAE | 2.74°C | p.319 |
| 수목 알베도 | 0.15 | p.312 |
| 수목 방사율 | 0.90 | p.312 |
| F_i (방위) | 0.22 | Eq.1, p.312 |
| F_i (상하) | 0.06 | Eq.1, p.312 |

---

## 10. 핵심 인용 형식

```
Lindberg, F., & Grimmond, C. S. B. (2011). 
The influence of vegetation and building morphology on shadow patterns 
and mean radiant temperatures in urban areas: model development and evaluation. 
Theoretical and Applied Climatology, 105, 311–323.
https://doi.org/10.1007/s00704-010-0382-8
```
