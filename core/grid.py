from .types import CoordType


def generate_all_coordinates(radius: int) -> list[CoordType]:
    result = []
    for q in range(-radius, radius + 1):
        r1 = max(-radius, -q - radius)
        r2 = min(radius, -q + radius)
        for r in range(r1, r2 + 1):
            result.append((q, r))
    return result


# class Tile:
#     def __init__(self, q: int, r: int) -> None:
#         self.q = q
#         self.r = r
#         self.layers: dict[str, float] = {}


# class HexGrid:
#     # flat-top directions
#     DIRECTIONS = [
#         (+1, 0), (+1, -1), (0, -1),
#         (-1, 0), (-1, +1), (0, +1)
#     ]

#     def __init__(self, radius: float) -> None:
#         self.radius = radius
#         self.tiles: dict[Coord, Tile] = {}
#         self._generate()

#     def _generate(self) -> None:
#         for q in range(-self.radius, self.radius + 1):
#             r1 = max(-self.radius, -q - self.radius)
#             r2 = min(self.radius, -q + self.radius)
#             for r in range(r1, r2 + 1):
#                 self.tiles[(q, r)] = Tile(q, r)

#     def neighbors(self, tile):
#         result = []
#         for dq, dr in self.DIRECTIONS:
#             coord = (tile.q + dq, tile.r + dr)
#             if coord in self.tiles:
#                 result.append(self.tiles[coord])
#         return result

#     def distance(self, a, b):
#         dq = a.q - b.q
#         dr = a.r - b.r
#         ds = -a.q - a.r + b.q + b.r
#         return (abs(dq) + abs(dr) + abs(ds)) // 2

#     def get_all_coords(self) -> list[Coord]:
#         return list(self.tiles.keys())
