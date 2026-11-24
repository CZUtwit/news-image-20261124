#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: one 1024x1024 picture summing up the
world news of Tuesday 24 November 2026. Pure Pillow, no network, deterministic.

v3 (2026-11-24 afternoon, per the improvement plan):
- every story re-verified against live news (AP/Reuters/SCMP/Japan Times);
  the stale Philippines item (announced 18 Nov) is replaced by the ICJ's
  landmark Myanmar genocide ruling (first state ever found guilty);
- hero headline names the company: NVIDIA'S HUANG IS BACK (two lines);
- hero visual is a big panel: NVDA +31%, large chip, rising chart;
- cell pictograms upgraded to story-telling scenes (ship + drone, Capitol
  dome, globe, satellite + orbit, scales of justice);
- small text enlarged throughout (summaries 23, body 25, footer 18).

Run: python3 tools/make_image.py  (writes entry.png next to the repo root)
"""

import math
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


def draw_hero_panel(d, x, y, w, h):
    """Big hero visual: NVDA +31% label, large GPU chip, rising chart."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=DARK_GREEN)
    cx = x + w // 2
    d.text((cx, y + 28), "NVDA  +31%", font=font(SANS_BOLD, 32),
           fill=WHITE, anchor="mm")
    cy = y + 122
    s = 104
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
    # Rising stock chart along the bottom.
    pts = [(x + 32, y + h - 28), (x + 92, y + h - 40), (x + 152, y + h - 35),
           (x + 212, y + h - 52), (x + 272, y + h - 62), (x + 316, y + h - 72)]
    d.line(pts, fill=GREEN, width=6, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx, hy), (hx - 18, hy + 2), (hx - 8, hy + 16)], fill=GREEN)


