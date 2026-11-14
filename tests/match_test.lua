-- Tests for src/match.lua. Run from the repo root through scripts/test.

local match = dofile("src/match.lua")

local VANILLA = { S = true, H = true, C = true, D = true }
local function is_anchor(suit) return not VANILLA[suit] end

-- Card shorthands: a natural card is its suit letter; W counts as every suit; "SC" and
-- "HD" are Spades/Clubs and Hearts/Diamonds under Smeared Joker; X has no suit (Stone).
local function parse(hand, suits)
  local options = {}
  for card in hand:gmatch("%S+") do
    local opts = {}
    if card == "W" then
      for _, s in ipairs(suits) do opts[#opts + 1] = s end
    elseif card ~= "X" then
      for s in card:gmatch(".") do opts[#opts + 1] = s end
    end
    options[#options + 1] = opts
  end
  return options
end

local FIVE = { "S", "H", "C", "D", "W" } -- vanilla suits plus Wild
local SIX = { "S", "H", "C", "D", "W", "F" } -- plus another modded suit

local function spectrum(hand, need, suits)
  return match.spectrum(parse(hand, suits or FIVE), need, is_anchor)
end

local function size(chosen) return chosen and #chosen or 0 end

return function(t)
  t("one of each suit plus a Wild", function(eq)
    eq(size(spectrum("S H C D W", 5)), 5)
  end)

  t("a repeated natural suit breaks it", function(eq)
    eq(spectrum("S S H D W", 5), nil)
    eq(spectrum("S S H H W", 5), nil)
  end)

  t("Smeared: one card fills one suit of its colour", function(eq)
    eq(size(spectrum("SC SC HD HD W", 5)), 5)
    eq(spectrum("SC SC SC HD W", 5), nil) -- three black cards, two black suits
  end)

  t("several Wilds fill the gaps", function(eq)
    eq(size(spectrum("S H W W W", 5)), 5)
    eq(size(spectrum("W W W W W", 5)), 5)
    eq(spectrum("S S H W W", 5), nil)
  end)

  t("a suitless card can't take part", function(eq)
    eq(spectrum("X S H C W", 5), nil)
  end)

  t("Four Fingers: four cards, but never without the anchor", function(eq)
    eq(spectrum("S H C D", 4), nil)
    eq(size(spectrum("S H D W", 4)), 4)
    eq(spectrum("SC SC HD HD", 4), nil)
    eq(size(spectrum("SC HD HD W", 4)), 4)
  end)

  t("Four Fingers: the odd card out doesn't score", function(eq)
    local chosen = spectrum("S S H D W", 4)
    eq(size(chosen), 4)
    eq(chosen[1], 1)
    eq(chosen[2], 3) -- the second Spade is left out
    eq(size(spectrum("X S H W W", 4)), 4)
  end)

  t("Four Fingers: a full Spectrum still scores all five", function(eq)
    eq(size(spectrum("S H C D W", 4)), 5)
  end)

  t("fewer cards than needed", function(eq)
    eq(spectrum("S H W", 4), nil)
    eq(spectrum("S H C W", 5), nil)
  end)

  t("another modded suit anchors too", function(eq)
    eq(size(spectrum("S H C D F", 5, SIX)), 5)
    eq(size(spectrum("S H C F", 4, SIX)), 4)
    eq(spectrum("S H C D", 4, SIX), nil)
  end)

  t("more cards than suits", function(eq)
    eq(size(spectrum("S H C D W W", 5)), 5)
  end)

  -- Brute force: try every assignment of cards to suits (or to nothing).
  local function brute(options, need)
    local best, used = 0, {}
    local function go(i, count, anchored)
      if i > #options then
        if anchored and count > best then best = count end
        return
      end
      go(i + 1, count, anchored)
      for _, s in ipairs(options[i]) do
        if not used[s] then
          used[s] = true
          go(i + 1, count + 1, anchored or is_anchor(s))
          used[s] = false
        end
      end
    end
    go(1, 0, false)
    return best >= need and best or 0
  end

  t("agrees with brute force on random hands", function(eq)
    local kinds = { "S", "H", "C", "D", "W", "X", "SC", "HD", "F" }
    math.randomseed(1729)
    for _ = 1, 4000 do
      local n = math.random(3, 7)
      local cards = {}
      for i = 1, n do cards[i] = kinds[math.random(#kinds)] end
      local hand = table.concat(cards, " ")
      for _, need in ipairs({ 4, 5 }) do
        local options = parse(hand, SIX)
        local got = size(match.spectrum(options, need, is_anchor))
        eq(got, brute(options, need), hand .. " need " .. need)
      end
    end
  end)
end
