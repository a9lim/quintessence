local planet_text = {
  "{S:0.8}({S:0.8,V:1}lvl.#1#{S:0.8}){} Level up",
  "{C:attention}#2#",
  "{C:mult}+#3#{} Mult and",
  "{C:chips}+#4#{} chips",
}

return {
  descriptions = {
    Joker = {
      j_quint_wacky = {
        name = "Wacky Joker",
        text = { "{C:red}+#1#{} Mult if played", "hand contains", "a {C:attention}#2#" },
      },
      j_quint_shrewd = {
        name = "Shrewd Joker",
        text = { "{C:chips}+#1#{} Chips if played", "hand contains", "a {C:attention}#2#" },
      },
      j_quint_coalition = {
        name = "The Coalition",
        text = { "{X:mult,C:white} X#1# {} Mult if played", "hand contains", "a {C:attention}#2#" },
      },
    },
    Planet = {
      c_quint_quaoar = { name = "Quaoar", text = planet_text },
      c_quint_haumea = { name = "Haumea", text = planet_text },
      c_quint_sedna = { name = "Sedna", text = planet_text },
      c_quint_makemake = { name = "Makemake", text = planet_text },
      c_quint_asteroid_belt = { name = "Asteroid Belt", text = planet_text },
    },
    -- Wild is a suit now. The enhancement survives only as what The Lovers and the
    -- other Wild sources hand out, so its tooltip describes the suit.
    Enhanced = {
      m_wild = { name = "Wild", text = { "A fifth suit that", "counts as every suit" } },
    },
    Tarot = {
      c_lovers = {
        name = "The Lovers",
        text = { "Moves {C:attention}#1#{} selected", "card to the", "{C:attention}Wild{} suit" },
      },
    },
    Other = {
      quint_wild_card = { text = { "Counts as every suit" } },
    },
  },
  misc = {
    suits_singular = { quint_Wild = "Wild" },
    suits_plural = { quint_Wild = "Wilds" },
    poker_hands = { quint_Bulwark = "Bulwark" },
    poker_hand_descriptions = {
      quint_Bulwark = { "5 cards with no rank or suit", "(Stone cards)" },
      spa_Spectrum = { "5 cards of 5 different suits,", "one of them Wild" },
      spa_Straight_Spectrum = { "5 cards in a row (consecutive ranks)", "of 5 different suits" },
      spa_Spectrum_House = { "A Three of a Kind and a Pair", "of 5 different suits" },
      spa_Spectrum_Five = { "5 cards with the same rank", "of 5 different suits" },
    },
    dictionary = {
      k_quint_minor_planets = "Minor Planets",
    },
  },
}
