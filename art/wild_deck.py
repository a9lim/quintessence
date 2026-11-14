"""wild_deck.py — the Wild suit: thirteen card fronts, the suit icon.

The fifth suit of Quintessence. Its pip is a solid four-pointed star: four
points for the four suits it stands in for. (An open-eyed version read too
thin beside vanilla's pips; the Ace keeps a quartered lozenge at its heart.)
Violet in the normal deck, green in the high-contrast deck (the hues the
other four suits leave free).

Fronts are ink only (the game draws the card body underneath): corner rank
glyph + corner pip, pips laid out the way a poker deck lays them out, one
big star for the Ace, and three double-headed court figures: the Jack with a
star-tipped wand, the Queen with a hand mirror, the King with an orb. Each
court wears the four old suit colours somewhere, because Wild is all of them.

Every pixel here is set by this program.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

from pixel import Canvas, Palette, dilate, sheet

W, H = 71, 95
CX, CY = 35, 47

# ---------------------------------------------------------------- palette ----
NORMAL = dict(
    k="#374649",   # outline / hair
    m="#9a5bd6",   # Wild violet: pips, glyphs, robes
    d="#7443b0",   # violet, shade
    g="#ffa300",   # gold
    b="#29adff",   # blue accent
    w="#ffffff",
    s="#e6e6e6",   # faces, hands
    a="#acacac",   # face shade
    H="#f03464", D="#f06b3f", C="#235955", S="#3c4368",   # the four suits
)
HIGH_CONTRAST = dict(
    m="#1fa84f", d="#157a39",
    H="#f83b2f", D="#e39100", C="#009cfd", S="#8a71e1",
)
PAL = Palette(**NORMAL)
PAL_HC = PAL.swapped(**HIGH_CONTRAST)

# ------------------------------------------------------------------ pips ----
PIP = """
.....#.....
....###....
....###....
...#####...
.#########.
###########
.#########.
...#####...
....###....
....###....
.....#.....
"""
PIP_SMALL = """
....#....
...###...
...###...
.#######.
#########
.#######.
...###...
...###...
....#....
"""
SPARK = """
...#...
...#...
..###..
#######
..###..
...#...
...#...
"""

# ---------------------------------------------------------------- glyphs ----
# My own 7x8 face: bold grotesque, two-pixel strokes. '10' is an 8-wide
# ligature.
GLYPHS = {
    "2": """
.#####.
##...##
.....##
...###.
.###...
##.....
#######
#######""",
    "3": """
.#####.
##...##
.....##
..####.
.....##
.....##
##...##
.#####.""",
    "4": """
....##.
...###.
..####.
.##.##.
##..##.
#######
....##.
....##.""",
    "5": """
#######
##.....
##.....
######.
.....##
.....##
##...##
.#####.""",
    "6": """
.#####.
##...##
##.....
######.
##...##
##...##
##...##
.#####.""",
    "7": """
#######
#######
....##.
...##..
...##..
..##...
..##...
..##...""",
    "8": """
.#####.
##...##
##...##
.#####.
##...##
##...##
##...##
.#####.""",
    "9": """
.#####.
##...##
##...##
##...##
.######
.....##
##...##
.#####.""",
    "10": """
.#..###.
##.##.##
##.##.##
##.##.##
##.##.##
##.##.##
##.##.##
##..###.""",
    "J": """
...####
....##.
....##.
....##.
....##.
##..##.
##..##.
.####..""",
    "Q": """
.#####.
##...##
##...##
##...##
##...##
##.####
##..##.
.###.##""",
    "K": """
##..##.
##.##..
####...
###....
####...
##.##..
##..##.
##...##""",
    "A": """
..###..
.#####.
##...##
##...##
#######
#######
##...##
##...##""",
}

