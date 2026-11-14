# Quintessence

[![CI](https://github.com/a9lim/quintessence/actions/workflows/ci.yml/badge.svg)](https://github.com/a9lim/quintessence/actions/workflows/ci.yml)
[![License: GPL-3.0-or-later](https://img.shields.io/badge/license-GPL--3.0--or--later-blue.svg)](LICENSE)

A vanilla-plus mod for [Balatro](https://store.steampowered.com/app/2379780/Balatro/). Wild stops being an
enhancement and becomes the **fifth suit**, and five new poker hands use it: the four **Spectrums**
(the opposite of a Flush) and **Bulwark**. Each new hand gets its planet, and Spectrum gets its jokers.
Everything is priced to sit beside vanilla's cards.

## Install

With [balala](https://github.com/a9lim/balala):

```sh
balala install a9lim/quintessence lord-ruby/SpectrumAPI
```

Or by hand: install [Steamodded](https://github.com/Steamodded/smods) and
[SpectrumAPI](https://github.com/lord-ruby/SpectrumAPI), then put this repo in your `Mods` folder.

## The Wild suit

A Wild card is a card of the Wild suit, and it counts as every suit: for flushes, for suit jokers like
Greedy Joker or Bloodstone, for Flower Pot and Seeing Double, and for the suit Boss Blinds, just as in vanilla.

- **Same sources, same odds.** The Lovers, Standard packs, Familiar, Grim and Incantation all still hand out
  Wild cards as often as before; they now move the card to the Wild suit. No starting deck has Wild cards, and
  nothing rolls the Wild suit at random.
- **A free enhancement slot.** A Wild card keeps its enhancement, so a Glass Wild or a Lucky Wild is possible now.
- **Suits can change back.** The Star, The Moon, The Sun, The World and Sigil set a card's suit, so they can take
  a card out of the Wild suit.
- **Vanilla still counts it.** Smeared Joker still unlocks with three Wild cards in the deck, Driver's License
  still counts Wild cards as enhanced, and Castle and The Idol never name the Wild suit.

## The hands

A **Spectrum** is five cards of five different suits, one card per suit. With only four other suits, every
Spectrum includes a Wild card. A card can stand for any suit it counts as, but it fills only one: with Smeared
Joker, two Spades, two Hearts and a Wild make a Spectrum (Spade, Club, Heart, Diamond, Wild).

**Four Fingers** shortens a Spectrum to four cards, but never by dropping the Wild. Spade, Heart, Diamond and Wild
is a Spectrum; Spade, Heart, Club and Diamond is not. Otherwise Four Fingers alone would make Spectrums out of any
deck: in an untouched deck, two hands in three hold all four suits.

**Bulwark** is five cards with no rank and no suit: five Stone cards, which used to play as a High Card.

| Hand | Base | Per level | Planet | Ranks between |
| --- | --- | --- | --- | --- |
| Spectrum | 45 × 4 | +20 / +2 | Quaoar | Full House and Four of a Kind |
| Straight Spectrum | 80 × 7 | +35 / +3 | Haumea | Four of a Kind and Straight Flush |
| Spectrum House | 90 × 8 | +35 / +3 | Sedna | Four of a Kind and Straight Flush |
| Spectrum Five | 130 × 13 | +40 / +3 | Makemake | Five of a Kind and Flush House |
| Bulwark | 25 × 5 | +10 / +2 | Asteroid Belt | Straight and Flush |

Like Five of a Kind and the Flush hands built on it, all five stay hidden until you play one, and their planets
only appear after that.

The values come from how often each hand turns up. Chance that an 8-card hand holds it, with *k* Wild cards in a
52-card deck:

| Hand | k = 1 | k = 2 | k = 4 | Its Flush counterpart, k = 4 |
| --- | --- | --- | --- | --- |
| Spectrum | 8.9% | 17% | 32% | Flush: 19% |
| Straight Spectrum | 0.20% | 0.40% | 0.84% | Straight Flush: 0.20% |
| Spectrum House | 0.14% | 0.27% | 0.57% | Flush House: ~0 |

A Wild or two makes a Spectrum commoner than a Flush, and Spectrum House is about as rare as a Straight Flush, not
a Flush House (which needs duplicated cards). So the hands are priced lower than other mods price them. Bulwark is
light on chips because five Stones already bring 250.

## Jokers

| Joker | Rarity | Effect |
| --- | --- | --- |
| Wacky Joker | Common | +10 Mult if played hand contains a Spectrum |
| Shrewd Joker | Common | +80 Chips if played hand contains a Spectrum |
| The Coalition | Rare | ×3 Mult if played hand contains a Spectrum |
| Envious Joker | Common | Played cards that don't score become Wild |

The Spectrum jokers only show up once a Spectrum is within reach: when your deck holds a Wild card, or after you
play a Spectrum. Envious Joker shows up once your deck holds a Wild card.

## Other mods

The Spectrum hands live in [SpectrumAPI](https://github.com/lord-ruby/SpectrumAPI), which Cryptid, UNIK's mod and
others share, so a modpack never shows two copies of them. Quintessence sets their values and their rules, and
those apply to the other mods' Spectrums too. While [Cryptid](https://github.com/SpectralPack/Cryptid)'s Bulwark is
switched on, its Bulwark and Asteroid Belt are used instead of these.

A run started before you installed Quintessence keeps its Wild cards as enhancements until it ends. They still
count as every suit, but a new enhancement replaces them, as in vanilla.

## Credits

Made by a9lim and Claude, code and art.

The ideas come from other mods:

- **Wild as a suit**: [Manifold](https://github.com/ouiiskey/Manifold) by ouiiskey, which also has Envious Joker.
- **Spectrum hands**: [Six Suits](https://github.com/Aurelius7309/SixSuits) by Aurelius7309, carried on by
  [Bunco](https://github.com/jumbocarrot0/Bunco) and [UNIK's mod](https://github.com/70UNIK/UNIKs-mod), whose dwarf
  planets these follow. [SpectrumAPI](https://github.com/lord-ruby/SpectrumAPI) lets them share one set.
- **Bulwark** and **Asteroid Belt**: [Cryptid](https://github.com/SpectralPack/Cryptid).

No code or art is copied from them.

## License

The code and the original art are [GPL-3.0-or-later](LICENSE).

Some sprites in `assets/` are built from Balatro's own art, © LocalThunk, so that they match the game: the Wild
suit's rank glyphs and court cards, the four jokers, and the planets' frames, name plates and hand strips. Those
pixels aren't ours to license. They're included only for use with Balatro and aren't covered by the GPL.
[art/NOTES.md](art/NOTES.md#provenance-what-derives-from-which-vanilla-cell) lists the vanilla card behind each one.
The programs in `art/` contain no Balatro pixels; they read the textures from your own copy of the game.

## Development

- `scripts/test` runs the unit tests on LuaJIT. Without `luajit` installed, it borrows the LÖVE runtime from your
  Balatro install.
- `scripts/selftest` boots the game with the in-game checks in `tests/ingame.lua` and prints the results. It needs
  Steam running and this repo in your `Mods` folder (a symlink works; balala leaves symlinked checkouts alone).
- Launching the game with `QUINTESSENCE_SHOWCASE=out.png` lays the new cards out beside vanilla ones, saves a
  screenshot and quits, for checking the art in the engine. Add `QUINTESSENCE_SHOWCASE_PALETTE=lc` (or `hc`) to
  show normal or high-contrast colours whatever your settings say.
- The art is made by the Python programs in `art/` on a small pixel-art engine (`art/pixel.py`), partly from
  Balatro's own textures. `python3 art/build.py` rebuilds `assets/`; it reads the textures from your Balatro install
  (set `BALATRO_LOVE` to the path of `Balatro.love` if it isn't in the default Steam folder). Design notes are in
  `art/NOTES.md`.
