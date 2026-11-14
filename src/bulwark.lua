-- Bulwark: five cards with no rank and no suit, which in vanilla means five Stone cards.
-- Five Stones otherwise play as a High Card, so a Stone deck had no hand of its own.
-- (From Cryptid. While Cryptid's own Bulwark is switched on, this one never matches, so
-- only Cryptid's is played.)

SMODS.PokerHand {
  key = "Bulwark",
  visible = false,
  -- Five Stones already bring 250 chips, so the hand itself is light on chips and leans
  -- on mult.
  chips = 25,
  mult = 5,
  l_chips = 10,
  l_mult = 2,
  example = {
    { "S_A", true, enhancement = "m_stone" },
    { "H_7", true, enhancement = "m_stone" },
    { "C_K", true, enhancement = "m_stone" },
    { "D_4", true, enhancement = "m_stone" },
    { "S_9", true, enhancement = "m_stone" },
  },
  evaluate = function(parts, hand)
    if Quintessence.cryptid_bulwark() then return {} end
    local stones = {}
    for _, card in ipairs(hand) do
      if SMODS.has_no_rank(card) and SMODS.has_no_suit(card) then stones[#stones + 1] = card end
    end
    return #stones >= 5 and { stones } or {}
  end,
}