# pip centres for the top-left origin of an 11x11 pip; (x, y, upside_down).
# The star is its own rotation, so the flag only documents the layout.
L, M_, R = 19, 30, 41
LAYOUT = {
    2: [(M_, 13), (M_, 71)],
    3: [(M_, 13), (M_, 42), (M_, 71)],
    4: [(L, 13), (R, 13), (L, 71), (R, 71)],
    5: [(L, 13), (R, 13), (M_, 42), (L, 71), (R, 71)],
    6: [(L, 13), (R, 13), (L, 42), (R, 42), (L, 71), (R, 71)],
    7: [(L, 13), (R, 13), (M_, 27), (L, 42), (R, 42), (L, 71), (R, 71)],
    8: [(L, 13), (R, 13), (M_, 27), (L, 42), (R, 42), (M_, 57), (L, 71), (R, 71)],
    9: [(L, 13), (R, 13), (M_, 24), (L, 35), (R, 35), (L, 49), (R, 49),
        (L, 71), (R, 71)],
    10: [(L, 13), (R, 13), (M_, 24), (L, 35), (R, 35), (L, 49), (R, 49),
         (M_, 60), (L, 71), (R, 71)],
}


def corners(c, rank):
    """Rank glyph and small pip, top-left, and the same rotated bottom-right."""
    t = Canvas(W, H, c.pal)
    t.stamp(GLYPHS[rank], 6, 7, {"#": "m"})
    t.stamp(PIP_SMALL, 5, 16, {"#": "m"})
    c.blit(t)
    c.blit(t.rot180())


def number_card(n):
    c = Canvas(W, H, PAL)
    corners(c, str(n))
    for x, y in LAYOUT[n]:
        c.stamp(PIP, x, y, {"#": "m"})
    return c


def big_star(c, cx, cy, rx, ry, p=7.0):
    """The Ace's star: two crossed lozenges (arm half-width p), and at its heart a lozenge quartered in
    the four suit colours (the one place there is room to say it outright)."""
    yy, xx = c.grid()
    dx, dy = np.abs(xx - cx), np.abs(yy - cy)
    star = (dx / p + dy / (ry + 0.5) <= 1.0) | (dx / (rx + 0.5) + dy / p <= 1.0)
    c.fill(star, "m")
    c.fill(dx + dy <= 5, 0)
    gem = dx + dy <= 3
    c.fill(gem & (xx <= cx) & (yy <= cy), "H")
    c.fill(gem & (xx > cx) & (yy <= cy), "D")
    c.fill(gem & (xx <= cx) & (yy > cy), "C")
    c.fill(gem & (xx > cx) & (yy > cy), "S")


def ace():
    c = Canvas(W, H, PAL)
    corners(c, "A")
    big_star(c, CX, CY, 18, 20)
    return c


# ---------------------------------------------------------------- courts ----
# Each court is drawn as one upright figure over the whole cell, then cut
# along a line through the centre and completed with its own 180-degree
# rotation (Canvas.double_head). The Jack and Queen are cut on opposite
# diagonals, the King straight across his belt.
def blob(c, m, col, edge="k"):
    """Fill a mask and ring it with a 1-px outline."""
    c.fill(m, col)
    if edge:
        c.fill(dilate(m) & ~m, edge)


def face(c, cx=35, top=13):
    """The blank oval face of a Balatro court: light, shaded low on one side."""
    yy, xx = c.grid()
    m = c.ellipse_mask(cx, top + 6, 4.6, 6.3)
    c.fill(m, "s")
    c.fill(m & (xx - cx + (yy - top - 6) * 0.6 > 3.2), "a")
    c.fill(m & (xx <= cx - 1) & (yy <= top + 5) & (xx - cx + (yy - top) * 0.8 > -3)
           & (xx - cx + (yy - top) * 0.8 < 0), "w")
    return m


def hand(c, x, y):
    m = c.blank()
    m[y:y + 4, x:x + 4] = True
    blob(c, m, "s")
    c.pxs([(x + 3, y + 3), (x + 2, y + 3), (x + 3, y + 2)], "a")


def frame(c):
    c.rect(17, 11, 53, 83, "k", fill=False)


def split(c, slope):
    """(top_mask, dist): dist > 0 above a line through the centre."""
    yy, xx = c.grid()
    dist = np.rint(slope * (xx - CX)) - (yy - CY)   # rint: exact under rotation
    return (dist > 0) | ((dist == 0) & (xx <= CX)), dist


def star_on(c, art, x, y, col="m"):
    t = Canvas(W, H, c.pal)
    t.stamp(art, x, y, {"#": col})
    blob(c, t.mask(), col)


