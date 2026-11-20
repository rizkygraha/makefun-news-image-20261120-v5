#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024) — V5 candidate.

Follows the structure of make.fun top-1 kho22 (judge 991.137): top bar,
giant serif masthead + red italic sub-headline, six-figure number strip,
seven-chip region count, three illustrated heroes + ten illustrated cards,
dark navy map with red numbered pins, flowing numbered briefs 14-36, a
red-bordered DATE CHECK box, and an honest footer.

Every fact comes from stories_v5.json (a verbatim copy of the verified
research/v5-stories.json plus layout metadata). Headlines and decks are
condensed ONLY to fit their boxes — no figure, date or name was changed.
Corrections vs kho22 that this build carries: Akvan landfall 07:30 IST with
winds 70-80 gusting 90 (not noon / 90-100); COP31 draft REMOVED fossil-fuel
references; GTA VI 19.1m / $1.84bn Sensor Tower estimate (not 1.7m /
$1.65bn); Nifty 25,368 (not 25,199); Han Duck-soo is a RETRIAL order, never
an acquittal; the Shenzhen declaration was silent on Ukraine and Iran.

All text is ASSERTED to fit its box whole — the generator fails loudly
instead of clipping a sentence mid-way. Every illustration is a flat
original drawing made with Pillow primitives — no photos, no network, no
clock, no randomness — so running this script twice produces byte-identical
PNGs. Pillow only.

Usage: python3 generate.py   -> writes entry.png next to this file.
"""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

# ---- palette ---------------------------------------------------------------
PAPER = (247, 241, 223)      # warm newspaper cream, as in kho22
RED = (166, 28, 28)          # accent: numbers, kickers, rules, pins
DARKRED = (140, 20, 20)
INK = (26, 26, 26)
GREY = (96, 94, 84)
HAIR = (198, 188, 164)
CARDLINE = (180, 172, 148)
NAVYMAP = (26, 43, 74)       # dark navy map panel
MAPDOT = (216, 205, 170)     # pale land dots on the navy map
GOLD = (201, 162, 39)

# region chip colours (kho22 order: europe, americas, asia-pacific,
# mideast, africa, oceania, world)
CHIP = {
    "europe": (0, 128, 128),
    "americas": (178, 34, 34),
    "asia": (46, 125, 50),
    "middle_east": (139, 90, 43),
    "africa": (46, 90, 172),
    "oceania": (123, 75, 166),
    "global": (110, 110, 110),
}
CHIP_ORDER = ["europe", "americas", "asia", "middle_east", "africa",
              "oceania", "global"]
# chip key -> (region_labels key, region_counts key)
CHIP_KEYS = {"europe": ("europe", "europe"),
             "americas": ("americas", "americas"),
             "asia": ("asia", "asia-pacific"),
             "middle_east": ("middle_east", "mideast"),
             "africa": ("africa", "africa"),
             "oceania": ("oceania", "oceania"),
             "global": ("global", "world")}


# ---- fonts -----------------------------------------------------------------
def load(name, size):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/liberation/%s.ttf" % name, size)


def serif_b(size):
    return load("LiberationSerif-Bold", size)


def serif_i(size):
    return load("LiberationSerif-Italic", size)


def sans_b(size):
    return load("LiberationSans-Bold", size)


def sans(size):
    return load("LiberationSans-Regular", size)


# ---- text helpers ----------------------------------------------------------
def wrap(d, text, f, maxw):
    """Greedy word wrap; returns lines that fit maxw pixels (never truncates)."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, f, maxw, maxlines, label):
    """Wrap and FAIL LOUDLY if the copy does not fit whole in maxlines."""
    lines = wrap(d, text, f, maxw)
    assert len(lines) <= maxlines, (
        "%s: %d lines, max %d -- %r" % (label, len(lines), maxlines, text))
    return lines


def put_lines(d, x, y, lines, f, fill, leading=None):
    lh = leading if leading is not None else int(f.size * 1.18)
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def label_bar(d, x, y, w, text):
    """Dark strip with a small white caption along the bottom of hero art."""
    d.rectangle([x, y, x + w, y + 20], fill=(16, 32, 66))
    d.text((x + 10, y + 4), text, font=sans_b(10), fill=(255, 255, 255))


