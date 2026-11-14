"""jokers.py — four Jokers.

  Wacky Joker    +Mult for a Spectrum: a fool whose cap has five tails, one
                 in each suit colour, mid-raspberry, over a five-suit fan.
  Shrewd Joker   +Chips for a Spectrum: narrow eyes, a one-sided smile, a
                 two-tone cap, five little cards he has already counted.
  The Coalition  xMult for a Spectrum: five banners in the five suit colours
                 swept in to one point, a five-suit hand held over the knot.
  Envious Joker  unscored cards turn Wild: green to the gills, glaring
                 sideways at a card as it turns into a star.

They follow the layout habits of Balatro's Jokers (white card, JOKER set
down the left edge and again, turned, up the right; the hand shown as small
cards under the figure) but the figures, faces, lettering and compositions
are drawn here from nothing.

Every pixel here is set by this program.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

from pixel import Canvas, Palette, dilate, erode, sheet

W, H = 71, 95

PAL = Palette(
    wh="#ffffff", bd="#bfc7d5", dk="#4f6367", sh="#dcdcdc", gy="#b4bcc8",
    g="#ffa300", g2="#d07c00",
    H="#f03464", D="#f06b3f", C="#235955", S="#3c4368", X="#9a5bd6",
    H2="#b8204a", D2="#c24e28", C2="#16403d", S2="#2a2f4d", X2="#7443b0",
    red="#fd5f55", blue="#009cfd", blue2="#0077c9",
    v1="#8e7cc3", v2="#5d5391", v3="#b7a9e0", t1="#6fa8a0", t2="#467a78", t3="#9ccdc4",
    e0="#1f5c3a", e1="#2f8a4e", e2="#56b76a", e3="#9ad98f", e4="#d2f0c0",
    slate="#4a5568", slate2="#3b4456", pale="#c7d0e0",
)

LETTERS = {
    "J": ["...####", "....##.", "....##.", "....##.", "....##.", "##..##.", "##..##.", ".####.."],
    "O": [".#####.", "##...##", "##...##", "##...##", "##...##", "##...##", "##...##", ".#####."],
    "K": ["##..##.", "##.##..", "####...", "###....", "####...", "##.##..", "##..##.", "##...##"],
    "E": ["#######", "##.....", "##.....", "#####..", "##.....", "##.....", "##.....", "#######"],
    "R": ["######.", "##...##", "##...##", "######.", "##.##..", "##..##.", "##...##", "##...##"],
}

MINI = {
    "H": [".#.#.", "#####", "#####", ".###.", "..#.."],
    "D": ["..#..", ".###.", "#####", ".###.", "..#.."],
    "C": [".###.", ".###.", "#####", "##.##", "..#.."],
    "S": ["..#..", ".###.", "#####", "##.##", "..#.."],
    "X": ["..#..", "..#..", "#####", "..#..", "..#.."],
}
SUITS = "HDXCS"


# ---------------------------------------------------------------- frames ----
def card_mask(c):
    m = c.blank()
    m[1:94, 1:70] = True
    for i, n in enumerate((3, 1, 1)):
        for y in (1 + i, 93 - i):
            m[y, 1:1 + n] = False
            m[y, 70 - n:70] = False
    return m


def card(c, fill=None):
    m = card_mask(c)
    c.fill(m, "bd")
    inner = erode(m, diag=True)
    c.fill(inner, "wh")
    if fill:
        field = erode(erode(inner, diag=True))
        c.fill(field, fill)
        return field
    return inner


def joker_text(c, col):
    t = Canvas(W, H, c.pal)
    for i, ch in enumerate("JOKER"):
        t.stamp(LETTERS[ch], 6, 7 + 9 * i, {"#": col})
    c.blit(t)
    c.blit(t.rot180())


# ----------------------------------------------------------------- parts ----
def blob(c, m, col, edge="dk"):
    c.fill(m, col)
    if edge:
        c.fill(dilate(m) & ~m, edge)


def tail(c, p0, p1, p2, r0, r1, col, shade=None, bell="g"):
    """A cap tail: a tapering stroke along a quadratic curve, with a bell."""
    yy, xx = c.grid()
    m = c.blank()
    for t in np.linspace(0, 1, 60):
        x = (1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1]
        r = r0 + (r1 - r0) * t
        m |= (xx - x) ** 2 + (yy - y) ** 2 <= r * r
    blob(c, m, col)
    if shade:
        low = m & ~np.roll(m, -1, axis=0) | (m & ~np.roll(m, -1, axis=1))
        c.fill(m & dilate(low) & erode(m) | low, shade)
    if bell:
        blob(c, c.ellipse_mask(round(p2[0]), round(p2[1]), 1.6, 1.6), bell)
    return m


def head(c, cx, cy, skin="wh", shade="sh", rx=8.4, ry=9.4):
    yy, xx = c.grid()
    m = c.ellipse_mask(cx, cy, rx, ry)
    blob(c, m, skin)
    c.fill(m & ~c.ellipse_mask(cx + 1.6, cy - 1.2, rx, ry), shade)
    return m


def grin(c, cx, cy, w, d, col, teeth=True, tilt=0.0):
    """A crescent smile: the lower part of an ellipse under a sagging lip."""
    yy, xx = c.grid()
    lip = cy + tilt * (xx - cx) + ((xx - cx) / w) ** 2 * -1.5
    m = (((xx - cx) / w) ** 2 + ((yy - cy) / d) ** 2 <= 1) & (yy >= lip)
    c.fill(m, col)
    if teeth:
        c.fill(m & (yy <= lip + 1.2) & (np.abs(xx - cx) < w - 1.5), "wh")
    return m


def mini_card(c, cx, cy, ang, suit=None, w=11, h=15, face="wh", edge="dk", dot=None,
              at=(0, 0)):
    """A small playing card leaning by ang degrees. It is sheared in whole
    pixel steps rather than rotated, so its edges stay clean staircases.
    `at` moves the pip from the centre, in the card's own frame."""
    yy, xx = c.grid()
    cx, cy = int(round(cx)), int(round(cy))
    t = np.tan(np.radians(ang))
    sx = np.rint((yy - cy) * t)
    sy = np.rint((xx - cx) * t)
    m = (np.abs(xx - cx + sx) <= w // 2) & (np.abs(yy - cy - sy) <= h // 2)
    blob(c, m, face, edge)
    x = cx + at[0] - int(np.rint(at[1] * t))
    y = cy + at[1] + int(np.rint(at[0] * t))
    if suit:
        c.stamp(MINI[suit], x - 2, y - 2, {"#": suit})
    if dot:
        c.rect(x - 1, y - 1, x, y, dot)
    return m


def fan(c, px, py, rad, spread, suits=SUITS, **kw):
    n = len(suits)
    for i, s in enumerate(suits):
        ang = (i - (n - 1) / 2) * spread
        a = np.radians(ang)
        mini_card(c, px + rad * np.sin(a), py - rad * np.cos(a), ang, s, at=(-2, -3), **kw)


def ruff(c, cx, y, n, wid, drop, cols, bells=True):
    """A collar of n hanging points."""
    step = wid / n
    for i in range(n):
        x0 = cx - wid / 2 + i * step
        d = drop * (0.75 + 0.25 * np.cos((i - (n - 1) / 2) / n * 2.2))
        m = c.poly_mask([(int(round(x0)), y), (int(round(x0 + step)), y),
                         (int(round(x0 + step / 2)), int(round(y + d)))])
        blob(c, m, cols[i % len(cols)])
        if bells:
            blob(c, c.ellipse_mask(round(x0 + step / 2), round(y + d) + 1, 1.2, 1.2), "g")


# ---------------------------------------------------------------- jokers ----
def wacky():
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    card(c)
    joker_text(c, "dk")
    cx, cy = 36, 41
    fan(c, cx - 1, 97, 24, 15)
    ruff(c, cx, cy + 6, 5, 34, 9, ["H", "D", "X", "C", "S"])
    # five tails, outermost first
    spec = [(-168, 16, 40, "H", "H2"), (-12, 16, -40, "S", "S2"),
            (-128, 17, 28, "D", "D2"), (-52, 17, -28, "C", "C2"),
            (-90, 17, 22, "X", "X2")]
    for ang, ln, curl, col, sh in spec:
        a = np.radians(ang)
        b = np.radians(ang - curl)
        p0 = (cx + 6 * np.cos(a), cy - 3 + 7 * np.sin(a))
        p1 = (p0[0] + ln * 0.6 * np.cos(a), p0[1] + ln * 0.6 * np.sin(a))
        p2 = (p1[0] + ln * 0.55 * np.cos(b), p1[1] + ln * 0.55 * np.sin(b))
        tail(c, p0, p1, p2, 4.2, 1.2, col, sh)
    m = head(c, cx, cy, rx=9.4, ry=9.4)
    band = m & (yy <= cy - 7)
    c.fill(band, "g")
    c.fill(m & (yy == cy - 6), "dk")
    # one eye wide, one winking
    c.rect(cx - 6, cy - 3, cx - 3, cy, "dk")
    c.rect(cx - 5, cy - 2, cx - 4, cy - 1, "wh")
    c.px(cx - 4, cy - 1, "dk")
    c.path([(cx + 2, cy - 1), (cx + 4, cy - 3), (cx + 6, cy - 1)], "dk")
    c.rect(cx - 1, cy + 1, cx, cy + 2, "red")                # nose
    grin(c, cx, cy + 3, 6.4, 4.8, "dk", teeth=True)
    c.rect(cx - 1, cy + 6, cx + 2, cy + 7, "red")            # tongue
    return c


def shrewd():
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    card(c)
    joker_text(c, "dk")
    cx, cy = 36, 35
    # five small cards, counted and squared away
    for i, s in enumerate(SUITS):
        mini_card(c, 19 + i * 8, 77 - (i % 2) * 3, 0, None, w=9, h=13, edge="gy", dot=s)
    # collar: a wide striped crescent in two halves
    for sg, a, b, hi in ((-1, "v1", "v2", "v3"), (1, "t1", "t2", "t3")):
        lobe = c.ellipse_mask(cx + sg * 9, cy + 16, 11.5, 7.5) & ((xx - cx) * sg >= 0)
        blob(c, lobe, a)
        rr = np.hypot((xx - cx - sg * 9) / 11.5, (yy - (cy + 16) + 9) / 14.0)
        c.fill(lobe & ((rr * 9).astype(int) % 2 == 0), b)
        c.fill(lobe & ~c.ellipse_mask(cx + sg * 9 + 1, cy + 17, 11.5, 7.5), hi)
    c.vline(cx, cy + 9, cy + 23, "dk")
    # cap: two heavy lobes, one long tail thrown over
    tail(c, (cx - 5, cy - 6), (cx - 15, cy - 16), (cx - 17, cy - 2), 5.0, 1.6, "v1", "v2")
    tail(c, (cx + 5, cy - 6), (cx + 14, cy - 18), (cx + 20, cy - 6), 5.0, 1.6, "t1", "t2")
    crown = c.ellipse_mask(cx, cy - 7, 9.2, 6.2) & (yy <= cy - 4)
    blob(c, crown & (xx <= cx), "v1")
    blob(c, crown & (xx > cx), "t1")
    c.fill(crown & (xx <= cx) & (yy == cy - 10), "v3")
    c.fill(crown & (xx > cx) & (yy == cy - 10), "t3")
    m = head(c, cx, cy + 1, rx=8.0, ry=8.8)
    c.fill(m & (yy <= cy - 4), "v1")
    c.fill(m & (yy <= cy - 4) & (xx > cx), "t1")
    c.fill(m & (yy == cy - 3), "dk")
    # narrow eyes looking sideways, one brow up
    for ex in (cx - 6, cx + 2):
        c.hline(ex, ex + 4, cy, "dk")
        c.rect(ex + 3, cy + 1, ex + 4, cy + 1, "dk")
        c.px(ex, cy + 1, "sh")
    c.path([(cx - 7, cy - 2), (cx - 3, cy - 1)], "dk")
    c.path([(cx + 2, cy - 2), (cx + 6, cy - 3)], "dk")
    c.pxs([(cx, cy + 3), (cx - 1, cy + 3)], "gy")              # nose
    g = grin(c, cx + 1, cy + 5, 5.4, 3.6, "blue", tilt=-0.22)
    return c


def coalition():
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    field = card(c, "slate")
    cx, cy = 35, 36
    dx, dy = xx - cx, yy - cy
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx) + r * 0.012 - 0.05
    sector = (th % (2 * np.pi)) / (2 * np.pi) * 5
    k = sector.astype(int) % 5
    f = sector - np.floor(sector)
    width = 0.22 + 0.26 * np.clip(r / 48, 0, 1)
    band = field & (np.abs(f - 0.5) < width / 2 + 0.02) & (r > 5)
    core = field & (np.abs(f - 0.5) < width / 2 - 0.07) & (r > 5)
    c.fill(field & ((xx * 3 + yy * 5) % 11 == 0) & ~band, "slate2")
    for i, (a, b) in enumerate((("H", "H2"), ("D", "D2"), ("X", "X2"), ("C", "C2"), ("S", "S2"))):
        if a in "CS":
            a, b = {"C": ("t2", "C"), "S": ("v2", "S")}[a]
        c.fill(band & (k == i), b)
        c.fill(core & (k == i), a)
    # the knot
    blob(c, c.ellipse_mask(cx, cy, 6.4, 6.4), "g", edge="slate2")
    c.ellipse(cx, cy, 4.2, 4.2, "g2", fill=False)
    c.stamp(MINI["X"], cx - 2, cy - 2, {"#": "wh"})
    fan(c, cx, 94, 27, 14, edge="slate2")
    joker_text(c, "wh")
    return c


