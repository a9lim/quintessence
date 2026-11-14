-- Spectrum matching, kept free of game state so the tests can run it under plain LuaJIT.
--
-- A Spectrum is `need` cards standing for `need` different suits, one card per suit.
-- A card may stand for any suit it counts as: a Wild card for every suit, a card under
-- Smeared Joker for either suit of its colour. One card still fills only one suit, so
-- finding a Spectrum is finding a large enough matching between cards and suits.
--
-- At least one of the matched suits must be an "anchor": a suit outside the vanilla four.
-- With five cards that is automatic, since four suits can't hold five cards. It matters
-- when Four Fingers lowers `need` to 4: a four-card Spectrum still has to include the
-- Wild suit (or another modded suit), so the vanilla suits alone never make one.

local M = {}

-- Maximum matching by augmenting paths (Kuhn). options[i] lists the suits card i can fill.
-- Card `skip` and suit `taken` are left out. Returns the size and an owner map (suit -> card).
local function kuhn(options, skip, taken)
  local owner = {}
  local function augment(i, seen)
    for _, suit in ipairs(options[i]) do
      if suit ~= taken and not seen[suit] then
        seen[suit] = true
        if owner[suit] == nil or augment(owner[suit], seen) then
          owner[suit] = i
          return true
        end
      end
    end
    return false
  end
  local size = 0
  for i = 1, #options do
    if i ~= skip and augment(i, {}) then size = size + 1 end
  end
  return size, owner
end

-- Find a Spectrum among the cards described by `options`.
--   options    array; options[i] is the array of suit keys card i can stand for
--   need       how many cards the Spectrum needs (5, or 4 with Four Fingers)
--   is_anchor  function(suit) -> true for suits outside the vanilla four
-- Returns the sorted indices of the cards in the Spectrum, or nil. The Spectrum is the
-- largest matching found, so with Four Fingers a full five-card Spectrum still scores all
-- five cards.
function M.spectrum(options, need, is_anchor)
  if #options < need then return nil end
  local best_size, best_pin, best_owner = 0, nil, nil
  for i, opts in ipairs(options) do
    for _, anchor in ipairs(opts) do
      if is_anchor(anchor) then
        -- Pin card i to the anchor suit and match everything else around it. Any matching
        -- that uses an anchor contains some pinned pair, so trying every pin finds the
        -- largest anchored matching.
        local size, owner = kuhn(options, i, anchor)
        if size + 1 > best_size then
          best_size, best_pin, best_owner = size + 1, i, owner
        end
      end
    end
  end
  if best_size < need then return nil end
  local chosen = { best_pin }
  for _, card in pairs(best_owner) do chosen[#chosen + 1] = card end
  table.sort(chosen)
  return chosen
end

return M
