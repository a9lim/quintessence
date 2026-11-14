# Quintessence art notes

Pixel art as code. Engine: `art/pixel.py`. One program per sheet;
`python3 art/build.py` regenerates everything into `assets/1x` and
`assets/2x` (2x = exact nearest-neighbour x2 of the 1x; build.py checks it).
`art/look.py` renders previews into `art/preview/` (gitignored).

**Round 2 (2026-11-14): the art now derives from Balatro's own textures.**
`art/vanilla.py` reads them at build time from the installed game archive
(`Balatro.love`, a zip; override the path with `BALATRO_LOVE`). Nothing from
the archive is stored in the repo as source, but the built PNGs in `assets/`
contain LocalThunk's pixels. build.py exits with a clear message if the
archive is missing.

## Wild suit colours (the suit's text colour)

- normal: **`#8b64b4`** (muted purple); shade `#684a8f`
- high contrast: **`#1fa84f`** (green); shade `#157a39`

The HC sheets are the same drawing with the palette swapped; the vanilla
suit colours used as accents swap to `#f83b2f #e39100 #009cfd #8a71e1`.

## Wild pip

An asterisk, six arms (`*`, Conway's star). Drawn here, not derived:
11x11 layout pips, 9x9 corner pips, 16x16 UI icon. On the Ace it is one
large asterisk whose upright is Wild purple and whose four slanted arms are
hearts, diamonds, clubs, spades colours. The mod icon is the same figure on
a dark tile.

## Provenance: what derives from which vanilla cell

Cells are (column, row), 0-based, 71x95, in `resources/textures/1x/`.

### `wild_deck.png`, `wild_deck_hc.png` -- derived from `8BitDeck.png`
- **Rank glyphs** (all 13 cells, both corners): the spades row's glyphs,
  cells (0..12, 3), re-inked.
- **Jack** (cell 9): head region from Jack of Hearts (9, 0); robes, frame
  and held things from Jack of Diamonds (9, 2).
- **Queen** (cell 10): head from Queen of Spades (10, 3); the rest from
  Queen of Hearts (10, 0).
- **King** (cell 11): head from King of Clubs (11, 1); the rest from King of
  Spades (11, 3).
- Collage rule: "head" = the two ends of the cell (|y-47| >= 23) within 17
  px of the centre column (12 for the Jack). Robes' suit colour (and the
  black suits' red) -> Wild purple; black suits' dark ink -> the common
  outline `#374649`; heads keep their suit's colours.
- **Not derived:** the asterisk pips, pip layouts (standard poker layouts),
  the Ace's asterisk. `8BitDeck_opt2.png` is not used.

### `wild_ui.png`, `wild_ui_hc.png` -- original (asterisk, no vanilla pixels)

### `jokers.png` -- derived from `Jokers.png`, whole cells re-inked
- **Wacky Joker** <- Droll Joker (6, 0): cap cone/horns/bells and the fan's
  pips re-inked in the five suit colours.
- **Shrewd Joker** <- Crafty Joker (4, 14): cap and ruff re-inked purple /
  teal; fan pips in the five suit colours.
- **The Coalition** <- The Tribe (9, 4): ground re-inked plum, cracks
  re-inked by direction in five suit colours, fan pips in five suit colours.

### `planets.png` -- derived from `Tarots.png`
- **Frame + top strip:** Planet X (9, 2) for Quaoar, Haumea, Sedna,
  Makemake; Ceres (8, 2) for Asteroid Belt.
- **Name plate shape:** Pluto (8, 3), widened/deepened by repeating its
  middle column/row.
- **Plate lettering:** traced from the plates of Pluto (8, 3), Mercury
  (0, 3), Saturn (5, 3), Earth (2, 3), Jupiter (4, 3). D, Q, K, B do not
  occur on vanilla plates and are drawn here to match.
- **Bottom hand strip** (each card's marks re-inked in a different suit
  colour): Quaoar <- Jupiter/Flush (4, 3); Haumea <- Neptune/Straight Flush
  (7, 3); Sedna <- Ceres/Flush House (8, 2); Makemake <- Eris/Flush Five (3, 2)
  (confirmed against the game's planet table); Asteroid Belt <-
  Planet X/Five of a Kind (9, 2), cards re-inked as stone.
- **Not derived:** the bodies (Quaoar + ring + Weywot, Haumea, Sedna + Sun +
  orbit arc, Makemake + moon, the rocks) and the starfields.

### `icon.png` -- original (no vanilla pixels)

## Things to look at again

- Settled with a9 (2026-11-14): the two-line "ASTEROID BELT" plate and the
  recoloured vanilla diamonds in the joker fans both stay. Envious Joker was
  removed from the mod (too strong for vanilla-plus), and its art with it.
