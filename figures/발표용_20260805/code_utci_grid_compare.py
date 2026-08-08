"""
UTCI 기존 vs 신규 06~19시 그리드 비교 — 서울/성동구 각 1장으로 합성
기존에 렌더링된 낱장 PNG(utci_old/new_{region}_{h}h.png)를 재사용해 조합만 함
"""
import os
from PIL import Image, ImageDraw, ImageFont

PROJ = '/Users/jin/석사논문/Thermal_Catchment'
SRC_DIR = os.path.join(PROJ, 'figures', '발표용_20260805', '2d', 'utci_compare')
LEGEND_PATH = os.path.join(PROJ, 'figures', '발표용_20260805', 'legends', 'legend_utci_allhours_compare.png')
OUT_DIR = os.path.join(PROJ, 'figures', '발표용_20260805', '2d')

HOURS = list(range(6, 20))
CELL = 260  # 각 타일 리사이즈 크기(정사각)
LABEL_H = 40
ROW_LABEL_W = 90
LEGEND_W = 160

try:
    font = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 22)
    font_small = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 18)
except Exception:
    font = ImageFont.load_default()
    font_small = font


def load_resized(path, size):
    img = Image.open(path).convert('RGBA')
    img.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    ox = (size - img.width) // 2
    oy = (size - img.height) // 2
    canvas.paste(img, (ox, oy), img)
    return canvas


def build_grid(region):
    n_hours = len(HOURS)
    W = ROW_LABEL_W + n_hours * CELL + LEGEND_W
    H = LABEL_H + 2 * CELL
    canvas = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    for j, h in enumerate(HOURS):
        x = ROW_LABEL_W + j * CELL
        draw.text((x + CELL // 2, LABEL_H // 2), f'{h:02d}시', font=font_small,
                   fill='black', anchor='mm')

    for i, ver in enumerate(['old', 'new']):
        y = LABEL_H + i * CELL
        label = '기존\n(단일값)' if ver == 'old' else '신규\n(KMA격자)'
        draw.multiline_text((ROW_LABEL_W // 2, y + CELL // 2), label, font=font_small,
                             fill='black', anchor='mm', align='center')
        for j, h in enumerate(HOURS):
            x = ROW_LABEL_W + j * CELL
            tile_path = os.path.join(SRC_DIR, f'utci_{ver}_{region}_{h:02d}h.png')
            tile = load_resized(tile_path, CELL)
            canvas.paste(tile, (x, y), tile)

    legend = Image.open(LEGEND_PATH).convert('RGBA')
    legend.thumbnail((LEGEND_W - 20, H - 20), Image.LANCZOS)
    canvas.paste(legend, (W - LEGEND_W + 10, (H - legend.height) // 2), legend)

    out_path = os.path.join(OUT_DIR, f'utci_grid_compare_{region}.png')
    canvas.convert('RGB').save(out_path, dpi=(150, 150))
    print('저장:', out_path)


build_grid('seoul')
build_grid('seongdong')
