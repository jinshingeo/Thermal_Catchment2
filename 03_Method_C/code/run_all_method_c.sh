#!/bin/bash
# Method C 파이프라인 전체 실행
# 실행: bash run_all_method_c.sh

export PROJ_LIB="/opt/miniconda3/lib/python3.13/site-packages/pyproj/proj_dir/share/proj"
CODE_DIR="$(dirname "$0")"

echo "======================================"
echo "[Step 1] MRT 링크 집계"
echo "======================================"
python3 "$CODE_DIR/mrt_link_aggregation.py"
if [ $? -ne 0 ]; then
  echo "ERROR: mrt_link_aggregation.py 실패. 중단."
  exit 1
fi

echo ""
echo "======================================"
echo "[Step 2] 응봉역/성수역 Catchment 비교 지도"
echo "======================================"
python3 "$CODE_DIR/catchment_contrast_map.py"
if [ $? -ne 0 ]; then
  echo "ERROR: catchment_contrast_map.py 실패."
  exit 1
fi

echo ""
echo "======================================"
echo "모든 단계 완료"
echo "결과 위치:"
echo "  링크 MRT CSV: /scratchpad/link_mrt_seongdong/link_mrt_method_c.csv"
echo "  GraphML:      /scratchpad/link_mrt_seongdong/"
echo "  지도 PNG:     Thermal_Catchment/03_Method_C/results/"
echo "  요약 CSV:     Thermal_Catchment/03_Method_C/results/2026-07-03_catchment_summary_method_c.csv"
echo "======================================"
