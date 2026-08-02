"""
작성일: 2026-08-02
목적: 서울 열린데이터광장 TbTraficWlkNet API(자치구별 도보 네트워크 공간정보) 전체 다운로드
      - OSM 기반 네트워크의 "차도 포함/직선화" 문제 대안으로 검토
근거논문: 없음 — 서울시 공식 공공데이터(data.seoul.go.kr), TbTraficWlkNet
"""
import os
import time
import re
import requests
import pandas as pd
import geopandas as gpd
from shapely import wkt as shapely_wkt

KEY = "4a5a7148777a63723532546a71414d"
BASE_URL = f"http://openapi.seoul.go.kr:8088/{KEY}/xml/TbTraficWlkNet"
PAGE_SIZE = 1000

OUT_DIR = "/Users/jin/석사논문/Thermal_Catchment/data/network"
OUT_GPKG = os.path.join(OUT_DIR, "2026-08-02_seoul_walk_api_network.gpkg")

FIELDS = [
    "LNKG_ID", "LNKG_WKT", "LNKG_TYPE_CD", "BGNG_LNKG_ID", "END_LNKG_ID",
    "LNKG_LEN", "SGG_NM", "EMD_NM", "EXPN_CAR_RD", "SBWY_NTW", "BRG",
    "TNL", "OVRP", "CRSWK", "PARK", "BLDG",
]

def parse_rows(xml_text):
    rows = re.findall(r"<row>(.*?)</row>", xml_text, re.S)
    total = None
    m = re.search(r"<list_total_count>(\d+)</list_total_count>", xml_text)
    if m:
        total = int(m.group(1))
    records = []
    for r in rows:
        rec = {}
        for f in FIELDS:
            mm = re.search(f"<{f}>(.*?)</{f}>", r, re.S)
            rec[f] = mm.group(1) if mm else None
        records.append(rec)
    return records, total

def main():
    first = requests.get(f"{BASE_URL}/1/5/", timeout=30).text
    _, total = parse_rows(first)
    print(f"전체 건수: {total:,}")

    all_records = []
    start = 1
    while start <= total:
        end = min(start + PAGE_SIZE - 1, total)
        url = f"{BASE_URL}/{start}/{end}/"
        for attempt in range(3):
            try:
                resp = requests.get(url, timeout=30)
                recs, _ = parse_rows(resp.text)
                break
            except Exception as e:
                print(f"  재시도 {attempt+1} ({start}-{end}): {e}")
                time.sleep(2)
        else:
            print(f"  실패, 스킵: {start}-{end}")
            recs = []
        all_records.extend(recs)
        if start // PAGE_SIZE % 20 == 0:
            print(f"  진행: {start:,}/{total:,} ({len(all_records):,}건 누적)")
        start = end + 1

    print(f"다운로드 완료: {len(all_records):,}건")
    df = pd.DataFrame(all_records)
    df = df.dropna(subset=["LNKG_WKT"])
    df["geometry"] = df["LNKG_WKT"].apply(shapely_wkt.loads)
    gdf = gpd.GeoDataFrame(df.drop(columns=["LNKG_WKT"]), geometry="geometry", crs=4326)
    gdf.to_file(OUT_GPKG, driver="GPKG")
    print(f"저장: {OUT_GPKG}")

    print("\nLNKG_TYPE_CD 분포:")
    print(gdf["LNKG_TYPE_CD"].value_counts())
    print("\nEXPN_CAR_RD 분포:", gdf["EXPN_CAR_RD"].value_counts().to_dict())
    print("SGG_NM 개수:", gdf["SGG_NM"].nunique())

if __name__ == "__main__":
    main()
