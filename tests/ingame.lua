-- In-game self-test. Launch the game with QUINTESSENCE_SELFTEST set to a file path; once
-- the main menu is up, this builds cards, checks the Wild suit and the new hands in the
-- real engine, writes PASS/FAIL lines to that file and quits. It never starts a run, so a
-- saved run is untouched: Four Fingers and Smeared Joker are faked by stubbing the joker
-- lookups instead of holding the jokers.

local out_path = os.getenv("QUINTESSENCE_SELFTEST")
local WILD = Quintessence.WILD
local lines, failed = {}, 0

local function check(name, ok, detail)
  if not ok then failed = failed + 1 end
  lines[#lines + 1] = (ok and "PASS " or "FAIL ") .. name .. (ok and "" or ("  (" .. tostring(detail) .. ")"))
end

local made = {}
local function card(code, center)
  local key = code:gsub("^W_", "quint_W_")
  local c = Card(0, 0, G.CARD_W, G.CARD_H, G.P_CARDS[key], G.P_CENTERS[center or "c_base"])
  made[#made + 1] = c
  return c
end

local function hand(spec, center)
  local list = {}
  for code in spec:gmatch("%S+") do list[#list + 1] = card(code, center) end
  return list
end

-- Pretend these jokers are held: names for find_joker, keys for SMODS.find_card.
local function holding(jokers, fn)
  local set = {}
  for _, j in ipairs(jokers) do set[j] = true end
  local find_joker_, find_card_ = find_joker, SMODS.find_card
  find_joker = function(name, ...) if set[name] then return { {} } end return find_joker_(name, ...) end
  SMODS.find_card = function(key, ...) if set[key] then return { {} } end return find_card_(key, ...) end
  local ok, err = pcall(fn)
  find_joker, SMODS.find_card = find_joker_, find_card_
  if not ok then error(err, 0) end
end

-- The played hand's name: the best hand in G.handlist that the cards make. This is
-- G.FUNCS.get_poker_hand_info without its joker step, which needs a run.
local function hand_name(spec, center)
  local results = evaluate_poker_hand(hand(spec, center))
  for _, name in ipairs(G.handlist) do
    if next(results[name]) then return name end
  end
  return "NULL"
end

local function expect_hand(name, spec, want, center)
  local got = hand_name(spec, center)
  check(name, got == want, ("got %s, want %s"):format(got, want))
end

local function find_text(node, text)
  if type(node) ~= "table" then return false end
  if node.config and node.config.text == text then return true end
  for _, v in pairs(node) do
    if type(v) == "table" and v ~= node.parent and find_text(v, text) then return true end
  end
  return false
end

local function run()
  local bulwark = Quintessence.cryptid_bulwark() and "cry_Bulwark" or "quint_Bulwark"

  -- Registration
  check("Wild suit registered", SMODS.Suits[WILD] ~= nil)
  check("Wild cards exist for every rank", G.P_CARDS.quint_W_A ~= nil and G.P_CARDS.quint_W_2 ~= nil)
  for _, key in ipairs({ "j_quint_wacky", "j_quint_shrewd", "j_quint_coalition",
                         "c_quint_quaoar", "c_quint_haumea", "c_quint_sedna", "c_quint_makemake" }) do
    check("registered " .. key, G.P_CENTERS[key] ~= nil)
  end
  check("Bulwark and Asteroid Belt registered", SMODS.PokerHands.quint_Bulwark ~= nil and G.P_CENTERS.c_quint_asteroid_belt ~= nil)
  check("Spectrum hand values set", SMODS.PokerHands.spa_Spectrum.chips == 45 and SMODS.PokerHands.spa_Spectrum.mult == 4)

  -- The Wild enhancement turns into the suit
  local fresh = card("S_A", "m_wild")
  check("a card created Wild is in the Wild suit", fresh.base.suit == WILD, fresh.base.suit)
  check("...with a plain body", fresh.config.center.key == "c_base", fresh.config.center.key)
  local glass = card("H_7", "m_glass")
  glass:set_ability(G.P_CENTERS.m_wild)
  check("The Lovers on a Glass card makes a Glass Wild",
    glass.base.suit == WILD and glass.config.center.key == "m_glass" and glass.base.value == "7",
    glass.base.suit .. " " .. glass.config.center.key)

  -- Suit semantics
  local wild, spade = card("W_9"), card("S_9")
  check("a Wild counts as Hearts", wild:is_suit("Hearts") == true)
  check("a Wild counts as Spades for flushes", wild:is_suit("Spades", nil, true) == true)
  check("a Wild counts as Wild", wild:is_suit(WILD) == true)
  check("a Spade isn't Wild", not spade:is_suit(WILD))
  check("a Stone Wild has no suit", not card("W_4", "m_stone"):is_suit("Hearts"))
  check("has_enhancement sees the Wild suit", SMODS.has_enhancement(wild, "m_wild"))

  -- Hands
  expect_hand("Spectrum", "S_2 H_5 C_9 D_J W_K", "spa_Spectrum")
  expect_hand("a repeated suit is no Spectrum", "S_2 S_5 H_9 H_J W_K", "High Card")
  holding({ "Smeared Joker" }, function()
    expect_hand("Smeared: two Spades, two Hearts and a Wild", "S_2 S_5 H_9 H_J W_K", "spa_Spectrum")
  end)
  holding({ "j_four_fingers" }, function()
    expect_hand("Four Fingers: three suits and a Wild", "S_2 H_5 D_9 W_K", "spa_Spectrum")
    expect_hand("Four Fingers: the four vanilla suits alone are not", "S_2 H_5 C_9 D_J", "High Card")
  end)
  holding({ "j_four_fingers", "Smeared Joker" }, function()
    expect_hand("Four Fingers + Smeared: still needs a Wild", "S_2 S_5 H_9 H_J", "High Card")
  end)
  expect_hand("Straight Spectrum", "S_5 H_6 C_7 D_8 W_9", "spa_Straight_Spectrum")
  expect_hand("Spectrum House", "S_7 H_7 W_7 C_K D_K", "spa_Spectrum_House")
  expect_hand("Spectrum Five", "S_7 H_7 C_7 D_7 W_7", "spa_Spectrum_Five")
  expect_hand("Four of a Kind with a Wild kicker stays Four of a Kind", "S_7 H_7 C_7 D_7 W_K", "Four of a Kind")
  expect_hand("Flush with a Wild", "H_2 H_5 H_9 H_J W_K", "Flush")
  expect_hand("five Wilds play as a Spectrum", "W_2 W_5 W_9 W_J W_K", "spa_Spectrum")
  expect_hand("Bulwark", "S_A H_7 C_K D_4 S_9", bulwark, "m_stone")

  -- Hand order: G.handlist runs from best to worst
  local idx = {}
  for i, k in ipairs(G.handlist) do idx[k] = i end
  local function above(a, b) return idx[a] and idx[b] and idx[a] < idx[b] end
  check("Four of a Kind > Spectrum > Full House", above("Four of a Kind", "spa_Spectrum") and above("spa_Spectrum", "Full House"))
  check("Straight Flush > Spectrum House > Straight Spectrum > Four of a Kind",
    above("Straight Flush", "spa_Spectrum_House") and above("spa_Spectrum_House", "spa_Straight_Spectrum")
      and above("spa_Straight_Spectrum", "Four of a Kind"))
  check("Flush House > Spectrum Five > Five of a Kind", above("Flush House", "spa_Spectrum_Five") and above("spa_Spectrum_Five", "Five of a Kind"))
  check("Flush > Bulwark > Straight", above("Flush", "quint_Bulwark") and above("quint_Bulwark", "Straight"))

  -- Castle and The Idol name a vanilla suit for a Wild card
  check("a natural card names its own suit", Quintessence.vanilla_suit("Hearts", "quint_test") == "Hearts")
  local ok, named = pcall(Quintessence.vanilla_suit, WILD, "quint_test")
  check("a Wild card names a vanilla suit", ok and ({ Spades = 1, Hearts = 1, Clubs = 1, Diamonds = 1 })[named] ~= nil, named)

  -- Jokers
  local spectrum_context = { joker_main = true, poker_hands = { spa_Spectrum = { {} } } }
  local plain_context = { joker_main = true, poker_hands = { spa_Spectrum = {} } }
  local function joker(key) return card("S_A", key) end -- front is ignored for jokers
  local function calc(key, context) local j = joker(key); return j.config.center:calculate(j, context) end
  local r = calc("j_quint_wacky", spectrum_context)
  check("Wacky Joker: +10 Mult on a Spectrum", r and r.mult == 10)
  check("Wacky Joker: nothing otherwise", calc("j_quint_wacky", plain_context) == nil)
  r = calc("j_quint_shrewd", spectrum_context)
  check("Shrewd Joker: +80 Chips on a Spectrum", r and r.chips == 80)
  r = calc("j_quint_coalition", spectrum_context)
  check("The Coalition: x3 Mult on a Spectrum", r and r.xmult == 3)

  -- Tooltip
  local ok, ui = pcall(function() return card("W_8"):generate_UIBox_ability_table() end)
  check("a Wild card's tooltip says it counts as every suit", ok and find_text(ui, "Counts as every suit"), ok and "text not found" or ui)
end

local done, frames = false, 0
local update = Game.update
function Game:update(dt)
  update(self, dt)
  if done then return end
  if G.STATE == G.STATES.MENU and G.MAIN_MENU_UI then frames = frames + 1 end
  if frames < 30 then return end
  done = true
  local ok, err = pcall(run)
  if not ok then check("self-test ran to the end", false, err) end
  for _, c in ipairs(made) do c:remove() end
  lines[#lines + 1] = ("%d checks, %d failed"):format(#lines, failed)
  local f = io.open(out_path, "w")
  if f then f:write(table.concat(lines, "\n"), "\n"); f:close() end
  print("QUINTESSENCE SELFTEST\n" .. table.concat(lines, "\n"))
  love.event.quit()
end
