"""planets.py — five planet cards for the new poker hands.

Quaoar (Spectrum), Haumea (Straight Spectrum), Sedna (Spectrum House),
Makemake (Spectrum Five) and the Asteroid Belt (Bulwark).

Round 2: the card itself is Balatro's. The frame and the solar-system strip
across the top are taken from Planet X (from Ceres for the Belt, which is
where Ceres lives); the name plate is Pluto's, stretched to fit; the plate
lettering is traced from vanilla plates (four letters vanilla never uses are
drawn to match); and the five little cards along the bottom are the strips
of the vanilla hand each new hand is the Spectrum cousin of (Flush, Straight
Flush, Flush House, Flush Five, Five of a Kind) with each card's marks
re-inked in a different suit colour. The bodies and the starfields are drawn
here: Quaoar's ring far outside where a ring should survive, with Weywot;
Haumea a fast-spinning ice egg with a dark red spot, a ring and two moons;
Sedna deep red and alone, the Sun only the brightest star and its orbit a
long thin arc; Makemake bright and tawny with one dark moon; the Belt a
river of rocks.

See NOTES.md for exactly which vanilla cells are used.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

import vanilla as V
from pixel import Canvas, Palette, components, dilate, erode, sheet

W, H = 71, 95

PAL = Palette(
    bg="#5b9baa", lt="#dff5fc", dk="#4f6367", pn="#84c5d2", wh="#ffffff",
    # suit dots on the little cards
    H="#f03464", D="#f06b3f", C="#235955", S="#3c4368", X="#8b64b4",
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

FRAME = {"5b9baa": "bg", "dff5fc": "lt", "4f6367": "dk", "84c5d2": "pn", "ffffff": "wh"}
SUITS = ["H", "D", "X", "C", "S"]

# Plate letters vanilla never uses, drawn to match its 4x6 face.
EXTRA = {
    "D": ["###.", "##.#", "##.#", "##.#", "##.#", "###."],
    "Q": [".##.", "##.#", "##.#", "##.#", "###.", ".#.#"],
    "K": ["##.#", "##.#", "###.", "###.", "##.#", "##.#"],
    "B": ["###.", "##.#", "###.", "##.#", "##.#", "###."],
}
# word on a vanilla plate -> (Tarots cell, the letters to take from it)
TRACE = [((8, 3), "PLUTO"), ((0, 3), "MERCURY"), ((5, 3), "SATURN"),
         ((2, 3), "EARTH"), ((4, 3), "JUPITER")]


def vcell(col, row):
    """A vanilla planet cell in this sheet's palette."""
    a = V.cell("Tarots", col, row)
    hx = V.hexes(a)
    c = Canvas(W, H, PAL)
    rgbs = {h: np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)]) for h in FRAME}
    for h in np.unique(hx):
        if not h:
            continue
        if h in FRAME:
            name = FRAME[h]
        else:
            rgb = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)])
            name = FRAME[min(rgbs, key=lambda k: ((rgbs[k] - rgb) ** 2).sum())]
        c.fill(hx == h, name)
    return c


def trace_font():
    font = dict(EXTRA)
    for (col, row), word in TRACE:
        d = vcell(col, row).mask("dk")[20:26, 10:61]
        runs, cur = [], []
        for i, v in enumerate(d.any(0)):
            if v:
                cur.append(i)
            elif cur:
                runs.append(d[:, cur[0]:cur[-1] + 1])
                cur = []
        runs = runs[1:-1]                        # the plate's own two ends
        assert len(runs) == len(word), (word, len(runs))
        for ch, g in zip(word, runs):
            font.setdefault(ch, ["".join("#" if v else "." for v in r) for r in g])
    return font


FONT = None


def text_width(s):
    return sum(len(FONT[ch][0]) + 1 for ch in s) - 1


def text(c, s, x, y, col):
    for ch in s:
        c.stamp(FONT[ch], x, y, {"#": col})
        x += len(FONT[ch][0]) + 1


