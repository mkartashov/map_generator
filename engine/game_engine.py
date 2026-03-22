# import random
# from core.types import CoordType
from core.base_layer import AnyBaseLayerType
# from core.config import SEA_LEVEL
# from layers.height import HeightLayer
# from layers.rivers import RiversLayer
# from layers.moisture import MoistureLayer
# from layers.sea import SeaLayer


# def assign_iron_ore(
#   height_layer: HeightLayer,
#   sea_layer: SeaLayer,
#   moisture_layer: MoistureLayer,
#   rivers_layer: RiversLayer,
#   iron_potential: IronPotentialLayer,
#   seed: int,
# ) -> dict[CoordType, float]:
#   random.seed(seed)

#   iron_deposits: dict[CoordType, float] = {}
#   coords = height_layer.get_all_coords()

#   for coord in coords:
#       base_spawn_chance = 0.0
#       deposit_range = (0, 0)

#       elevation = height_layer.get_value_at(coord) - SEA_LEVEL
#       is_river = rivers_layer.get_value_at(coord)
#       moisture = moisture_layer.get_value_at(coord)
#       neighbours = height_layer.get_neighbours_of(coord)
#       rivers_around = sum(int(rivers_layer.get_value_at(n)) for n in neighbours)
#       is_next_to_land = any(
#           not rivers_layer.get_value_at(n) and
#           not sea_layer.get_value_at(n)
#           for n in neighbours
#       )

#       if sea_layer.get_value_at(coord):
#           continue

#       if (elevation <= 200.0):
#           if is_river and is_next_to_land:
#               deposit_range = (2_000, 25_000)
#               base_spawn_chance = 0.7
#           elif (0.65 <= moisture <= 1.0) and rivers_around:
#               deposit_range = (
#                   2_000 * (1 + 0.3*(1 - exp(-0.7*rivers_around))),
#                   25_000 * (1 + 0.6*(1 - exp(-0.7*rivers_around)))
#               )
#               base_spawn_chance = 0.5
#           elif (0.35 <= moisture < 0.65):
#               deposit_range = (10_000, 60_000)
#               base_spawn_chance = 0.15
#           else:
#               deposit_range = (1_000, 15_000)
#               base_spawn_chance = 0.15

#       elif (200.0 < elevation <= 600.0):
#           if is_river and is_next_to_land:
#               deposit_range = (40_000, 180_000)
#               base_spawn_chance = 0.55
#           elif (0.35 <= moisture <= 0.7):
#               deposit_range = (40_000, 180_000)
#               base_spawn_chance = 0.35
#           elif (0.0 <= moisture < 0.35):
#               deposit_range = (40_000, 300_000)
#               base_spawn_chance = 0.2

#       elif (600.0 < elevation):
#           if (0.5 <= moisture <= 1.0):
#               deposit_range = (2_000, 120_000)
#               base_spawn_chance = 0.25
#           elif (0.3 <= moisture < 0.5):
#               deposit_range = (150_000, 1_000_000)
#               base_spawn_chance = 0.45
#           else: # < 0.3
#               deposit_range = (300_000, 5_000_000)
#               base_spawn_chance = 0.60
#       else:
#           base_spawn_chance = 0.0


#       spawn_chance = base_spawn_chance * (0.2 + 0.8*iron_potential)
#       final_tonnage = deposit_range[0] + (deposit_range[1] - deposit_range[0]) * iron_potential

#       if random.random() < spawn_chance:
#           # congratulations, we have some iron!
#           iron_deposits[coord] = final_tonnage

#   return iron_deposits

def export_game_map(layers: list[AnyBaseLayerType], seed: int) -> None:
    pass
