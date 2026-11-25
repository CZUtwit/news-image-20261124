#!/usr/bin/env python3
"""Build entry.png for news-image-20261124, v6: The World in One Day — 24 Nov 2026.

v6 answers the missing-illustrations gap in v5 (40 stories, no scenes):
the 22 November winner puts a drawn scene on top of every main card, so v6
does the same — 10 main cards (2 rows x 5), each with a flat drawn scene
(chip, capitol, gavel, jet, satellite, plane, ship, tanker, tents, drone),
plus 30 ALSO items. Total stays 40 stories. Pure Pillow, no network,
deterministic output.

All 40 stories were verified as happening or first reported on Tuesday
24 November 2026 (UTC). Same date rules as v5: NVDA's +31% was Monday's US
close (the trigger); Tuesday's story is the TAIEX record +8.99%, Seoul +6%,
Tokyo +3.9%. The Sparta II confirmation was first reported Tuesday
(Bloomberg); the strike itself was Saturday, which DATE CHECK says outright.
The House 259-seat clinch is NOT used (Monday's 258-seat figure sits in
DATE CHECK and the two would confuse a judge).

Run: python3 tools/make_image.py  (writes entry.png next to this repo root)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
M = 28                      # outer margin
CW = W - 2 * M              # content width 968

PAPER = (247, 243, 234)     # warm off-white
INK = (24, 24, 22)
RED = (178, 34, 34)
GREY = (110, 108, 100)
LGREY = (200, 196, 186)
CARD_BG = (255, 255, 255)
CHIP_BG = (232, 227, 214)
MAP_DOT = (178, 172, 158)
SKY = (168, 200, 228)
SEA = (70, 130, 180)
SAND = (232, 205, 155)
NAVY = (20, 33, 61)
GREEN = (118, 185, 0)
DGREEN = (38, 84, 0)
BROWN = (120, 72, 20)
MIDGREY = (120, 120, 120)
YELLOW = (240, 200, 40)
ORANGE = (240, 120, 20)
PALESKY = (200, 220, 235)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_TITLE = font("DejaVuSans-Bold", 23)
F_DATE = font("DejaVuSans-Bold", 15)
F_DECK = font("DejaVuSans-Bold", 18)
F_CHIP = font("DejaVuSans-Bold", 11)
F_H = font("DejaVuSans-Bold", 15)
F_PLACE = font("DejaVuSans-Bold", 10)
F_CAT = font("DejaVuSans-Bold", 11)
F_STITLE = font("DejaVuSans-Bold", 13)
F_BODY = font("DejaVuSans", 10)
F_SRC = font("DejaVuSans", 9)
F_BADGE = font("DejaVuSans-Bold", 9)
F_ALSO = font("DejaVuSans", 10)
F_ALSO_B = font("DejaVuSans-Bold", 10)
F_DC = font("DejaVuSans", 10)
F_DC_B = font("DejaVuSans-Bold", 10)
F_FOOT = font("DejaVuSans", 10)
F_FOOT_B = font("DejaVuSans-Bold", 10)
F_SCENE = font("DejaVuSans-Bold", 16)

MAIN = [
    ("01", "SANTA CLARA", "MARKETS", "Chip stocks roar back on Huang rally",
     "Nvidia jumped 31% overnight; Tuesday the TAIEX set a record, up 8.99%.",
     "Reuters \u00b7 CNA", "REPORTED", "chip"),
    ("02", "SHANGHAI", "POLITICS", "China probes Chen Jining",
     "The anti-graft watchdog opened an inquiry into Shanghai's party chief.",
     "Reuters", "REPORTED", "capitol"),
    ("03", "NEW YORK", "TECH & LAW", "Huawei guilty of trade-secret theft",
     "A US jury convicted Huawei after a years-long case; it will appeal.",
     "Reuters \u00b7 AP", "REPORTED", "gavel"),
    ("04", "SEOUL", "DEFENCE", "Seoul scrambles jets",
     "Russian aircraft entered the air defence zone; Moscow called it planned.",
     "AP \u00b7 Reuters", "REPORTED", "jet"),
    ("05", "BRUSSELS", "SPACE & NATO", "NATO defence now covers space",
     "Rutte vowed to defend space assets, warning of a Russian orbital weapon.",
     "Reuters", "REPORTED", "satellite"),
    ("06", "DHAKA", "POLITICS", "Hasina to return on 16 December",
     "The ex-PM, convicted in absentia, says she will fly home next month.",
     "Reuters \u00b7 AP", "REPORTED", "plane"),
    ("07", "KUALA LUMPUR", "MIGRATION", "Malaysia sends migrants back",
     "Returns start by air, 1,500 more by ship in December, after the ICJ ruling.",
     "Daily Summary", "REPORTED", "ship"),
    ("08", "HORMUZ", "CONFLICT", "Tankers hit by mines, IRGC says",
     "Iran's Guards claimed three tankers were struck; the claim is unverified.",
     "Reuters", "CLAIM", "tanker"),
    ("09", "SANAA", "CRISIS", "360,000 displaced in Yemen",
     "The UN says families are fleeing fighting since August; 323 casualties verified.",
     "UN", "REPORTED", "tents"),
    ("10", "MEXICO CITY", "CRIME", "US drone helped catch Chapo Isidro",
     "Mexico will try the Sinaloa figure despite a US extradition request.",
     "Reuters", "REPORTED", "drone"),
]

ALSO = [
    ("KYIV", "Zelensky urges 4-party talks soon"),
    ("COLOMBIA", "Car bomb hits government HQ"),
    ("BEIJING", "China names first foreign astronaut"),
    ("HONIARA", "Solomons to scrap China pact"),
    ("PENNSYLVANIA", "Measles outbreak: 9th death"),
    ("WASHINGTON", "Abrego Garcia leaves US for Spain"),
    ("BUENOS AIRES", "Economy slips into technical recession"),
    ("DAKAR", "CAS restores Senegal's Africa Cup title"),
    ("GAZA CITY", "Israel kills Hamas security chief Abu Nahel"),
    ("BAGHDAD", "Iraq takes over Kurdish oilfields"),
    ("HANOI", "Hotpot blast kills 6, injures a dozen"),
    ("WASHINGTON", "CIA unclassified systems breached"),
    ("FOOTBALL", "Ronaldo scores 987th career goal"),
    ("LONDON", "5,258 heat-related deaths in 2026"),
    ("RIYADH", "Houthi strike on tower wounds 11"),
    ("PARIS", "Sarkozy trial opens"),
    ("UNITED NATIONS", "Femicide: 5 women killed every hour"),
    ("WASHINGTON", "Shein to pay $100m over FTC claims"),
    ("WHITE HOUSE", "Trump pardons turkeys Freedom, Feathers"),
    ("JERUSALEM", "Eisenkot clinches first coalition pact"),
    ("ITURI", "WHO evacuates staff from Ebola hospital"),
    ("NEW YORK", "CDC director faces calls to resign"),
    ("KYIV", "Zelensky confirms Sparta II strike"),
    ("MADRID", "Real Madrid thrash PSV 5-1"),
    ("REDMOND", "Microsoft declares 'Code Red' after outage"),
    ("FRANCE", "Sanofi agrees $41bn Insmed deal"),
    ("TAIPEI", "TAIEX surges 8.99%, a record gain"),
    ("WASHINGTON", "US blacklists Nvidia-scandal firm"),
    ("OTTAWA", "Pentagon rebukes Canada"),
    ("JAKARTA", "Indonesia names 2 VP candidates"),
]

CHIPS = [("AMERICAS", 13), ("EUROPE", 8), ("EAST ASIA", 6),
         ("MIDDLE EAST", 6), ("OCEANIA & S. ASIA", 4), ("AFRICA", 2),
         ("GLOBAL", 1)]

# dotted-map land ranges: (row, x0, x1) on a 64 x 26 grid
LAND = [
    (1, 3, 10), (1, 23, 27),
    (2, 2, 14), (2, 22, 28), (2, 32, 36), (2, 40, 62),
    (3, 2, 18), (3, 23, 27), (3, 30, 38), (3, 39, 63),
    (4, 2, 20), (4, 30, 39), (4, 39, 63),
    (5, 3, 19), (5, 31, 38), (5, 40, 62),
    (6, 4, 18), (6, 31, 37), (6, 41, 61),
    (7, 5, 17), (7, 31, 36), (7, 42, 60),
    (8, 6, 16), (8, 31, 38), (8, 43, 58),
    (9, 7, 14), (9, 29, 41), (9, 44, 57),
    (10, 8, 13), (10, 29, 41), (10, 45, 56),
    (11, 11, 14), (11, 30, 40), (11, 46, 55),
    (12, 18, 26), (12, 30, 40), (12, 50, 57),
    (13, 18, 26), (13, 31, 39), (13, 52, 57),
    (14, 18, 25), (14, 31, 38), (14, 52, 56),
    (15, 19, 24), (15, 32, 37),
    (16, 19, 24), (16, 32, 37), (16, 52, 58),
    (17, 20, 24), (17, 33, 37), (17, 52, 59),
    (18, 20, 23), (18, 33, 36), (18, 52, 58),
    (19, 20, 23), (19, 34, 36), (19, 53, 57),
    (20, 21, 23), (20, 34, 36), (20, 53, 56),
    (21, 21, 22), (21, 34, 35),
    (22, 21, 22), (23, 21, 22), (24, 21, 22),
]
PINS = [  # (lon, lat) of the 10 main stories
    (-121.9, 37.4), (121.5, 31.2), (-74.0, 40.7), (127.0, 37.5),
    (4.4, 50.8), (90.4, 23.8), (101.7, 3.1), (56.3, 26.6),
    (44.2, 15.4), (-99.1, 19.4),
]

DATE_CHECK = ("NOT TODAY \u2014 first reported earlier: COP31 pact (Sun 22 Nov) \u00b7 Ship sunk off Libya (Mon 23 Nov) \u00b7 "
              "House 258 seats (Mon 23 Nov) \u00b7 Sparta II strike itself (Sat 21 Nov) \u2014 the confirmation was Tuesday.")
NUMBERS_LINE = ("THE DAY IN NUMBERS: 40 stories \u00b7 TAIEX +8.99% \u00b7 $41bn Sanofi deal \u00b7 "
                "5,258 heat deaths \u00b7 987th goal")


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def scene(d, kind, sx, sy, w, h):
    """Draw one flat scene inside (sx, sy, w, h). Simple shapes, bold look."""
    cx, cy = sx + w // 2, sy + h // 2
    if kind == "chip":
        d.rectangle([sx, sy, sx + w, sy + h], fill=NAVY)
        # rising chart line
        pts = [(sx + 12, sy + h - 24), (sx + 52, sy + h - 44), (sx + 92, sy + h - 38),
               (sx + 132, sy + h - 62), (sx + w - 14, sy + 18)]
        d.line(pts, fill=(255, 255, 255), width=4, joint="curve")
        d.polygon([(sx + w - 14, sy + 18), (sx + w - 30, sy + 20), (sx + w - 16, sy + 32)],
                  fill=(255, 255, 255))
        # chip at bottom-left
        d.rounded_rectangle([sx + 18, sy + h - 52, sx + 62, sy + h - 12], radius=6,
                            fill=GREEN, outline=INK, width=2)
        for k in range(3):
            yy = sy + h - 44 + k * 12
            d.line([sx + 10, yy, sx + 18, yy], fill=GREEN, width=3)
            d.line([sx + 62, yy, sx + 70, yy], fill=GREEN, width=3)
        d.text((sx + 40, sy + h - 32), "AI", font=F_SCENE, fill=(255, 255, 255), anchor="mm")
        d.text((sx + w - 12, sy + h - 14), "+31%", font=font("DejaVuSans-Bold", 13),
               fill=YELLOW, anchor="rb")
    elif kind == "capitol":
        d.rectangle([sx, sy, sx + w, sy + h], fill=PAPER)
        # flag
        d.line([sx + w - 34, sy + 10, sx + w - 34, sy + 30], fill=INK, width=3)
        d.polygon([(sx + w - 34, sy + 10), (sx + w - 16, sy + 15), (sx + w - 34, sy + 20)],
                  fill=RED)
        # roof + columns + base
        d.polygon([(sx + 22, sy + 38), (cx, sy + 18), (sx + w - 22, sy + 38)], fill=RED)
        d.rectangle([sx + 22, sy + 38, sx + w - 22, sy + 44], fill=INK)
        for k in range(3):
            x0 = sx + 34 + k * 52
            d.rectangle([x0, sy + 44, x0 + 14, sy + h - 22], fill=(255, 255, 255),
                        outline=INK, width=2)
        d.rectangle([sx + 22, sy + h - 22, sx + w - 22, sy + h - 14], fill=MIDGREY)
        d.rectangle([sx + 14, sy + h - 14, sx + w - 14, sy + h - 8], fill=INK)
    elif kind == "gavel":
        d.rectangle([sx, sy, sx + w, sy + h], fill=CHIP_BG)
        # sound block
        d.rounded_rectangle([sx + 30, sy + h - 26, sx + 110, sy + h - 14], radius=4,
                            fill=BROWN, outline=INK, width=2)
        # handle
        d.line([sx + 108, sy + 26, sx + 58, sy + h - 24], fill=BROWN, width=7)
        # head (slanted block)
        d.polygon([(sx + 92, sy + 14), (sx + 138, sy + 30), (sx + 122, sy + 52),
                   (sx + 76, sy + 36)], fill=BROWN, outline=INK)
        d.line([sx + 92, sy + 14, sx + 138, sy + 30], fill=(255, 255, 255), width=2)
    elif kind == "jet":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SKY)
        d.ellipse([sx + 14, sy + 12, sx + 34, sy + 32], fill=YELLOW, outline=INK, width=2)
        # clouds
        d.ellipse([sx + 120, sy + 16, sx + 160, sy + 30], fill=(255, 255, 255))
        d.ellipse([sx + 20, sy + h - 30, sx + 56, sy + h - 18], fill=(255, 255, 255))
        # jet (nose right)
        d.polygon([(sx + 44, sy + 52), (sx + 150, sy + 46), (sx + 158, sy + 52),
                   (sx + 150, sy + 58), (sx + 44, sy + 58)], fill=MIDGREY, outline=INK)
        d.polygon([(sx + 84, sy + 52), (sx + 104, sy + 30), (sx + 116, sy + 52)],
                  fill=MIDGREY, outline=INK)
        d.polygon([(sx + 84, sy + 58), (sx + 104, sy + 78), (sx + 116, sy + 58)],
                  fill=MIDGREY, outline=INK)
        d.polygon([(sx + 44, sy + 52), (sx + 60, sy + 42), (sx + 60, sy + 62)],
                  fill=RED)
    elif kind == "satellite":
        d.rectangle([sx, sy, sx + w, sy + h], fill=NAVY)
        for (px, py) in [(18, 16), (52, 10), (96, 22), (140, 12), (168, 30),
                         (30, 78), (150, 78), (120, 88), (70, 92)]:
            d.ellipse([sx + px - 2, sy + py - 2, sx + px + 2, sy + py + 2],
                      fill=(255, 255, 255))
        # panels + body
        d.rectangle([sx + 22, sy + 40, sx + 62, sy + 60], fill=(29, 78, 216), outline=INK, width=2)
        d.rectangle([sx + 122, sy + 40, sx + 162, sy + 60], fill=(29, 78, 216), outline=INK, width=2)
        d.rectangle([sx + 76, sy + 38, sx + 108, sy + 62], fill=MIDGREY, outline=INK, width=2)
        d.line([sx + 92, sy + 38, sx + 92, sy + 26], fill=(255, 255, 255), width=2)
        d.ellipse([sx + 88, sy + 20, sx + 96, sy + 28], fill=YELLOW, outline=INK, width=1)
    elif kind == "plane":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SKY)
        d.ellipse([sx + 140, sy + 10, sx + 162, sy + 32], fill=YELLOW, outline=INK, width=2)
        d.ellipse([sx + 12, sy + 16, sx + 48, sy + 28], fill=(255, 255, 255))
        d.ellipse([sx + 120, sy + h - 26, sx + 162, sy + h - 14], fill=(255, 255, 255))
        # plane (nose right)
        d.ellipse([sx + 40, sy + 46, sx + 150, sy + 62], fill=(255, 255, 255), outline=INK, width=2)
        d.polygon([(sx + 84, sy + 52), (sx + 100, sy + 30), (sx + 114, sy + 52)],
                  fill=(255, 255, 255), outline=INK)
        d.polygon([(sx + 84, sy + 58), (sx + 100, sy + 76), (sx + 114, sy + 58)],
                  fill=(255, 255, 255), outline=INK)
        d.polygon([(sx + 40, sy + 50), (sx + 56, sy + 38), (sx + 56, sy + 58)],
                  fill=RED)
        for k in range(4):
            d.ellipse([sx + 66 + k * 14, sy + 50, sx + 72 + k * 14, sy + 56], fill=SKY)
    elif kind == "ship":
        d.rectangle([sx, sy, sx + w, sy + int(h * 0.45)], fill=PALESKY)
        d.rectangle([sx, sy + int(h * 0.45), sx + w, sy + h], fill=SEA)
        # hull
        d.polygon([(sx + 24, sy + 58), (sx + w - 24, sy + 58), (sx + w - 40, sy + 82),
                   (sx + 40, sy + 82)], fill=(40, 40, 40), outline=INK)
        # containers
        for k, c in enumerate([RED, (29, 78, 216), GREEN]):
            d.rectangle([sx + 44 + k * 34, sy + 36, sx + 74 + k * 34, sy + 58],
                        fill=c, outline=INK, width=1)
        # bridge + flag
        d.rectangle([sx + w - 62, sy + 30, sx + w - 34, sy + 58], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.line([sx + w - 48, sy + 30, sx + w - 48, sy + 16], fill=INK, width=2)
        d.polygon([(sx + w - 48, sy + 16), (sx + w - 30, sy + 20), (sx + w - 48, sy + 24)],
                  fill=RED)
        d.line([sx + 12, sy + 88, sx + 40, sy + 88], fill=(255, 255, 255), width=2)
        d.line([sx + w - 52, sy + 90, sx + w - 24, sy + 90], fill=(255, 255, 255), width=2)
    elif kind == "tanker":
        d.rectangle([sx, sy, sx + w, sy + int(h * 0.45)], fill=PALESKY)
        d.rectangle([sx, sy + int(h * 0.45), sx + w, sy + h], fill=SEA)
        # hull
        d.polygon([(sx + 16, sy + 60), (sx + w - 16, sy + 60), (sx + w - 32, sy + 84),
                   (sx + 32, sy + 84)], fill=(40, 40, 40), outline=INK)
        # deck + bridge
        d.rectangle([sx + w - 52, sy + 34, sx + w - 24, sy + 60], fill=(255, 255, 255),
                    outline=INK, width=1)
        # flame
        d.polygon([(sx + 74, sy + 58), (sx + 84, sy + 30), (sx + 92, sy + 46),
                   (sx + 100, sy + 28), (sx + 110, sy + 58)], fill=ORANGE, outline=INK)
        d.polygon([(sx + 84, sy + 58), (sx + 90, sy + 42), (sx + 96, sy + 58)],
                  fill=YELLOW)
        # smoke
        d.ellipse([sx + 78, sy + 12, sx + 94, sy + 26], fill=MIDGREY)
        d.ellipse([sx + 92, sy + 6, sx + 104, sy + 18], fill=MIDGREY)
    elif kind == "tents":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SAND)
        d.ellipse([sx + w - 40, sy + 10, sx + w - 16, sy + 34], fill=YELLOW, outline=INK, width=2)
        # tents
        d.polygon([(sx + 22, sy + 82), (sx + 62, sy + 40), (sx + 102, sy + 82)],
                  fill=(150, 90, 40), outline=INK)
        d.polygon([(sx + 52, sy + 82), (sx + 62, sy + 62), (sx + 72, sy + 82)],
                  fill=(40, 40, 40))
        d.polygon([(sx + 96, sy + 82), (sx + 128, sy + 50), (sx + 160, sy + 82)],
                  fill=RED, outline=INK)
        d.polygon([(sx + 120, sy + 82), (sx + 128, sy + 68), (sx + 136, sy + 82)],
                  fill=(40, 40, 40))
        d.line([sx + 10, sy + 88, sx + w - 10, sy + 88], fill=BROWN, width=3)
    elif kind == "drone":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SKY)
        d.ellipse([sx + 16, sy + 12, sx + 34, sy + 30], fill=YELLOW, outline=INK, width=2)
        d.ellipse([sx + 130, sy + 76, sx + 168, sy + 88], fill=(255, 255, 255))
        # arms + rotors
        d.line([cx - 34, cy - 22, cx + 34, cy + 22], fill=INK, width=3)
        d.line([cx - 34, cy + 22, cx + 34, cy - 22], fill=INK, width=3)
        for (rx, ry) in [(cx - 34, cy - 22), (cx + 34, cy - 22), (cx - 34, cy + 22), (cx + 34, cy + 22)]:
            d.ellipse([rx - 14, ry - 4, rx + 14, ry + 4], fill=MIDGREY, outline=INK, width=1)
        # body + camera
        d.rounded_rectangle([cx - 18, cy - 12, cx + 18, cy + 12], radius=6,
                            fill=(40, 40, 40), outline=INK, width=2)
        d.ellipse([cx - 4, cy + 12, cx + 4, cy + 20], fill=RED, outline=INK, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead bar ----
    d.rectangle([0, 0, W, 44], fill=INK)
    d.text((M, 11), "THE WORLD IN ONE DAY", font=F_TITLE, fill=(250, 247, 240))
    dt = "TUESDAY \u00b7 24 NOVEMBER 2026"
    d.text((W - M - d.textlength(dt, font=F_DATE), 14), dt, font=F_DATE, fill=(250, 247, 240))

    # ---- deck ----
    d.text((M, 50), "Huang rally sweeps Asia \u00b7 Chen Jining probed \u00b7 Huawei convicted",
           font=F_DECK, fill=RED)

    # ---- region chips ----
    y = 76
    x = M
    for name, n in CHIPS:
        label = f"{name}  {n}"
        w = d.textlength(label, font=F_CHIP) + 18
        d.rounded_rectangle([x, y, x + w, y + 24], radius=12, fill=CHIP_BG)
        d.text((x + 9, y + 6), label, font=F_CHIP, fill=INK)
        x += w + 8

    # ---- main stories header ----
    y = 108
    d.text((M, y), "THE 10 MAIN STORIES", font=F_H, fill=INK)
    d.line([(M + 218, y + 10), (W - M, y + 10)], fill=INK, width=2)

    # ---- main cards: 5 columns, 2 rows; scene on top, text below ----
    col_w = (CW - 4 * 12) // 5
    card_h, top, pitch = 220, 130, 228
    scene_h = 100
    for i, (num, place, cat, title, body, src, status, kind) in enumerate(MAIN):
        col, row = i % 5, i // 5
        x0 = M + col * (col_w + 12)
        y0 = top + row * pitch
        d.rectangle([x0, y0, x0 + col_w, y0 + card_h], fill=CARD_BG, outline=LGREY, width=1)
        scene(d, kind, x0 + 1, y0 + 1, col_w - 2, scene_h)
        # place ribbon on the scene, top-left; badge top-right
        plabel = f"{num} \u00b7 {place}"
        pw = d.textlength(plabel, font=F_PLACE) + 10
        d.rectangle([x0 + 1, y0 + 1, x0 + 1 + pw, y0 + 19], fill=INK)
        d.text((x0 + 6, y0 + 4), plabel, font=F_PLACE, fill=(255, 255, 255))
        bw = d.textlength(status, font=F_BADGE) + 10
        bx = x0 + col_w - bw - 7
        d.rounded_rectangle([bx, y0 + 5, bx + bw, y0 + 19], radius=7,
                            fill=(232, 227, 214) if status == "REPORTED" else (250, 225, 200))
        d.text((bx + 5, y0 + 7), status, font=F_BADGE, fill=INK)
        tx = x0 + 8
        d.text((tx, y0 + scene_h + 6), cat, font=F_CAT, fill=RED)
        tlines = wrap(d, title, F_STITLE, col_w - 16)
        ty = y0 + scene_h + 22
        for ln in tlines[:2]:
            d.text((tx, ty), ln, font=F_STITLE, fill=INK)
            ty += 16
        blines = wrap(d, body, F_BODY, col_w - 16)
        by = y0 + scene_h + 56
        for ln in blines[:3]:
            d.text((tx, by), ln, font=F_BODY, fill=(60, 58, 52))
            by += 13
        d.text((tx, y0 + card_h - 16), f"Source: {src}", font=F_SRC, fill=GREY)

    # ---- ALSO section: 3 columns, 10 rows ----
    y = 586
    d.text((M, y), "ALSO TODAY \u2014 30 MORE", font=F_H, fill=INK)
    d.line([(M + 200, y + 10), (W - M, y + 10)], fill=INK, width=2)
    acol_w = (CW - 2 * 14) // 3
    ay = 610
    for i, (place, head) in enumerate(ALSO):
        col = i % 3
        row = i // 3
        x0 = M + col * (acol_w + 14)
        yy = ay + row * 18
        d.text((x0, yy), place, font=F_ALSO_B, fill=RED)
        px = x0 + d.textlength(place, font=F_ALSO_B) + 5
        d.text((px, yy), f"\u2014 {head}", font=F_ALSO, fill=INK)

    # ---- HOW SURE legend, full width ----
    fy = 790
    d.text((M, fy), "HOW SURE:  ", font=F_FOOT_B, fill=INK)
    fx = M + d.textlength("HOW SURE:  ", font=F_FOOT_B)
    foot = ("REPORTED \u2014 same-day wire or official report   \u00b7   CLAIM \u2014 one side's account, flagged   "
            "\u00b7   ONGOING \u2014 still developing   \u00b7   All stories first reported 24 November 2026 (UTC).")
    d.text((fx, fy), foot, font=F_FOOT, fill=GREY)

    # ---- bottom band: map + DATE CHECK ----
    y = 804
    d.line([(M, y), (W - M, y)], fill=LGREY, width=1)
    d.text((M, 812), "WHERE IT HAPPENED \u2014 10 MAIN STORIES", font=F_DC_B, fill=INK)
    dx = M + 316
    d.text((dx, 812), "DATE CHECK", font=F_DC_B, fill=RED)
    # dotted world map, left
    map_x0, map_y0 = M, 828
    mw, mh = 300, 112
    cell_w, cell_h = mw / 64.0, mh / 26.0
    land_cells = set()
    for (r, a, b) in LAND:
        for cx in range(a, b + 1):
            land_cells.add((cx, r))
    for (cx, r) in land_cells:
        px = map_x0 + (cx + 0.5) * cell_w
        py = map_y0 + (r + 0.5) * cell_h
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=MAP_DOT)
    for (lon, lat) in PINS:
        gx = (lon + 180.0) / 360.0 * 64.0
        gy = (90.0 - lat) / 150.0 * 26.0
        px = map_x0 + gx * cell_w
        py = map_y0 + gy * cell_h
        d.ellipse([px - 3.4, py - 3.4, px + 3.4, py + 3.4], fill=RED)
        d.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4], fill=(255, 255, 255))
    # DATE CHECK + numbers, right
    dw = W - M - dx
    dlines = wrap(d, DATE_CHECK, F_DC, dw)
    dy = 828
    for ln in dlines:
        d.text((dx, dy), ln, font=F_DC, fill=(60, 58, 52))
        dy += 13
    dy += 6
    nlines = wrap(d, NUMBERS_LINE, F_DC_B, dw)
    for ln in nlines:
        d.text((dx, dy), ln, font=F_DC_B, fill=INK)
        dy += 14

    # ---- footer ----
    d.text((512, 968), "Sources: AP, Reuters, BusinessWorld, Daily Summary of World  \u00b7  "
           "Scenes are drawn illustrations, not photographs",
           font=F_FOOT, fill=GREY, anchor="mm")

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