# ---- hero illustrations (309x92, original flat drawings) -------------------
def art_cyclone(d, x, y, w, h):
    """Severe cyclone over the sea: spiral bands, a calm gold eye, rain."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 64, 92))
    cx, cy = x + w * 0.58, y + h * 0.42
    for k, r in enumerate((46, 36, 26, 16)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + k * 55, 330,
              fill=(255, 255, 255), width=3)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(232, 180, 60))
    for i in range(8):  # slanting rain, left side
        rx = x + 12 + i * 15
        d.line([rx, y + 10, rx - 6, y + 30], fill=(170, 205, 230), width=2)
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(38, 84, 130))
    for wx in range(0, w, 28):
        d.arc([x + wx, y + h - 22, x + wx + 24, y + h - 8], 0, 180,
              fill=(140, 190, 220), width=2)
    # low coastline with two small houses, right
    d.polygon([(x + w - 104, y + h - 24), (x + w - 36, y + h - 24),
               (x + w - 18, y + h - 12), (x + w - 112, y + h - 12)],
              fill=(96, 116, 84))
    for hx in (w - 92, w - 62):
        d.rectangle([x + hx, y + h - 38, x + hx + 18, y + h - 24],
                    fill=(240, 230, 200))
        d.polygon([(x + hx - 2, y + h - 38), (x + hx + 9, y + h - 46),
                   (x + hx + 20, y + h - 38)], fill=(166, 28, 28))
    label_bar(d, x, y + h - 20, w, "LANDFALL: 07:30 IST")


def art_cop31(d, x, y, w, h):
    """Antalya hills and lake under an orange sun; the closing day."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 210))
    d.ellipse([x + w - 62, y + 8, x + w - 18, y + 52], fill=(232, 130, 40))
    d.ellipse([x + w // 2 - 78, y + 26, x + w // 2 + 78, y + 58],
              fill=(110, 160, 200))
    d.polygon([(x, y + h - 20), (x + w * 0.42, y + 44), (x + w * 0.75, y + h - 20)],
              fill=(90, 150, 80))
    d.polygon([(x + w * 0.55, y + h - 20), (x + w * 0.85, y + 52),
               (x + w, y + h - 20)], fill=(60, 125, 70))
    d.text((x + 12, y + 8), "FINAL DAY", font=sans_b(17), fill=DARKRED)
    label_bar(d, x, y + h - 20, w, "ANTALYA · CLOSING DAY")


def art_anthropic(d, x, y, w, h):
    """First trading day: candlesticks climbing on a dark green board."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 60, 40))
    d.text((x + 10, y + 6), "ANT", font=sans_b(22), fill=(255, 255, 255))
    t = "$97.17"
    f = sans_b(20)
    d.text((x + w - 10 - d.textlength(t, font=f), y + 8), t, font=f,
           fill=(232, 180, 60))
    # candles stepping up, mostly green
    tops = (52, 46, 50, 40, 44, 34, 28)
    for i, top in enumerate(tops):
        cx = x + 22 + i * 40
        d.line([cx + 7, y + top - 7, cx + 7, y + top + 24],
               fill=(255, 255, 255), width=1)
        c = (60, 180, 90) if i % 3 != 2 else (220, 60, 60)
        d.rectangle([cx, y + top, cx + 14, y + top + 17], fill=c)
    d.line([x + 18, y + 56, x + w - 24, y + 30], fill=(232, 180, 60), width=2)
    label_bar(d, x, y + h - 20, w, "FIRST CLOSE · +17%")


HERO_ART = {1: art_cyclone, 2: art_cop31, 3: art_anthropic}


# ---- card illustrations (180x42, small bold original drawings) ------------
def art_shenzhen(d, x, y, w, h):
    """Dusk skyline with three small flags on poles."""
    d.rectangle([x, y, x + w, y + h], fill=(245, 200, 120))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(52, 52, 58))
    for bx, bw, bh in [(4, 20, 14), (30, 14, 18), (50, 22, 12), (78, 16, 16),
                       (100, 20, 14), (126, 16, 18), (148, 18, 12),
                       (170, 8, 14)]:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + bw, y + h - 14],
                    fill=(70, 70, 78))
    for i, kind in enumerate(("us", "cn", "ru")):
        fx = x + 24 + i * 58
        d.line([fx + 12, y + 4, fx + 12, y + 22], fill=(60, 60, 60), width=2)
        if kind == "us":
            for s in range(3):
                d.rectangle([fx, y + 4 + s * 5, fx + 26, y + 9 + s * 5],
                            fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, y + 4, fx + 11, y + 12], fill=(30, 50, 110))
        elif kind == "cn":
            d.rectangle([fx, y + 4, fx + 26, y + 19], fill=(222, 41, 16))
            d.ellipse([fx + 4, y + 8, fx + 9, y + 13], fill=(255, 220, 60))
        else:
            d.rectangle([fx, y + 4, fx + 26, y + 9], fill=(255, 255, 255))
            d.rectangle([fx, y + 9, fx + 26, y + 14], fill=(0, 60, 160))
            d.rectangle([fx, y + 14, fx + 26, y + 19], fill=(200, 30, 30))


def art_berlin(d, x, y, w, h):
    """Brandenburg Gate, simplified: pediment, five columns, gold quadriga."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 212, 226))
    qx = x + w // 2
    gw = int(w * 0.72)
    gx = x + (w - gw) // 2
    d.rectangle([qx - 10, y + 6, qx + 10, y + 9], fill=(52, 56, 70))
    d.rounded_rectangle([qx - 9, y + 2, qx + 1, y + 6], radius=2,
                        fill=(52, 56, 70))
    d.rectangle([qx + 4, y + 3, qx + 10, y + 8], fill=(201, 162, 39))
    d.polygon([(gx, y + 16), (gx + gw, y + 16), (qx, y + 9)],
              fill=(74, 78, 94))
    d.ellipse([qx - 3, y + 12, qx + 3, y + 18], fill=(201, 162, 39))
    d.rectangle([gx, y + 16, gx + gw, y + 20], fill=(52, 56, 70))
    step = (gw - 10 - 8) / 4
    for i in range(5):
        cx = gx + 5 + int(i * step)
        d.rectangle([cx, y + 20, cx + 8, y + h - 6], fill=(52, 56, 70))
    d.rectangle([gx, y + h - 6, gx + gw, y + h - 2], fill=(52, 56, 70))
    # small German flag, bottom right
    d.rectangle([x + w - 22, y + h - 14, x + w - 4, y + h - 11], fill=(0, 0, 0))
    d.rectangle([x + w - 22, y + h - 11, x + w - 4, y + h - 8], fill=(200, 30, 30))
    d.rectangle([x + w - 22, y + h - 8, x + w - 4, y + h - 5], fill=(255, 200, 40))


def art_kyiv(d, x, y, w, h):
    """A pale civic building struck by two red diagonal lines, smoke above."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    d.rectangle([x + 40, y + 14, x + w - 40, y + h - 6], fill=(240, 238, 228))
    d.polygon([(x + 34, y + 14), (x + w - 34, y + 14), (x + w // 2, y + 4)],
              fill=(90, 100, 115))
    for cx in range(52, w - 44, 20):
        d.rectangle([x + cx, y + 18, x + cx + 6, y + h - 6], fill=(180, 180, 170))
    for sx, sy, r in ((w // 2 - 6, 6, 5), (w // 2 + 8, 10, 7)):
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(150, 150, 150))
    d.line([x + 14, y + h - 4, x + 70, y + 8], fill=(200, 30, 30), width=3)
    d.line([x + w - 70, y + 4, x + w - 16, y + h - 8], fill=(200, 30, 30),
           width=3)


def art_senate(d, x, y, w, h):
    """The Capitol dome on a pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 230, 216))
    bx = x + w // 2
    d.rectangle([bx - 52, y + h - 10, bx + 52, y + h - 4], fill=(70, 80, 95))
    d.rectangle([bx - 44, y + 16, bx + 44, y + h - 10], fill=(88, 96, 112))
    d.pieslice([bx - 26, y + 2, bx + 26, y + 30], 180, 360, fill=(88, 96, 112))
    d.rectangle([bx - 2, y + 0, bx + 2, y + 4], fill=(88, 96, 112))
    for cx in (-36, -18, 0, 18, 36):
        d.rectangle([bx + cx - 3, y + 18, bx + cx + 3, y + h - 10],
                    fill=(240, 240, 235))
    d.rectangle([x, y + h - 4, x + w, y + h], fill=(90, 130, 80))


