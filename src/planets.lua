-- Planets for the new hands. Like vanilla's Ceres and Eris, they only appear once their
-- hand has been played (softlock). The Spectrum planets go through SpectrumAPI so that
-- other mods' copies don't show up alongside them.

SMODS.Atlas { key = "planets", path = "planets.png", px = 71, py = 95 }

local to_number = rawget(_G, "to_number") or function(x) return x end

local function planet(key, hand, x, badge)
  return {
    object_type = "Planet",
    key = key,
    set = "Planet",
    atlas = "planets",
    pos = { x = x, y = 0 },
    cost = 3,
    config = { hand_type = hand, softlock = true },
    priority = 10, -- SpectrumAPI keeps the highest priority; other mods use 0
    set_card_type_badge = function(self, card, badges)
      badges[#badges + 1] = create_badge(localize(badge), get_type_colour(self, card), nil, 1.2)
    end,
    loc_vars = function(self, info_queue, card)
      local h = G.GAME.hands[self.config.hand_type]
      local level = to_number(h.level)
      return {
        vars = {
          h.level,
          localize(self.config.hand_type, "poker_hands"),
          h.l_mult,
          h.l_chips,
          colours = { level == 1 and G.C.UI.TEXT_DARK or G.C.HAND_LEVELS[math.min(7, level)] },
        },
      }
    end,
  }
end

SpectrumAPI.add_content(planet("quaoar", "spa_Spectrum", 0, "k_dwarf_planet"), { hand = "spa_Spectrum" })
SpectrumAPI.add_content(planet("haumea", "spa_Straight_Spectrum", 1, "k_dwarf_planet"), { hand = "spa_Straight_Spectrum" })
SpectrumAPI.add_content(planet("sedna", "spa_Spectrum_House", 2, "k_dwarf_planet"), { hand = "spa_Spectrum_House" })
SpectrumAPI.add_content(planet("makemake", "spa_Spectrum_Five", 3, "k_dwarf_planet"), { hand = "spa_Spectrum_Five" })

-- Out of the shop and the collection while Cryptid's Asteroid Belt is in play.
local belt = planet("asteroid_belt", "quint_Bulwark", 4, "k_quint_minor_planets")
belt.in_pool = function() return not Quintessence.cryptid_bulwark() end
belt.no_collection = function() return Quintessence.cryptid_bulwark() end
SMODS.Planet(belt)
