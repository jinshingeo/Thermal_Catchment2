"""
[파일럿/미확정] 서울 전체 — 링크별 UTCI 산출
================================================================
이미 계산된 링크별 Tmrt(17번 산출물)에 시간대별 met.txt 단일값(Ta/RH/풍속)을
그대로 적용해 UTCI로 변환 — 라스터 zonal_stats 재계산 없이 즉시 산출 가능
(Ta/RH/풍속이 공간적으로 균일한 단일값이라, Tmrt->UTCI 변환은 링크 단위로
사후 적용해도 라스터 단위 계산과 동일함).
"""
import os
import time
import numpy as np
import pandas as pd
import geopandas as gpd
from pythermalcomfort.models import utci

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
GPKG_IN = os.path.join(PROJ, '03_Method_C', 'results', '2026-07-16_link_tmrt_seoul_5m.gpkg')
MET_CSV = os.path.join(PROJ, '04_MeteoComparison', 'results', 'seoul_met_profile_06_19h.csv')
OUT_DIR = os.path.join(PROJ, '03_Method_C', 'results')

met = pd.read_csv(MET_CSV).set_index('hour')

t0 = time.time()
print("링크 Tmrt 로드 중...")
gdf = gpd.read_file(GPKG_IN)
hours = list(range(6, 20))

for h in hours:
    Ta, RH, wind = met.loc[h, 'Ta'], met.loc[h, 'RH'], met.loc[h, 'wind']
    tmrt_vals = gdf[f'Tmrt_{h:02d}'].values
    result = utci(tdb=Ta, tr=tmrt_vals.tolist(), v=wind, rh=RH,
                  limit_inputs=False, round_output=False)
    gdf[f'UTCI_{h:02d}'] = np.array(result.utci)
    print(f"  {h:02d}시 완료 (Ta={Ta}, RH={RH}, wind={wind})")

gpkg_out = os.path.join(OUT_DIR, '2026-07-16_link_utci_seoul_5m_PILOT.gpkg')
gdf.to_file(gpkg_out, driver='GPKG')
print(f"저장: {gpkg_out}")

csv_out = os.path.join(OUT_DIR, '2026-07-16_link_utci_seoul_5m_PILOT.csv')
gdf.drop(columns='geometry').to_csv(csv_out, index=False, encoding='utf-8-sig')
print(f"저장: {csv_out}")
print(f"총 소요시간: {time.time()-t0:.1f}초")