def jack():
    """The Jack: a page in a slouched cap with a feather, a star on a wand,
    and a sash striped in the four suits."""
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    frame(c)
    top, dist = split(c, 1 / 3)

    body = c.poly_mask([(30, 26), (40, 26), (50, 30), (57, 38), (59, 68),
                        (11, 68), (13, 38), (20, 30)])
    blob(c, body, "m")
    with c.clip(body):
        for sg in (-1, 1):
            for a, b in ((4, 12), (6, 19)):
                c.line(CX + sg * a, 30, CX + sg * b, 68, "g")
                c.line(CX + sg * (a + 1), 30, CX + sg * (b + 1), 68, "k")
        for sx in (11, 53):                      # checked sleeves
            pm = c.blank()
            pm[40:69, sx:sx + 7] = True
            c.fill(pm, "w")
            c.checker(pm, "m")
        c.vline(18, 40, 68, "k")
        c.vline(52, 40, 68, "k")
        c.rect(33, 28, 37, 68, "w")              # placket and buttons
        c.vline(32, 28, 68, "k")
        c.vline(38, 28, 68, "k")
        for y in range(36, 68, 4):
            c.px(35, y, "g")
            c.px(35, y + 1, "k")
        for lo, hi, col in ((0, 1, "k"), (1, 3, "H"), (3, 5, "D"),
                            (5, 6, "C"), (6, 7, "S"), (7, 8, "k")):
            c.fill(body & (dist >= lo) & (dist < hi), col)
    for sx in (19, 51):                          # shoulder rolls
        blob(c, c.ellipse_mask(sx, 33, 5.2, 3.4), "g")
        for o in (-3, -1, 1, 3):
            c.line(sx + o, 31, sx + o - 1, 35, "m")
    c.polygon([(29, 26), (35, 32), (41, 26), (41, 28), (35, 34), (29, 28)], "w")
    c.path([(28, 26), (35, 33), (42, 26)], "k")
    c.path([(29, 29), (35, 35), (41, 29)], "k")
    c.rect(33, 24, 37, 27, "a")
    c.ellipse(35, 19, 7.4, 7.6, "k")             # hair: a dark bob
    c.rect(28, 19, 42, 25, "k")
    c.pxs([(27, 24), (43, 24), (28, 26), (42, 26)], "k")
    face(c)
    cap = c.poly_mask([(27, 13), (25, 10), (26, 7), (30, 5), (38, 5), (43, 7),
                       (45, 10), (43, 13)])
    blob(c, cap, "m")
    c.fill(cap & (yy >= 12), "g")
    c.fill(cap & (yy == 11), "k")
    c.pxs([(28, 9), (29, 8), (30, 7), (31, 7)], "w")
    c.pxs([(40, 8), (41, 9), (39, 7)], "d")
    c.path([(41, 8), (45, 5), (48, 5), (50, 7)], "w")   # feather
    c.path([(42, 9), (45, 6), (48, 6), (49, 8)], "w")
    c.path([(41, 7), (44, 4), (48, 4), (51, 6), (51, 8), (49, 9)], "k")
    c.pxs([(43, 10), (44, 9), (46, 8), (47, 8), (45, 7)], "k")
    c.px(40, 10, "b")
    c.vline(60, 14, 51, "g")                     # wand
    c.vline(59, 14, 51, "k")
    c.vline(61, 14, 51, "k")
    for y in (18, 24, 30, 36):
        c.px(60, y, "k")
    blob(c, c.ellipse_mask(60, 52, 1.5, 1.5), "g")
    star_on(c, PIP_SMALL, 56, 5)
    c.px(60, 9, "w")
    c.rect(54, 41, 56, 44, "g")                  # cuff
    c.rect(54, 40, 56, 40, "k")
    c.rect(54, 45, 56, 45, "k")
    hand(c, 58, 41)
    c.double_head(top)
    corners(c, "J")
    return c


