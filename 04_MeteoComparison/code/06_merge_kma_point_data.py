"""
KMA 특정지점 다운로드 결과 병합 — 격자셀 x 시각별 12일 평균
================================================================
raw_point/{grid_row}_{grid_col}_{YYYYMMDD}.csv 27,600개를 합쳐
격자셀(2,300개) x 시각(06~19시) 단위 12일 평균 기온·습도·풍속을 산출.
"""
import os
import glob
import pandas as pd

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
CACHE = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache')
RAW_DIR = os.path.join(CACHE, 'raw_point')
HOURS = list(range(6, 20))  # 06~19시(다운로드는 20시까지 여유있게 받았음, 여기서 트림)

files = glob.glob(os.path.join(RAW_DIR, '*.csv'))
print(f"파일 {len(files):,}개 로드 중...")

frames = []
for f in files:
    base = os.path.basename(f).replace('.csv', '')
    grid_row, grid_col, _ = base.split('_')
    df = pd.read_csv(f)
    df['grid_row'] = int(float(grid_row))
    df['grid_col'] = int(float(grid_col))
    frames.append(df)

all_df = pd.concat(frames, ignore_index=True)
all_df['tm'] = pd.to_datetime(all_df['tm'], format='%Y%m%d%H%M')
all_df['hour'] = all_df['tm'].dt.hour
all_df = all_df[all_df['hour'].isin(HOURS)]
print(f"필터 후 행 수: {len(all_df):,}")

agg = all_df.groupby(['grid_row', 'grid_col', 'hour'])[['ta', 'hm', 'ws_10m']].mean().reset_index()
agg = agg.round(2)
print(f"격자셀x시각 조합: {len(agg):,} (기대값: 2300*14={2300*14})")

out_path = os.path.join(CACHE, 'kma_grid_met_12day_avg.csv')
agg.to_csv(out_path, index=False, encoding='utf-8-sig')
print(f"저장: {out_path}")

# 결측 확인
n_cells = agg[['grid_row', 'grid_col']].drop_duplicates().shape[0]
print(f"고유 격자셀 수: {n_cells} (기대값: 2300)")
missing = agg.groupby(['grid_row', 'grid_col']).size()
incomplete = missing[missing < 14]
print(f"14시간 미만 격자셀: {len(incomplete)}개")
