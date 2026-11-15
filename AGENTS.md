# AGENTS.md — Quintessence editing contract

Quintessence is a vanilla-plus Balatro mod on Steamodded: Wild becomes the fifth suit, and the Spectrum hands and
Bulwark join the hand list. `README.md` is the player-facing description and the source of truth for the rules;
this file records how the code holds them and how to check a change. Git history is the record of what changed.

## Stance

- **Vanilla-plus.** Everything should read as if it shipped with the game, and be priced against its vanilla
  sibling by how often it turns up (README has the odds). New Wild sources are out of scope: Wild cards come only
  from vanilla's sources. Envious Joker was removed for that reason.
- **Credit the source mods** (Manifold, Six Suits, Bunco, UNIK's mod, SpectrumAPI, Cryptid) in the README. Their
  ideas are reimplemented; their code is never copied (most of them carry no license).
- **License:** MIT for the code and original art. The sprites derived from Balatro's art are © LocalThunk and
  carved out (`assets/NOTICE.md`, README). `art/NOTES.md` lists the vanilla cell behind each derived sprite; keep
  it accurate whenever the art changes.

## Map

| path | role |
| --- | --- |
| `main.lua` | entry point; `Quintessence` global, `cryptid_bulwark()`, loads `src/` |
| `src/match.lua` | the Spectrum matching core; pure Lua, no game state |
| `src/wild.lua` | the Wild suit, the `has_any_suit` / `has_enhancement` overrides, the `set_ability` / `set_base` hooks |
| `src/spectrum.lua` | SpectrumAPI config (hand values), our Spectrum part, `spectrums_possible()` |
| `src/bulwark.lua`, `src/planets.lua`, `src/jokers.lua` | the rest of the content |
| `lovely/wild.toml` | patches for vanilla code that knows Wild only as an enhancement |
| `lovely/spectrumapi.toml` | a fix for SpectrumAPI's `SMODS.current_mod` handling |
| `localization/en-us.lua` | all text, in vanilla's voice, including overrides of vanilla's Wild and Lovers text |
| `tests/` | unit tests, the in-game self-test, the showcase |
| `art/` | the programs that make `assets/` (see Art) |

## Invariants

- **Wild is a suit, `quint_Wild`** (card key `quint_W`). `SMODS.has_any_suit` is true for it, so `Card:is_suit`
  and everything built on it (flushes, Smeared, Flower Pot, Seeing Double, suit Boss Blinds) treat it as every
  suit. The suit's `in_pool` is always false: nothing rolls it at random, and the deck view hides its row while empty.
- **The `m_wild` enhancement stays in its pools** but never sticks: `Card:set_ability(m_wild)` moves an existing card
  to the Wild suit and keeps its enhancement. A card being created gets a plain body, and its front turns Wild in
  `set_base`, because `Card:init` sets the ability *before* the base.
- **A Spectrum** is `need` cards matched to `need` distinct suits, one card per suit, where a card may take any
  suit it counts as (`is_suit(s, nil, true)`). At least one matched suit must be outside the vanilla four (the
  "anchor"). `need = SMODS.four_fingers('spectrum')`, so Four Fingers shortens a Spectrum but never lets it drop
  the Wild. The largest matching scores. `match.lua` holds this and is tested against brute force.
- **The Spectrum hands belong to SpectrumAPI** (`spa_*` keys). We set `SpectrumAPI.configuration` at load and take
  ownership of its `spa_spectrum_part`; our planets and jokers go through `SpectrumAPI.add_content` at priority 10.
- **The hand list sorts on chips × mult.** New values must not tie another hand's product exactly, and must keep the
  order in README (Spectrum between Full House and Four of a Kind, and so on). The self-test checks the order.
- **Bulwark always exists.** It matches nothing, and its planet is hidden, while Cryptid's own Bulwark is on
  (`Quintessence.cryptid_bulwark()`, asked at play time because Cryptid loads after us).
- **Lovely patches run at priority 10**, after Steamodded's (≤ 0), and their patterns must match the post-Steamodded
  text in `Mods/lovely/dump/`. Lovely matches whole trimmed lines.

## Verify

- `scripts/test`: unit tests on LuaJIT. It uses `luajit` from PATH (CI installs it) or borrows an unfused copy
  of the LÖVE runtime from the local Balatro install. Nothing gets installed on the Mac, which is deliberately
  Homebrew-free.
- `scripts/selftest`: boots the game with `tests/ingame.lua`, which checks registration, the Wild conversions,
  suit semantics, every hand, the hand order and the jokers at the main menu, then quits. It needs Steam
  running (the game quits without it) and the mod in `Mods/`. Joker presence is stubbed (`find_joker`,
  `SMODS.find_card`), and hands are named with `evaluate_poker_hand` + `G.handlist` because
  `G.FUNCS.get_poker_hand_info` needs a run. To cover the Cryptid path, clear `Mods/lovely/blacklist.txt` (a9
  keeps Cryptid there), run it, and restore the file.
- `QUINTESSENCE_SHOWCASE=out.png balala` lays out the new cards beside vanilla ones, screenshots them at real scale
  and quits. Add `QUINTESSENCE_SHOWCASE_PALETTE=lc|hc` to force normal or high-contrast colours; a9 plays with
  high contrast on, and the showcase puts the settings back.
- After any Lovely change, grep `Mods/lovely/dump/` to confirm the patch landed.

## Dev setup

`Mods/Quintessence` is a symlink to this repo; balala leaves symlinked checkouts alone. SpectrumAPI is installed
with balala. `balala` launches the game and `balala logs -f` follows its log.

## Art

`art/build.py` rebuilds `assets/` from the programs in `art/`: `wild_deck.py`, `planets.py`, `jokers.py`,
`icons.py`, on the pixel-art engine `pixel.py`. `vanilla.py` reads Balatro's textures straight from the game
archive (`BALATRO_LOVE` overrides its path); nothing from the archive is stored in the programs.

- 1x is the master and 2x is its exact nearest-neighbour double, as in vanilla. `build.py` checks every size and
  the doubling; the Lua side depends on the sheet sizes and cell orders.
- The high-contrast deck comes from vanilla's high-contrast sheet (`8BitDeck_opt2`), not from re-inking the
  normal one: vanilla shades its high-contrast suits and changes court accents per suit.
- The Wild colours are `#8b64b4` (normal) and `#1fa84f` (high contrast). `src/wild.lua` repeats them as the
  suit's text colour, so change both together.
- `art/look.py` renders blow-ups into `art/preview/` (gitignored); the showcase shows the art in the engine.

## Release

Bump `version` in `Quintessence.json`, add a `CHANGELOG.md` entry, run both test scripts, then tag `vX.Y.Z` and
publish a GitHub release. `balala install -s` takes the newest release.
