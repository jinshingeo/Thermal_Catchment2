"""15m 포함 트레이드오프 데이터 병합 (v2)"""
import pandas as pd

BASE = '/Users/jin/석사논문/Thermal_Catchment/03_Method_C/results/compare_resolution_tradeoff'

timing = pd.read_csv(f'{BASE}/2026-07-29_timing_summary.csv')
timing_15m = pd.DataFrame([{
    'resolution': '15m', 'downsample_sec': 1, 'wallheight_sec': 17, 'svf_sec': 19,
    'solweig_sec': 42, 'utci_sec': 1, 'total_seconds': 80,
    'note': '1mtrue 다운샘플 소스, 단일 실행'
}])
timing2 = pd.concat([timing, timing_15m], ignore_index=True)
timing2.to_csv(f'{BASE}/2026-07-29_timing_summary_v2.csv', index=False)

precision = pd.read_csv(f'{BASE}/2026-07-29_precision_vs_1mtrue_v2.csv')
precision_1m = pd.DataFrame([{
    'resolution': '1m', 'pixel_Tmrt_MAE': 0, 'pixel_Tmrt_r': 1.0, 'pixel_UTCI_MAE': 0,
    'pixel_UTCI_r': 1.0, 'pixel_HardCut38_agree_pct': 100.0, 'link_Tmrt_MAE': 0,
    'link_Tmrt_r': 1.0, 'link_UTCI_MAE': 0, 'link_UTCI_r': 1.0,
    'link_HardCut38_agree_pct': 100.0, 'link_n_disagree': 0, 'link_n_total': None,
}])
precision2 = pd.concat([precision_1m, precision], ignore_index=True)

merged = pd.merge(timing2, precision2, on='resolution', how='left')
order = {'1m': 0, '5m': 1, '10m': 2, '15m': 3, '30m': 4}
merged['sort_key'] = merged['resolution'].map(order)
merged = merged.sort_values('sort_key').drop(columns='sort_key')
merged['res_m'] = merged['resolution'].str.replace('m', '').astype(float)

out = f'{BASE}/2026-07-29_tradeoff_merged_v2.csv'
merged.to_csv(out, index=False)
print(f'저장: {out}')
print(merged[['resolution', 'total_seconds', 'link_HardCut38_agree_pct', 'link_UTCI_r']])
