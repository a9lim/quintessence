"""planets.py — five planet cards for the new poker hands.

Quaoar (Spectrum), Haumea (Straight Spectrum), Sedna (Spectrum House),
Makemake (Spectrum Five) and the Asteroid Belt (Bulwark). All trans-Neptunian
dwarfs but the last, so they are drawn to sit beside Ceres and Eris: the teal
planet-card frame, a name plate, a small body on a starfield, and a strip of
five little cards along the bottom that spells out the hand.

What is true of each body is what is drawn: Quaoar's ring far outside where a
ring should survive, with Weywot; Haumea a fast-spinning ice egg with a dark
red spot, a ring and two moons; Sedna deep red and alone, the Sun only the
brightest star and its orbit a long thin arc; Makemake bright and tawny with
one dark moon; the Belt a river of rocks.

Every pixel here is set by this program.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

from pixel import Canvas, Palette, dilate, sheet

W, H = 71, 95

PAL = Palette(
    bg="#5b9baa", lt="#dff5fc", dk="#4f6367", pn="#84c5d2", wh="#ffffff",
    # suit dots on the little cards
    H="#f03464", D="#f06b3f", C="#235955", S="#3c4368", X="#9a5bd6",
    st1="#b8bcc0", st2="#8d9499", st3="#6b7378",
    # Quaoar
    q0="#6e3a34", q1="#96503f", q2="#bd6a4c", q3="#dc8b63", q4="#f2b088",
    # Haumea
    h0="#7f9db5", h1="#a9c4d6", h2="#d5e8f2", h3="#f4fbff", hs="#b5483c", hs2="#8a3430",
    # Sedna
    s0="#4d1a22", s1="#7a2426", s2="#a8342c", s3="#cf5238", s4="#ea7a50",
    # Makemake
    m0="#7d4c3c", m1="#a86a4b", m2="#cf9266", m3="#ecb886", m4="#fbd9ae",
    moon="#4a4f55", moon2="#6c737a",
    # rocks
    r0="#57504c", r1="#7b7269", r2="#a1978a", r3="#c7bdae", r4="#e4dccd",
)

# 5x6 plate lettering, mine: two-pixel stems.
FONT = {
    "A": [".###.", "##.##", "##.##", "#####", "##.##", "##.##"],
    "B": ["####.", "##.##", "####.", "##.##", "##.##", "####."],
    "D": ["####.", "##.##", "##.##", "##.##", "##.##", "####."],
    "E": ["#####", "##...", "####.", "##...", "##...", "#####"],
    "H": ["##.##", "##.##", "#####", "##.##", "##.##", "##.##"],
    "I": ["##", "##", "##", "##", "##", "##"],
    "K": ["##.##", "##.##", "####.", "####.", "##.##", "##.##"],
    "L": ["##..", "##..", "##..", "##..", "##..", "####"],
    "M": ["##.##", "#####", "#####", "##.##", "##.##", "##.##"],
    "N": ["##..#", "###.#", "#####", "##.##", "##..#", "##..#"],
    "O": [".###.", "##.##", "##.##", "##.##", "##.##", ".###."],
    "Q": [".###.", "##.##", "##.##", "##.##", "##.#.", ".##.#"],
    "R": ["####.", "##.##", "##.##", "####.", "##.##", "##.##"],
    "S": [".####", "##...", ".###.", "...##", "...##", "####."],
    "T": ["####", ".##.", ".##.", ".##.", ".##.", ".##."],
    "U": ["##.##", "##.##", "##.##", "##.##", "##.##", ".###."],
}


def text_width(s):
    return sum(len(FONT[ch][0]) + 1 for ch in s) - 1


def text(c, s, x, y, col):
    for ch in s:
        c.stamp(FONT[ch], x, y, {"#": col})
        x += len(FONT[ch][0]) + 1


def card_mask(c):
    m = c.blank()
    m[1:94, 4:67] = True
    for i, n in enumerate((3, 2, 1)):          # stepped corner
        for y in (1 + i, 93 - i):
            m[y, 4:4 + n] = False
            m[y, 67 - n:67] = False
    return m


def planet_card(index, lines, seed):
    """Frame, top strip (which of the five this is), name plate, stars."""
    c = Canvas(W, H, PAL)
    yy, xx = c.grid()
    m0 = card_mask(c)
    from pixel import erode
    m1 = erode(m0, diag=False)
    m2 = erode(m1)
    m3 = erode(erode(m2))
    c.fill(m0, "bg")
    c.fill(m1, "dk")
    c.fill(m2, "lt")
    c.fill(m3, "bg")
    # top and bottom panels
    for y0, y1 in ((4, 12), (78, 90)):
        pm = c.rrect_mask(9, y0, 61, y1, 1)
        c.fill(pm, "pn")
    # top strip: five bodies, this one lit; a little sun at the left
    c.stamp(["..#..", ".###.", "#####", ".###.", "..#.."], 12, 6, {"#": "lt"})
    c.hline(19, 22, 8, "dk")
    for i in range(5):
        x = 26 + i * 7
        c.rect(x, 7, x + 2, 9, "dk", fill=False)
        if i == index:
            c.rect(x - 1, 6, x + 3, 10, "dk", fill=False)
            c.rect(x, 7, x + 2, 9, "wh")
        if i < 4:
            c.px(x + 5, 8, "dk")
    # stars
    rng = np.random.default_rng(seed)
    field = c.blank()
    field[14:77, 9:62] = True
    for _ in range(46):
        x, y = int(rng.integers(9, 62)), int(rng.integers(14, 77))
        c.px(x, y, "lt")
    for _ in range(3):
        x, y = int(rng.integers(12, 59)), int(rng.integers(34, 74))
        c.vline(x, y - 2, y + 2, "lt")
        c.hline(x - 1, x + 1, y, "lt")
    # name plate
    wmax = max(text_width(s) for s in lines)
    half = min(26, max(23, (wmax + 1) // 2 + 3))
    y0, y1 = 16, 16 + 5 + 7 * len(lines)
    pm = c.rrect_mask(35 - half, y0, 35 + half, y1, 5)
    c.fill(pm, "lt")
    c.fill(pm & ~erode(pm), "dk")
    c.fill(dilate(pm) & ~pm, "bg")
    for j, s in enumerate(lines):
        text(c, s, 35 - text_width(s) // 2, y0 + 3 + 7 * j, "dk")
    return c


def hand_strip(c, dots, heights=None, groups=None, stone=False, big=False):
    """Five little cards along the bottom panel."""
    xs = [12, 22, 32, 42, 52] if groups is None else groups
    for i, x in enumerate(xs):
        dy = 0 if heights is None else heights[i]
        y = 80 + dy
        if stone:
            c.rect(x, y, x + 6, y + 8, "st1")
            c.pxs([(x + 1, y + 2), (x + 4, y + 1), (x + 2, y + 5), (x + 5, y + 6), (x + 3, y + 3)], "st2")
            c.pxs([(x + 5, y + 3), (x + 1, y + 7), (x + 3, y + 7)], "st3")
            c.pxs([(x, y), (x + 6, y), (x, y + 8), (x + 6, y + 8)], "pn")
            continue
        c.rect(x, y, x + 6, y + 8, "lt")
        c.pxs([(x, y), (x + 6, y), (x, y + 8), (x + 6, y + 8)], "pn")
        if big:
            c.rect(x + 2, y + 3, x + 4, y + 5, dots[i])
        else:
            c.rect(x + 2, y + 3, x + 4, y + 4, dots[i])
            c.rect(x + 3, y + 2, x + 3, y + 5, dots[i])


def noise(c, seed, scale=5.0):
    """Smooth deterministic mottling in -1..1 (a few summed sines)."""
    rng = np.random.default_rng(seed)
    yy, xx = c.grid()
    n = np.zeros((c.h, c.w))
    for _ in range(6):
        a = rng.uniform(0, 2 * np.pi)
        f = rng.uniform(0.6, 1.8) / scale
        ph = rng.uniform(0, 2 * np.pi)
        n += np.sin((xx * np.cos(a) + yy * np.sin(a)) * f * 2 * np.pi / 3 + ph)
    return n / 6 * 2


def body(c, cx, cy, rx, ry, tones, seed, angle=0.0, mott=0.10, dith=0.10):
    """A lit ellipsoid: light from the upper left, banded tones, dark rim,
    pale halo. Returns its mask."""
    yy, xx = c.grid()
    ca, sa = np.cos(angle), np.sin(angle)
    u = (xx - cx) * ca + (yy - cy) * sa
    v = -(xx - cx) * sa + (yy - cy) * ca
    r2 = (u / rx) ** 2 + (v / ry) ** 2
    m = r2 <= 1.0
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    nu, nv = u / rx, v / ry
    nx = nu * ca - nv * sa
    ny = nu * sa + nv * ca
    lam = -0.52 * nx - 0.60 * ny + 0.60 * nz
    t = np.clip(lam * 0.62 + 0.42 + mott * noise(c, seed), 0, 0.999)
    c.fill(dilate(dilate(m)) & ~m, "lt")
    c.fill(dilate(m) & ~m, "dk")
    c.bands(m, t, tones, dither=dith)
    return m


def ring(c, cx, cy, a, b, angle, col, front, gap_mask=None):
    """Half of a thin tilted ring: the far half (front=False) is drawn before
    the body, the near half after."""
    ca, sa = np.cos(angle), np.sin(angle)
    for th in np.linspace(0, 2 * np.pi, 720, endpoint=False):
        near = np.sin(th) > 0
        if near != front:
            continue
        x = cx + a * np.cos(th) * ca - b * np.sin(th) * sa
        y = cy + a * np.cos(th) * sa + b * np.sin(th) * ca
        xi, yi = int(round(x)), int(round(y))
        if gap_mask is not None and gap_mask[yi, xi]:
            continue
        c.px(xi, yi, col)


def moon(c, x, y, r, col, col2=None):
    m = c.ellipse_mask(x, y, r, r)
    c.fill(dilate(m) & ~m, "dk")
    c.fill(m, col)
    if col2:
        yy, xx = c.grid()
        c.fill(m & ((xx - x) + (yy - y) > 0.5), col2)


def quaoar():
    c = planet_card(0, ["QUAOAR"], 11)
    cx, cy = 35, 53
    ring(c, cx, cy, 24, 7, -0.30, "lt", front=False)
    m = body(c, cx, cy, 10.5, 10.5, ["q0", "q1", "q2", "q3", "q4"], 3)
    ring(c, cx, cy, 24, 7, -0.30, "lt", front=True)
    ring(c, cx, cy, 24, 7, -0.30, "dk", front=True, gap_mask=~m)
    moon(c, 54, 37, 1.6, "st1", "st2")
    hand_strip(c, ["H", "S", "X", "D", "C"], heights=[0, 1, 0, 1, 0])
    return c


def haumea():
    c = planet_card(1, ["HAUMEA"], 23)
    yy, xx = c.grid()
    cx, cy, ang = 35, 53, -0.38
    ring(c, cx, cy, 25, 5, ang + 0.05, "lt", front=False)
    m = body(c, cx, cy, 17.5, 9.2, ["h0", "h1", "h2", "h3"], 5, angle=ang, mott=0.06)
    spot = c.ellipse_mask(41, 49, 3.6, 2.4) & m
    c.fill(spot, "hs")
    c.fill(spot & ((xx + yy) % 2 == 0) & (yy >= 50), "hs2")
    ring(c, cx, cy, 25, 5, ang + 0.05, "lt", front=True)
    ring(c, cx, cy, 25, 5, ang + 0.05, "dk", front=True, gap_mask=~m)
    moon(c, 15, 39, 1.6, "h2", "h1")
    moon(c, 52, 68, 1.0, "h2")
    # spin ticks
    c.pxs([(18, 66), (19, 67), (21, 68)], "lt")
    c.pxs([(50, 38), (52, 39), (53, 40)], "lt")
    hand_strip(c, ["H", "D", "X", "C", "S"], heights=[2, 1, 0, -1, -2])
    return c


def sedna():
    c = planet_card(2, ["SEDNA"], 37)
    # the long orbit, and the Sun as only the brightest star
    for th in np.linspace(0.05, 1.5, 260):
        x = 14 + 62 * np.cos(th) - 14
        y = 77 - 44 * np.sin(th) ** 1.6
        xi, yi = int(round(x)), int(round(y))
        if 9 <= xi <= 61 and 31 <= yi <= 76 and (xi + yi) % 3:
            c.px(xi, yi, "pn")
    c.vline(15, 67, 73, "wh")
    c.hline(12, 18, 70, "wh")
    c.pxs([(14, 69), (16, 69), (14, 71), (16, 71)], "lt")
    body(c, 39, 52, 8.6, 8.6, ["s0", "s1", "s2", "s3", "s4"], 9, mott=0.08)
    hand_strip(c, ["H", "X", "S", "D", "C"], heights=[0, 0, 0, 1, 1],
               groups=[11, 20, 29, 44, 53])
    return c


def makemake():
    c = planet_card(3, ["MAKEMAKE"], 51)
    body(c, 34, 54, 12.5, 12.5, ["m0", "m1", "m2", "m3", "m4"], 14, mott=0.14)
    moon(c, 53, 42, 1.6, "moon2", "moon")
    hand_strip(c, ["H", "D", "X", "C", "S"], big=True)
    return c


def rock(c, cx, cy, r, seed, tones=("r0", "r1", "r2", "r3", "r4")):
    """An irregular lit boulder."""
    rng = np.random.default_rng(seed)
    n = 9
    rad = r * rng.uniform(0.68, 1.12, n)
    ph = rng.uniform(0, 2 * np.pi)
    pts = [(cx + rad[i] * np.cos(ph + i * 2 * np.pi / n),
            cy + rad[i] * np.sin(ph + i * 2 * np.pi / n) * 0.85) for i in range(n)]
    m = c.poly_mask([(int(round(x)), int(round(y))) for x, y in pts])
    yy, xx = c.grid()
    lam = (-(xx - cx) * 0.55 - (yy - cy) * 0.65) / max(r, 1) * 0.55 + 0.5
    t = np.clip(lam + 0.16 * noise(c, seed + 100, 3.0), 0, 0.999)
    c.fill(dilate(m) & ~m, "dk")
    c.bands(m, t, list(tones), dither=0.08)
    return m


def belt():
    c = planet_card(4, ["ASTEROID", "BELT"], 67)
    rng = np.random.default_rng(8)
    # dust along the band, then rocks back to front
    for _ in range(40):
        t = rng.uniform(0, 1)
        x = 9 + t * 52
        y = 71 - 26 * t + 6 * np.sin(t * 3.0) + rng.normal(0, 4.5)
        if 38 <= y <= 76:
            c.px(int(x), int(y), "r3" if rng.random() < 0.5 else "r2")
    spec = [(14, 68, 3.2), (24, 60, 2.2), (20, 72, 1.6), (33, 63, 5.6), (30, 50, 1.8),
            (45, 55, 3.6), (41, 68, 2.0), (54, 47, 4.4), (51, 62, 1.5), (58, 57, 2.0),
            (25, 44, 1.3), (47, 42, 1.4), (38, 73, 1.3), (57, 70, 1.2)]
    for i, (x, y, r) in enumerate(spec):
        rock(c, x, y, r, 40 + i)
    hand_strip(c, None, stone=True)
    return c


def cells():
    return [quaoar(), haumea(), sedna(), makemake(), belt()]


def sheet_canvas():
    return sheet(cells())


def outputs():
    return {"planets.png": (sheet_canvas(), PAL)}
