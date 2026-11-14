-- Jokers. Spectrum gets the trio every vanilla base hand has (+Mult, +Chips, xMult), at
-- vanilla rates; they go through SpectrumAPI so other mods' Spectrum trios don't stack up
-- beside them. They stay out of the shop until a Spectrum is within reach.

SMODS.Atlas { key = "jokers", path = "jokers.png", px = 71, py = 95 }

local function has_spectrum(context)
  return context.poker_hands and next(context.poker_hands.spa_Spectrum or {})
end

local function spectrum_joker(slot, def)
  def.object_type = "Joker"
  def.atlas = "jokers"
  def.priority = 10 -- SpectrumAPI keeps the highest priority; other mods use 0
  def.blueprint_compat = true
  def.in_pool = function()
    return Quintessence.spectrums_possible()
  end
  SpectrumAPI.add_content(def, slot)
end

-- The Spectrum sibling of Jolly, Zany, Mad, Crazy and Droll.
spectrum_joker("mult_handtype_jokers", {
  key = "wacky",
  pos = { x = 0, y = 0 },
  rarity = 1,
  cost = 4,
  config = { extra = { mult = 10 } },
  loc_vars = function(self, info_queue, card)
    return { vars = { card.ability.extra.mult, localize("spa_Spectrum", "poker_hands") } }
  end,
  calculate = function(self, card, context)
    if context.joker_main and has_spectrum(context) then
      return { mult = card.ability.extra.mult }
    end
  end,
})

-- The Spectrum sibling of Sly, Wily, Clever, Devious and Crafty.
spectrum_joker("chips_handtype_jokers", {
  key = "shrewd",
  pos = { x = 1, y = 0 },
  rarity = 1,
  cost = 4,
  config = { extra = { chips = 80 } },
  loc_vars = function(self, info_queue, card)
    return { vars = { card.ability.extra.chips, localize("spa_Spectrum", "poker_hands") } }
  end,
  calculate = function(self, card, context)
    if context.joker_main and has_spectrum(context) then
      return { chips = card.ability.extra.chips }
    end
  end,
})

-- The Spectrum sibling of The Duo, Trio, Family, Order and Tribe. Higher than The Tribe's
-- x2 because a Spectrum needs a Wild card first.
spectrum_joker("xmult_handtype_jokers", {
  key = "coalition",
  pos = { x = 2, y = 0 },
  rarity = 3,
  cost = 8,
  config = { extra = { xmult = 3 } },
  loc_vars = function(self, info_queue, card)
    return { vars = { card.ability.extra.xmult, localize("spa_Spectrum", "poker_hands") } }
  end,
  calculate = function(self, card, context)
    if context.joker_main and has_spectrum(context) then
      return { xmult = card.ability.extra.xmult }
    end
  end,
})

-- Played cards that don't score become Wild. From Manifold, at its rarity and price, and
-- like there it only shows up once the deck holds a Wild card. Like Midas Mask, it changes
-- the cards before scoring, and copying it does nothing.
SMODS.Joker {
  key = "envious",
  atlas = "jokers",
  pos = { x = 3, y = 0 },
  rarity = 1,
  cost = 5,
  blueprint_compat = false,
  in_pool = function()
    for _, card in ipairs(G.playing_cards or {}) do
      if card.base.suit == Quintessence.WILD then return true end
    end
    return false
  end,
  loc_vars = function(self, info_queue, card)
    return { vars = { colours = { G.C.SUITS[Quintessence.WILD] } } }
  end,
  calculate = function(self, card, context)
    if not (context.before and not context.blueprint) then return end
    local scoring = {}
    for _, c in ipairs(context.scoring_hand) do scoring[c] = true end
    local turned = 0
    for _, c in ipairs(context.full_hand) do
      if not scoring[c] and c.base.suit ~= Quintessence.WILD and not SMODS.has_no_suit(c) then
        turned = turned + 1
        Quintessence.make_wild(c, true)
        G.E_MANAGER:add_event(Event({ func = function()
          c:juice_up()
          c:set_sprites(nil, c.config.card)
          return true
        end }))
      end
    end
    if turned > 0 then
      return { message = localize("k_quint_wild"), colour = G.C.SUITS[Quintessence.WILD] }
    end
  end,
}
