"""wild_deck.py — the Wild suit: thirteen card fronts, the suit icon.

The fifth suit of Quintessence, and it is made out of the other four.

The pip is an asterisk: six arms, `*`. (In Conway's game theory `*`, "star",
is the value confused with zero: the wildest number there is.) Muted purple
in the normal deck, green in the high-contrast deck.

Round 2: the fronts are now derived from Balatro's own deck so they read as
the same hand. Rank glyphs are vanilla's, re-inked. The three courts are
collages of vanilla courts: each takes its head from one suit, its robes
from a second and what it holds from a third, so all four old suits turn up
across J, Q, K. The robes are re-inked Wild purple; heads and held things
keep the colours of the suit they came from. On the Ace the asterisk's arms
are inked in the four suit colours, with Wild's own purple up the middle.

The pips, the layouts and the collage rules are this program's; the court
and glyph pixels are LocalThunk's (see NOTES.md for the exact list).

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

import vanilla as V
from pixel import Canvas, Palette, sheet

W, H = 71, 95
CX, CY = 35, 47

# ---------------------------------------------------------------- palette ----
NORMAL = dict(
    k="#374649",   # vanilla outline
    m="#8b64b4",   # Wild purple: pips, glyphs, robes
    d="#684a8f",   # purple, shade
    g="#ffa300", b="#29adff", w="#ffffff", s="#e6e6e6", a="#acacac",
    r="#fe5f55",   # the red the black suits use as a second colour
    H="#f03464", D="#f06b3f", C="#235955", S="#3c4368",   # the four suits
)
HIGH_CONTRAST = dict(
    m="#1fa84f", d="#157a39",
    H="#f83b2f", D="#e39100", C="#009cfd", S="#8a71e1",
)
PAL = Palette(**NORMAL)
PAL_HC = PAL.swapped(**HIGH_CONTRAST)
HEX2NAME = {v.lstrip("#"): k for k, v in NORMAL.items() if k not in "md"}
SUIT_ROW = dict(H=0, C=1, D=2, S=3)
RANK_COL = {str(n): n - 2 for n in range(2, 11)} | dict(J=9, Q=10, K=11, A=12)

# ------------------------------------------------------------------ pips ----
PIP = """
....###....
....###....
##..###..##
###.###.###
.#########.
...#####...
.#########.
###.###.###
##..###..##
....###....
....###....
"""
PIP_SMALL = """
...###...
...###...
##.###.##
.#######.
..#####..
.#######.
##.###.##
...###...
...###...
"""

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


def from_vanilla(a, remap=None):
    """A vanilla RGBA cell as a canvas in our palette. `remap` re-inks
    palette names, e.g. {"H": "m"}; colours we have no name for go to the
    nearest one we do."""
    c = Canvas(a.shape[1], a.shape[0], PAL)
    hx = V.hexes(a)
    table = PAL.table().astype(int)
    for h in np.unique(hx):
        if not h:
            continue
        name = HEX2NAME.get(h)
        if name is None:
            rgb = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)])
            name = PAL.names[1 + int(np.argmin(((table[1:, :3] - rgb) ** 2).sum(1)))]
        c.fill(hx == h, (remap or {}).get(name, name))
    return c


def corners(c, rank):
    """Vanilla's rank glyph re-inked, and the small asterisk under it; the
    same again, turned, bottom right."""
    t = Canvas(W, H, c.pal)
    src = from_vanilla(V.cell("8BitDeck", RANK_COL[rank], SUIT_ROW["S"]))
    glyph = src.mask() & (t.grid()[0] < 16) & (t.grid()[1] < 16)
    t.fill(glyph, "m")
    t.stamp(PIP_SMALL, 5, 16, {"#": "m"})
    c.blit(t)
    c.blit(t.rot180())


def number_card(n):
    c = Canvas(W, H, PAL)
    corners(c, str(n))
    for x, y in LAYOUT[n]:
        c.stamp(PIP, x, y, {"#": "m"})
    return c


def big_star(c, cx, cy, r=18.0, hw=3.3):
    """The Ace: one large asterisk. The upright is Wild purple; the four
    slanted arms are the four old suits."""
    yy, xx = c.grid()
    dx, dy = xx - cx, yy - cy

    def arm(ang):
        ux, uy = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        along = dx * ux + dy * uy
        across = np.abs(-dx * uy + dy * ux)
        return (along >= 0) & (along <= r) & (across <= hw - 0.9 * (along > r - 1.5))

    for ang, col in ((-150, "H"), (-30, "D"), (150, "C"), (30, "S"), (-90, "m"), (90, "m")):
        c.fill(arm(ang), col)
    hub = np.abs(dx) + np.abs(dy) <= 5
    c.fill(hub, "m")


def ace():
    c = Canvas(W, H, PAL)
    corners(c, "A")
    big_star(c, CX, CY)
    return c


# ---------------------------------------------------------------- courts ----
# Each court is two vanilla courts of the same rank: the head (hat, crown,
# face: the two ends of the cell inside the frame) from one suit, set on the
# robes, frame and held things of another. Vanilla courts are their own
# 180-degree rotation and so is the head region, so the collage stays
# double-headed. The robes' suit colour is re-inked Wild purple; the head
# keeps its own suit's colours. The black suits' dark ink becomes the common
# outline so the join does not show.
def head_region(half=17):
    yy, xx = np.mgrid[0:H, 0:W]
    return (np.abs(xx - CX) <= half) & (np.abs(yy - CY) >= 23)


def court(rank, head, robes, half=17):
    col = RANK_COL[rank]
    hm = head_region(half)
    c = Canvas(W, H, PAL)
    for suit, m, remap in (
            (robes, ~hm, {"H": "m", "D": "m", "r": "m", "C": "k", "S": "k"}),
            (head, hm, {"C": "k", "S": "k"})):
        src = from_vanilla(V.cell("8BitDeck", col, SUIT_ROW[suit]), remap)
        src.a[:26, :15] = 0                      # drop the source's corner index
        src.a[-26:, -15:] = 0
        c.a[m] = src.a[m]
    corners(c, rank)
    return c


COURTS = {"J": ("H", "D", 12), "Q": ("S", "H"), "K": ("C", "S")}   # rank: (head, robes[, half-width])


def cells():
    return ([number_card(n) for n in range(2, 11)]
            + [court(r, *COURTS[r]) for r in "JQK"] + [ace()])


def deck():
    return sheet(cells())


UI_ICON = """
......####......
......####......
......####......
###...####...###
#####.####.#####
.##############.
...##########...
.....######.....
.....######.....
...##########...
.##############.
#####.####.#####
###...####...###
......####......
......####......
......####......
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
