"""icons.py — the mod icon.

Quintessence: the fifth element, the fifth suit. The Wild asterisk on a dark
tile, inked the way the Ace is: the upright in Wild purple, the four slanted
arms in the four old suit colours (lightened where the dark tile would
swallow them).

Every pixel here is set by this program.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

from pixel import Canvas, Palette, dilate

PAL = Palette(
    bg="#374649", bg2="#4f6367", edge="#2a3538",
    X="#a27fd0", H="#f03464", D="#f06b3f", C="#3f9f92", S="#6a74b8",
)


def icon():
    c = Canvas(34, 34, PAL)
    yy, xx = c.grid()
    tile = c.rrect_mask(1, 1, 32, 32, 5)
    c.fill(tile, "bg")
    c.fill(tile & ~np.roll(tile, 1, axis=0), "bg2")           # top bevel
    c.fill(dilate(tile) & ~tile, "edge")
    dx, dy = xx - 16.5, yy - 16.5

    def arm(ang, r=12.5, hw=2.6):
        ux, uy = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        along = dx * ux + dy * uy
        across = np.abs(-dx * uy + dy * ux)
        return (along >= 0) & (along <= r) & (across <= hw - 0.9 * (along > r - 1.2))

    for ang, col in ((-150, "H"), (-30, "D"), (150, "C"), (30, "S"), (-90, "X"), (90, "X")):
        c.fill(arm(ang), col)
    c.fill(np.abs(dx) + np.abs(dy) <= 4, "X")
    return c


def outputs():
    return {"icon.png": (icon(), PAL)}