def queen():
    """The Queen: long dark hair, a crown of three points, a hand mirror,
    and a girdle set with four stones."""
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    frame(c)
    top, dist = split(c, -1 / 3)

    body = c.poly_mask([(31, 26), (39, 26), (48, 30), (55, 40), (58, 68),
                        (12, 68), (15, 40), (22, 30)])
    blob(c, body, "m")
    with c.clip(body):
        lat = ((xx + yy) % 6 == 0) | ((xx - yy) % 6 == 0)   # quilted bodice
        c.fill(lat, "d")
        c.fill(((xx + yy) % 6 == 0) & ((xx - yy) % 6 == 0), "g")
        for sx, e in ((12, 21), (49, 58)):       # white undersleeves
            pm = c.blank()
            pm[42:69, sx:e + 1] = True
            c.fill(pm, "w")
            c.fill(pm & (yy % 3 == 0), "b")
        c.vline(22, 42, 68, "k")
        c.vline(48, 42, 68, "k")
        c.vline(23, 34, 68, "g")
        c.vline(47, 34, 68, "g")
        # the girdle along the split: gold, four stones
        c.fill(body & (dist >= 0) & (dist < 5), "g")
        c.fill(body & (dist >= 5) & (dist < 6), "k")
        for i, col in enumerate("HDCS"):
            x0 = 19 + i * 9
            c.fill(body & (dist >= 2) & (dist < 4) & (xx >= x0) & (xx < x0 + 3), col)
    for sx in (20, 50):                          # puffed shoulders
        puff = c.ellipse_mask(sx, 35, 5.2, 4.6)
        blob(c, puff, "m")
        with c.clip(puff):
            for o in (-3, 0, 3):
                c.line(sx + o + 1, 31, sx + o - 1, 39, "d")
            c.fill(puff & (yy >= 39), "g")
    # hair, long, turned out at the ends
    c.ellipse(35, 18, 7.6, 7.6, "k")
    c.rect(27, 18, 43, 30, "k")
    c.pxs([(26, 28), (26, 29), (25, 30), (26, 30), (44, 28), (44, 29), (45, 30), (44, 30),
           (27, 31), (43, 31)], "k")
    # ermine collar
    col_l = c.poly_mask([(31, 27), (24, 30), (27, 35), (35, 35)])
    col_r = c.poly_mask([(39, 27), (46, 30), (43, 35), (35, 35)])
    blob(c, col_l | col_r, "w")
    c.pxs([(27, 31), (30, 33), (30, 30), (40, 30), (43, 31), (40, 33)], "k")
    neck = c.poly_mask([(32, 25), (38, 25), (35, 32)])
    blob(c, neck, "s")
    c.pxs([(33, 27), (34, 28), (36, 28), (37, 27)], "g")
    c.px(35, 29, "b")
    face(c)
    c.pxs([(30, 24), (40, 24), (30, 25), (40, 25)], "k")
    crown = c.poly_mask([(28, 12), (28, 6), (31, 9), (35, 5), (39, 9), (42, 6), (42, 12)])
    blob(c, crown, "g")
    c.hline(28, 42, 12, "k")
    c.pxs([(28, 5), (42, 5), (35, 4)], "b")
    c.pxs([(31, 11), (35, 10), (39, 11)], "m")
    c.pxs([(35, 8)], "w")
    # hand mirror, raised in the right hand
    c.vline(60, 18, 30, "g")
    c.vline(59, 18, 30, "k")
    c.vline(61, 18, 30, "k")
    blob(c, c.ellipse_mask(60, 31, 1.5, 1.5), "g")
    blob(c, c.ellipse_mask(60, 12, 4.4, 5.4), "g")
    c.fill(c.ellipse_mask(60, 12, 2.6, 3.6), "b")
    c.pxs([(59, 10), (59, 11), (60, 9)], "w")
    c.pxs([(60, 6), (60, 18)], "m")
    c.rect(54, 23, 56, 26, "g")
    c.rect(54, 22, 56, 22, "k")
    c.rect(54, 27, 56, 27, "k")
    hand(c, 58, 23)
    c.double_head(top)
    corners(c, "Q")
    return c


