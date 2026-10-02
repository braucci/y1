#!/usr/bin/env python3
"""Draw original placeholder sleeves so the theme works before personalisation."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DEST = Path(__file__).resolve().parent.parent / "demo-covers"
DEST.mkdir(parents=True, exist_ok=True)

PALETTES = [
    ("Orbit", "#112e42", "#7cdee5", "01"),
    ("Afterglow", "#4a2141", "#f5a3a2", "02"),
    ("Blue Hour", "#1b3551", "#a7b9ef", "03"),
    ("Solstice", "#4d361b", "#eec681", "04"),
    ("Night Drive", "#222447", "#c1adff", "05"),
    ("New Worlds", "#173c3b", "#9be0bc", "06"),
]

for title, background, accent, number in PALETTES:
    image = Image.new("RGB", (480, 480), background)
    draw = ImageDraw.Draw(image)
    draw.ellipse((82, 80, 398, 396), outline=accent, width=3)
    draw.ellipse((134, 132, 346, 344), outline=accent, width=2)
    draw.arc((48, 48, 432, 432), 14, 154, fill=accent, width=13)
    draw.line((55, 312, 420, 130), fill=accent, width=5)
    draw.rectangle((22, 22, 458, 458), outline=accent, width=2)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 64)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    except OSError:
        font = small = ImageFont.load_default()
    draw.text((240, 247), number, fill="white", font=font, anchor="mm")
    draw.text((240, 424), "HACK MY Y1  /  DEMO ART", fill=accent, font=small, anchor="mm")
    image.save(DEST / f"Demo Artist - {title} - 2026.png", optimize=True)

print(f"Created {len(PALETTES)} original demo sleeves in {DEST}")
