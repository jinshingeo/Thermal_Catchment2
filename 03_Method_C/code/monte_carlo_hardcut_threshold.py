"""
Hard Cut 임계값 Monte Carlo 산출
근거논문: Huang et al.(2026), Thorsson et al.(2014)
met/clo: Huang et al.(2026) Table 1 (p.5) 실측치
SD: 문헌 미확보 → 가정 + 민감도 분석 (본 스크립트의 핵심 설계)
"""
import numpy as np
import pandas as pd
from pythermalcomfort.models import pet_steady, utci
from scipy.optimize import brentq

# 성동구 13시 기상조건 (기존 파이프라인)
Ta, RH, V = 35.77, 52.56, 1.8

# ---------- 1. Huang et al.(2026) 경로: PET 임계값 -> UTCI 환산 ----------
# met: 100 W/m^2 "Walking about"(최빈활동, 각 코호트 68~81%) / 58.2 = 1.718 met
# clo: 코호트별 평균 (Table 1, p.5)
MET = 100 / 58.2
huang_cohorts = {
    "60-69": {"pet": 37.48, "clo": 0.32, "age": 65},
    "70-79": {"pet": 39.87, "clo": 0.31, "age": 75},
    "80+":   {"pet": 39.55, "clo": 0.33, "age": 85},
}

def pet_at_tr(tr, clo, age):
    return pet_steady(tdb=Ta, tr=tr, v=V, rh=RH, met=MET, clo=clo,
                       position="standing", age=age).pet

rows = []
for name, c in huang_cohorts.items():
    f = lambda tr: pet_at_tr(tr, c["clo"], c["age"]) - c["pet"]
    tr_sol = brentq(f, Ta, 80.0, xtol=1e-3)
    u = utci(tdb=Ta, tr=tr_sol, v=V, rh=RH).utci
    rows.append({"source": "Huang2026", "age_group": name, "utci_mean": u})

# ---------- 2. Thorsson et al.(2014) 경로: Tmrt 임계값 -> UTCI 환산 (Table 4, p.339) ----------
# "위험 증가 시작"(>=0% risk increase) 임계값만 사용 (5%/10%는 민감도 비교용으로 별도 표기)
thorsson_onset = {
    "45-79": 46.7,
    "80+": 47.6,
}
for name, tr in thorsson_onset.items():
    u = utci(tdb=Ta, tr=tr, v=V, rh=RH).utci
    rows.append({"source": "Thorsson2014", "age_group": name, "utci_mean": u})

df = pd.DataFrame(rows)
df.to_csv("/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/2026-07-29_age_threshold_means.csv", index=False)
print(df.to_string(index=False))
