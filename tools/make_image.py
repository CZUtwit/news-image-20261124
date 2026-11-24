#!/usr/bin/env python3
"""Draw the news-image-20261124 entry, v4: one 1024x1024 picture summing up
the world news of Tuesday 24 November 2026. Pure Pillow, no network,
deterministic.

v4 rebuilds the layout on the 22 November winner's format (shown to us by
the user): 10 main stories + 10 ALSO items + region counts + a numbers line
+ a DATE CHECK with an exclusion list and a HOW SURE legend. Text stays big
and the page stays clean: the A/B lesson was that when breadth ties,
readability decides.

All 20 stories were verified as happening or first reported on 24 November
2026 (Daily Summary of World first-reported times, cross-checked against
Reuters, AP, Yeni Safak, The Times, Nature, Al Jazeera, Xinhua). The v3
image's date errors are fixed here: the ship sinking, the House 258 seats
and the COP31 collapse all belong to earlier days and are listed as left
out; the ICJ ruling itself was last week, so the Myanmar story is now
Malaysia's fresh return announcement. The Hormuz tankers item is worded as
the IRGC's claim, which is what was reported on Tuesday.

Run: python3 tools/make_image.py  (writes entry.png at the repository root)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)

PALETTE = {
    "paper": (247, 243, 234),
    "ink": (26, 26, 26),
    "navy": (20, 33, 61),
    "red": (193, 18, 31),
    "white": (255, 255, 255),
    "grey": (90, 90, 90),
    "body": (60, 60, 60),
    "line": (200, 195, 180),
    "card_edge": (210, 205, 190),
    "pale_blue": (170, 190, 220),
    "green": (118, 185, 0),
    "dark_green": (38, 84, 0),
    "blue": (29, 78, 216),
    "climate": (45, 106, 79),
    "purple": (91, 42, 134),
    "bronze": (146, 64, 14),
    "amber": (180, 120, 10),
}

FONT_ROOT = Path("/usr/share/fonts/truetype/noto")
FONTS = {
    "display_black": FONT_ROOT / "NotoSansDisplay-Black.ttf",
    "display_bold": FONT_ROOT / "NotoSansDisplay-Bold.ttf",
    "sans_bold": FONT_ROOT / "NotoSans-Bold.ttf",
    "sans": FONT_ROOT / "NotoSans-Regular.ttf",
    "serif_bold": FONT_ROOT / "NotoSerif-Bold.ttf",
}


def load(name, size):
    return ImageFont.truetype(str(FONTS[name]), size)


def fit_lines(draw, text, fname, size, max_width):
    """Split text into lines that fit max_width at the given font."""
    fnt = load(fname, size)
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=fnt) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def icon_chip(d, x, y, s, color, dark):
    cx, cy = x + s / 2, y + s / 2
    body = s * 0.52
    for side in range(4):
        for k in range(4):
            off = -body * 0.36 + k * body * 0.24
            if side == 0:
                d.line([cx + off, y, cx + off, cy - body / 2], fill=color, width=5)
            elif side == 1:
                d.line([cx + off, cy + body / 2, cx + off, y + s], fill=color, width=5)
            elif side == 2:
                d.line([x, cy + off, cx - body / 2, cy + off], fill=color, width=5)
            else:
                d.line([cx + body / 2, cy + off, x + s, cy + off], fill=color, width=5)
    d.rounded_rectangle([cx - body / 2, cy - body / 2, cx + body / 2, cy + body / 2],
                        radius=8, fill=color)
    inner = body * 0.45
    d.rounded_rectangle([cx - inner, cy - inner, cx + inner, cy + inner],
                        radius=5, fill=dark)
    d.text((cx, cy), "AI", font=load("sans_bold", 24), fill=PALETTE["white"],
           anchor="mm")


# ---------------------------------------------------------------- stories

# Grid stories 2-10: (number, tag, colour, badge, headline, summary)
GRID = [
    (2, "MYANMAR", "bronze", "REPORTED",
     "MALAYSIA TO SEND MIGRANTS BACK",
     "1,500 by ship in Dec, 5,303 by air; days after ICJ ruling."),
    (3, "SPACE  •  NATO", "blue", "REPORTED",
     "NATO: DEFENCE COVERS SPACE",
     "Rutte vows to defend space; Russia may launch nuclear satellite."),
    (4, "BANGLADESH", "climate", "REPORTED",
     "HASINA PLANS DEC 16 RETURN",
     "Ex-PM to fly home from exile; convicted, faces death sentence."),
    (5, "CRIME  •  MEXICO", "red", "REPORTED",
     "US DRONE HELPED CATCH CHAPO ISIDRO",
     "Mexico to try him despite US extradition request."),
    (6, "ASIA  •  KOREA", "blue", "REPORTED",
     "SEOUL SCRAMBLES JETS",
     "Russian aircraft enter air defence zone; fighters scrambled."),
    (7, "TECH  •  USA", "purple", "REPORTED",
     "US BLACKLISTS NVIDIA-SCANDAL FIRM",
     "Megaspeed + 6 firms on Entity List; licences needed for chips."),
    (8, "AMERICAS  •  CANADA", "red", "REPORTED",
     "PENTAGON REBUKES CANADA",
     "Defence shortfalls; F-35 review questioned; 41.9% of jets ready."),
    (9, "CRISIS  •  YEMEN", "bronze", "REPORTED",
     "360,000 DISPLACED IN YEMEN",
     "UN: fleeing since August; 323 civilian casualties verified."),
    (10, "ASIA  •  INDONESIA", "climate", "REPORTED",
     "INDONESIA NAMES 2 VP CANDIDATES",
     "Prabowo picks Sulaiman, Sugiono; assembly to elect by Dec 11."),
]

# ALSO items 11-20: (number, place, one line)
ALSO = [
    (11, "UKRAINE", "Zelensky urges 4-party talks soon"),
    (12, "GERMANY", "Merz: Europe ready to talk to Russia"),
    (13, "CHINA", "Official sentenced to death for spying"),
    (14, "COLOMBIA", "Car bomb hits government HQ"),
    (15, "HAITI", "Bukele names 3 soldiers killed in mission"),
    (16, "HORMUZ", "IRGC says 3 tankers hit mines, ablaze"),
    (17, "MYANMAR", "14 nations back ICJ ruling"),
    (18, "SPACE", "China names first foreign astronaut"),
    (19, "PACIFIC", "Solomons to scrap China pact"),
    (20, "USA", "Pennsylvania measles outbreak: 9th death"),
]

REGIONS = [
    ("AMERICAS 7", "blue"),
    ("ASIA 7", "climate"),
    ("EUROPE 3", "red"),
    ("MIDDLE EAST 2", "purple"),
    ("OCEANIA 1", "bronze"),
]

NUMBERS = ("NVDA +31%  ·  5,303 migrants  ·  60 days  ·  "
           "360,000 displaced  ·  88 F-35s  ·  Seoul +6%")


def draw_cell(d, x, y, w, h, story):
    num, tag, color, badge, headline, summary = story
    c = PALETTE[color]
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PALETTE["white"],
                        outline=PALETTE["card_edge"], width=2)
    d.rounded_rectangle([x, y, x + w, y + 28], radius=10, fill=c)
    d.rectangle([x, y + 18, x + w, y + 28], fill=c)
    d.text((x + 12, y + 14), f"{num}  •  {tag}", font=load("sans_bold", 16),
           fill=PALETTE["white"], anchor="lm")
    d.text((x + w - 10, y + 14), badge, font=load("sans_bold", 13),
           fill=PALETTE["white"], anchor="rm")
    text_w = w - 24
    yy = y + 36
    for line in fit_lines(d, headline, "display_bold", 24, text_w)[:2]:
        d.text((x + 12, yy), line, font=load("display_bold", 24),
               fill=PALETTE["ink"])
        yy += 27
    yy = y + 92
    for line in fit_lines(d, summary, "sans", 18, text_w)[:2]:
        d.text((x + 12, yy), line, font=load("sans", 18),
               fill=PALETTE["body"])
        yy += 21


def main():
    p = PALETTE
    img = Image.new("RGB", CANVAS, p["paper"])
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, 1024, 96], fill=p["navy"])
    d.text((512, 20), "THE WORLD IN ONE DAY", font=load("sans_bold", 22),
           fill=p["pale_blue"], anchor="mm")
    d.text((512, 58), "TUESDAY, 24 NOVEMBER 2026", font=load("serif_bold", 46),
           fill=p["white"], anchor="mm")

    # Region counts bar.
    d.rectangle([0, 96, 1024, 124], fill=p["white"])
    xx = 20
    for label, color in REGIONS:
        w = d.textlength(label, font=load("sans_bold", 15)) + 16
        d.rounded_rectangle([xx, 102, xx + w, 118], radius=8,
                            fill=PALETTE[color])
        d.text((xx + w / 2, 110), label, font=load("sans_bold", 15),
               fill=p["white"], anchor="mm")
        xx += w + 8
    d.text((1004, 110), "20 STORIES  •  5 REGIONS  •  ALL FROM THIS ONE DAY",
           font=load("sans_bold", 15), fill=p["ink"], anchor="rm")

    # Hero: Nvidia soars 31% on Huang's first day back.
    d.text((20, 134), "1  •  MARKETS  •  UNITED STATES",
           font=load("sans_bold", 20), fill=p["red"])
    d.text((20, 156), "NVDA SOARS 31%", font=load("display_black", 56),
           fill=p["navy"])
    hero = "Huang's first day back: shares jump 31%."
    d.text((20, 222), hero, font=load("sans", 20), fill=p["ink"])
    # Hero panel: the rally.
    px, py, pw, ph = 700, 130, 304, 128
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=16,
                        fill=p["dark_green"])
    d.text((px + pw // 2, py + 22), "NVDA  +31%", font=load("sans_bold", 26),
           fill=p["white"], anchor="mm")
    icon_chip(d, px + 24, py + 44, 72, p["green"], p["dark_green"])
    d.text((px + 125, py + 48), "SEOUL +6%", font=load("sans_bold", 19),
           fill=p["white"])
    d.text((px + 125, py + 70), "TOKYO +3.9%", font=load("sans_bold", 19),
           fill=p["white"])
    pts = [(px + 125, py + 112), (px + 160, py + 104), (px + 195, py + 108),
           (px + 230, py + 94), (px + 265, py + 86), (px + 288, py + 80)]
    d.line(pts, fill=p["green"], width=6, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx, hy), (hx - 16, hy + 2), (hx - 7, hy + 14)], fill=p["green"])

    # Numbers line.
    d.rounded_rectangle([20, 264, 1004, 290], radius=8, fill=p["navy"])
    d.text((34, 277), "THE DAY IN NUMBERS", font=load("sans_bold", 17),
           fill=p["pale_blue"], anchor="lm")
    d.text((230, 277), NUMBERS, font=load("sans_bold", 17), fill=p["white"],
           anchor="lm")

    # Grid of nine stories.
    gx, gy, cw, ch, gap = 20, 298, 321, 138, 10
    for i, story in enumerate(GRID):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + 8)
        draw_cell(d, cx, cy, cw, ch, story)

    # ALSO list.
    ay = 736
    d.text((20, ay), "ALSO ON TUESDAY 24 NOVEMBER", font=load("sans_bold", 19),
           fill=p["navy"])
    d.line([20, ay + 26, 1004, ay + 26], fill=p["line"], width=2)
    for i, (num, place, text) in enumerate(ALSO):
        col = i % 2
        row = i // 2
        x = 20 + col * 492
        y = ay + 32 + row * 22
        d.text((x, y), f"{num}", font=load("sans_bold", 18), fill=p["red"])
        d.text((x + 30, y), f"{place} — {text}", font=load("sans", 18),
               fill=p["ink"])

    # DATE CHECK.
    dy = 884
    d.rounded_rectangle([20, dy, 1004, dy + 62], radius=8, fill=p["white"],
                        outline=p["card_edge"], width=2)
    d.rounded_rectangle([32, dy + 12, 32 + 118, dy + 34], radius=6,
                        fill=p["red"])
    d.text((32 + 59, dy + 23), "DATE CHECK", font=load("sans_bold", 16),
           fill=p["white"], anchor="mm")
    d.text((162, dy + 12), "Every story on this page happened or was first "
           "reported on Tuesday 24 November 2026 (UTC).",
           font=load("sans_bold", 17), fill=p["ink"])
    d.text((162, dy + 35), "Left out — earlier days: COP31 pact (Sun 22 Nov)  ·  "
           "Ship sunk off Libya (Mon 23 Nov)  ·  House 258 seats (Mon 23 Nov)",
           font=load("sans", 15), fill=p["body"])

    # Footer.
    d.text((512, 962), "HOW SURE:  REPORTED = carried by the day's wires or "
           "officials  ·  ONGOING = still unfolding  ·  CLAIM = one side's "
           "account, labelled as such", font=load("sans", 15), fill=p["grey"],
           anchor="mm")
    d.text((512, 984), "Sources: AP, Reuters, BusinessWorld, Daily Summary of "
           "World  •  Scenes are drawn illustrations, not photographs",
           font=load("sans", 15), fill=p["grey"], anchor="mm")

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