def draw_ship(d, x, y, s, color):
    """Warship with a sea drone above and waves below."""
    # Drone silhouette (small quad) upper right.
    dx, dy = x + s * 0.62, y - 6
    d.rectangle([dx, dy + 4, dx + 22, dy + 10], fill=color)
    d.line([dx - 6, dy, dx + 28, dy], fill=color, width=3)
    d.ellipse([dx - 10, dy - 3, dx - 2, dy + 3], fill=color)
    d.ellipse([dx + 24, dy - 3, dx + 32, dy + 3], fill=color)
    # Hull.
    d.polygon([(x, y + 34), (x + s, y + 34), (x + s - 14, y + 62), (x + 14, y + 62)],
              fill=color)
    d.rectangle([x + s * 0.32, y, x + s * 0.62, y + 34], fill=color)
    d.line([x + s * 0.47, y - 16, x + s * 0.47, y], fill=color, width=4)
    d.line([x + s * 0.47, y - 16, x + s * 0.62, y - 8], fill=color, width=3)
    for i in range(3):
        wx = x + i * (s // 3)
        d.arc([wx, y + 70, wx + 34, y + 86], start=0, end=180, fill=color, width=4)


def draw_capitol(d, x, y, s, color):
    """US Capitol silhouette: dome, columns, base."""
    cx = x + s // 2
    d.line([cx, y + 2, cx, y + 12], fill=color, width=3)
    d.polygon([(cx, y + 2), (cx + 10, y + 6), (cx, y + 10)], fill=color)
    d.pieslice([cx - s * 0.30, y + 8, cx + s * 0.30, y + 8 + s * 0.42],
               start=180, end=360, fill=color)
    d.rectangle([x + s * 0.12, y + s * 0.42, x + s * 0.88, y + s * 0.50], fill=color)
    for i in range(5):
        px = x + s * 0.16 + i * s * 0.17
        d.rectangle([px, y + s * 0.52, px + 5, y + s * 0.78], fill=color)
    d.rectangle([x + s * 0.06, y + s * 0.78, x + s * 0.94, y + s * 0.86], fill=color)
    d.rectangle([x, y + s * 0.88, x + s, y + s * 0.96], fill=color)


def draw_globe(d, x, y, s, color):
    d.ellipse([x, y, x + s, y + s], outline=color, width=6)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=color, width=4)
    d.line([x, y + s // 2, x + s, y + s // 2], fill=color, width=4)
    d.arc([x, y + s * 0.2, x + s, y + s * 0.8], start=90, end=270, fill=color, width=4)


def draw_satellite(d, x, y, s, color):
    """Satellite on a tilted orbit ring."""
    cx, cy = x + s // 2, y + s // 2
    rx, ry, tilt = s * 0.52, s * 0.20, math.radians(-24)
    pts = []
    for k in range(49):
        a = 2 * math.pi * k / 48
        ex, ey = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + ex * math.cos(tilt) - ey * math.sin(tilt),
                    cy + ex * math.sin(tilt) + ey * math.cos(tilt)))
    d.line(pts, fill=color, width=3, joint="curve")
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
    yy = y + 48
    for line in hl[:2]:
        d.text((x + 16, yy), line, font=font(DISPLAY_BOLD, 30), fill=INK)
        yy += 32
    yy = y + 118
    for line in wrap(d, summary, font(SANS, 23), text_w)[:3]:
        d.text((x + 16, yy), line, font=font(SANS, 23), fill=(60, 60, 60))
        yy += 27
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

    # Hero: Nvidia / Huang. Headline names the company; big visual panel right.
    d.text((28, 170), "TECH  •  UNITED STATES", font=font(SANS_BOLD, 23), fill=RED)
    d.text((28, 196), "NVIDIA'S HUANG", font=font(DISPLAY_BLACK, 68), fill=NAVY)
    d.text((28, 264), "IS BACK", font=font(DISPLAY_BLACK, 68), fill=NAVY)
    hero = ("Nvidia reinstates Jensen Huang as CEO, 11 days after he resigned. "
            "Shares jump 31% after Trump intervened.")
    yy = 344
    for line in wrap(d, hero, font(SANS, 25), 600):
        d.text((28, yy), line, font=font(SANS, 25), fill=INK)
        yy += 32
    draw_hero_panel(d, 648, 168, 348, 268)
    d.line([28, 452, 996, 452], fill=(200, 195, 180), width=2)

    # Grid of four stories.
    gx, gy, cw, ch, gap, vgap = 28, 468, 474, 200, 20, 12
    story_cell(d, gx, gy, cw, ch, "WAR  •  UKRAINE", RED,
               "KYIV SAYS IT SANK RUSSIAN WARSHIP",
               "Kyiv says sea drones sank a Russian warship off Libya. "
               "Strikes kill 15 near Kyiv.", draw_ship)
    story_cell(d, gx + cw + gap, gy, cw, ch, "POLITICS  •  USA", BLUE,
               "DEMOCRATS TAKE THE HOUSE",
               "Biggest House majority since 1992: at least 258 seats.",
               draw_capitol)
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
    y = 892
    d.rounded_rectangle([28, y, 996, y + 94], radius=12, fill=WHITE,
                        outline=(210, 205, 190), width=2)
    d.text((48, y + 10), "JUSTICE  •  MYANMAR", font=font(SANS_BOLD, 21),
           fill=BRONZE)
    d.text((48, y + 32), "MYANMAR GUILTY OF GENOCIDE",
           font=font(DISPLAY_BOLD, 33), fill=INK)
    d.text((48, y + 66), "UN court finds Myanmar committed genocide; "
           "reparations ordered.",
           font=font(SANS, 23), fill=(60, 60, 60))
    draw_scales(d, 908, y + 12, 72, BRONZE)

    # Footer.
    d.text((W // 2, 1002), "Six stories that defined the day  •  Sources: "
           "AP, Reuters, SCMP, The Japan Times  •  24 November 2026",
           font=font(SANS, 18), fill=GREY, anchor="mm")

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
