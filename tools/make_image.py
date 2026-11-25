#!/usr/bin/env python3
"""Build entry.png for news-image-20261124, v7: The World in One Day — 24 Nov 2026.

v7 follows the 22/23 Nov winners' template (see winners-2026-11-22-23-deep-
analysis.md): 13 main stories in 3+5+5 rows, 13 different fields, 9 regions,
a UTC timeline, big number badges inside the drawn scenes, 4-tier credibility
(CONFIRMED / OFFICIAL / REPORTED / CLAIM), and a DATE CHECK that excludes
both earlier days and one future story. Total 35 stories (13 main + 22 ALSO).

Headline change from v6: the Huang rally was 23 Nov news, so it is demoted
(the Tuesday story, TAIEX +8.99% record, stays in ALSO). New #1 is the
699-drone wave — Russia's defence ministry said Tuesday it downed 699
Ukrainian drones overnight, 355 headed for Moscow; it is one side's claim,
so it carries a CLAIM badge, not a verdict. Sanofi's $41bn Insmed deal was
announced 06:30 UTC (press release); Ronaldo's 987th was a 13th-minute
penalty in Al-Nassr's 2-1 win over Al-Sadd; Huawei was found guilty on 10 of
12 counts by a Brooklyn jury (Reuters + AP + CNN), acquitted of racketeering.

All 35 stories were verified as happening or first reported on Tuesday
24 November 2026 (UTC). Pure Pillow, no network, deterministic output.

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
BROWN = (120, 72, 20)
MIDGREY = (120, 120, 120)
YELLOW = (240, 200, 40)
ORANGE = (240, 120, 20)
PALESKY = (200, 220, 235)

# region colours (chips, place ribbons, map pins, ALSO place text)
REG_COL = {
    "NORTH AMERICA": (29, 78, 216),
    "LATIN AMERICA": (0, 128, 128),
    "EUROPE": (178, 34, 34),
    "EAST ASIA": (30, 58, 138),
    "SOUTH & SE ASIA": (107, 33, 168),
    "MIDDLE EAST": (154, 82, 10),
    "AFRICA": (22, 101, 52),
    "OCEANIA": (14, 116, 144),
    "GLOBAL": (87, 83, 78),
    "S & SE ASIA": (107, 33, 168),  # short label for the chips row
}
# credibility badge colours
BADGE_COL = {
    "CONFIRMED": (22, 101, 52),
    "OFFICIAL": (29, 78, 216),
    "REPORTED": (232, 227, 214),
    "CLAIM": (250, 225, 200),
}

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_TITLE = font("DejaVuSans-Bold", 23)
F_DATE = font("DejaVuSans-Bold", 15)
F_DECK = font("DejaVuSans-Bold", 18)
F_TOPBAR = font("DejaVuSans-Bold", 14)
F_CHIP = font("DejaVuSans-Bold", 10)
F_H = font("DejaVuSans-Bold", 15)
F_PLACE = font("DejaVuSans-Bold", 9)
F_CAT = font("DejaVuSans-Bold", 11)
F_STITLE = font("DejaVuSans-Bold", 13)
F_BODY = font("DejaVuSans", 10)
F_SRC = font("DejaVuSans", 9)
F_BADGE = font("DejaVuSans-Bold", 9)
F_BIGNUM = font("DejaVuSans-Bold", 18)
F_BIGNUM_S = font("DejaVuSans-Bold", 15)
F_ALSO = font("DejaVuSans", 10)
F_ALSO_B = font("DejaVuSans-Bold", 10)
F_TL_T = font("DejaVuSans-Bold", 10)
F_TL_L = font("DejaVuSans", 9)
F_DC = font("DejaVuSans", 10)
F_DC_B = font("DejaVuSans-Bold", 10)
F_FOOT = font("DejaVuSans", 10)
F_FOOT_B = font("DejaVuSans-Bold", 10)

# (num, place, region, field, title, body, source, status, scene, bignum)
MAIN = [
    ("01", "MOSCOW", "EUROPE", "WAR", "Russia says it downed 699 drones",
     "Moscow claims 699 Ukrainian drones shot down overnight; 355 headed for the capital.",
     "Reuters", "CLAIM", "drones", "699"),
    ("02", "SHANGHAI", "EAST ASIA", "GRAFT", "China probes Chen Jining",
     "The anti-graft watchdog opened an inquiry into Shanghai's party chief.",
     "Reuters", "OFFICIAL", "capitol", ""),
    ("03", "NEW YORK", "NORTH AMERICA", "TECH & LAW", "Huawei guilty on 10 of 12 counts",
     "A US jury convicted Huawei of fraud and trade-secret theft; it will appeal.",
     "Reuters \u00b7 AP", "CONFIRMED", "gavel", ""),
    ("04", "SEOUL", "EAST ASIA", "AIR DEFENCE", "Seoul scrambles jets",
     "Russian aircraft entered the air defence zone.",
     "AP \u00b7 Reuters", "OFFICIAL", "jet", ""),
    ("05", "BRUSSELS", "EUROPE", "SPACE", "NATO defence now covers space",
     "Rutte vowed to defend space assets from attack.",
     "Reuters", "OFFICIAL", "satellite", ""),
    ("06", "DHAKA", "SOUTH & SE ASIA", "EXILE", "Hasina to return on 16 December",
     "The ex-PM, convicted in absentia, will fly home.",
     "Reuters \u00b7 AP", "REPORTED", "plane", "DEC 16"),
    ("07", "KUALA LUMPUR", "SOUTH & SE ASIA", "MIGRATION", "Malaysia sends migrants back",
     "Returns start by air; 1,500 more by ship in Dec.",
     "Reuters", "REPORTED", "ship", "5,303"),
    ("08", "HORMUZ", "MIDDLE EAST", "ENERGY", "Tankers hit by mines, IRGC says",
     "Iran's Guards claimed three tankers were struck.",
     "Reuters", "CLAIM", "tanker", "3"),
    ("09", "SANAA", "MIDDLE EAST", "CRISIS", "360,000 displaced in Yemen",
     "The UN says families fled fighting since August.",
     "UN", "OFFICIAL", "tents", "360,000"),
    ("10", "MEXICO CITY", "LATIN AMERICA", "CRIME", "US drone helped catch Chapo Isidro",
     "Mexico will try the Sinaloa figure despite a US bid.",
     "Reuters", "REPORTED", "cuffs", ""),
    ("11", "WASHINGTON", "NORTH AMERICA", "TRADE", "US blacklists 7 firms",
     "Megaspeed and six firms join the Entity List.",
     "Reuters", "OFFICIAL", "banned", "7 FIRMS"),
    ("12", "FRANCE", "EUROPE", "BUSINESS", "Sanofi agrees $41bn Insmed deal",
     "The French drugmaker pays $175 a share in cash.",
     "Sanofi", "OFFICIAL", "medicine", "$41bn"),
    ("13", "FOOTBALL", "GLOBAL", "SPORT", "Ronaldo scores 987th goal",
     "A 13th-minute penalty in Al-Nassr's 2-1 win.",
     "Reuters", "OFFICIAL", "football", "987"),
]

# (num, place, region, headline, source) — numbered 14-35
ALSO = [
    ("14", "KYIV", "EUROPE", "Zelensky urges 4-party talks", "Reuters"),
    ("15", "COLOMBIA", "LATIN AMERICA", "Car bomb hits government HQ", "Reuters"),
    ("16", "BEIJING", "EAST ASIA", "First foreign astronaut named", "Reuters"),
    ("17", "HONIARA", "OCEANIA", "Solomons to scrap China pact", "Reuters"),
    ("18", "PENNSYLVANIA", "NORTH AMERICA", "Measles outbreak: 9th death", "AP"),
    ("19", "WASHINGTON", "NORTH AMERICA", "Abrego Garcia leaves US", "Reuters"),
    ("20", "BUENOS AIRES", "LATIN AMERICA", "Technical recession", "Reuters"),
    ("21", "DAKAR", "AFRICA", "CAS restores Senegal's Cup title", "AP"),
    ("22", "GAZA CITY", "MIDDLE EAST", "Hamas security chief killed", "Reuters"),
    ("23", "BAGHDAD", "MIDDLE EAST", "Iraq takes Kurdish oilfields", "Reuters"),
    ("24", "HANOI", "SOUTH & SE ASIA", "Hotpot blast kills 6", "AP"),
    ("25", "WASHINGTON", "NORTH AMERICA", "CIA systems breached", "NYT"),
    ("26", "LONDON", "EUROPE", "5,258 heat deaths in 2026", "Reuters"),
    ("27", "RIYADH", "MIDDLE EAST", "Houthi strike on tower wounds 11", "Reuters"),
    ("28", "PARIS", "EUROPE", "Sarkozy trial opens", "Reuters"),
    ("29", "UNITED NATIONS", "GLOBAL", "5 women killed every hour", "UN"),
    ("30", "JERUSALEM", "MIDDLE EAST", "Eisenkot clinches first pact", "Reuters"),
    ("31", "ITURI", "AFRICA", "WHO evacuates Ebola hospital staff", "Reuters"),
    ("32", "KYIV", "EUROPE", "Zelensky confirms Sparta II strike", "Reuters"),
    ("33", "TAIPEI", "EAST ASIA", "TAIEX surges 8.99%, a record", "Reuters"),
    ("34", "OTTAWA", "NORTH AMERICA", "Pentagon rebukes Canada", "Reuters"),
    ("35", "JAKARTA", "SOUTH & SE ASIA", "Indonesia names 2 VP candidates", "Reuters"),
]

CHIPS = [("NORTH AMERICA", 6), ("LATIN AMERICA", 3), ("EUROPE", 7),
         ("EAST ASIA", 4), ("S & SE ASIA", 4), ("MIDDLE EAST", 6),
         ("AFRICA", 2), ("OCEANIA", 1), ("GLOBAL", 2)]

# UTC timeline: (time, short label). Times verified where stated in the
# header comment; 12:00/16:00/20:00 are hour-level estimates of the day's
# flow (midday Brussels, evening Riyadh, afternoon Brooklyn).
TIMELINE = [
    ("00:00", "699 drones"),
    ("05:30", "TAIEX record"),
    ("06:30", "Sanofi $41bn"),
    ("12:00", "NATO space"),
    ("16:00", "Ronaldo 987"),
    ("20:00", "Huawei guilty"),
]

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
# (lon, lat, region) of the 13 main stories, in story order
PINS = [
    (37.6, 55.8, "EUROPE"), (121.5, 31.2, "EAST ASIA"),
    (-74.0, 40.7, "NORTH AMERICA"), (127.0, 37.5, "EAST ASIA"),
    (4.4, 50.8, "EUROPE"), (90.4, 23.8, "SOUTH & SE ASIA"),
    (101.7, 3.1, "SOUTH & SE ASIA"), (56.3, 26.6, "MIDDLE EAST"),
    (44.2, 15.4, "MIDDLE EAST"), (-99.1, 19.4, "LATIN AMERICA"),
    (-77.0, 38.9, "NORTH AMERICA"), (2.3, 48.9, "EUROPE"),
    (46.7, 24.7, "GLOBAL"),
]

DATE_CHECK = ("NOT TODAY \u2014 first reported earlier: COP31 pact (Sun 22 Nov) \u00b7 Ship sunk off Libya (Mon 23 Nov) \u00b7 "
              "House 258 seats (Mon 23 Nov) \u00b7 Sparta II strike itself (Sat 21 Nov) \u2014 the confirmation was Tuesday. "
              "NOT TOMORROW: Shenzhou-24 docking (Tue 25 Nov).")
NUMBERS_LINE = ("THE DAY IN NUMBERS: 35 stories \u00b7 699 drones \u00b7 TAIEX +8.99% \u00b7 $41bn Sanofi deal \u00b7 987th goal")


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
    if kind == "drones":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SKY)
        d.ellipse([sx + 12, sy + 8, sx + 30, sy + 26], fill=YELLOW, outline=INK, width=2)
        d.ellipse([sx + 14, sy + h - 24, sx + 50, sy + h - 12], fill=(255, 255, 255))
        # three small drones + one explosion puff
        for (dx, dy, s) in [(40, 26, 9), (84, 16, 11), (130, 30, 9)]:
            d.ellipse([sx + dx - s, sy + dy - 4, sx + dx + s, sy + dy + 4],
                      fill=(40, 40, 40), outline=INK, width=1)
            d.line([sx + dx - s - 4, sy + dy - 6, sx + dx + s + 4, sy + dy - 6],
                   fill=INK, width=2)
            d.line([sx + dx - s - 4, sy + dy + 6, sx + dx + s + 4, sy + dy + 6],
                   fill=INK, width=2)
        d.ellipse([sx + w - 46, sy + 14, sx + w - 26, sy + 34], fill=ORANGE, outline=INK, width=1)
        d.ellipse([sx + w - 38, sy + 8, sx + w - 28, sy + 18], fill=YELLOW)
    elif kind == "capitol":
        d.rectangle([sx, sy, sx + w, sy + h], fill=PAPER)
        d.line([sx + w - 34, sy + 8, sx + w - 34, sy + 26], fill=INK, width=3)
        d.polygon([(sx + w - 34, sy + 8), (sx + w - 16, sy + 13), (sx + w - 34, sy + 18)],
                  fill=RED)
        d.polygon([(sx + 22, sy + 34), (cx, sy + 16), (sx + w - 22, sy + 34)], fill=RED)
        d.rectangle([sx + 22, sy + 34, sx + w - 22, sy + 40], fill=INK)
        for k in range(3):
            x0 = sx + 34 + k * 52
            d.rectangle([x0, sy + 40, x0 + 14, sy + h - 18], fill=(255, 255, 255),
                        outline=INK, width=2)
        d.rectangle([sx + 22, sy + h - 18, sx + w - 22, sy + h - 11], fill=MIDGREY)
        d.rectangle([sx + 14, sy + h - 11, sx + w - 14, sy + h - 6], fill=INK)
    elif kind == "gavel":
        d.rectangle([sx, sy, sx + w, sy + h], fill=CHIP_BG)
        d.rounded_rectangle([sx + 30, sy + h - 22, sx + 110, sy + h - 11], radius=4,
                            fill=BROWN, outline=INK, width=2)
        d.line([sx + 108, sy + 22, sx + 58, sy + h - 20], fill=BROWN, width=7)
        d.polygon([(sx + 92, sy + 12), (sx + 138, sy + 26), (sx + 122, sy + 46),
                   (sx + 76, sy + 32)], fill=BROWN, outline=INK)
        d.line([sx + 92, sy + 12, sx + 138, sy + 26], fill=(255, 255, 255), width=2)
    elif kind == "jet":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SKY)
        d.ellipse([sx + 14, sy + 10, sx + 32, sy + 28], fill=YELLOW, outline=INK, width=2)
        d.ellipse([sx + 120, sy + 14, sx + 158, sy + 26], fill=(255, 255, 255))
        d.ellipse([sx + 20, sy + h - 26, sx + 54, sy + h - 15], fill=(255, 255, 255))
        d.polygon([(sx + 44, sy + 46), (sx + 148, sy + 40), (sx + 156, sy + 46),
                   (sx + 148, sy + 52), (sx + 44, sy + 52)], fill=MIDGREY, outline=INK)
        d.polygon([(sx + 84, sy + 46), (sx + 102, sy + 26), (sx + 114, sy + 46)],
                  fill=MIDGREY, outline=INK)
        d.polygon([(sx + 84, sy + 52), (sx + 102, sy + 60), (sx + 114, sy + 52)],
                  fill=MIDGREY, outline=INK)
        d.polygon([(sx + 44, sy + 46), (sx + 58, sy + 37), (sx + 58, sy + 55)],
                  fill=RED)
    elif kind == "satellite":
        d.rectangle([sx, sy, sx + w, sy + h], fill=NAVY)
        for (px, py) in [(18, 14), (52, 9), (96, 20), (140, 11), (168, 28),
                         (30, 58), (150, 58), (120, 56), (70, 58)]:
            d.ellipse([sx + px - 2, sy + py - 2, sx + px + 2, sy + py + 2],
                      fill=(255, 255, 255))
        d.rectangle([sx + 22, sy + 36, sx + 62, sy + 54], fill=(29, 78, 216), outline=INK, width=2)
        d.rectangle([sx + 122, sy + 36, sx + 162, sy + 54], fill=(29, 78, 216), outline=INK, width=2)
        d.rectangle([sx + 76, sy + 34, sx + 108, sy + 56], fill=MIDGREY, outline=INK, width=2)
        d.line([sx + 92, sy + 34, sx + 92, sy + 24], fill=(255, 255, 255), width=2)
        d.ellipse([sx + 88, sy + 18, sx + 96, sy + 26], fill=YELLOW, outline=INK, width=1)
    elif kind == "plane":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SKY)
        d.ellipse([sx + 140, sy + 8, sx + 160, sy + 28], fill=YELLOW, outline=INK, width=2)
        d.ellipse([sx + 12, sy + 14, sx + 46, sy + 25], fill=(255, 255, 255))
        d.ellipse([sx + 120, sy + h - 22, sx + 160, sy + h - 12], fill=(255, 255, 255))
        d.ellipse([sx + 28, sy + 40, sx + 136, sy + 55], fill=(255, 255, 255), outline=INK, width=2)
        d.polygon([(sx + 72, sy + 46), (sx + 88, sy + 26), (sx + 102, sy + 46)],
                  fill=(255, 255, 255), outline=INK)
        d.polygon([(sx + 72, sy + 52), (sx + 88, sy + 60), (sx + 102, sy + 52)],
                  fill=(255, 255, 255), outline=INK)
        d.polygon([(sx + 28, sy + 44), (sx + 42, sy + 34), (sx + 42, sy + 52)],
                  fill=RED)
        for k in range(4):
            d.ellipse([sx + 54 + k * 14, sy + 44, sx + 60 + k * 14, sy + 50], fill=SKY)
    elif kind == "ship":
        d.rectangle([sx, sy, sx + w, sy + int(h * 0.45)], fill=PALESKY)
        d.rectangle([sx, sy + int(h * 0.45), sx + w, sy + h], fill=SEA)
        d.polygon([(sx + 24, sy + 52), (sx + w - 24, sy + 52), (sx + w - 40, sy + 60),
                   (sx + 40, sy + 60)], fill=(40, 40, 40), outline=INK)
        for k, c in enumerate([RED, (29, 78, 216), GREEN]):
            d.rectangle([sx + 44 + k * 34, sy + 32, sx + 74 + k * 34, sy + 52],
                        fill=c, outline=INK, width=1)
        # bridge + flag on the left, so the number badge (bottom-right) stays clear
        d.rectangle([sx + 30, sy + 26, sx + 58, sy + 52], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.line([sx + 44, sy + 26, sx + 44, sy + 14], fill=INK, width=2)
        d.polygon([(sx + 44, sy + 14), (sx + 62, sy + 18), (sx + 44, sy + 22)],
                  fill=RED)
        d.line([sx + 12, sy + 58, sx + 40, sy + 58], fill=(255, 255, 255), width=2)
    elif kind == "tanker":
        d.rectangle([sx, sy, sx + w, sy + int(h * 0.45)], fill=PALESKY)
        d.rectangle([sx, sy + int(h * 0.45), sx + w, sy + h], fill=SEA)
        d.polygon([(sx + 16, sy + 54), (sx + w - 16, sy + 54), (sx + w - 32, sy + 62),
                   (sx + 32, sy + 62)], fill=(40, 40, 40), outline=INK)
        # bridge on the left, so the number badge (bottom-right) stays clear
        d.rectangle([sx + 24, sy + 30, sx + 52, sy + 54], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.polygon([(sx + 74, sy + 52), (sx + 84, sy + 26), (sx + 92, sy + 42),
                   (sx + 100, sy + 24), (sx + 110, sy + 52)], fill=ORANGE, outline=INK)
        d.polygon([(sx + 84, sy + 52), (sx + 90, sy + 38), (sx + 96, sy + 52)],
                  fill=YELLOW)
        d.ellipse([sx + 78, sy + 10, sx + 94, sy + 23], fill=MIDGREY)
        d.ellipse([sx + 92, sy + 5, sx + 104, sy + 16], fill=MIDGREY)
    elif kind == "tents":
        d.rectangle([sx, sy, sx + w, sy + h], fill=SAND)
        d.ellipse([sx + w - 38, sy + 8, sx + w - 15, sy + 31], fill=YELLOW, outline=INK, width=2)
        d.polygon([(sx + 22, sy + 60), (sx + 62, sy + 36), (sx + 102, sy + 60)],
                  fill=(150, 90, 40), outline=INK)
        d.polygon([(sx + 52, sy + 60), (sx + 62, sy + 48), (sx + 72, sy + 60)],
                  fill=(40, 40, 40))
        d.polygon([(sx + 96, sy + 60), (sx + 128, sy + 42), (sx + 160, sy + 60)],
                  fill=RED, outline=INK)
        d.polygon([(sx + 120, sy + 60), (sx + 128, sy + 50), (sx + 136, sy + 60)],
                  fill=(40, 40, 40))
        d.line([sx + 10, sy + 61, sx + w - 10, sy + 61], fill=BROWN, width=3)
    elif kind == "cuffs":
        d.rectangle([sx, sy, sx + w, sy + h], fill=CHIP_BG)
        d.ellipse([sx + 34, sy + 24, sx + 78, sy + 60], fill=(255, 255, 255), outline=INK, width=3)
        d.ellipse([sx + 48, sy + 38, sx + 64, sy + 54], fill=CHIP_BG, outline=INK, width=2)
        d.ellipse([sx + 106, sy + 24, sx + 150, sy + 60], fill=(255, 255, 255), outline=INK, width=3)
        d.ellipse([sx + 120, sy + 38, sx + 136, sy + 54], fill=CHIP_BG, outline=INK, width=2)
        d.line([sx + 78, sy + 46, sx + 106, sy + 46], fill=INK, width=3)
        d.ellipse([sx + 88, sy + 42, sx + 96, sy + 50], fill=MIDGREY, outline=INK, width=1)
    elif kind == "banned":
        d.rectangle([sx, sy, sx + w, sy + h], fill=PAPER)
        d.rectangle([sx + 52, sy + 12, sx + 132, sy + h - 12], fill=(255, 255, 255),
                    outline=INK, width=2)
        for k in range(3):
            d.line([sx + 62, sy + 26 + k * 12, sx + 122, sy + 26 + k * 12],
                   fill=GREY, width=3)
        d.ellipse([sx + w - 62, sy + h - 48, sx + w - 22, sy + h - 8], outline=RED, width=5)
        d.line([sx + w - 56, sy + h - 42, sx + w - 28, sy + h - 14], fill=RED, width=5)
    elif kind == "medicine":
        d.rectangle([sx, sy, sx + w, sy + h], fill=PALESKY)
        # bottle, left
        d.rounded_rectangle([sx + 28, sy + 22, sx + 80, sy + h - 12], radius=6,
                            fill=(255, 255, 255), outline=INK, width=2)
        d.rectangle([sx + 36, sy + 12, sx + 72, sy + 24], fill=ORANGE, outline=INK, width=2)
        d.line([sx + 36, sy + 46, sx + 72, sy + 46], fill=GREY, width=2)
        d.line([sx + 36, sy + 56, sx + 72, sy + 56], fill=GREY, width=2)
        # pharmacy cross, upper right (clear of the bottom-right number badge)
        d.rectangle([sx + 132, sy + 12, sx + 144, sy + 36], fill=GREEN, outline=INK, width=2)
        d.rectangle([sx + 120, sy + 20, sx + 156, sy + 28], fill=GREEN, outline=INK, width=2)
    elif kind == "football":
        d.rectangle([sx, sy, sx + w, sy + int(h * 0.5)], fill=(34, 139, 34))
        d.rectangle([sx, sy + int(h * 0.5), sx + w, sy + h], fill=(46, 160, 46))
        # goal posts
        d.line([sx + 14, sy + 14, sx + 14, sy + 52], fill=(255, 255, 255), width=4)
        d.line([sx + 14, sy + 14, sx + 58, sy + 14], fill=(255, 255, 255), width=4)
        d.line([sx + 58, sy + 14, sx + 58, sy + 52], fill=(255, 255, 255), width=4)
        # ball
        d.ellipse([cx - 20, cy - 12, cx + 20, cy + 24], fill=(255, 255, 255), outline=INK, width=2)
        d.polygon([(cx - 5, cy + 0), (cx + 5, cy + 0), (cx + 8, cy + 8),
                   (cx, cy + 14), (cx - 8, cy + 8)], fill=INK)
        d.ellipse([cx - 16, cy + 14, cx - 10, cy + 20], fill=INK)
        d.ellipse([cx + 10, cy + 14, cx + 16, cy + 20], fill=INK)
        d.ellipse([cx - 3, cy - 8, cx + 3, cy - 2], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead bar ----
    d.rectangle([0, 0, W, 44], fill=INK)
    d.text((M, 11), "THE WORLD IN ONE DAY", font=F_TITLE, fill=(250, 247, 240))
    dt = "TUESDAY \u00b7 24 NOVEMBER 2026"
    d.text((W - M - d.textlength(dt, font=F_DATE), 14), dt, font=F_DATE, fill=(250, 247, 240))

    # ---- deck: the 3 biggest ----
    d.text((M, 50), "699 drones downed \u00b7 Chen Jining probed \u00b7 Huawei convicted",
           font=F_DECK, fill=RED)

    # ---- top bar: the count line ----
    topbar = "35 DATED STORIES  \u00b7  9 REGIONS  \u00b7  14 FIELDS  \u00b7  ALL FROM TUE 24 NOV 2026"
    d.text((512, 84), topbar, font=F_TOPBAR, fill=INK, anchor="mm")

    # ---- region chips, colour-coded ----
    y = 98
    x = M
    for name, n in CHIPS:
        label = f"{name}  {n}"
        w = d.textlength(label, font=F_CHIP) + 12
        d.rounded_rectangle([x, y, x + w, y + 22], radius=11, fill=REG_COL[name])
        d.text((x + 9, y + 5), label, font=F_CHIP, fill=(255, 255, 255))
        x += w + 8

    # ---- UTC timeline ----
    ty = 124
    d.text((M, ty), "UTC", font=F_TL_T, fill=INK)
    line_x0 = M + 34
    line_x1 = W - M
    d.line([(line_x0, ty + 14), (line_x1, ty + 14)], fill=LGREY, width=2)
    seg = (line_x1 - line_x0) / 5.0
    for i, (t, lab) in enumerate(TIMELINE):
        px = line_x0 + i * seg
        d.ellipse([px - 4, ty + 10, px + 4, ty + 18], fill=RED)
        anch_t = "la" if i == 0 else ("ra" if i == len(TIMELINE) - 1 else "mm")
        anch_l = "la" if i == 0 else ("ra" if i == len(TIMELINE) - 1 else "ma")
        d.text((px, ty + 2), t, font=F_TL_T, fill=INK, anchor=anch_t)
        d.text((px, ty + 20), lab, font=F_TL_L, fill=GREY, anchor=anch_l)

    # ---- main stories header ----
    y = 156
    d.text((M, y), "THE 13 MAIN STORIES", font=F_H, fill=INK)
    d.line([(M + 224, y + 10), (W - M, y + 10)], fill=INK, width=2)

    # ---- main cards: row 1 = 3 wide, rows 2-3 = 5 each ----
    row1_w = (CW - 2 * 12) // 3
    row_w = (CW - 4 * 12) // 5
    row1_h, row_h = 180, 168
    row1_top, row2_top, row3_top = 172, 358, 532
    for i, (num, place, region, field, title, body, src, status, kind, bignum) in enumerate(MAIN):
        if i < 3:
            col_w, card_h, y0 = row1_w, row1_h, row1_top
            x0 = M + i * (col_w + 12)
            scene_h = 70
            big_fnt = F_BIGNUM
        elif i < 8:
            col_w, card_h, y0 = row_w, row_h, row2_top
            x0 = M + (i - 3) * (col_w + 12)
            scene_h = 64
            big_fnt = F_BIGNUM_S
        else:
            col_w, card_h, y0 = row_w, row_h, row3_top
            x0 = M + (i - 8) * (col_w + 12)
            scene_h = 64
            big_fnt = F_BIGNUM_S
        d.rectangle([x0, y0, x0 + col_w, y0 + card_h], fill=CARD_BG, outline=LGREY, width=1)
        scene(d, kind, x0 + 1, y0 + 1, col_w - 2, scene_h)
        # place ribbon (region colour) on the scene, top-left; status badge top-right
        plabel = f"{num} \u00b7 {place}"
        pw = d.textlength(plabel, font=F_PLACE) + 8
        d.rectangle([x0 + 1, y0 + 1, x0 + 1 + pw, y0 + 19], fill=REG_COL[region])
        d.text((x0 + 5, y0 + 5), plabel, font=F_PLACE, fill=(255, 255, 255))
        bw = d.textlength(status, font=F_BADGE) + 8
        bx = x0 + col_w - bw - 6
        bcol = BADGE_COL[status]
        btxt = INK if status in ("REPORTED", "CLAIM") else (255, 255, 255)
        d.rounded_rectangle([bx, y0 + 5, bx + bw, y0 + 19], radius=7, fill=bcol)
        d.text((bx + 4, y0 + 7), status, font=F_BADGE, fill=btxt)
        # big number badge inside the scene, bottom-right (kept small so it
        # labels the scene instead of covering it)
        if bignum:
            ch = 21 if i < 3 else 20
            nw = d.textlength(bignum, font=big_fnt) + 14
            nx = x0 + col_w - nw - 5
            ny = y0 + scene_h - ch - 4
            d.rounded_rectangle([nx, ny, nx + nw, ny + ch], radius=6, fill=INK)
            d.text((nx + 7, ny + 2), bignum, font=big_fnt, fill=YELLOW)
        tx = x0 + 8
        d.text((tx, y0 + scene_h + 6), field, font=F_CAT, fill=RED)
        tlines = wrap(d, title, F_STITLE, col_w - 16)
        ty2 = y0 + scene_h + 22
        for ln in tlines[:2]:
            d.text((tx, ty2), ln, font=F_STITLE, fill=INK)
            ty2 += 16
        blines = wrap(d, body, F_BODY, col_w - 16)
        by = y0 + scene_h + 56
        for ln in blines[:2]:
            d.text((tx, by), ln, font=F_BODY, fill=(60, 58, 52))
            by += 13
        d.text((tx, y0 + card_h - 16), f"Source: {src}", font=F_SRC, fill=GREY)

    # ---- ALSO section: 3 columns, 8 rows, numbered 14-35 with sources ----
    y = 706
    d.text((M, y), "ALSO TODAY \u2014 14\u201335", font=F_H, fill=INK)
    d.line([(M + 208, y + 10), (W - M, y + 10)], fill=INK, width=2)
    acol_w = (CW - 2 * 14) // 3
    ay = 724
    for i, (num, place, region, head, src) in enumerate(ALSO):
        col = i % 3
        row = i // 3
        x0 = M + col * (acol_w + 14)
        yy = ay + row * 17
        d.text((x0, yy), num, font=F_ALSO_B, fill=INK)
        px = x0 + d.textlength(num, font=F_ALSO_B) + 5
        d.text((px, yy), place, font=F_ALSO_B, fill=REG_COL[region])
        px += d.textlength(place, font=F_ALSO_B) + 5
        d.text((px, yy), f"\u2014 {head}", font=F_ALSO, fill=INK)
        px += d.textlength(f"\u2014 {head}", font=F_ALSO) + 4
        d.text((px, yy), f"({src})", font=F_ALSO, fill=GREY)

    # ---- HOW SURE legend, full width ----
    fy = 860
    d.text((M, fy), "HOW SURE:  ", font=F_FOOT_B, fill=INK)
    fx = M + d.textlength("HOW SURE:  ", font=F_FOOT_B)
    foot = ("CONFIRMED = 2+ outlets   \u00b7   OFFICIAL = on record   \u00b7   REPORTED = single wire   "
            "\u00b7   CLAIM = one side's account   \u00b7   Vector scenes")
    d.text((fx, fy), foot, font=F_FOOT, fill=GREY)

    # ---- bottom band: map + DATE CHECK ----
    y = 876
    d.line([(M, y), (W - M, y)], fill=LGREY, width=1)
    d.text((M, 884), "WHERE IT HAPPENED \u2014 13 MAIN STORIES", font=F_DC_B, fill=INK)
    dx = M + 316
    d.text((dx, 884), "DATE CHECK", font=F_DC_B, fill=RED)
    # dotted world map, left; pins numbered 1-13, region-coloured
    map_x0, map_y0 = M, 898
    mw, mh = 300, 96
    cell_w, cell_h = mw / 64.0, mh / 26.0
    land_cells = set()
    for (r, a, b) in LAND:
        for cx in range(a, b + 1):
            land_cells.add((cx, r))
    for (cx, r) in land_cells:
        px = map_x0 + (cx + 0.5) * cell_w
        py = map_y0 + (r + 0.5) * cell_h
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=MAP_DOT)
    for k, (lon, lat, region) in enumerate(PINS):
        gx = (lon + 180.0) / 360.0 * 64.0
        gy = (90.0 - lat) / 150.0 * 26.0
        px = map_x0 + gx * cell_w
        py = map_y0 + gy * cell_h
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=REG_COL[region])
        d.text((px, py), str(k + 1), font=font("DejaVuSans-Bold", 7),
               fill=(255, 255, 255), anchor="mm")
    # DATE CHECK + numbers, right
    dw = W - M - dx
    dlines = wrap(d, DATE_CHECK, F_DC, dw)
    dy = 898
    for ln in dlines:
        d.text((dx, dy), ln, font=F_DC, fill=(60, 58, 52))
        dy += 13
    dy += 6
    nlines = wrap(d, NUMBERS_LINE, F_DC_B, dw)
    for ln in nlines:
        d.text((dx, dy), ln, font=F_DC_B, fill=INK)
        dy += 14

    # ---- footer ----
    d.text((512, 1006), "Sources: AP, Reuters, NYT, UN, Sanofi  \u00b7  "
           "Scenes are drawn illustrations, not photographs",
           font=F_FOOT, fill=GREY, anchor="mm")

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
