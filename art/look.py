"""look.py — preview tool. Not part of the build; nothing it makes ships.

Renders big nearest-neighbour blow-ups into art/preview/ (gitignored). Deck
fronts are shown on a mock white card body. If a directory of reference
textures is given as the second argument, a few reference cells are placed
beside ours for side-by-side judging; they are only ever looked at.

    python3 art/look.py deck|deck_hc|planets|jokers|icons [REF_DIR] [k]

fable, 2026-11-14 (claude-fable-5-2)
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

from pixel import Canvas, Palette, hex_rgba, hstack, upscale, vstack

HERE = Path(__file__).parent
OUT = HERE / "preview"


def card_body(n=1):
    p = Palette(w="#ffffff", e="#c8d0d0")
    c = Canvas(71, 95, p)
    c.rrect(1, 1, 69, 93, 4, "w")
    c.rrect(1, 1, 69, 93, 4, "e", fill=False)
    im = c.image()
    out = Image.new("RGBA", (71 * n, 95), (0, 0, 0, 0))
    for i in range(n):
        out.alpha_composite(im, (71 * i, 0))
    return out


def on_cards(im):
    b = card_body(im.width // 71)
    b.alpha_composite(im)
    return b


def ref(ref_dir, name, boxes):
    im = Image.open(Path(ref_dir) / name).convert("RGBA")
    return hstack([im.crop(b) for b in boxes], gap=0)


def cell(col, row, w=71, h=95, n=1):
    return (col * w, row * h, (col + n) * w, (row + 1) * h)


def save(im, name, k, bg="#5b7a68"):
    b = Image.new("RGBA", im.size, hex_rgba(bg))
    b.alpha_composite(im)
    OUT.mkdir(exist_ok=True)
    upscale(b, k).save(OUT / name)
    print(OUT / name, b.size, "x", k)


def main():
    what = sys.argv[1]
    refd = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    if what in ("deck", "deck_hc"):
        import wild_deck as wd
        pal = wd.PAL_HC if what == "deck_hc" else wd.PAL
        cs = wd.cells()
        rname = "8BitDeck_opt2.png" if what == "deck_hc" else "8BitDeck.png"

        def strip(lo, hi, refs):
            from pixel import sheet
            im = on_cards(sheet(cs[lo:hi]).image(pal))
            if refd and refs:
                im = hstack([im, on_cards(ref(refd, rname, refs))], gap=3)
            return im
        save(strip(0, 5, [cell(3, 3), cell(4, 0)]), f"{what}_a.png", k)
        save(strip(5, 9, [cell(8, 1), cell(7, 2)]), f"{what}_b.png", k)
        save(strip(9, 13, [cell(9, 0), cell(11, 3)]), f"{what}_c.png", k)
        save(strip(9, 12, []), f"{what}_courts.png", 8)
    elif what == "planets":
        import planets
        im = planets.sheet_canvas().image()
        if refd:
            im = hstack([im, ref(refd, "Tarots.png", [cell(8, 3, n=2), cell(1, 5)])], gap=3)
        save(im, "planets.png", k)
    elif what == "jokers":
        import jokers
        im = jokers.sheet_canvas().image()
        if refd:
            im = vstack([im, ref(refd, "Jokers.png", [cell(*p) for p in sys_ref_jokers()])], gap=3)
        save(im, "jokers.png", k)
    elif what == "icons":
        import icons
        import wild_deck as wd
        ims = [icons.icon().image(), wd.ui_icon().image(wd.PAL), wd.ui_icon().image(wd.PAL_HC)]
        if refd:
            ims.append(Image.open(Path(refd) / "ui_assets.png").convert("RGBA").crop((0, 18, 72, 36)))
        save(hstack(ims, gap=3), "icons.png", 10)


def sys_ref_jokers():
    return [(6, 0), (2, 0), (0, 14), (5, 4)]


if __name__ == "__main__":
    main()
