-- The Spectrum hands: Spectrum, Straight Spectrum, Spectrum House and Spectrum Five.
--
-- They live in SpectrumAPI, which Cryptid, UNIK's mod and others share, so a player never
-- sees two copies of them. Quintessence sets their values and replaces the rule that finds
-- a Spectrum (see src/match.lua): five cards of five different suits, one card per suit,
-- where a card may stand for any suit it counts as. With Four Fingers, four cards are
-- enough, but one of them must still be Wild (or another suit beyond the vanilla four).

local cfg = SpectrumAPI.configuration

-- Starting values, priced by how often each hand turns up once a deck holds a Wild or two:
-- a Spectrum is a little commoner than a Flush, Straight Spectrum and Spectrum House sit
-- just under Straight Flush, and Spectrum Five needs duplicated cards like any Five of a
-- Kind. Chips x mult must not tie another hand's exactly, since the hand list sorts on it.
cfg.hand_values.spa_Spectrum = { c = 45, m = 4, l_c = 20, l_m = 2 }
cfg.hand_values.spa_Straight_Spectrum = { c = 80, m = 7, l_c = 35, l_m = 3 }
cfg.hand_values.spa_Spectrum_House = { c = 90, m = 8, l_c = 35, l_m = 3 }
cfg.hand_values.spa_Spectrum_Five = { c = 130, m = 13, l_c = 40, l_m = 3 }
-- Other mods read this to learn that Four Fingers shortens Spectrums.
cfg.misc.four_fingers_spectrums = true
-- The example hands in the Run Info screen show a Wild card.
cfg.misc.spectrum_example_suit = "quint_W"

Quintessence.SPECTRUMS = {
  "spa_Spectrum",
  "spa_Straight_Spectrum",
  "spa_Spectrum_House",
  "spa_Spectrum_Five",
}

local VANILLA = { Spades = true, Hearts = true, Clubs = true, Diamonds = true }
local function is_anchor(suit)
  return not VANILLA[suit]
end

-- The cards of the largest Spectrum in `hand`, or nil.
function Quintessence.find_spectrum(hand)
  local options = {}
  for i, card in ipairs(hand) do
    local suits = {}
    for _, suit in ipairs(SMODS.Suit.obj_buffer) do
      -- flush_calc = true: the suits a card counts as for hand-making, as for a Flush.
      if card:is_suit(suit, nil, true) then suits[#suits + 1] = suit end
    end
    options[i] = suits
  end
  local chosen = Quintessence.match.spectrum(options, SMODS.four_fingers("spectrum"), is_anchor)
  if not chosen then return nil end
  local cards = {}
  for _, i in ipairs(chosen) do cards[#cards + 1] = hand[i] end
  return cards
end

SMODS.PokerHandPart:take_ownership("spa_spectrum_part", {
  func = function(hand)
    local cards = Quintessence.find_spectrum(hand)
    return cards and { cards } or {}
  end,
}, true)

local to_number = rawget(_G, "to_number") or function(x) return x end

-- True once a Spectrum is within reach this run: the deck holds a card that counts as every
-- suit, or a Spectrum hand has been played. Spectrum jokers only show up after that.
function Quintessence.spectrums_possible()
  if not (G.GAME and G.GAME.hands) then return false end
  for _, key in ipairs(Quintessence.SPECTRUMS) do
    local hand = G.GAME.hands[key]
    if hand and to_number(hand.played or 0) > 0 then return true end
  end
  for _, card in ipairs(G.playing_cards or {}) do
    if SMODS.has_any_suit(card) then return true end
  end
  return false
end
