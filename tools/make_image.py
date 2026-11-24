#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: one 1024x1024 picture summing up the
world news of Tuesday 24 November 2026. Pure Pillow, no network, deterministic.

Run: python3 tools/make_image.py  (writes entry.png next to the repo root)
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
RED = (193, 18, 31)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
GREEN = (118, 185, 0)
DARK_GREEN = (38, 84, 0)
BLUE = (29, 78, 216)
CLIMATE = (45, 106, 79)
PURPLE = (91, 42, 134)
GOLD = (180, 83, 9)

FONT_DIR = Path("/usr/share/fonts/truetype")
DISPLAY_BLACK = FONT_DIR / "noto/NotoSansDisplay-Black.ttf"
DISPLAY_BOLD = FONT_DIR / "noto/NotoSansDisplay-Bold.ttf"
SANS_BOLD = FONT_DIR / "noto/NotoSans-Bold.ttf"
SANS = FONT_DIR / "noto/NotoSans-Regular.ttf"
SERIF_BOLD = FONT_DIR / "noto/NotoSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning lines that fit max_width."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_chip(d, x, y, w, h):
    """Stylised GPU chip on a dark green panel."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=DARK_GREEN)
    cx, cy = x + w // 2, y + h // 2 - 18
    s = 120
    for i in range(5):
        off = -56 + i * 28
        d.line([cx + off, cy - s // 2 - 22, cx + off, cy - s // 2], fill=GREEN, width=6)
        d.line([cx + off, cy + s // 2, cx + off, cy + s // 2 + 22], fill=GREEN, width=6)
        d.line([cx - s // 2 - 22, cy + off, cx - s // 2, cy + off], fill=GREEN, width=6)
        d.line([cx + s // 2, cy + off, cx + s // 2 + 22, cy + off], fill=GREEN, width=6)
    d.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                        radius=10, fill=GREEN)
    d.rounded_rectangle([cx - 34, cy - 34, cx + 34, cy + 34], radius=6, fill=DARK_GREEN)
    d.text((cx, cy), "AI", font=font(SANS_BOLD, 34), fill=WHITE, anchor="mm")
    d.text((x + w // 2, y + h - 58), "NVDA  +31%", font=font(SANS_BOLD, 34),
           fill=WHITE, anchor="mm")


def draw_ship(d, x, y, s, color):
    d.polygon([(x, y + 34), (x + s, y + 34), (x + s - 14, y + 62), (x + 14, y + 62)],
              fill=color)
    d.rectangle([x + s * 0.32, y, x + s * 0.62, y + 34], fill=color)
    d.line([x + s * 0.47, y - 16, x + s * 0.47, y], fill=color, width=4)
    d.line([x + s * 0.47, y - 16, x + s * 0.62, y - 8], fill=color, width=3)
    for i in range(3):
        wx = x + i * (s // 3)
        d.arc([wx, y + 70, wx + 34, y + 86], start=0, end=180, fill=color, width=4)


def draw_star(d, x, y, s, color):
    import math
    cx, cy = x + s // 2, y + s // 2
    outer, inner = s * 0.48, s * 0.20
    points = []
    for i in range(10):
        r = outer if i % 2 == 0 else inner
        a = math.radians(-90 + i * 36)
        points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(points, fill=color)


def draw_globe(d, x, y, s, color):
    d.ellipse([x, y, x + s, y + s], outline=color, width=6)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=color, width=4)
    d.line([x, y + s // 2, x + s, y + s // 2], fill=color, width=4)
    d.arc([x, y + s * 0.2, x + s, y + s * 0.8], start=90, end=270, fill=color, width=4)


def draw_satellite(d, x, y, s, color):
    d.rectangle([x + s * 0.40, y + s * 0.36, x + s * 0.60, y + s * 0.64], fill=color)
    d.rectangle([x, y + s * 0.42, x + s * 0.36, y + s * 0.58], outline=color, width=4)
    d.rectangle([x + s * 0.64, y + s * 0.42, x + s, y + s * 0.58], outline=color,
                width=4)
    d.line([x + s * 0.36, y + s * 0.5, x + s * 0.40, y + s * 0.5], fill=color, width=4)
    d.line([x + s * 0.60, y + s * 0.5, x + s * 0.64, y + s * 0.5], fill=color, width=4)
    d.line([x + s * 0.5, y + s * 0.36, x + s * 0.62, y + s * 0.18], fill=color, width=4)
    for sx, sy in [(0.12, 0.14), (0.86, 0.1), (0.9, 0.82), (0.08, 0.8)]:
        d.ellipse([x + s * sx - 3, y + s * sy - 3, x + s * sx + 3, y + s * sy + 3],
                  fill=color)


def draw_sun(d, x, y, s, color):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=color)
    for i in range(8):
        import math
        a = math.radians(i * 45)
        x1, y1 = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        x2, y2 = cx + 46 * math.cos(a), cy + 46 * math.sin(a)
        d.line([x1, y1, x2, y2], fill=color, width=5)


def story_cell(d, x, y, w, h, tag, tag_color, headline, summary, pictogram):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=WHITE,
                        outline=(210, 205, 190), width=2)
    d.rounded_rectangle([x, y, x + w, y + 34], radius=12, fill=tag_color)
    d.rectangle([x, y + 22, x + w, y + 34], fill=tag_color)
    d.text((x + 16, y + 17), tag, font=font(SANS_BOLD, 19), fill=WHITE, anchor="lm")
    text_w = w - 32 - 96
    hl = wrap(d, headline, font(DISPLAY_BOLD, 27), text_w)
    yy = y + 48
    for line in hl[:2]:
        d.text((x + 16, yy), line, font=font(DISPLAY_BOLD, 27), fill=INK)
        yy += 33
    yy += 4
    for line in wrap(d, summary, font(SANS, 20), text_w)[:3]:
        d.text((x + 16, yy), line, font=font(SANS, 20), fill=(60, 60, 60))
        yy += 26
    pictogram(d, x + w - 96, y + 52, 72, tag_color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead: the day, named loud.
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((W // 2, 30), "THE WORLD IN ONE DAY", font=font(SANS_BOLD, 22),
           fill=(170, 190, 220), anchor="mm")
    d.text((W // 2, 92), "TUESDAY, 24 NOVEMBER 2026", font=font(SERIF_BOLD, 52),
           fill=WHITE, anchor="mm")
    d.rectangle([0, 148, W, 154], fill=RED)

    # Hero: Nvidia / Huang.
    d.text((28, 176), "TECH  •  UNITED STATES", font=font(SANS_BOLD, 21), fill=RED)
    d.text((28, 206), "HUANG IS BACK", font=font(DISPLAY_BLACK, 72), fill=NAVY)
    hero = ("Nvidia reinstates Jensen Huang as chief executive, 11 days after "
            "he resigned, after Donald Trump intervened. Shares jump 31%.")
    yy = 292
    for line in wrap(d, hero, font(SANS, 25), 560):
        d.text((28, yy), line, font=font(SANS, 25), fill=INK)
        yy += 33
    draw_chip(d, 620, 172, 376, 232)
    d.line([28, 424, 996, 424], fill=(200, 195, 180), width=2)

    # Grid of four stories.
    gx, gy, cw, ch, gap = 28, 440, 474, 192, 20
    story_cell(d, gx, gy, cw, ch, "WAR  •  UKRAINE", RED,
               "KYIV SAYS IT SANK RUSSIAN WARSHIP",
               "Sea drones sank a Russian warship off Libya, Kyiv says. "
               "Russian strikes kill at least 15 near Kyiv.", draw_ship)
    story_cell(d, gx + cw + gap, gy, cw, ch, "POLITICS  •  USA", BLUE,
               "DEMOCRATS TAKE THE HOUSE",
               "Biggest House majority since 1992: at least 258 seats.",
               draw_star)
    story_cell(d, gx, gy + ch + gap, cw, ch, "CLIMATE  •  COP31", CLIMATE,
               "COP31 COLLAPSES",
               "Climate talks end with no deal as the EU rejects a text "
               "silent on fossil fuels.", draw_globe)
    story_cell(d, gx + cw + gap, gy + ch + gap, cw, ch, "SPACE  •  SECURITY",
               PURPLE, "NUCLEAR SATELLITE ALERT",
               "NATO vows space defence as allies warn Russia may launch a "
               "nuclear-armed satellite.", draw_satellite)

    # Bottom strip: Asia.
    y = 856
    d.rounded_rectangle([28, y, 996, y + 108], radius=12, fill=WHITE,
                        outline=(210, 205, 190), width=2)
    d.text((48, y + 14), "ASIA-PACIFIC", font=font(SANS_BOLD, 19), fill=GOLD)
    d.text((48, y + 38), "TRUMP OFFERS MANILA $2.4BN",
           font=font(DISPLAY_BOLD, 30), fill=INK)
    d.text((48, y + 76), "US offers the Philippines $2.4 billion for "
           "self-defence, with strings attached.",
           font=font(SANS, 20), fill=(60, 60, 60))
    draw_sun(d, 906, y + 14, 76, GOLD)

    # Footer.
    d.text((W // 2, 992), "Six stories that defined the day  •  Sources: "
           "SCMP, The Japan Times, AP  •  24 November 2026",
           font=font(SANS, 16), fill=GREY, anchor="mm")

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