def art_nvidia(d, x, y, w, h):
    """A green AI chip on a dark board."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    cx, cy = x + w // 2, y + h // 2
    for px in (-24, 24):
        for py in (-12, 0, 12):
            d.line([cx + px, cy + py, cx + px + (10 if px < 0 else -10),
                    cy + py], fill=(120, 200, 140), width=2)
    d.rectangle([cx - 16, cy - 14, cx + 16, cy + 14], fill=(46, 160, 80))
    d.rectangle([cx - 9, cy - 7, cx + 9, cy + 7], fill=(24, 28, 44))
    d.text((cx - 5, cy - 6), "AI", font=sans_b(11), fill=(255, 255, 255))
    d.text((x + 8, y + 4), "AI CHIPS", font=sans_b(10), fill=(255, 255, 255))


def art_cricket(d, x, y, w, h):
    """Green pitch, a big 118, bat and red ball."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
    d.rectangle([x, y + 8, x + w, y + h - 8], fill=(210, 190, 140))
    d.text((x + 10, y + 2), "118", font=sans_b(30), fill=(255, 255, 255))
    for sx in (w - 30, w - 23, w - 16):
        d.rectangle([x + sx, y + 12, x + sx + 3, y + 28], fill=(240, 200, 60))
    d.rectangle([x + w - 30, y + 10, x + w - 13, y + 12], fill=(240, 200, 60))
    d.polygon([(x + 92, y + 8), (x + 100, y + 12), (x + 116, y + 30),
               (x + 108, y + 34)], fill=(220, 180, 120),
              outline=(120, 90, 50))
    d.ellipse([x + 128, y + 6, x + 138, y + 16], fill=(178, 34, 52))


