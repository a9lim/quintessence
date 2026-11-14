# Quintessence art notes

Painting-as-code, pixel edition. Engine: `art/pixel.py`. One program per
sheet; `python3 art/build.py` regenerates everything into `assets/1x` and
`assets/2x` (2x = exact nearest-neighbour x2). `art/look.py` renders previews
into `art/preview/` (gitignored); it is the only thing that may be pointed at
reference textures, and nothing it makes ships.

## Wild suit

- **Pip:** a solid four-pointed star (compass star / sparkle). 11x11 for the
  layout pips, 9x9 in the corners, 16x16 for the UI icon. Chosen because it is
  the one simple silhouette that none of heart/diamond/club/spade resembles
  (concave between the points where a diamond is straight), it is its own
  180-degree rotation, and four points = the four suits it stands in for.
- **Ace:** one big star (two crossed lozenges) with an open eye, and in the
  eye a lozenge quartered in the four vanilla suit colours.
- **Colours (suit text colour):**
  - normal: **`#9a5bd6`** (violet); shade `#7443b0`
  - high contrast: **`#1fa84f`** (green); shade `#157a39`
  - violet/green are the hues the other four suits leave free in each palette
    (HC spades is already purple `#8a71e1`).
- Shared with vanilla's look: outline `#374649`, gold `#ffa300`, blue
  `#29adff`, whites `#ffffff/#e6e6e6/#acacac`; the four suit colours
  `#f03464 #f06b3f #235955 #3c4368` (HC: `#f83b2f #e39100 #009cfd #8a71e1`)
  appear as accents on the courts.
- **Glyphs:** own 7x8 bold grotesque (2-px strokes), at vanilla's position
  (x 6..12, y 7..14); corner pip x 5..13, y 16..24. Pip grid follows the
  standard poker layouts; the whole cell is exactly 180-degree symmetric.
- **Courts:** drawn as one upright figure, cut through the centre, completed
  by 180-degree rotation (`Canvas.double_head`). Jack: slouched cap + feather,
  star wand, sash striped in the four suits (diagonal cut). Queen: crown, long
  hair, ermine collar, raised hand mirror, gold girdle with four stones
  (opposite diagonal). King: beard, ermine mantle, orb staff, four stones in
  crown and belt (horizontal cut). Held items are always top-right /
  bottom-left so they clear the corner glyphs.

## Planets (`planets.py`, 5 cells: Quaoar, Haumea, Sedna, Makemake, Asteroid Belt)

Vanilla planet-card conventions: teal frame (`#5b9baa` ground, `#dff5fc`
light, `#4f6367` dark, `#84c5d2` panels), name plate, body on a starfield,
bottom strip of five little cards that spells the hand. Own 5x6 plate font.
Top strip is ours: a sun and five boxes, the lit box = which of the five.
Bottom strips: Spectrum = five suit-coloured pips at uneven heights;
Straight Spectrum = a staircase; Spectrum House = grouped 3 | 2;
Spectrum Five = five identical big pips; Bulwark = five stone cards.
Quaoar: far ring + Weywot. Haumea: tilted ice ellipsoid, dark red spot,
ring, two moons. Sedna: small deep-red disc, the Sun as a bright star, a
long dashed orbit arc. Makemake: tawny disc, one dark moon. Belt: rocks.

## Jokers (`jokers.py`, 4 cells: Wacky, Shrewd, The Coalition, Envious)

White joker card (`#bfc7d5` border), own JOKER lettering down the left and
turned up the right. Wacky: a five-tailed cap, one tail per suit colour,
five-suit fan beneath. Shrewd: two-tone cap (muted violet / teal), narrow
eyes, lopsided blue smile, five counted cards with five coloured dots.
Coalition: dark slate card, five banners (five suit colours) swept into a
gold knot, five-suit fan. Envious: green jester glaring at a plain card ->
star card. Mini cards are sheared in whole-pixel steps, not rotated.

## Icon (`icons.py`)

34x34 dark tile, four suit-coloured lozenges at the corners, the Wild star
in the middle.

## Status

All seven outputs build and pass the size / exact-2x check in `build.py`.

Things I would look at again with more time:
- The courts are cleaner and plainer than vanilla's (less robe ornament);
  the Queen's raised hand floats a little.
- Wacky's face is busy at 1x; Envious reads "grumpy green jester" more
  than specifically "envy".
- HC: the orange stone on the Queen's gold girdle is low-contrast.
