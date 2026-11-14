-- Showcase: launch the game with QUINTESSENCE_SHOWCASE set to a .png path; once the main
-- menu is up, this clears it, lays out the new cards beside a few vanilla ones at real
-- scale, saves a screenshot there and quits. For checking the art in the engine.
-- QUINTESSENCE_SHOWCASE_PALETTE=lc or hc shows every suit in normal or high-contrast
-- colours for the shot, whatever the settings say; the settings are put back before quitting.

local out_path = os.getenv("QUINTESSENCE_SHOWCASE")
local palette = os.getenv("QUINTESSENCE_SHOWCASE_PALETTE")
local saved_palettes

local rows = {
  { "j_quint_wacky", "j_quint_shrewd", "j_quint_coalition", "j_droll", "j_tribe" },
  { "c_quint_quaoar", "c_quint_haumea", "c_quint_sedna", "c_quint_makemake", "c_quint_asteroid_belt", "c_ceres", "c_eris" },
  { "quint_W_2", "quint_W_7", "quint_W_T", "quint_W_J", "quint_W_Q", "quint_W_K", "quint_W_A", "S_A", "H_K" },
}

local function build()
  for _, ui in ipairs({ "MAIN_MENU_UI", "PROFILE_BUTTON" }) do
    if G[ui] then G[ui]:remove(); G[ui] = nil end
  end
  if G.title_top then G.title_top:remove(); G.title_top = nil end
  if G.SPLASH_LOGO then G.SPLASH_LOGO:remove(); G.SPLASH_LOGO = nil end

  if palette then
    saved_palettes = copy_table(G.SETTINGS.colour_palettes)
    for _, suit in ipairs(SMODS.Suit.obj_buffer) do G.SETTINGS.colour_palettes[suit] = palette end
  end

  local w, h = G.ROOM.T.w, G.ROOM.T.h
  local row_h = G.CARD_H * 1.12
  local top = (h - row_h * #rows) / 2
  for r, keys in ipairs(rows) do
    local width = math.min(w - 1, #keys * G.CARD_W * 1.05)
    local area = CardArea((w - width) / 2, top + (r - 1) * row_h, width, G.CARD_H, { card_limit = #keys, type = "title" })
    for _, key in ipairs(keys) do
      -- Show undiscovered cards face up.
      local params = { bypass_discovery_center = true, bypass_discovery_ui = true }
      local card
      if G.P_CARDS[key] then
        card = Card(area.T.x, area.T.y, G.CARD_W, G.CARD_H, G.P_CARDS[key], G.P_CENTERS.c_base, params)
      else
        card = Card(area.T.x, area.T.y, G.CARD_W, G.CARD_H, G.P_CARDS.empty, G.P_CENTERS[key], params)
      end
      area:emplace(card)
    end
  end
end

local phase, frames = "wait", 0
local update = Game.update
function Game:update(dt)
  update(self, dt)
  frames = frames + 1
  if phase == "wait" and G.STATE == G.STATES.MENU and G.MAIN_MENU_UI and frames > 60 then
    build()
    phase, frames = "settle", 0
  elseif phase == "settle" and frames > 120 then
    phase = "shot"
    love.graphics.captureScreenshot(function(image)
      local f = io.open(out_path, "wb")
      if f then f:write(image:encode("png"):getString()); f:close() end
      phase = "done"
    end)
  elseif phase == "done" then
    if saved_palettes then G.SETTINGS.colour_palettes = saved_palettes end
    love.event.quit()
  end
end