def envious():
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    card(c)
    joker_text(c, "dk")
    cx, cy = 33, 38
    ruff(c, cx, cy + 6, 4, 28, 8, ["e1", "e0"], bells=True)
    tail(c, (cx - 5, cy - 6), (cx - 16, cy - 14), (cx - 13, cy + 2), 4.6, 1.4, "e1", "e0")
    tail(c, (cx + 4, cy - 7), (cx + 8, cy - 22), (cx + 19, cy - 15), 4.6, 1.4, "e2", "e1")
    m = head(c, cx, cy, skin="e4", shade="e3")
    cap = m & (yy <= cy - 5)
    c.fill(cap, "e1")
    c.fill(cap & (xx > cx), "e2")
    c.fill(m & (yy == cy - 4), "dk")
    # eyes cut hard to the right, brows down
    for ex in (cx - 6, cx + 2):
        eye = (yy >= cy - 1) & (yy <= cy) & (xx >= ex) & (xx <= ex + 4)
        blob(c, eye, "wh")
        c.rect(ex + 3, cy - 1, ex + 4, cy, "e0")
    c.path([(cx - 7, cy - 4), (cx - 2, cy - 3)], "dk")
    c.path([(cx + 7, cy - 4), (cx + 2, cy - 3)], "dk")
    c.pxs([(cx, cy + 3), (cx + 1, cy + 3)], "e2")
    # a sour mouth, bitten lip
    c.path([(cx - 4, cy + 7), (cx - 2, cy + 5), (cx + 2, cy + 5), (cx + 4, cy + 6), (cx + 5, cy + 5)], "dk")
    c.rect(cx - 1, cy + 6, cx, cy + 6, "wh")
    # what he wants: a card turning into a star
    mini_card(c, 20, 76, 0, None, w=11, h=15, dot="gy")
    c.hline(28, 33, 76, "X")
    c.path([(31, 74), (33, 76), (31, 78)], "X")
    mini_card(c, 44, 75, 0, None, w=13, h=17)
    c.stamp(["...#...", "...#...", "..###..", "#######", "..###..", "...#...", "...#..."],
            41, 72, {"#": "X"})
    for x, y in ((54, 64), (36, 65), (53, 86)):                 # sparks
        c.vline(x, y - 1, y + 1, "X")
        c.hline(x - 1, x + 1, y, "X")
    return c


def cells():
    return [wacky(), shrewd(), coalition(), envious()]


def sheet_canvas():
    return sheet(cells())


def outputs():
    return {"jokers.png": (sheet_canvas(), PAL)}