def king():
    """The King: bearded, in an ermine mantle, an orb on a staff, the four
    suits set in his crown and on his belt."""
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    frame(c)
    top = (yy < CY) | ((yy == CY) & (xx <= CX))

    mantle = c.poly_mask([(28, 27), (42, 27), (52, 30), (57, 38), (58, 47),
                          (12, 47), (13, 38), (18, 30)])
    blob(c, mantle, "w")
    with c.clip(mantle):
        c.fill(mantle & (yy % 5 == 2) & ((xx + (yy // 5) * 3) % 6 == 0), "k")
        c.fill(mantle & (yy % 5 == 3) & ((xx + (yy // 5) * 3) % 6 == 0), "k")
        robe = c.poly_mask([(30, 27), (40, 27), (45, 47), (25, 47)])
        c.fill(robe, "m")
        c.line(30, 27, 25, 47, "k")
        c.line(40, 27, 45, 47, "k")
        c.line(31, 27, 26, 47, "g")
        c.line(39, 27, 44, 47, "g")
        c.fill(robe & (xx > 28) & (xx < 42) & (yy > 30) & ((xx + yy) % 2 == 0)
               & (np.abs(xx - CX) > 3) & (np.abs(xx - CX) < 6 + (yy - 30) * 0.2), "d")
        c.rect(33, 30, 37, 47, "w")
        c.vline(32, 30, 47, "k")
        c.vline(38, 30, 47, "k")
        for y in range(33, 44, 3):
            c.px(35, y, "b")
        # belt
        c.rect(12, 43, 58, 43, "k")
        c.rect(12, 44, 58, 47, "g")
        for x0, col in ((16, "H"), (23, "D"), (44, "C"), (51, "S")):
            c.rect(x0, 45, x0 + 2, 46, col)
        c.rect(32, 44, 38, 47, "k")
        c.rect(33, 45, 37, 47, "m")
    c.hline(13, 57, 47, "k")
    c.rect(33, 47, 37, 47, "w")
    # hair and beard
    c.ellipse(35, 19, 7.6, 7.6, "k")
    c.rect(28, 19, 42, 26, "k")
    face(c)
    beard = c.poly_mask([(30, 21), (40, 21), (41, 25), (39, 29), (35, 32), (31, 29), (29, 25)])
    c.fill(beard, "k")
    c.pxs([(33, 22), (34, 21), (35, 21), (36, 21), (37, 22)], "s")   # under the nose
    c.pxs([(32, 26), (34, 28), (36, 27), (38, 25)], "a")
    crown = c.poly_mask([(27, 13), (26, 7), (30, 10), (33, 6), (35, 9), (37, 6), (40, 10),
                         (44, 7), (43, 13)])
    blob(c, crown, "g")
    c.pxs([(26, 6), (44, 6), (33, 5), (37, 5)], "b")
    c.hline(27, 43, 13, "k")
    for x0, col in ((29, "H"), (33, "D"), (37, "C"), (41, "S")):
        c.rect(x0, 11, x0, 12, col)
    c.vline(35, 3, 6, "g")
    c.hline(34, 36, 4, "g")
    # staff and orb, right hand
    c.vline(60, 16, 47, "g")
    c.vline(59, 16, 47, "k")
    c.vline(61, 16, 47, "k")
    for y in (20, 26, 32):
        c.px(60, y, "k")
    orb = c.ellipse_mask(60, 11, 4.4, 4.4)
    blob(c, orb, "b")
    c.fill(orb & (yy == 11), "g")
    c.fill(orb & (xx == 60) & (yy < 11), "g")
    c.pxs([(58, 8), (58, 9), (57, 9)], "w")
    c.stamp(SPARK, 57, 0, {})
    c.vline(60, 3, 5, "g")
    c.hline(59, 61, 4, "g")
    c.rect(54, 37, 56, 40, "m")
    hand(c, 58, 37)
    c.double_head(top)
    corners(c, "K")
    return c


# ----------------------------------------------------------------- sheet ----
def cells():
    return [number_card(n) for n in range(2, 11)] + [jack(), queen(), king(), ace()]


def deck():
    return sheet(cells())


UI_ICON = """
.......##.......
......####......
......####......
.....######.....
.....######.....
....########....
.##############.
################
################
.##############.
....########....
.....######.....
.....######.....
......####......
......####......
.......##.......
"""


def ui_icon():
    c = Canvas(18, 18, PAL)
    c.stamp(UI_ICON, 1, 1, {"#": "m"})
    return c


def outputs():
    """name -> (canvas, palette)"""
    d, u = deck(), ui_icon()
    return {
        "wild_deck.png": (d, PAL),
        "wild_deck_hc.png": (d, PAL_HC),
        "wild_ui.png": (u, PAL),
        "wild_ui_hc.png": (u, PAL_HC),
    }
