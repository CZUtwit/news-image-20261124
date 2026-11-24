#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: one 1024x1024 picture summing up the
world news of Tuesday 24 November 2026. Pure Pillow, no network, deterministic.

v2 (2026-11-24 afternoon): every story re-verified against live news; the
stale Philippines item (announced 18 Nov) is replaced by the ICJ's landmark
Myanmar genocide ruling; small text enlarged throughout and the hero made
stronger (full-width headline, larger chip panel).

Run: python3 tools/make_image.py  (writes entry.png next to the repo root)
"""

import math
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
BRONZE = (146, 64, 14)

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
    """Stylised GPU chip on a dark green panel, sized to the panel."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=DARK_GREEN)
    cx = x + w // 2
    cy = y + h // 2 - 18
    s = min(96, int(h * 0.45))
    for i in range(5):
        off = -44 + i * 22
        d.line([cx + off, cy - s // 2 - 20, cx + off, cy - s // 2], fill=GREEN, width=6)
        d.line([cx + off, cy + s // 2, cx + off, cy + s // 2 + 20], fill=GREEN, width=6)
        d.line([cx - s // 2 - 20, cy + off, cx - s // 2, cy + off], fill=GREEN, width=6)
        d.line([cx + s // 2, cy + off, cx + s // 2 + 20, cy + off], fill=GREEN, width=6)
    d.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                        radius=10, fill=GREEN)
    d.rounded_rectangle([cx - 30, cy - 30, cx + 30, cy + 30], radius=6, fill=DARK_GREEN)
    d.text((cx, cy), "AI", font=font(SANS_BOLD, 30), fill=WHITE, anchor="mm")
    d.text((x + w // 2, y + h - 38), "NVDA  +31%", font=font(SANS_BOLD, 30),
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


def draw_scales(d, x, y, s, color):
    """Scales of justice: post, beam and two pans."""
    cx = x + s // 2
    d.line([cx, y + 6, cx, y + s - 8], fill=color, width=5)
    d.line([x + 6, y + 16, x + s - 6, y + 16], fill=color, width=5)
    d.line([cx - 16, y + s - 8, cx + 16, y + s - 8], fill=color, width=5)
    for px in (x + 8, x + s - 8):
        d.line([px, y + 16, px - 14, y + s * 0.62], fill=color, width=3)
        d.line([px, y + 16, px + 14, y + s * 0.62], fill=color, width=3)
        d.arc([px - 16, y + s * 0.62, px + 16, y + s * 0.62 + 26],
              start=0, end=180, fill=color, width=4)


def story_cell(d, x, y, w, h, tag, tag_color, headline, summary, pictogram):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=WHITE,
                        outline=(210, 205, 190), width=2)
    d.rounded_rectangle([x, y, x + w, y + 36], radius=12, fill=tag_color)
    d.rectangle([x, y + 24, x + w, y + 36], fill=tag_color)
    d.text((x + 16, y + 18), tag, font=font(SANS_BOLD, 21), fill=WHITE, anchor="lm")
    text_w = w - 32 - 88
    hl = wrap(d, headline, font(DISPLAY_BOLD, 30), text_w)
    yy = y + 50
    for line in hl[:2]:
        d.text((x + 16, yy), line, font=font(DISPLAY_BOLD, 30), fill=INK)
        yy += 34
    yy = y + 124
    for line in wrap(d, summary, font(SANS, 23), text_w)[:3]:
        d.text((x + 16, yy), line, font=font(SANS, 23), fill=(60, 60, 60))
        yy += 28
    pictogram(d, x + w - 88, y + 58, 68, tag_color)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead: the day, named loud.
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.text((W // 2, 30), "THE WORLD IN ONE DAY", font=font(SANS_BOLD, 24),
           fill=(170, 190, 220), anchor="mm")
    d.text((W // 2, 94), "TUESDAY, 24 NOVEMBER 2026", font=font(SERIF_BOLD, 56),
           fill=WHITE, anchor="mm")
    d.rectangle([0, 150, W, 156], fill=RED)

    # Hero: Nvidia / Huang, full-width headline, chip panel at right.
    d.text((28, 176), "TECH  •  UNITED STATES", font=font(SANS_BOLD, 23), fill=RED)
    d.text((28, 204), "HUANG IS BACK", font=font(DISPLAY_BLACK, 80), fill=NAVY)
    hero = ("Nvidia reinstates Jensen Huang as chief executive, 11 days after "
            "he resigned, after Donald Trump intervened. Shares jump 31%.")
    yy = 310
    for line in wrap(d, hero, font(SANS, 27), 600):
        d.text((28, yy), line, font=font(SANS, 27), fill=INK)
        yy += 37
    draw_chip(d, 664, 200, 332, 208)
    d.line([28, 428, 996, 428], fill=(200, 195, 180), width=2)

    # Grid of four stories.
    gx, gy, cw, ch, gap, vgap = 28, 444, 474, 208, 20, 14
    story_cell(d, gx, gy, cw, ch, "WAR  •  UKRAINE", RED,
               "KYIV SAYS IT SANK RUSSIAN WARSHIP",
               "Sea drones sank a Russian warship off Libya. "
               "Russian strikes kill 15 near Kyiv.", draw_ship)
    story_cell(d, gx + cw + gap, gy, cw, ch, "POLITICS  •  USA", BLUE,
               "DEMOCRATS TAKE THE HOUSE",
               "Biggest House majority since 1992: at least 258 seats.",
               draw_star)
    story_cell(d, gx, gy + ch + vgap, cw, ch, "CLIMATE  •  COP31", CLIMATE,
               "COP31 COLLAPSES",
               "Climate talks end with no deal as the EU rejects a text "
               "silent on fossil fuels.", draw_globe)
    story_cell(d, gx + cw + gap, gy + ch + vgap, cw, ch, "SPACE  •  SECURITY",
               PURPLE, "NUCLEAR SATELLITE ALERT",
               "NATO vows space defence as allies warn Russia may launch a "
               "nuclear-armed satellite.", draw_satellite)

    # Bottom strip: the ICJ's Myanmar ruling (replaces the stale 18 Nov
    # Philippines item; verified: first state ever found guilty of genocide).
    y = 886
    d.rounded_rectangle([28, y, 996, y + 98], radius=12, fill=WHITE,
                        outline=(210, 205, 190), width=2)
    d.text((48, y + 12), "JUSTICE  •  MYANMAR", font=font(SANS_BOLD, 21),
           fill=BRONZE)
    d.text((48, y + 36), "MYANMAR GUILTY OF GENOCIDE",
           font=font(DISPLAY_BOLD, 33), fill=INK)
    d.text((48, y + 72), "UN court finds Myanmar committed genocide; "
           "reparations ordered.",
           font=font(SANS, 23), fill=(60, 60, 60))
    draw_scales(d, 908, y + 14, 72, BRONZE)

    # Footer.
    d.text((W // 2, 1002), "Six stories that defined the day  •  Sources: "
           "AP, Reuters, SCMP, The Japan Times  •  24 November 2026",
           font=font(SANS, 18), fill=GREY, anchor="mm")

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
