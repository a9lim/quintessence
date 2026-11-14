-- The Wild suit. Wild stops being an enhancement and becomes a fifth suit that counts as
-- every suit. (Ouiiskey's Manifold had the idea first.)
--
-- Anything that would give a card the Wild enhancement moves it to the Wild suit instead:
-- The Lovers, Standard packs, Familiar, Grim and Incantation. Wild cards turn up exactly as
-- often as in vanilla, and a Wild card keeps whatever enhancement it had, so a Glass Wild
-- or a Lucky Wild is possible now. Suit-changing tarots (The Star, The Moon, The Sun,
-- The World) and Sigil overwrite the suit like any other, so they can take a card out of
-- the Wild suit.

local WILD = Quintessence.WILD

SMODS.Atlas { key = "wild_deck", path = "wild_deck.png", px = 71, py = 95 }
SMODS.Atlas { key = "wild_deck_hc", path = "wild_deck_hc.png", px = 71, py = 95 }
SMODS.Atlas { key = "wild_ui", path = "wild_ui.png", px = 18, py = 18 }
SMODS.Atlas { key = "wild_ui_hc", path = "wild_ui_hc.png", px = 18, py = 18 }

SMODS.Suit {
  key = "Wild",
  card_key = "W",
  pos = { y = 0 },
  ui_pos = { x = 0, y = 0 },
  lc_atlas = "wild_deck",
  hc_atlas = "wild_deck_hc",
  lc_ui_atlas = "wild_ui",
  hc_ui_atlas = "wild_ui_hc",
  -- Violet, and green in high contrast, where Spades are already purple (art/NOTES.md).
  lc_colour = "9a5bd6",
  hc_colour = "1fa84f",
  -- Never rolled at random: not in starting decks, not as a Standard pack front, not for
  -- newly created cards. Returning false for { rank = "" } also hides the Wild row in the
  -- deck view until you own a Wild card.
  in_pool = function(self, args)
    return false
  end,
}

-- A Wild card counts as every suit. Card:is_suit, flushes, Smeared Joker, Flower Pot,
-- Seeing Double and the suit Boss Blinds all ask this.
local has_any_suit = SMODS.has_any_suit
function SMODS.has_any_suit(card)
  return (card and card.base and card.base.suit == WILD) or has_any_suit(card)
end

-- Mods that look for the Wild enhancement find Wild cards.
local has_enhancement = SMODS.has_enhancement
function SMODS.has_enhancement(card, key)
  if key == "m_wild" and card and card.base and card.base.suit == WILD then return true end
  return has_enhancement(card, key)
end

-- The enhancement stays in its pools, so everything that rolls it still does at vanilla
-- rates; the hooks below turn each roll into the Wild suit. It leaves the collection.
SMODS.Enhancement:take_ownership("wild", { no_collection = true }, true)

local function wild_front(front)
  local rank = front and SMODS.Ranks[front.value]
  return rank and G.P_CARDS[SMODS.Suits[WILD].card_key .. "_" .. rank.card_key] or front
end

-- The suit Castle and The Idol name for a card: its own, or a random vanilla suit for a
-- Wild card (lovely/wild.toml).
local VANILLA_SUITS = { "Spades", "Hearts", "Clubs", "Diamonds" }
function Quintessence.vanilla_suit(suit, seed)
  if suit ~= WILD then return suit end
  return (pseudorandom_element(VANILLA_SUITS, pseudoseed(seed)))
end

-- Move a card to the Wild suit, keeping its rank and enhancement. With `manual_sprites`
-- the caller redraws it later (for flip animations).
function Quintessence.make_wild(card, manual_sprites)
  if card.base.suit == WILD then return end
  SMODS.change_base(card, WILD, nil, manual_sprites)
  if G.GAME and G.GAME.blind and card.playing_card then G.GAME.blind:debuff_card(card) end
end

local set_ability = Card.set_ability
function Card:set_ability(center, initial, delay_sprites)
  if type(center) == "string" then center = G.P_CENTERS[center] end
  if center and center.key == "m_wild" then
    if self.base and self.base.suit then
      -- An existing card joins the Wild suit and keeps its enhancement.
      Quintessence.make_wild(self, delay_sprites)
      if delay_sprites then
        G.E_MANAGER:add_event(Event({ func = function()
          if not self.REMOVED then self:set_sprites(nil, self.config.card) end
          return true
        end }))
      end
      return
    end
    -- A card being created: Card:init sets the ability before the base, so give it a
    -- plain body now and make its front Wild when set_base arrives.
    self.quint_wild_front = true
    center = G.P_CENTERS.c_base
  end
  return set_ability(self, center, initial, delay_sprites)
end

local set_base = Card.set_base
function Card:set_base(card, initial, manual_sprites)
  if self.quint_wild_front then
    self.quint_wild_front = nil
    card = wild_front(card)
  end
  return set_base(self, card, initial, manual_sprites)
end