def art_gta(d, x, y, w, h):
    """Miami sunset stripes, an orange sun and a big VI."""
    for i, c in enumerate(((90, 40, 120), (180, 60, 130), (240, 120, 80),
                           (250, 170, 90), (255, 220, 120))):
        d.rectangle([x, y + i * h // 5, x + w, y + (i + 1) * h // 5 + 1],
                    fill=c)
    d.ellipse([x + 24, y + 4, x + 52, y + 32], fill=(255, 200, 80))
    d.text((x + w - 62, y + 2), "VI", font=sans_b(30), fill=(255, 255, 255))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(40, 40, 60))


def art_senegal(d, x, y, w, h):
    """A small boat on a blue sea."""
    d.rectangle([x, y, x + w, y + h], fill=(70, 120, 170))
    d.polygon([(x + w // 2 - 26, y + h - 12), (x + w // 2 + 30, y + h - 12),
               (x + w // 2 + 20, y + h - 22), (x + w // 2 - 18, y + h - 22)],
              fill=(120, 70, 40))
    d.polygon([(x + w // 2, y + 8), (x + w // 2, y + h - 24),
               (x + w // 2 + 22, y + h - 24)], fill=(240, 235, 210))
    d.line([x + w // 2, y + 8, x + w // 2, y + h - 22], fill=(60, 60, 60),
           width=2)
    for wx in range(0, w, 26):
        d.arc([x + wx, y + h - 10, x + wx + 22, y + h + 2], 180, 360,
              fill=(200, 225, 240), width=2)


def art_tonga(d, x, y, w, h):
    """Dry mountains under a hard orange sun."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 228, 190))
    d.ellipse([x + w - 46, y + 4, x + w - 14, y + 36], fill=(232, 130, 40))
    d.polygon([(x, y + h), (x + w * 0.30, y + 10), (x + w * 0.60, y + h)],
              fill=(140, 100, 60))
    d.polygon([(x + w * 0.45, y + h), (x + w * 0.75, y + 4),
               (x + w, y + h)], fill=(110, 80, 50))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(90, 120, 60))


def art_rose(d, x, y, w, h):
    """A baseball on a green field."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
    d.text((x + 8, y + 4), "PETE ROSE", font=sans_b(10),
           fill=(255, 255, 255))
    cx, cy = x + w - 44, y + h // 2 + 4
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 255, 255))
    d.arc([cx - 11, cy - 11, cx + 11, cy + 11], 300, 60, fill=(200, 30, 30),
          width=2)
    d.arc([cx - 11, cy - 11, cx + 11, cy + 11], 120, 240, fill=(200, 30, 30),
          width=2)


CARD_ART = {4: art_shenzhen, 5: art_berlin, 6: art_kyiv, 7: art_senate,
            8: art_nvidia, 9: art_cricket, 10: art_gta, 11: art_senegal,
            12: art_tonga, 13: art_rose}


# ---- dark navy dotted world map --------------------------------------------
def lonlat(lon, lat, x0, y0, w, h):
    return (x0 + (lon + 180) / 360 * w, y0 + (75 - lat) / 130 * h)


# Simplified continent outlines (equirectangular lon/lat polygons), drawn
# from general geography for the dotted map.
LAND = {
    "na": [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
           (-85, 66), (-80, 73), (-65, 60), (-55, 47), (-60, 45),
           (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21),
           (-97, 16), (-92, 15), (-100, 17), (-105, 20), (-110, 24),
           (-115, 28), (-120, 34), (-125, 40), (-125, 49), (-130, 55),
           (-140, 60), (-155, 58), (-165, 60), (-168, 66)],
    "sa": [(-78, 9), (-62, 9), (-52, 5), (-50, 0), (-40, -5), (-35, -8),
           (-38, -15), (-40, -22), (-48, -28), (-55, -35), (-65, -41),
           (-70, -52), (-73, -44), (-73, -30), (-72, -18), (-78, -8),
           (-80, 0), (-78, 9)],
    "af": [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (0, 36), (10, 37),
           (15, 32), (20, 32), (30, 31), (32, 31), (35, 28), (38, 22),
           (43, 12), (48, 11), (51, 10), (48, 2), (42, -5), (40, -12),
           (36, -18), (33, -26), (28, -33), (20, -35), (16, -28),
           (12, -18), (12, -8), (9, -1), (9, 4), (-8, 5), (-13, 8),
           (-17, 15)],
    "eu": [(-10, 36), (-9, 43), (-2, 44), (-2, 48), (0, 50), (3, 52),
           (7, 54), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58),
           (28, 60), (30, 62), (28, 70), (20, 70), (12, 70), (5, 60),
           (-2, 58), (-5, 50), (-10, 48), (-10, 36)],
    "as": [(30, 70), (40, 68), (55, 69), (70, 72), (90, 75), (110, 74),
           (130, 72), (150, 70), (165, 66), (178, 65), (170, 60),
           (162, 58), (158, 52), (150, 59), (142, 50), (140, 40),
           (135, 35), (127, 35), (122, 30), (120, 22), (112, 20),
           (108, 12), (105, 8), (100, 6), (97, 10), (94, 17), (90, 22),
           (86, 20), (80, 15), (76, 10), (72, 20), (66, 25), (60, 25),
           (54, 27), (50, 29), (48, 30), (44, 29), (40, 32), (36, 36),
           (33, 36), (30, 36), (30, 42), (28, 45), (30, 70)],
    "oc": [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33),
           (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
           (145, -38), (150, -37), (153, -27), (153, -24), (150, -22),
           (146, -19), (142, -11), (137, -12), (132, -12), (126, -14),
           (122, -14), (117, -20), (113, -22)],
    "nz": [(167, -35), (170, -40), (174, -41), (178, -38), (174, -35),
           (167, -35)],
}


def spread_pins(featured, x0, y0, w, h, min_dist=18.0, max_nudge=36.0):
    """Fan crowded pins apart deterministically: pairwise repulsion from the
    true lon/lat spot, nudges clamped, fixed iteration count. Returns the
    list of (true_x, true_y, pin_x, pin_y) in page coordinates."""
    pts = [lonlat(s["lon"], s["lat"], x0, y0, w, h) for s in featured]
    nudges = [[0.0, 0.0] for _ in pts]
    for _ in range(120):
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                xi = pts[i][0] + nudges[i][0]
                yi = pts[i][1] + nudges[i][1]
                xj = pts[j][0] + nudges[j][0]
                yj = pts[j][1] + nudges[j][1]
                dx, dy = xj - xi, yj - yi
                dist = math.hypot(dx, dy)
                if dist < min_dist:
                    if dist < 0.01:
                        # identical spots (e.g. four Washington pins):
                        # push apart along a deterministic direction
                        ang = math.radians(37 * (i + 1) + 71 * (j + 1))
                        dx, dy, dist = math.cos(ang), math.sin(ang), 1.0
                    ux, uy = dx / dist, dy / dist
                    push = (min_dist - dist) / 2 + 0.05
                    nudges[i][0] -= ux * push
                    nudges[i][1] -= uy * push
                    nudges[j][0] += ux * push
                    nudges[j][1] += uy * push
        # clamp nudges and keep pins inside the panel
        for i in range(len(pts)):
            for k in (0, 1):
                nudges[i][k] = max(-max_nudge, min(max_nudge, nudges[i][k]))
            px = min(max(pts[i][0] + nudges[i][0], x0 + 10), x0 + w - 10)
            py = min(max(pts[i][1] + nudges[i][1], y0 + 10), y0 + h - 10)
            nudges[i][0] = px - pts[i][0]
            nudges[i][1] = py - pts[i][1]
    out = []
    for s, (tx, ty), (nx, ny) in zip(featured, pts, nudges):
        out.append((tx, ty, tx + nx, ty + ny))
    return out


def draw_map(d, x0, y0, w, h, featured):
    """Dark navy panel, pale dotted continents, red numbered pins 1-13."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVYMAP)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for pts in LAND.values():
        md.polygon([lonlat(lon, lat, 0, 0, w, h) for lon, lat in pts], fill=255)
    step = 6
    for gy in range(3, h, step):
        for gx in range(3, w, step):
            if mask.getpixel((gx, gy)):
                d.ellipse([x0 + gx - 1, y0 + gy - 1, x0 + gx + 1, y0 + gy + 1],
                          fill=MAPDOT)
    pins = spread_pins(featured, x0, y0, w, h)
    for a in range(len(pins)):
        for b in range(a + 1, len(pins)):
            dist = math.hypot(pins[a][2] - pins[b][2], pins[a][3] - pins[b][3])
            assert dist >= 17.0, (
                "map pins %d and %d only %.1f px apart"
                % (featured[a]["n"], featured[b]["n"], dist))
    for s, (tx, ty, px, py) in zip(featured, pins):
        if math.hypot(px - tx, py - ty) > 3:
            d.line([tx, ty, px, py], fill=(150, 150, 150), width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(150, 150, 150))
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = sans_b(10)
        t = str(s["n"])
        d.text((px - d.textlength(t, font=f) / 2, py - 6), t, font=f,
               fill=(255, 255, 255))
    return pins


# ---- flowing briefs paragraph ----------------------------------------------
def draw_briefs_para(d, x, y, width, briefs, f_reg, f_bold, leading):
    """One flowing paragraph: bold 'N PLACE —' lead-ins, regular body.
    Words wrap greedily across the full column width. Returns line count."""
    words = []  # (word, font)
    for idx, (lead, body) in enumerate(briefs):
        for w in lead.split():
            words.append((w, f_bold))
        for w in body.split():
            words.append((w, f_reg))
        if idx < len(briefs) - 1:
            words.append((" ", f_reg))  # separator between briefs
    space_w = d.textlength(" ", font=f_reg)
    lines, cur, cur_w = [], [], 0.0
    for word, f in words:
        ww = d.textlength(word, font=f)
        add = ww if not cur else ww + space_w
        if cur_w + add <= width or not cur:
            cur.append((word, f))
            cur_w += add
        else:
            lines.append(cur)
            cur, cur_w = [(word, f)], ww
    if cur:
        lines.append(cur)
    yy = y
    for line in lines:
        xx = x
        for j, (word, f) in enumerate(line):
            if word != " ":
                d.text((xx, yy), word, font=f, fill=INK)
            xx += d.textlength(word, font=f) + (space_w if j < len(line) - 1
                                                else 0)
        yy += leading
    return len(lines)


# ---- page ------------------------------------------------------------------
MX = 36
CW = W - 2 * MX  # 952


def main():
    data = json.loads((HERE / "stories_v5.json").read_text())
    stories = {s["n"]: s for s in data["stories"]}
    lay = data["layout"]
    assert len(stories) == 36
    for n, s in stories.items():
        assert s["verified"] is True, "story %d not verified" % n

    # region counts, recomputed from the verified JSON (must total 36)
    from collections import Counter
    counts = Counter(s["region"] for s in stories.values())
    assert sum(counts.values()) == 36
    for key, val in lay["region_counts"].items():
        assert counts[{"europe": "europe", "americas": "americas",
                       "asia-pacific": "asia", "mideast": "middle_east",
                       "africa": "africa", "oceania": "oceania",
                       "world": "global"}[key]] == val, key

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    report = []

    # --- top bar ------------------------------------------------------------
    d.text((MX, 7), lay["top_bar_left"], font=sans_b(12), fill=RED)
    rt = lay["top_bar_right"]
    d.text((W - MX - d.textlength(rt, font=sans_b(12)), 7), rt,
           font=sans_b(12), fill=INK)
    d.line([0, 24, W, 24], fill=INK, width=1)

    # --- masthead -----------------------------------------------------------
    mast = lay["title"]
    mf = serif_b(72)
    assert d.textlength(mast, font=mf) <= CW, "masthead too wide"
    d.text((MX, 30), mast, font=mf, fill=INK)
    sub = lay["sub_headline"]
    sf = serif_i(16)
    assert d.textlength(sub, font=sf) <= CW, "sub-headline too wide"
    d.text((MX, 103), sub, font=sf, fill=RED)
    d.line([MX, 127, W - MX, 127], fill=INK, width=1)

    # --- big-number strip ---------------------------------------------------
    strip = lay["big_number_strip"]
    col_w = CW // 6
    for i, cell in enumerate(strip):
        cx = MX + i * col_w
        d.text((cx, 135), cell["figure"], font=sans_b(27), fill=RED)
        lines = fit_lines(d, cell["caption"], sans(10), col_w - 8, 2,
                          "strip %d caption" % i)
        put_lines(d, cx, 165, lines, sans(10), INK, 12)
    d.line([MX, 193, W - MX, 193], fill=INK, width=1)
    report.append("number strip: 6 cells, captions <=2 lines")

    # --- region chips -------------------------------------------------------
    chip_y = 199
    xx = MX
    for key in CHIP_ORDER:
        lk, ck = CHIP_KEYS[key]
        label = "%s %d" % (lay["region_labels"][lk], lay["region_counts"][ck])
        f = sans_b(11)
        tw = d.textlength(label, font=f)
        d.rectangle([xx, chip_y, xx + tw + 16, chip_y + 22], fill=CHIP[key])
        d.text((xx + 8, chip_y + 4), label, font=f, fill=(255, 255, 255))
        xx += tw + 16 + 8
    assert xx - 8 <= W - MX, "region chips overflow"
    report.append("region chips: %s = 36 total"
                  % " + ".join("%s %d" % (lay["region_labels"][CHIP_KEYS[k][0]],
                                          lay["region_counts"][CHIP_KEYS[k][1]])
                               for k in CHIP_ORDER))

    # --- heroes 1-3 ---------------------------------------------------------
    hero_x = [MX, MX + 321, MX + 642]
    hero_w = 309
    hero_y = 229
    for i, n in enumerate((1, 2, 3)):
        s = stories[n]
        x = hero_x[i]
        HERO_ART[n](d, x, hero_y, hero_w, 84)
        d.text((x, hero_y + 90), "%d · %s" % (n, s["tag"]), font=sans_b(10),
               fill=RED)
        hl = fit_lines(d, s["headline"], serif_b(24), hero_w, 2,
                       "hero %d headline" % n)
        put_lines(d, x, hero_y + 104, hl, serif_b(24), INK, 27)
        dl = fit_lines(d, lay["hero_decks"][str(n)], sans(11), hero_w, 2,
                       "hero %d deck" % n)
        put_lines(d, x, hero_y + 160, dl, sans(11), (60, 60, 60), 13)
        report.append("hero %d: headline %d line(s), deck %d line(s)"
                      % (n, len(hl), len(dl)))
    d.line([MX, 423, W - MX, 423], fill=HAIR, width=1)

    # --- cards 4-13 (2 rows x 5) --------------------------------------------
    card_x = [MX, MX + 192, MX + 384, MX + 576, MX + 768]
    card_w = 180
    card_rows = [431, 573]
    for i, n in enumerate(range(4, 14)):
        s = stories[n]
        x = card_x[i % 5]
        y = card_rows[i // 5]
        d.rectangle([x, y, x + card_w, y + 134], outline=CARDLINE, width=1)
        CARD_ART[n](d, x + 1, y + 1, card_w - 2, 36)
        d.text((x + 6, y + 44), "%d · %s" % (n, s["tag"]), font=sans_b(9),
               fill=RED)
        headline = lay.get("card_headlines", {}).get(str(n), s["headline"])
        hl = fit_lines(d, headline, serif_b(13), card_w - 12, 2,
                       "card %d headline" % n)
        put_lines(d, x + 6, y + 58, hl, serif_b(13), INK, 16)
        dl = fit_lines(d, lay["card_decks"][str(n)], sans(10), card_w - 12,
                       3, "card %d deck" % n)
        put_lines(d, x + 6, y + 92, dl, sans(10), (60, 60, 60), 11)
        report.append("card %d: headline %d line(s), deck %d line(s)"
                      % (n, len(hl), len(dl)))

    # --- map + briefs -------------------------------------------------------
    d.text((MX, 715), "WHERE IT HAPPENED", font=sans_b(11), fill=RED)
    brief_head = "ALSO ON FRIDAY 20 NOVEMBER — 23 MORE STORIES"
    d.text((W - MX - d.textlength(brief_head, font=sans_b(11)), 715),
           brief_head, font=sans_b(11), fill=RED)
    d.line([MX, 731, W - MX, 731], fill=RED, width=2)
    featured = [stories[n] for n in range(1, 14)]
    draw_map(d, MX, 737, 330, 180, featured)
    d.text((MX, 921), "Red numbers mark stories 1–13. Positions are "
           "approximate.", font=serif_i(9), fill=GREY)
    brief_items = []
    for n in range(14, 37):
        s = stories[n]
        text = lay["briefs"][str(n)]
        lead, _, body = text.partition(" — ")
        brief_items.append((lead + " —", body))
    nlines = draw_briefs_para(d, MX + 342, 737, W - MX - (MX + 342),
                              brief_items, sans(9), sans_b(9), 11)
    assert nlines * 11 <= 210, "briefs need %d lines, box holds 19" % nlines
    report.append("briefs: %d lines at 9px/11px leading (box: 19 lines max)"
                  % nlines)

    # --- DATE CHECK ---------------------------------------------------------
    dc_y, dc_h = 956, 50
    d.rectangle([MX, dc_y, W - MX, dc_y + dc_h], outline=RED, width=2)
    dc_label = "DATE CHECK"
    d.text((MX + 8, dc_y + 6), dc_label, font=sans_b(11), fill=RED)
    label_w = d.textlength(dc_label, font=sans_b(11)) + 16
    dc_text = lay["date_check"]
    # first line starts right of the label, following lines full width
    first_w = (W - MX - 8) - (MX + 8 + label_w)
    full_w = W - MX - 8 - (MX + 8)
    first = wrap(d, dc_text, sans(10), first_w)
    rest = " ".join(first[1:]) if len(first) > 1 else ""
    # re-wrap: line 1 = first[0]; remaining text wrapped at full width
    remaining = dc_text[len(first[0]):].strip()
    rest_lines = wrap(d, remaining, sans(10), full_w) if remaining else []
    dc_lines = [first[0]] + rest_lines
    assert len(dc_lines) <= 3, "DATE CHECK: %d lines, max 3" % len(dc_lines)
    put_lines(d, MX + 8 + label_w, dc_y + 6, dc_lines[:1], sans(10), INK, 12)
    put_lines(d, MX + 8, dc_y + 18, dc_lines[1:], sans(10), INK, 12)
    report.append("DATE CHECK: %d line(s), %d chars"
                  % (len(dc_lines), len(dc_text)))

    # --- footer -------------------------------------------------------------
    footer = lay["footer"]
    assert d.textlength(footer, font=sans(9)) <= CW, "footer too long"
    d.text((MX, 1010), footer, font=sans(9), fill=GREY)
    report.append("footer: 1 line, %d chars" % len(footer))

    # 256-colour palette PNG: smaller bytes; quantisation is deterministic.
    img.convert("P", palette=Image.ADAPTIVE, colors=256).save(
        HERE / "entry.png", optimize=True)
    print("wrote", HERE / "entry.png")
    for line in report:
        print("  -", line)


if __name__ == "__main__":
    main()