def plate(c, lines):
    """Pluto's name plate, widened (and for two lines, deepened) by
    repeating its middle column / row."""
    src = vcell(8, 3)
    sil = src.mask("dk", "lt")
    yy, xx = c.grid()
    sil &= (yy >= 15) & (yy <= 30) & (xx >= 9) & (xx <= 61)
    sil = next(p for p in components(sil) if p[17, 35])
    ys, xs = np.nonzero(sil)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    wmax = max(text_width(s) for s in lines)
    ex = max(0, (wmax + 4 - (x1 - x0 - 3) + 1) // 2)
    ey = 7 * (len(lines) - 1)
    out = c.blank()
    for y in range(y0, y1 + 1 + ey):
        sy = y if y <= 22 else max(22, y - ey)
        for x in range(x0 - ex, x1 + 1 + ex):
            sx = x + ex if x < 35 - ex else (x - ex if x > 35 + ex else 35)
            out[y, x] = sil[sy, sx]
    c.fill(dilate(out), "bg")
    c.fill(out, "lt")
    c.fill(out & ~erode(out), "dk")
    for j, s in enumerate(lines):
        text(c, s, 35 - (text_width(s) - 1) // 2, 20 + 7 * j, "dk")


def planet_card(lines, seed, top=(9, 2), strip=(9, 2), inks=SUITS, stone=False):
    """Vanilla frame and top strip, a fresh starfield, the plate, and the
    hand strip of a vanilla cousin with each card re-inked."""
    global FONT
    if FONT is None:
        FONT = trace_font()
    c = vcell(*top)
    yy, xx = c.grid()
    c.fill((yy >= 13) & (yy <= 77) & (xx >= 8) & (xx <= 62), "bg")
    low = (yy >= 78) & (yy <= 90) & (xx >= 8) & (xx <= 62)
    c.a[low] = vcell(*strip).a[low]
    for i, x in enumerate((12, 22, 32, 42, 52)):
        card = low & (xx >= x) & (xx <= x + 6) & (yy >= 80) & (yy <= 88)
        if stone:
            c.fill(card & c.mask("lt", "dk"), "st1")
            c.pxs([(x + 1, 82), (x + 4, 81), (x + 2, 85), (x + 5, 86), (x + 3, 83)], "st2")
            c.pxs([(x + 5, 83), (x + 1, 87), (x + 3, 87)], "st3")
        else:
            c.fill(card & c.mask("dk"), inks[i])
    rng = np.random.default_rng(seed)
    for _ in range(46):
        c.px(int(rng.integers(9, 62)), int(rng.integers(14, 77)), "lt")
    for _ in range(3):
        x, y = int(rng.integers(12, 59)), int(rng.integers(36, 74))
        c.vline(x, y - 2, y + 2, "lt")
        c.hline(x - 1, x + 1, y, "lt")
    plate(c, lines)
    return c


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
    c = planet_card(["QUAOAR"], 11, strip=(4, 3))
    cx, cy = 35, 53
    ring(c, cx, cy, 24, 7, -0.30, "lt", front=False)
    m = body(c, cx, cy, 10.5, 10.5, ["q0", "q1", "q2", "q3", "q4"], 3)
    ring(c, cx, cy, 24, 7, -0.30, "lt", front=True)
    ring(c, cx, cy, 24, 7, -0.30, "dk", front=True, gap_mask=~m)
    moon(c, 54, 37, 1.6, "st1", "st2")
    return c


def haumea():
    c = planet_card(["HAUMEA"], 23, strip=(7, 3))
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
    return c


def sedna():
    c = planet_card(["SEDNA"], 37, strip=(8, 2))
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
    return c


def makemake():
    c = planet_card(["MAKEMAKE"], 51, strip=(3, 2))
    body(c, 34, 54, 12.5, 12.5, ["m0", "m1", "m2", "m3", "m4"], 14, mott=0.14)
    moon(c, 53, 42, 1.6, "moon2", "moon")
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
    c = planet_card(["ASTEROID", "BELT"], 67, top=(8, 2), stone=True)
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
    return c


def cells():
    return [quaoar(), haumea(), sedna(), makemake(), belt()]


def sheet_canvas():
    return sheet(cells())


def outputs():
    return {"planets.png": (sheet_canvas(), PAL)}
