-- Quintessence: Wild becomes the fifth suit, and the Spectrum hands and Bulwark join the
-- hand list. See README.md for the rules and the mods each idea comes from.

Quintessence = SMODS.current_mod
Quintessence.WILD = "quint_Wild" -- the Wild suit's key

-- True while Cryptid's own Bulwark is switched on; Quintessence's Bulwark and Asteroid Belt
-- step aside then. Asked at play time, since Cryptid loads after this mod and its content
-- sets can be turned off.
function Quintessence.cryptid_bulwark()
  return type(Cryptid) == "table" and type(Cryptid.enabled) == "function"
    and Cryptid.enabled("set_cry_poker_hand_stuff") == true
    and Cryptid.enabled("c_cry_asteroidbelt") == true
end

local function load(path)
  return assert(SMODS.load_file(path))()
end

SMODS.Atlas { key = "modicon", path = "icon.png", px = 34, py = 34 }

Quintessence.match = load("src/match.lua")
load("src/wild.lua")
load("src/spectrum.lua")
load("src/bulwark.lua")
load("src/planets.lua")
load("src/jokers.lua")

if os.getenv("QUINTESSENCE_SELFTEST") then load("tests/ingame.lua") end
if os.getenv("QUINTESSENCE_SHOWCASE") then load("tests/showcase.lua") end
