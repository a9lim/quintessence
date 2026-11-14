"""build.py — regenerate every texture.

    python3 art/build.py

Runs each sheet program and writes assets/1x/<name> and assets/2x/<name>,
the 2x being the 1x upscaled by exact nearest-neighbour x2. Then checks the
sizes the Lua side depends on.

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import icons      # noqa: E402
import jokers     # noqa: E402
import planets    # noqa: E402
import wild_deck  # noqa: E402
from pixel import export  # noqa: E402

ASSETS = HERE.parent / "assets"

EXPECT = {
    "wild_deck.png": (923, 95), "wild_deck_hc.png": (923, 95),
    "wild_ui.png": (18, 18), "wild_ui_hc.png": (18, 18),
    "planets.png": (355, 95), "jokers.png": (284, 95), "icon.png": (34, 34),
}


def main():
    made = {}
    for mod in (wild_deck, planets, jokers, icons):
        for name, (canvas, pal) in mod.outputs().items():
            export(canvas, name, ASSETS, pal)
            made[name] = canvas
    ok = True
    for name, size in EXPECT.items():
        one = Image.open(ASSETS / "1x" / name)
        two = Image.open(ASSETS / "2x" / name)
        a, b = np.asarray(one.convert("RGBA")), np.asarray(two.convert("RGBA"))
        good = (one.size == size and two.size == (size[0] * 2, size[1] * 2)
                and np.array_equal(np.repeat(np.repeat(a, 2, 0), 2, 1), b))
        ok &= good
        print(f"{'ok ' if good else 'BAD'} {name:18s} {one.size} -> {two.size}")
    missing = set(EXPECT) ^ set(made)
    if missing:
        ok = False
        print("unexpected/missing:", missing)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
