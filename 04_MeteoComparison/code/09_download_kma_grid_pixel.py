"""
KMA 융합기상 500m 격자 다운로드 — 서울 Tmrt 래스터 전체 도메인 대응 격자셀
================================================================
04_download_kma_grid_seoul.py(링크 대응 2,300셀)의 픽셀 버전. 08번 스크립트가
만든 pixel_to_kma_grid_cells.csv(4,403셀, 기존 2,300셀 전부 포함)를 사용.
폭염일 12일 x 06~19시 x {ta,hm,ws_10m} = 504회 API 호출. 로직은 04번과 동일
(재개 가능, (obs,tm) 단위 개별 저장, 지터·휴식 포함).

출력: 04_MeteoComparison/data/kma_grid_cache/raw_pixel/{obs}_{tm}.npy (개별)
      04_MeteoComparison/data/kma_grid_cache/pixel_{obs}_wide.csv (병합)
      04_MeteoComparison/data/kma_grid_cache/pixel_kma_grid_met_12day_avg.csv (12일 평균)
"""
import os
import time
import urllib.request
import numpy as np
import pandas as pd

PROJ = os.environ.get('THERMAL_PROJ_DIR', '/Users/jin/석사논문/Thermal_Catchment')
CACHE = os.path.join(PROJ, '04_MeteoComparison', 'data', 'kma_grid_cache')
RAW_DIR = os.path.join(CACHE, 'raw_pixel')
os.makedirs(RAW_DIR, exist_ok=True)
KEY = os.environ['KMA_API_KEY']

DATES = pd.date_range('2025-07-23', '2025-08-03', freq='D')
HOURS = range(6, 20)
OBS_LIST = ['ta', 'hm', 'ws_10m']

cells = pd.read_csv(os.path.join(CACHE, 'pixel_to_kma_grid_cells.csv'))
rows_arr, cols_arr = cells['grid_row'].values, cells['grid_col'].values
print(f"대상 격자셀: {len(cells):,}개", flush=True)


def load_grid(text):
    lines = text.strip().split('\n')
    nrow, ncol = int(lines[0].split(',')[0]), int(lines[0].split(',')[1])
    vals = []
    for line in lines[1:]:
        row = [float(x) for x in line.strip().rstrip(',').split(',') if x]
        vals.extend(row)
    return np.array(vals, dtype=np.float64).reshape(nrow, ncol)


HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/124.0.0.0 Safari/537.36'),
}


def fetch(obs, tm, retries=2):
    url = (f'https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-sfc_obs_nc_api'
           f'?obs={obs}&tm={tm}&disp=A&authKey={KEY}')
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode('utf-8')
            arr = load_grid(text)
            return arr[rows_arr, cols_arr]
        except Exception as e:
            if attempt == retries:
                print(f"  실패: obs={obs} tm={tm} ({e})", flush=True)
                return None
            time.sleep(2)


jobs = []
for d in DATES:
    for h in HOURS:
        tm = f"{d.strftime('%Y%m%d')}{h:02d}00"
        for obs in OBS_LIST:
            jobs.append((obs, tm))

total = len(jobs)
todo = [(obs, tm) for obs, tm in jobs
        if not os.path.exists(os.path.join(RAW_DIR, f'{obs}_{tm}.npy'))]
print(f"전체 {total}건 중 이미 완료 {total - len(todo)}건, 남은 {len(todo)}건", flush=True)

t0 = time.time()
n_done = total - len(todo)
for obs, tm in todo:
    vals = fetch(obs, tm)
    if vals is not None:
        np.save(os.path.join(RAW_DIR, f'{obs}_{tm}.npy'), vals)
    n_done += 1
    if n_done % 10 == 0:
        elapsed = time.time() - t0
        print(f"  {n_done}/{total} 완료 ({elapsed:.0f}초 경과)", flush=True)
    if n_done % 100 == 0:
        print(f"  {n_done}건마다 60초 휴식...", flush=True)
        time.sleep(60)
    else:
        time.sleep(2 + np.random.uniform(0, 1))

# ── 병합 ────────────────────────────────────────────────────────────
wide = {}
for obs in OBS_LIST:
    df = cells.copy()
    for d in DATES:
        for h in HOURS:
            tm = f"{d.strftime('%Y%m%d')}{h:02d}00"
            path = os.path.join(RAW_DIR, f'{obs}_{tm}.npy')
            df[tm] = np.load(path) if os.path.exists(path) else np.nan
    out_path = os.path.join(CACHE, f'pixel_{obs}_wide.csv')
    df.to_csv(out_path, index=False)
    n_missing = df.filter(regex=r'^\d{12}$').isna().all(axis=0).sum()
    print(f"저장: {out_path} ({df.shape}, 결측 시각 {n_missing}개)", flush=True)
    wide[obs] = df

# ── 12일 평균(06~19시) — 03/07번 스크립트가 쓰는 kma_grid_met_12day_avg.csv 형식과 동일 ──
records = []
for h in HOURS:
    tm_cols = [f"{d.strftime('%Y%m%d')}{h:02d}00" for d in DATES]
    part = pd.DataFrame({
        'grid_row': cells['grid_row'],
        'grid_col': cells['grid_col'],
        'hour': h,
        'ta': wide['ta'][tm_cols].mean(axis=1),
        'hm': wide['hm'][tm_cols].mean(axis=1),
        'ws_10m': wide['ws_10m'][tm_cols].mean(axis=1),
    })
    records.append(part)
avg_df = pd.concat(records, ignore_index=True)
avg_out = os.path.join(CACHE, 'pixel_kma_grid_met_12day_avg.csv')
avg_df.to_csv(avg_out, index=False)
print(f"저장: {avg_out} ({avg_df.shape})")

print(f"총 소요시간: {time.time()-t0:.0f}초", flush=True)
