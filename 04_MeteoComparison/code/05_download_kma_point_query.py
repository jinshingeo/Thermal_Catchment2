"""
KMA 특정지점 다중요소 API — 격자셀 2,300개 x 12일, 1일 1호출 방식
================================================================
전체영역 API(04번 스크립트)는 호출당 28~42MB라 5GB 일일 용량 한도에 걸림.
이 API(1.3 특정지점 다중요소, sfc_nc_var.php)는 호출당 응답이 1KB 미만으로
가벼운 대신, 호출 1번당 최대 약 24시간까지만 조회 가능 — 지점(2,300) x
일자(12일) = 27,600회 필요.

일일 호출 횟수 제약(약 2만건 추정) 회피를 위해 두 API 키로 절반씩 분담.
사용법: python3 05_download_kma_point_query.py {half} {api_key}
  half: 1(격자셀 앞 절반) 또는 2(뒤 절반)
"""
import os
import sys
import time
import urllib.request
import numpy as np
import pandas as pd

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
CACHE = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache')
RAW_DIR = os.path.join(CACHE, 'raw_point')
os.makedirs(RAW_DIR, exist_ok=True)

HALF = int(sys.argv[1])
KEY = sys.argv[2]

DATES = pd.date_range('2025-07-23', '2025-08-03', freq='D')
HOUR_START, HOUR_END = 6, 20  # 06~20시(여유분 포함)

idx = pd.read_csv(os.path.join(CACHE, 'link_to_kma_grid_index.csv'))
cells = idx[['grid_row', 'grid_col', 'grid_lon', 'grid_lat']].drop_duplicates(
    subset=['grid_row', 'grid_col']).reset_index(drop=True)
cells = cells.sort_values(['grid_row', 'grid_col']).reset_index(drop=True)

mid = len(cells) // 2
cells = cells.iloc[:mid] if HALF == 1 else cells.iloc[mid:]
cells = cells.reset_index(drop=True)
print(f"[half {HALF}] 대상 격자셀: {len(cells):,}개, 총 호출 예정 {len(cells)*len(DATES):,}건", flush=True)

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/124.0.0.0 Safari/537.36'),
}


def fetch(lon, lat, tm1, tm2, retries=2):
    url = ('https://apihub.kma.go.kr/api/typ01/url/sfc_nc_var.php'
           f'?tm1={tm1}&tm2={tm2}&lon={lon}&lat={lat}&obs=ta,hm,ws_10m&itv=60&help=0&authKey={KEY}')
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                text = resp.read().decode('utf-8', errors='ignore')
            rows = []
            for line in text.strip().split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = [p.strip() for p in line.split(',')]
                if len(parts) != 4:
                    continue
                tm, ta, hm, ws = parts
                rows.append((tm, float(ta), float(hm), float(ws)))
            return rows
        except Exception as e:
            if attempt == retries:
                print(f"  실패: lon={lon} lat={lat} tm1={tm1} ({e})", flush=True)
                return None
            time.sleep(1)


jobs = [(row.grid_row, row.grid_col, row.grid_lon, row.grid_lat, d)
        for _, row in cells.iterrows() for d in DATES]
total = len(jobs)
todo = [j for j in jobs if not os.path.exists(
    os.path.join(RAW_DIR, f"{j[0]}_{j[1]}_{j[4].strftime('%Y%m%d')}.csv"))]
print(f"[half {HALF}] 전체 {total}건 중 이미 완료 {total-len(todo)}건, 남은 {len(todo)}건", flush=True)

t0 = time.time()
n_done = total - len(todo)
for grid_row, grid_col, lon, lat, d in todo:
    tm1 = f"{d.strftime('%Y%m%d')}{HOUR_START:02d}00"
    tm2 = f"{d.strftime('%Y%m%d')}{HOUR_END:02d}00"
    rows = fetch(lon, lat, tm1, tm2)
    out_path = os.path.join(RAW_DIR, f"{grid_row}_{grid_col}_{d.strftime('%Y%m%d')}.csv")
    if rows is not None:
        pd.DataFrame(rows, columns=['tm', 'ta', 'hm', 'ws_10m']).to_csv(out_path, index=False)
    n_done += 1
    if n_done % 200 == 0:
        elapsed = time.time() - t0
        print(f"[half {HALF}] {n_done}/{total} 완료 ({elapsed:.0f}초 경과)", flush=True)
    if n_done % 2000 == 0:
        print(f"[half {HALF}] {n_done}건마다 30초 휴식...", flush=True)
        time.sleep(30)
    else:
        time.sleep(0.3 + np.random.uniform(0, 0.2))

print(f"[half {HALF}] 완료. 총 소요시간: {time.time()-t0:.0f}초", flush=True)
