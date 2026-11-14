"""jokers.py — three Jokers, each re-inked from the vanilla Joker it is kin to.

  Wacky Joker    +Mult for a Spectrum. From Droll Joker (the Jolly / Zany /
                 Mad / Crazy / Droll family): the cap re-inked so cone, horns
                 and bells take the five suit colours, and the fan under him
                 dealt one card of each suit.
  Shrewd Joker   +Chips for a Spectrum. From Crafty Joker (the Sly / Wily /
                 Clever / Devious / Crafty family): cap and ruff in Wild
                 purple and teal, the five cards one of each suit.
  The Coalition  xMult for a Spectrum. From The Tribe (Duo / Trio / Family /
                 Order / Tribe): a plum ground, the cracks inked by direction
                 in the five suit colours, a five-suit hand.

Round 2: the figures, lettering and frames are LocalThunk's pixels, read
from the game archive at build time; the re-inking, the suit assignment and
the five-suit fans are this program's. See NOTES.md for the exact cells.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import numpy as np

import vanilla as V
from pixel import components, erode, from_rgba, sheet

W, H = 71, 95
SUIT = dict(H="#f03464", D="#f06b3f", X="#8b64b4", C="#235955", S="#3c4368")
ORDER = "HDXCS"


def load(col, row):
    return from_rgba(V.cell("Jokers", col, row))


def deal(c, ink, pivot_y, colours, box=None, small=None):
    """Re-ink the fan's pips so the five cards are five different suits.
    Pips are sorted into cards by their bearing from the fan's pivot."""
    yy, xx = c.grid()
    m = c.mask(ink)
    if box:
        x0, y0, x1, y1 = box
        m &= (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)
    for piece in components(m, diag=True):
        if small and piece.sum() > small:
            continue
        ys, xs = np.nonzero(piece)
        u = (xs.mean() - 35) / (pivot_y - ys.mean())
        k = int(np.searchsorted([-0.29, -0.09, 0.09, 0.27], u))
        c.fill(piece, colours[k])


def wacky():
    c = load(6, 0)
    yy, xx = c.grid()
    red, dark = "#fd5f55", "#4f6367"
    deal(c, red, 118, [SUIT[s] for s in ORDER], box=(12, 60, 58, 90))
    top = yy < 37
    pieces = components(c.mask(red) & top, diag=True)
    c.fill(pieces[0], SUIT["X"])                               # the cone
    for p in pieces[1:3]:                                      # the two bells
        c.fill(p, SUIT["C"] if np.nonzero(p)[1].mean() < 35 else SUIT["S"])
    horns = components(erode(c.mask(dark) & (yy < 50)), diag=True)[:2]
    for p in horns:                                            # the two horns
        c.fill(p, SUIT["H"] if np.nonzero(p)[1].mean() < 35 else SUIT["D"])
    return c


def shrewd():
    c = load(4, 14)
    deal(c, "#009cfd", 118, [SUIT[s] for s in ORDER], box=(12, 60, 58, 90))
    c.replace("#fd5f55", "#8b64b4")
    c.replace("#dd463c", "#684a8f")
    c.replace("#6a7c7f", "#4f9d95")
    return c


def coalition():
    c = load(9, 4)
    yy, xx = c.grid()
    red, dim, ground = "#fd5f55", "#b96762", "#5a757a"
    deal(c, red, 89, [SUIT[s] for s in ORDER], box=(17, 38, 56, 56), small=25)
    new_ground = "#5c5470"
    bright = ["#f03464", "#f06b3f", "#b08ae0", "#4fb3a6", "#7f8fd6"]
    th = (np.arctan2(yy - 47, xx - 35) + np.pi * 0.5) % (2 * np.pi)
    k = (th / (2 * np.pi) * 5).astype(int) % 5
    g = np.array([int(new_ground[i:i + 2], 16) for i in (1, 3, 5)])
    for i, col in enumerate(bright):
        rgb = np.array([int(col[j:j + 2], 16) for j in (1, 3, 5)])
        mix = "#%02x%02x%02x" % tuple(((rgb + g) // 2).astype(int))
        c.fill(c.mask(red) & (k == i), col)
        c.fill(c.mask(dim) & (k == i), mix)
    c.replace(ground, new_ground)
    return c


def cells():
    return [wacky(), shrewd(), coalition()]


def sheet_canvas():
    return sheet(cells())


def outputs():
    s = sheet_canvas()
    return {"jokers.png": (s, s.pal)}
