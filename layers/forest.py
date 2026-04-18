# 1️⃣ Forest as a Resource Layer
# Each tile has a forest score (0–1) representing richness, density, and overall quality.
# No need to model individual trees; abstraction is enough for resource management and game mechanics.
# High-score tiles are prime forest; low-score tiles are marginal patches.
# 2️⃣ Yield vs Regrowth
# The forest score informs regrowth per turn, not direct harvest.
# Rich forests regenerate quickly, allowing multiple lumber operations sustainably.
# Small or poor forests regenerate very slowly and can be depleted quickly.
# Nonlinear scaling makes high-quality forests more rewarding than small patches.
# 3️⃣ Harvesting Mechanics
# Each lumber operation (camp/mill) subtracts a flat amount from the current stock.
# The number of operations a tile can support sustainably is proportional to regrowth.
# Overharvesting reduces forest stock, creating strategic decisions for the player.
# 4️⃣ Sustainability Options
# Forests can be permanently depletable, regenerated slowly, or fully abstracted as infinite.
# Adding regeneration allows players to choose between exploitative extraction or sustainable management.
# Optional mechanics like policies, tech, or species type can influence regrowth or yield.
# 5️⃣ Integration with Gameplay
# Rich forests → encourage investment, multiple mills, strategic focus.
# Poor forests → one-time harvest, after which the tile can be converted to another land use (e.g., grassland).
# Works alongside your ore abstraction model, creating a consistent approach for natural resources.
# 6️⃣ Scale Considerations
# Tile size sets the real-world inspiration, but operations are abstracted:
# Even a 200×200 m tile represents thousands of trees.
# Regrowth and mill consumption are scaled to feel realistic without modeling each tree.

# ✅ Overall Concept

# Forest = numeric resource per tile
# Regrowth = nonlinear function of forest richness
# Mills consume a fixed portion per turn
# High-quality forests support multiple operations; small forests are transient
# Mechanic encourages strategic planning and balances realism with abstraction