# layers/moisture.py
import random
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import RIVERS_SOURCE_RIVER_SPAWN_PROBABILITY


RELATIVE_HEIGHT = 0.5
HEIGHT_WEIGHT = 0.7
MOISTURE_WEIGHT = 0.3
MEANDERING_PROBABILITY = 0.1
FLOWING_UPHILL_PROBABILITY = 0.5


class RiversLayer(BaseLayer[bool]):
    def name(self) -> str:
        return "rivers"

    def depends_on(self) -> list[str]:
        return ["height", "sea", "lakes"]

    def frequency(self) -> float:
        """Probability of a candidate spot to make a river."""
        return 1.0

    def seed_offset(self) -> int:
        return 13

    def max_layer_value(self) -> float:
        raise NotImplementedError()

    def _select_river_source_candidates(
        self,
        coords: list[CoordType],
        height_layer: AnyBaseLayerType,
        sea_layer: AnyBaseLayerType,
        moisture_layer: AnyBaseLayerType,
        lakes_layer: AnyBaseLayerType,
    ) -> dict[CoordType, float]:

        candidates: dict[CoordType, float] = {}
        for coord in coords:
            current_height = height_layer.get_value_at(coord)
            neighbours = height_layer.get_neighbours_of(coord)

            # already pretty wet
            if sea_layer.get_value_at(coord) or lakes_layer.get_value_at(coord):
                continue

            # do not start in local basins
            if not any(height_layer.get_value_at(n) <= current_height for n in neighbours):
                continue

            candidates[coord] = (
                # ** 3 - favour high sources but dont exclude lower ones
                # ** 3 - favour the high moisture
                0.7 * (current_height / height_layer.max_layer_value()) ** 3 +
                0.3 * (moisture_layer.get_value_at(coord) / moisture_layer.max_layer_value()) ** 3
            ) * RIVERS_SOURCE_RIVER_SPAWN_PROBABILITY

        return candidates

    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[AnyBaseLayerType]
    ) -> None:
        """
        """
        random.seed(seed + self.seed_offset())

        height_layer = next(layer for layer in layers if layer.name() == "height")
        moisture_layer = next(layer for layer in layers if layer.name() == "moisture")
        sea_layer = next(layer for layer in layers if layer.name() == "sea")
        lakes_layer = next(layer for layer in layers if layer.name() == "lakes")

        source_candidates = self._select_river_source_candidates(
            coords,
            height_layer=height_layer,
            sea_layer=sea_layer,
            moisture_layer=moisture_layer,
            lakes_layer=lakes_layer,
        )

        sources: list[CoordType] = []
        for coord, score in source_candidates.items():
            if random.random() < score * self.frequency():
                sources.append(coord)

        print('#'*80)
        print(len(sources))

        rivers: set[CoordType] = set()

        def find_path(source: CoordType) -> set[CoordType] | None:
            path: list[CoordType] = []
            visited: set[CoordType] = set()

            current = source

            MAX_STEPS = int(3 * radius ** 2)

            for _ in range(MAX_STEPS):
                path.append(current)
                visited.add(current)

                # TERMINATION CONDITIONS
                if sea_layer.get_value_at(current) or lakes_layer.get_value_at(current):
                    return set(path)

                if current in rivers:
                    return set(path)

                neighbours = height_layer.get_neighbours_of(current)
                if not neighbours:
                    return None

                current_height = height_layer.get_value_at(current)

                # sort neighbours by height (ascending)
                neighbours_sorted = sorted(
                    neighbours,
                    key=lambda n: height_layer.get_value_at(n)
                )

                # take a few lowest for slight variation
                k = min(3, len(neighbours_sorted))
                lowest_candidates = neighbours_sorted[:k]

                # prefer strictly downhill
                downhill = [
                    n for n in lowest_candidates
                    if height_layer.get_value_at(n) < current_height
                ]

                if downhill:
                    # small randomness among best downhill options
                    next_coord = random.choice(downhill)
                else:
                    # no downhill → force lowest (prevents getting stuck)
                    next_coord = neighbours_sorted[0]

                # avoid tiny loops
                if next_coord in visited:
                    return set(path)

                current = next_coord

            return None

        for source in sources:
            path = find_path(source)
            if path is None:
                continue

            rivers.update(path)

        for coord in coords:
            self._set_value_at(coord, False)

        for river_tile in rivers:
            self._set_value_at(river_tile, True)
