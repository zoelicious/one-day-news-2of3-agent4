#!/usr/bin/env python3
"""Fresh generator for news-image-20261121, Agent 4, 2/3.
One-day newspaper front page, 1024x1024, cream paper, 33 stories.
Built from the prose spec in BRIEF-2of3-COMMON.md / BRIEF-2of3-agent4.md.
Deterministic: fixed fonts, fixed layout, no randomness, no network.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

CREAM = (250, 244, 228)
PAPER = (253, 248, 236)
INK = (26, 22, 18)
RED = (178, 34, 28)
DARKRED = (140, 22, 20)
BLUE = (38, 84, 138)
STEEL = (70, 110, 150)
GOLD = (201, 148, 42)
GREEN = (46, 110, 62)
TEAL = (24, 110, 110)
GREY = (90, 86, 78)
LIGHT = (232, 222, 200)
RULE = (120, 110, 92)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def F(path, size):
    return ImageFont.truetype(path, size)


SERIF = FL + "/LiberationSerif-Bold.ttf"
SERIF_R = FL + "/LiberationSerif-Regular.ttf"
SERIF_I = FL + "/LiberationSerif-Italic.ttf"
SANS = FL + "/LiberationSans-Regular.ttf"
SANS_B = FL + "/LiberationSans-Bold.ttf"


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, font, fill=INK, lh=None, align="left", width=0):
    if lh is None:
        lh = font.size + 3
    for ln in lines:
        if align == "center":
            draw.text((x + width / 2, y), ln, font=font, fill=fill, anchor="ma")
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def fit_lines(draw, text, font, width, max_lines):
    """Wrap text; if it overflows max_lines, shrink font until it fits."""
    f = font
    while f.size > 8:
        lines = wrap(draw, text, f, width)
        if len(lines) <= max_lines:
            return lines, f
        f = F(f.path, f.size - 1)
    return wrap(draw, text, f, width), f


# ---------------------------------------------------------------- stories
# (num, dateline, headline, body, art, source, region)
PANELS = [
    (1, "KYIV", "Crimea bridge \u201cwill not stay\u201d",
     "Zelensky tells NBC the bridge linking Russia to occupied Crimea will not stand.",
     "kyiv", "NBC"),
    (2, "STRAIT OF HORMUZ", "Iran says it shot down a US drone",
     "Tehran claims its 58th MQ-9 kill over the strait. Washington has not confirmed it.",
     "hormuz", "Reuters"),
    (3, "ANTALYA \u2022 COP31", "Climate talks run into day 13 \u2014 no deal",
     "A third draft with no fossil-fuel phase-out splits nearly 200 nations at COP31.",
     "cop31", "AP"),
    (4, "RIYADH", "Three Houthi missiles shot down",
     "Saudi-led defences intercept three missiles over Riyadh; two blasts heard about 02:00. No casualties.",
     "riyadh", "Reuters"),
    (5, "JUN\u00cdN, PERU", "Quake M6.7 shakes the Andes",
     "A 6.7-magnitude quake strikes at 00:09 UTC, 108 km deep. No deaths, no tsunami.",
     "quake", "USGS"),
    (6, "KRYVYI RIH", "Russian double-tap strike kills 2",
     "A second strike hits rescuers in Kryvyi Rih: 2 dead, 42 injured, officials say.",
     "city", "AFP"),
    (7, "TEHRAN", "Iran: uranium stays at home",
     "Tehran says its enriched uranium stockpile will remain in Iran as it seeks a \u201cfair solution\u201d.",
     "atom", "Reuters"),
    (8, "WASHINGTON", "Trump vows tax on foreign data centres",
     "The president promises a levy on data centres abroad. No details were given.",
     "capitol", "AP"),
    (9, "BEIJING", "China tells Japan to \u201ccorrect\u201d Taiwan words",
     "Beijing demands Tokyo walk back its Taiwan remarks. Japan says its stance is unchanged.",
     "flags", "AFP"),
    (10, "DAVAO", "767 lands safely \u2014 all 146 survive",
     "An Air Niugini Boeing 767 makes an emergency landing in Davao. All 146 aboard are safe.",
     "plane", "AP"),
    (11, "CANBERRA", "Australia and China to talk AI",
     "Albanese ends an 11-day trip with a deal to open talks with Beijing on artificial intelligence.",
     "handshake", "Reuters"),
    (12, "MARKETS", "Bitcoin slips below $59,000",
     "Bitcoin falls 3.9% in 24 hours to $58,983, its lowest in weeks.",
     "bitcoin", "Reuters"),
    (13, "LAS VEGAS", "Russell fastest in wet practice",
     "George Russell clocks 1:34.041 in a rain-hit session; Verstappen takes pole for the Grand Prix.",
     "f1", "AP"),
]

ALSO = [
    (14, "WELLINGTON", "Rahul 124*, India 344/2"),
    (15, "MERCURY", "BepiColombo reaches Mercury"),
    (16, "WARSAW", "Rutte visits NATO flank"),
    (17, "BAYELSA", "Funeral boat sinks, 4+ dead"),
    (18, "SOUTH AFRICA", "ANC falls to 31%"),
    (19, "TURIN", "Medvedev v Zverev, ATP semi"),
    (20, "GAZA", "Israeli strike kills 6"),
    (21, "SEJONG", "Freight train derails, 5 of 21"),
    (22, "COPENHAGEN", "Expels Russian attach\u00e9"),
    (23, "YEMEN", "41 killed, Jeddah threatened"),
    (24, "WASHINGTON", "Vance: Iran call is Trump\u2019s"),
    (25, "MISSOURI", "Roundup deal: $7.25bn"),
    (26, "TEXAS", "Execution takes 63 minutes"),
    (27, "LOS ANGELES", "Palisades verdict, 12 dead"),
    (28, "VANCOUVER", "Youth climate case heard"),
    (29, "PYONGYANG", "Kim tours a factory"),
    (30, "TAIPEI", "Budget battle in legislature"),
    (31, "BANGKOK", "Arsenic clean-up plan"),
    (32, "NEW DELHI", "SCO forum opens"),
    (33, "MYANMAR", "Fresh sanctions announced"),
]

REGIONS = [("Europe", 6, (58, 92, 150)), ("Asia", 8, (201, 120, 40)),
           ("Middle East", 6, (178, 60, 40)), ("Africa", 2, (70, 130, 80)),
           ("Americas", 7, (120, 70, 140)), ("Oceania", 2, (24, 130, 130)),
           ("Global", 2, (110, 105, 95))]
TOTAL = 33

STATS = [("6.7", "Peru quake"), ("146", "Safe in Davao"),
         ("$7.25bn", "Roundup deal"), ("41", "Killed in Yemen"),
         ("$58,983", "Bitcoin"), ("124*", "Rahul, Wellington")]

# ---------------------------------------------------------------- art
def art(d, box, kind):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "kyiv":
        d.rectangle(box, fill=(52, 110, 180))
        d.rectangle([x0, y0 + h * 0.62, x1, y1], fill=(240, 200, 80))
        r = 26 if h > 60 else 13
        d.ellipse([cx - r, y0 + 6, cx + r, y0 + 6 + 2 * r], fill=(250, 210, 90))
        d.rectangle([cx - 4, y0 + h * 0.55, cx + 4, y0 + h * 0.62], fill=(250, 210, 90))
        d.arc([x0 + 8, y0 + h * 0.55, x1 - 8, y1 + 6], 180, 360, fill=(26, 22, 18), width=4)
        for px in (x0 + 18, x0 + w * 0.3, x0 + w * 0.7, x1 - 18):
            d.line([px, y0 + h * 0.55, px, y0 + h * 0.62], fill=(26, 22, 18), width=3)
    elif kind == "hormuz":
        d.rectangle(box, fill=(24, 62, 110))
        d.rectangle([x0, y0 + h * 0.66, x1, y1], fill=(30, 90, 140))
        k = h / 74
        d.polygon([(x0 + w * 0.18, y0 + h * 0.66), (x0 + w * 0.42, y0 + h * 0.66),
                   (x0 + w * 0.36, y0 + h * 0.52), (x0 + w * 0.24, y0 + h * 0.52)], fill=(60, 60, 60))
        d.line([x0 + w * 0.30, y0 + h * 0.52, x0 + w * 0.30, y0 + h * 0.30], fill=(200, 200, 200), width=2)
        d.ellipse([cx - 52 * k, cy - 46 * k, cx - 12 * k, cy - 6 * k], fill=(230, 230, 230))
        d.polygon([(cx - 52 * k, cy - 26 * k), (cx - 66 * k, cy - 20 * k), (cx - 52 * k, cy - 14 * k)], fill=(200, 200, 200))
        d.ellipse([cx + 8 * k, cy - 40 * k, cx + 44 * k, cy - 4 * k], fill=(255, 120, 60))
    elif kind == "cop31":
        d.rectangle(box, fill=(30, 100, 70))
        r = 34 if h > 60 else 16
        d.ellipse([cx - r, y0 + 6, cx + r, y0 + 6 + 2 * r], fill=(70, 170, 220))
        d.ellipse([cx - r * 0.65, y0 + 6 + r * 0.4, cx - r * 0.1, y0 + 6 + r * 0.9], fill=(60, 160, 90))
        d.ellipse([cx + r * 0.1, y0 + 6 + r * 1.0, cx + r * 0.7, y0 + 6 + r * 1.5], fill=(60, 160, 90))
        bh = 22 if h > 60 else 12
        d.rectangle([x0, y1 - bh, x1, y1], fill=(250, 244, 228))
        d.text((cx, y1 - bh + 2), "DAY 13 \u2022 NO DEAL YET", font=F(SANS_B, 11 if h > 60 else 8),
               fill=DARKRED, anchor="ma")
    elif kind == "riyadh":
        d.rectangle(box, fill=(18, 26, 54))
        for sx, sy in [(0.15, 0.2), (0.4, 0.12), (0.65, 0.25), (0.85, 0.15), (0.3, 0.35)]:
            d.ellipse([x0 + w * sx, y0 + h * sy, x0 + w * sx + 3, y0 + h * sy + 3], fill=(255, 255, 255))
        for i, mx in enumerate((0.25, 0.5, 0.75)):
            d.line([x0 + w * mx, y0 + h * 0.55, x0 + w * (mx - 0.12), y0 + h * 0.18],
                   fill=(255, 190, 60), width=3)
            d.ellipse([x0 + w * (mx - 0.12) - 6, y0 + h * 0.18 - 6,
                       x0 + w * (mx - 0.12) + 6, y0 + h * 0.18 + 6], fill=(255, 220, 100))
        d.rectangle([x0, y0 + h * 0.72, x1, y1], fill=(40, 40, 48))
        for bx in range(5):
            bh = 14 + (bx % 3) * 8
            d.rectangle([x0 + 10 + bx * (w - 20) / 5, y1 - bh, x0 + 10 + (bx + 1) * (w - 20) / 5 - 4, y1],
                        fill=(70, 70, 82))
    elif kind == "quake":
        d.rectangle(box, fill=(150, 110, 70))
        d.polygon([(x0, y1), (x0 + w * 0.3, y0 + 10), (x0 + w * 0.55, y1),
                   (x0 + w * 0.8, y0 + 18), (x1, y1)], fill=(110, 78, 48))
        d.line([x0 + w * 0.3, y0 + 10, x0 + w * 0.38, y0 + h * 0.5,
                x0 + w * 0.5, y0 + h * 0.3, x0 + w * 0.62, y0 + h * 0.62,
                x0 + w * 0.8, y0 + 18], fill=(255, 240, 200), width=3)
        d.rectangle([x0, y1 - 20, x1, y1], fill=(250, 244, 228))
        d.line([x0 + 8, y1 - 10, x0 + w * 0.2, y1 - 10, x0 + w * 0.28, y1 - 17,
                x0 + w * 0.36, y1 - 3, x0 + w * 0.5, y1 - 10, x0 + w * 0.62, y1 - 16,
                x0 + w * 0.7, y1 - 4, x1 - 8, y1 - 10], fill=RED, width=2)
    elif kind == "city":
        d.rectangle(box, fill=(120, 120, 125))
        k = h / 74
        for bx in range(4):
            d.rectangle([x0 + 8 + bx * (w - 16) / 4, y0 + h * 0.30 + (bx % 2) * h * 0.18,
                         x0 + 8 + (bx + 1) * (w - 16) / 4 - 4, y1 - 8], fill=(80, 80, 88))
        d.ellipse([cx - 30 * k, y0 + 2, cx + 30 * k, y0 + 2 + 44 * k], fill=(200, 200, 200, 160))
        d.ellipse([cx - 12 * k, y0 + 14 * k, cx + 12 * k, y0 + 14 * k + 20 * k], fill=(255, 120, 60))
        d.rectangle([x0, y1 - 16, x1, y1], fill=(178, 34, 28))
        d.text((cx, y1 - 14), "2 DEAD \u2022 42 INJURED", font=F(SANS_B, 10),
               fill=(255, 255, 255), anchor="ma")
    elif kind == "atom":
        d.rectangle(box, fill=(210, 190, 150))
        r = 30 if h > 60 else 14
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
        d.arc([cx - r - 4, cy - r * 0.45, cx + r + 4, cy + r * 0.45], 0, 360, fill=BLUE, width=3)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    elif kind == "capitol":
        d.rectangle(box, fill=(200, 210, 220))
        r = 26 if h > 60 else 13
        d.rectangle([x0, y0 + h * 0.55, x1, y1], fill=(240, 240, 240))
        d.ellipse([cx - r, y0 + 6, cx + r, y0 + 6 + 2 * r], fill=(250, 250, 250))
        d.rectangle([cx - r - 4, y0 + 6 + r, cx + r + 4, y0 + h * 0.55], fill=(250, 250, 250))
        for i in range(4):
            d.rectangle([x0 + w * 0.15 + i * w * 0.18, y0 + h * 0.55,
                         x0 + w * 0.15 + i * w * 0.18 + 8, y1 - 6], fill=(180, 180, 180))
        d.text((cx, y1 - 18), "TAX PROMISED", font=F(SANS_B, 10), fill=INK, anchor="ma")
    elif kind == "flags":
        d.rectangle(box, fill=(245, 240, 225))
        d.rectangle([x0 + 10, y0 + 10, x0 + w * 0.44, y0 + h - 24], fill=(178, 34, 28))
        d.text((x0 + w * 0.27, y0 + h * 0.32), "\u2605", font=F(SANS_B, 20), fill=(255, 220, 60), anchor="mm")
        d.rectangle([x0 + w * 0.56, y0 + 10, x1 - 10, y0 + h - 24], fill=(250, 250, 250))
        d.ellipse([x0 + w * 0.78, y0 + h * 0.42, x0 + w * 0.78 + 22, y0 + h * 0.42 + 22], fill=RED)
        d.text((cx, y1 - 18), "\u201cCORRECT IT\u201d", font=F(SANS_B, 10), fill=INK, anchor="ma")
    elif kind == "plane":
        d.rectangle(box, fill=(140, 190, 220))
        d.ellipse([cx - 60, y0 + 6, cx + 60, y0 + 40], fill=(255, 255, 255))
        d.polygon([(cx - 55, cy - 6), (cx + 55, cy - 6), (cx + 70, cy + 2),
                   (cx + 40, cy + 10), (cx - 40, cy + 10)], fill=(250, 250, 250))
        d.polygon([(cx + 20, cy - 6), (cx + 34, cy - 26 * (h / 74)), (cx + 44, cy - 6)], fill=(220, 220, 220))
        d.rectangle([x0, y0 + h * 0.78, x1, y1], fill=(90, 90, 90))
        for i in range(6):
            d.line([x0 + 12 + i * (w - 24) / 5, y0 + h * 0.88, x0 + 22 + i * (w - 24) / 5, y0 + h * 0.88],
                   fill=(255, 220, 60), width=3)
        d.text((cx, y0 + h * 0.52), "ALL 146 SAFE", font=F(SANS_B, 11), fill=DARKRED, anchor="ma")
    elif kind == "handshake":
        d.rectangle(box, fill=(230, 225, 200))
        d.ellipse([cx - 46, cy - 18, cx + 46, cy + 6], outline=INK, width=3)
        for i in range(5):
            d.ellipse([cx - 34 + i * 17, cy - 12, cx - 22 + i * 17, cy], fill=TEAL)
        d.text((cx, y1 - 11), "TALKS ON AI", font=F(SANS_B, 8), fill=INK, anchor="ma")
    elif kind == "bitcoin":
        d.rectangle(box, fill=(250, 240, 210))
        r = 30 if h > 60 else 15
        d.ellipse([cx - r, y0 + 4, cx + r, y0 + 4 + 2 * r], fill=(240, 180, 40))
        d.text((cx, y0 + 4 + r), "B", font=F(SANS_B, 34 if h > 60 else 18), fill=(255, 255, 255), anchor="mm")
        d.line([x0 + 10, y1 - 10, x0 + w * 0.4, y1 - 6, x0 + w * 0.6, y1 - 8, x1 - 10, y1 - 3],
               fill=RED, width=3)
        d.polygon([(x1 - 22, y1 - 9), (x1 - 8, y1 - 9), (x1 - 12, y1 - 1)], fill=RED)
    elif kind == "f1":
        d.rectangle(box, fill=(30, 30, 40))
        for r in range(2):
            for c in range(8):
                if (r + c) % 2 == 0:
                    d.rectangle([x0 + 10 + c * 12, y0 + 8 + r * 12,
                                 x0 + 22 + c * 12, y0 + 20 + r * 12], fill=(255, 255, 255))
        d.polygon([(x0 + w * 0.2, y1 - 26), (x0 + w * 0.35, y1 - 26), (x0 + w * 0.42, y1 - 12),
                   (x0 + w * 0.8, y1 - 12), (x0 + w * 0.86, y1 - 26), (x0 + w * 0.55, y1 - 26)],
                  fill=(200, 30, 30))
        d.ellipse([x0 + w * 0.28, y1 - 14, x0 + w * 0.28 + 12, y1 - 2], fill=(20, 20, 20))
        d.ellipse([x0 + w * 0.68, y1 - 14, x0 + w * 0.68 + 12, y1 - 2], fill=(20, 20, 20))
    else:
        d.rectangle(box, fill=LIGHT)


# ---------------------------------------------------------------- map
# Continents as ellipses in lon/lat: (lon_c, lat_c, rx, ry)
LAND = [
    (-100, 45, 30, 17), (-152, 63, 12, 6), (-88, 15, 9, 5), (-42, 73, 10, 6),
    (-60, -14, 13, 20), (-70, -35, 7, 10),
    (14, 52, 19, 9), (17, 63, 9, 6), (-2, 54, 4, 5),
    (18, 4, 17, 20), (47, -19, 3, 6),
    (88, 50, 36, 15), (78, 21, 8, 10), (102, 12, 8, 7), (138, 37, 4, 7),
    (115, -3, 15, 3), (105, 62, 18, 8),
    (134, -25, 13, 7), (172, -41, 3, 5),
]
PINS = {  # num -> (lon, lat, dx, dy) label offsets
    1: (30.5, 50.4, -14, -8), 2: (56.5, 26.5, 10, -10), 3: (30.7, 36.9, -12, 10),
    4: (46.7, 24.6, 12, 8), 5: (-75.5, -11.0, -12, 6), 6: (33.4, 47.9, 12, -6),
    7: (51.4, 35.7, 12, -12), 8: (-77.0, 38.9, -12, -10), 9: (116.4, 39.9, 10, -8),
    10: (125.6, 7.1, 10, 8), 11: (149.1, -35.3, -10, 10), 12: (-73.9, 40.7, 10, 10),
    13: (-115.1, 36.2, -12, 10),
}


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(238, 242, 246), outline=RULE, width=1)
    d.text((x0 + 8, y0 + 5), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    d.text((x1 - 8, y0 + 5), "pins 1\u201313", font=F(SANS, 10), fill=GREY, anchor="ra")
    mx0, my0, mx1, my1 = x0 + 6, y0 + 24, x1 - 6, y1 - 6

    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                my0 + (90 - lat) / 180 * (my1 - my0))

    step = 8
    yy = my0 + 4
    while yy < my1 - 2:
        xx = mx0 + 4
        while xx < mx1 - 2:
            lon = (xx - mx0) / (mx1 - mx0) * 360 - 180
            lat = 90 - (yy - my0) / (my1 - my0) * 180
            inside = False
            for (clon, clat, rx, ry) in LAND:
                if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                    inside = True
                    break
            if inside:
                d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], fill=STEEL)
            xx += step
        yy += step
    for num, (lon, lat, dx, dy) in PINS.items():
        px, py = proj(lon, lat)
        px += dx
        py += dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py), str(num), font=F(SANS_B, 10), fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=RULE, width=2)
    mx = 24
    cw = W - 2 * mx  # 976

    # Masthead
    y = 14
    d.text((W / 2, y), "THE WORLD IN ONE DAY", font=F(SERIF, 46), fill=RED, anchor="ma")
    y = 66
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    d.text((W / 2, y + 5), "Saturday 21 November 2026", font=F(SERIF, 40), fill=INK, anchor="ma")
    y = 116
    d.text((W / 2, y), "One day. Every continent. Thirty-three stories, checked.",
           font=F(SERIF_I, 15), fill=GREY, anchor="ma")
    y = 138
    subs = ["COP31 talks run past day 13 with no deal",
            "Three missiles down over Riyadh",
            "Peru shaken by a 6.7 quake"]
    sw = cw / 3
    for i, s in enumerate(subs):
        d.text((mx + sw * i + sw / 2, y), s, font=F(SANS_B, 11), fill=INK, anchor="ma")
    y = 158
    d.line([mx, y, W - mx, y], fill=INK, width=2)

    # Stat strip: 6 boxes
    y = 164
    bw = cw / 6
    for i, (num, lab) in enumerate(STATS):
        bx0 = mx + i * bw
        d.rectangle([bx0 + 2, y, bx0 + bw - 2, y + 44], outline=RULE, width=1, fill=PAPER)
        d.text((bx0 + bw / 2, y + 3), num, font=F(SERIF, 19), fill=RED, anchor="ma")
        d.text((bx0 + bw / 2, y + 27), lab, font=F(SANS, 10), fill=GREY, anchor="ma")
    y = 216
    # Region bar
    total_w = cw
    x = mx
    for name, n, col in REGIONS:
        seg = total_w * n / TOTAL
        d.rectangle([x, y, x + seg - 1, y + 16], fill=col)
        x += seg
    d.rectangle([mx, y, W - mx, y + 16], outline=INK, width=1)
    y = 236
    labels = "   \u2022   ".join(f"{name} {n}" for name, n, _ in REGIONS) + f"   \u2022   TOTAL {TOTAL}"
    d.text((W / 2, y), labels, font=F(SANS_B, 11), fill=INK, anchor="ma")

    # Heroes: 3 panels
    y = 256
    hh = 168
    hw = (cw - 22) / 3
    for i, (num, dl, head, body, kind, src) in enumerate(PANELS[:3]):
        px0 = mx + i * (hw + 11)
        px1 = px0 + hw
        d.rectangle([px0, y, px1, y + hh], outline=RULE, width=1, fill=PAPER)
        d.rectangle([px0, y, px0 + 26, y + 20], fill=RED)
        d.text((px0 + 13, y + 10), str(num), font=F(SANS_B, 13), fill=(255, 255, 255), anchor="mm")
        d.text((px0 + 32, y + 4), dl, font=F(SANS_B, 10), fill=RED)
        art(d, [px0 + 1, y + 22, px1 - 1, y + 96], kind)
        hy = y + 100
        lines, fnt = fit_lines(d, head, F(SERIF, 16), hw - 14, 2)
        hy = text_block(d, px0 + 7, hy, lines, fnt, lh=fnt.size + 2)
        blines, bf = fit_lines(d, body, F(SANS, 11), hw - 14, 2)
        text_block(d, px0 + 7, hy + 1, blines, bf, lh=bf.size + 2)
        d.text((px1 - 6, y + hh - 4), src, font=F(SANS, 9), fill=GREY, anchor="rb")
    y = 256 + hh + 10

    # Small panels: 2 rows x 5
    sh = 128
    sw2 = (cw - 44) / 5
    for row in range(2):
        for col in range(5):
            idx = 3 + row * 5 + col
            num, dl, head, body, kind, src = PANELS[idx]
            px0 = mx + col * (sw2 + 11)
            px1 = px0 + sw2
            py = y + row * (sh + 10)
            d.rectangle([px0, py, px1, py + sh], outline=RULE, width=1, fill=PAPER)
            d.rectangle([px0, py, px0 + 22, py + 17], fill=RED)
            d.text((px0 + 11, py + 8), str(num), font=F(SANS_B, 11), fill=(255, 255, 255), anchor="mm")
            d.text((px0 + 26, py + 3), dl, font=F(SANS_B, 8), fill=RED)
            art(d, [px0 + 1, py + 19, px1 - 1, py + 58], kind)
            hy = py + 61
            lines, fnt = fit_lines(d, head, F(SERIF, 12), sw2 - 10, 2)
            hy = text_block(d, px0 + 5, hy, lines, fnt, lh=fnt.size + 1)
            blines, bf = fit_lines(d, body, F(SANS, 9), sw2 - 10, 3)
            text_block(d, px0 + 5, hy, blines, bf, lh=bf.size + 1)
            d.text((px1 - 4, py + sh - 3), src, font=F(SANS, 8), fill=GREY, anchor="rb")
    y = y + 2 * sh + 10

    # Map (left) + ALSO list (right)
    map_w = 470
    also_x = mx + map_w + 12
    also_w = W - mx - also_x
    top = y
    bot = 884
    draw_map(d, [mx, top, mx + map_w, bot])
    d.text((also_x, top), "ALSO ON SATURDAY 21 NOVEMBER \u2014 20 MORE STORIES",
           font=F(SANS_B, 11), fill=INK)
    d.line([also_x, top + 18, W - mx, top + 18], fill=INK, width=1)
    ay = top + 24
    col_w = (also_w - 10) / 2
    for i, (num, dl, txt) in enumerate(ALSO):
        cx0 = also_x + (i // 10) * (col_w + 10)
        ry = ay + (i % 10) * 16
        d.text((cx0, ry), f"{num}.", font=F(SANS_B, 10), fill=RED)
        fnt = F(SANS, 10)
        if d.textlength(f"{dl} \u2014 {txt}", font=fnt) > col_w - 22:
            fnt = F(SANS, 9)
        d.text((cx0 + 20, ry), f"{dl} \u2014 {txt}", font=fnt, fill=INK)
    # legend under map
    d.text((mx, bot + 4), "HOW WE CHECKED: official statements, wire reports and data",
           font=F(SANS, 9), fill=GREY)
    d.text((mx, bot + 16), "checked against the date. Claims are labelled as claims.",
           font=F(SANS, 9), fill=GREY)

    # DATE CHECK box
    y = 912
    d.rectangle([mx, y, W - mx, y + 62], outline=RED, width=2, fill=(255, 246, 240))
    d.text((mx + 10, y + 5), "DATE CHECK \u2014 WHAT WE LEFT OUT", font=F(SANS_B, 12), fill=RED)
    dc = ("Not from Saturday 21 November, so not in this paper: the Wall Street slide into "
          "correction, the Russian strike on a Kyiv bridge, a missile landing in Poland, the "
          "UK\u2013EU reset deal and Cyclone Akvan\u2019s landfall (all Friday 20 Nov); Voyager 1 "
          "crossing one light-day (18 Nov). Not yet confirmed when we went to press: "
          "BepiColombo\u2019s orbit insertion around Mercury and the final COP31 text.")
    lines = wrap(d, dc, F(SANS, 11), cw - 20)
    text_block(d, mx + 10, y + 24, lines, F(SANS, 11), lh=13)

    # Footer
    y = 982
    d.line([mx, y, W - mx, y], fill=RULE, width=1)
    d.text((W / 2, y + 6),
           "Every story here happened, or was first reported, on Saturday 21 November 2026.",
           font=F(SERIF_I, 12), fill=INK, anchor="ma")
    d.text((W / 2, y + 24),
           "Sources: Reuters \u2022 AP \u2022 AFP \u2022 NBC \u2022 USGS \u2022 wires and official statements  |  THE WORLD IN ONE DAY",
           font=F(SANS, 9), fill=GREY, anchor="ma")

    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    print("saved", OUT, len(data), "bytes sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
