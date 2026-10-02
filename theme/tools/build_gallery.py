#!/usr/bin/env python3
"""Build the iClassic Galleria menu artwork from locally owned cover images.

This recreates the same Rockbox skin technique used on the author's Y1:
clock-gated 10-second slots, pre-rendered 16-frame crossfades and a small
horizontal drift. It never reads or modifies music files or Rockbox firmware.
"""

from __future__ import annotations

import argparse
import random
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat

HERE = Path(__file__).resolve().parent
SKIN_DIR = "iClassic_Galleria"
FRAME_COUNT = 16
PANEL_SIZE = (264, 360)
VISIBLE_WIDTH = 240
CANVAS_COLOR = "#101923"
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def fit_text(draw: ImageDraw.ImageDraw, words: str, width: int, size: int, bold: bool = False) -> tuple[str, ImageFont.ImageFont]:
    fnt = font(size, bold)
    value = words.strip()
    while value and draw.textbbox((0, 0), value, font=fnt)[2] > width:
        value = value[:-1].rstrip()
    if value != words.strip() and len(value) > 1:
        value = value[:-1].rstrip() + "…"
    return value, fnt


def metadata(path: Path) -> tuple[str, str, str]:
    # Preferred: Artist - Album - 2025.jpg. Year is optional.
    parts = [p.strip() for p in path.stem.split(" - ")]
    if len(parts) >= 2:
        artist, album = parts[0], " - ".join(parts[1:])
    else:
        artist, album = "MY LIBRARY", path.stem
    year = ""
    match = re.search(r" - (19\d{2}|20\d{2})$", album)
    if match:
        year = match.group(1)
        album = album[: match.start()]
    return artist, album, year


def panel(path: Path) -> Image.Image:
    artist, album, year = metadata(path)
    with Image.open(path) as raw:
        cover = raw.convert("RGB")
    cover = ImageOps.fit(cover, (188, 188), method=Image.Resampling.LANCZOS)
    mean = tuple(int(x) for x in ImageStat.Stat(cover.resize((1, 1))).mean[:3])
    base = Image.new("RGB", PANEL_SIZE, CANVAS_COLOR)
    tint = Image.new("RGB", PANEL_SIZE, mean).filter(ImageFilter.GaussianBlur(24))
    base = Image.blend(base, tint, 0.12)
    draw = ImageDraw.Draw(base)
    draw.text((132, 19), fit_text(draw, artist, 214, 13, True)[0], fill="white", font=font(13, True), anchor="ma")
    draw.rectangle((25, 43, 215, 233), outline="#d2e6f1", width=1)
    base.paste(cover, (27, 45))
    reflection = cover.transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((188, 43))
    base.paste(Image.blend(Image.new("RGB", reflection.size, CANVAS_COLOR), reflection, 0.2), (27, 237))
    draw = ImageDraw.Draw(base)
    title, title_font = fit_text(draw, album, 216, 16, True)
    draw.text((132, 309), title, fill="white", font=title_font, anchor="ma")
    if year:
        draw.text((132, 344), year, fill="#a8becb", font=font(12), anchor="ma")
    return base


def animation(label: str, slot: int) -> str:
    start = (slot % 6) * 10
    branch = f"%xd({label},16)"
    for second in (1, 0):
        frames = []
        numbers = list(range(second * 8 + 1, min(second * 8 + 9, 16)))
        for n in numbers:
            delay = "2" if n == numbers[-1] else "0.1"
            frames.append(f"%t({delay})%xd({label},{n})")
        branch = f"%?if(%cS,<,{start + second + 1})<" + ";".join(frames) + "|" + branch + ">"
    return branch


def build(covers: Path, output: Path, seed: int) -> None:
    files = sorted(p for p in covers.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED)
    if not 2 <= len(files) <= 43:
        raise SystemExit("Use between 2 and 43 JPG, PNG, WebP or BMP cover images in the covers folder.")
    panels = [panel(path) for path in files]
    order = list(range(len(panels)))
    random.Random(seed).shuffle(order)
    schedule = [order[i % len(order)] for i in range(360)]
    pairs = list(dict.fromkeys((schedule[(i - 1) % 360], schedule[i]) for i in range(360)))
    soft = output / "wps" / SKIN_DIR / "soft"
    soft.mkdir(parents=True, exist_ok=True)
    for old in soft.glob("fade*.bmp"):
        old.unlink()
    for pair_index, (previous, current) in enumerate(pairs):
        strip = Image.new("RGB", (VISIBLE_WIDTH, 360 * FRAME_COUNT))
        for frame_index in range(1, FRAME_COUNT + 1):
            u = frame_index / FRAME_COUNT
            blend = u * u * (3 - 2 * u)
            left = panels[previous].transform(
                (VISIBLE_WIDTH, 360), Image.Transform.AFFINE,
                (1, 0, 12 + 4 * blend, 0, 1, 0), resample=Image.Resampling.BICUBIC,
            )
            right = panels[current].transform(
                (VISIBLE_WIDTH, 360), Image.Transform.AFFINE,
                (1, 0, 8 + 4 * blend, 0, 1, 0), resample=Image.Resampling.BICUBIC,
            )
            strip.paste(Image.blend(left, right, blend), (0, (frame_index - 1) * 360))
        strip.save(soft / f"fade{pair_index:02d}.bmp")
        print(f"Rendered transition {pair_index + 1}/{len(pairs)}", flush=True)

    credits = """# Theme: iClassic Galleria for Innioasis Y1 (480x360)
# Adapted from CarlosPixel's iClassic 1.4, itself based on Humberto Santana's iClassic.
# iLike elements credited to Alan Brito and H. Pearce.
# Theme license: CC BY-SA 3.0. https://creativecommons.org/licenses/by-sa/3.0/
# Menu artwork: 16-frame pre-rendered blend, 4-pixel drift, 10-second clock slots.
"""
    lines = [credits, "%wd", "%?Lt<|>", "%Fl(2,23-arial-unicode-ms-bold.fnt)"]
    for index in range(len(pairs)):
        lines.append(f"%xl(fade{index:02d},soft/fade{index:02d}.bmp,0,0,{FRAME_COUNT})")
    pair_names = {pair: f"fade{i:02d}" for i, pair in enumerate(pairs)}
    def slot_animation(slot: int) -> str:
        pair = (schedule[(slot - 1) % 360], schedule[slot])
        return animation(pair_names[pair], slot)
    minutes = []
    for minute in range(60):
        branch = slot_animation(minute * 6 + 5)
        for slot in range(4, -1, -1):
            branch = f"%?if(%cS,<,{(slot + 1) * 10})<{slot_animation(minute * 6 + slot)}|{branch}>"
        minutes.append(branch)
    lines.append("%V(240,0,240,360,-)%Vb(101923)")
    lines.append("%?cM<" + "|".join(minutes[1:] + minutes[:1]) + ">")
    lines.append((HERE / "iclassic-menu-tail.sbs").read_text(encoding="utf-8"))
    (output / "wps" / "iClassic_Galleria.sbs").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Done: {len(files)} covers, {len(pairs)} transitions. Copy the generated .rockbox contents to the Y1.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--covers", type=Path, default=HERE.parent / "demo-covers")
    parser.add_argument("--output", type=Path, default=HERE.parent / ".rockbox")
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    build(args.covers.expanduser().resolve(), args.output.expanduser().resolve(), args.seed)
