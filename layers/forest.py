# Forest design notes
#
# Forest should be modeled with two related but distinct concepts:
#
# 1. forest_richness (static, generated at map creation)
#    - A value in the range 0..1 representing the long-term quality of the site for forest.
#    - This is not "how many trees are currently standing here".
#    - It represents carrying capacity / site productivity:
#      moisture, soil quality, climate, elevation, and general suitability for dense forest.
#    - High richness means the tile can sustain more biomass and recover better after harvesting.
#    - Low richness means the tile supports only marginal woodland or scrub-like forest.
#
# 2. forest_stock (dynamic, changes during play)
#    - The current standing forest biomass / usable timber on the tile.
#    - This is the value that harvesting removes from.
#    - Stock may be high or low independently of richness at any given moment,
#      because a productive site may have been recently cut, burned, or disturbed,
#      while a poorer site may still hold a mature stand if left untouched.
#
# Why separate these values?
# - One number is not enough to express:
#   (a) how good the land is for forest,
#   (b) how much wood is standing there right now,
#   (c) how quickly the forest recovers after use.
# - Keeping richness and stock separate makes the system more realistic and easier to balance.
# - It also creates better gameplay: the player can distinguish between
#   "good land that has been overcut" and "bad land that was never very forested".
#
# Starting state for an untouched island
# - Most forested tiles should begin near their local maximum stock.
# - That reflects a world with little or no prior human extraction.
# - However, tiles should not all start at exactly 100%:
#   natural forests contain gaps, patchiness, storm damage, age variation, and uneven structure.
# - A good default is:
#       max_stock   = richness * MAX_FOREST_STOCK
#       start_stock = max_stock * random value in ~0.8..1.0
# - This gives the map a believable "mostly mature, but not perfectly uniform" forest cover.
#
# Harvesting model
# - Lumber camps / mills do not reduce richness.
# - They reduce stock.
# - Richness is the long-term potential of the tile; stock is the short-term resource state.
# - This allows overharvesting, recovery, and strategic planning.
#
# Sustainability idea
# - Rich forest tiles are valuable because they support both:
#   (a) larger total standing stock
#   (b) stronger long-term regrowth
# - Poor forests may still provide an initial harvest, but are bad long-term production sites.
# - After depletion, poor forest tiles may be better converted to another land use.
#
# Proposed regrowth formula
#
# Let:
#   stock_ratio = forest_stock / max_stock
#
# Then per-turn regrowth can be:
#
#   regrowth = R * (forest_richness ** alpha) * stock_ratio * (1 - stock_ratio)
#
# where:
#   R      = base regrowth constant
#   alpha  = tuning exponent, usually around 1.5 to 2.0
#
# Interpretation:
# - forest_richness ** alpha makes prime forest disproportionately better than mediocre forest.
# - stock_ratio * (1 - stock_ratio) gives a simple logistic-shaped growth curve:
#   - near empty forest regrows slowly
#   - mid-density forest regrows fastest
#   - near-full forest regrows slowly again
# - This avoids unrealistic infinite-yield behavior and encourages sustainable management.
#
# Turn update sketch
#
#   max_stock = forest_richness * MAX_FOREST_STOCK
#   stock_ratio = forest_stock / max_stock
#   regrowth = R * (forest_richness ** alpha) * stock_ratio * (1 - stock_ratio)
#   forest_stock = min(max_stock, forest_stock + regrowth - harvest_demand)
#
# Notes:
# - harvest_demand is the fixed amount consumed by camps / mills this turn.
# - If desired, an almost-empty tile can be clamped to 0 and treated as cleared / exhausted.
# - Richness normally stays fixed unless the game later adds mechanics such as reforestation,
#   long-term degradation, irrigation, policy effects, species shifts, etc.
#
# Overall concept
# - richness = long-term forest potential
# - stock    = current standing timber
# - harvest removes stock
# - regrowth depends mostly on richness, but also on how full the stand currently is
# - untouched maps start near full stock, but not perfectly full everywhere
# - this keeps the model abstract, strategic, and ecologically plausible
