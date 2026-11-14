"""icons.py — the mod icon.

Quintessence: the fifth element, the fifth suit. Four small lozenges in the
four old suit colours sit at the compass points, and the Wild star stands in
the middle of them, on a dark rounded tile.

Every pixel here is set by this program.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

from pixel import Canvas, Palette, dilate

PAL = Palette(
    bg="#374649", bg2="#4f6367", edge="#2a3538",
    X="#9a5bd6", X2="#c9a2f2", wh="#ffffff",
    H="#f03464", D="#f06b3f", C="#2f8f83", S="#6a74b8", g="#ffa300",
)

STAR = """
.......##.......
.......##.......
......####......
......####......
.....######.....
....########....
..############..
################
################
..############..
....########....
.....######.....
......####......
......####......
.......##.......
.......##.......
"""


def icon():
    c = Canvas(34, 34, PAL)
    yy, xx = c.grid()
    tile = c.rrect_mask(1, 1, 32, 32, 5)
    c.fill(tile, "bg")
    c.fill(tile & ~np.roll(tile, 1, axis=0), "bg2")           # top bevel
    c.fill(dilate(tile) & ~tile, "edge")
    # the four suits, as lozenges at the corners
    for (x, y), col in (((8, 8), "H"), ((25, 8), "D"), ((8, 25), "C"), ((25, 25), "S")):
        d = np.abs(xx - x - 0.0) + np.abs(yy - y - 0.0)
        c.fill(d <= 3, col)
    # the fifth
    t = Canvas(34, 34, PAL)
    t.stamp(STAR, 9, 9, {"#": "X"})
    c.fill(dilate(t.mask(), diag=True) & tile, "bg")
    c.blit(t)
    c.fill(t.mask() & (np.abs(xx - 16.5) + np.abs(yy - 16.5) <= 2.5), "wh")
    c.fill(t.mask() & (np.abs(xx - 16.5) + np.abs(yy - 16.5) <= 1), "g")
    return c


def outputs():
    return {"icon.png": (icon(), PAL)}
