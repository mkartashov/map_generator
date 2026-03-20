# layers/moisture.py
import random
from core.base_layer import BaseLayer
from core.types import CoordType, LayerMapFloatType
from opensimplex import OpenSimplex


RELATIVE_HEIGHT = 0.5
HEIGHT_WEIGHT = 0.7
MOISTURE_WEIGHT = 0.3
MEANDERING_PROBABILITY = 0.1
FLOWING_UPHILL_PROBABILITY = 0.5

class RiversLayer(BaseLayer):
    def name(self) -> str:
        return "rivers"

    def depends_on(self) -> list[str]:
        return ["height", "sea"]

    def frequency(self) -> float:
        """Probability of a wet high spot to make a river."""
        return 1.0

    def seed_offset(self) -> int:
        return 0

    def max_layer_value(self) -> float:
        raise NotImplementedError()

    def _select_river_source_candidates(
        self, 
        coords: list[CoordType],
        height_layer: BaseLayer,
        sea_layer: BaseLayer, 
        moisture_layer: BaseLayer,
    ) -> dict[CoordType, float]:
        max_height = height_layer.max_layer_value()
        max_moisture = moisture_layer.max_layer_value()
        candidates = {}

        for coord in coords:
            relative_height = height_layer.get_value_at(coord) / max_height
            is_sea = sea_layer.get_value_at(coord)

            if relative_height >= RELATIVE_HEIGHT and not is_sea:
                score = (
                    HEIGHT_WEIGHT * relative_height + 
                    MOISTURE_WEIGHT * moisture_layer.get_value_at(coord) / max_moisture
                )
                candidates[coord] = score

        return candidates


    def _find_path(height_layer, current_path, previous_height, current_coord, uphill_count):
        curr_height = height_layer.get_value_at(current_coord)
        if curr_height > previous_height and uphill_count == 3:
            return None



    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[BaseLayer]
    ) -> LayerMapFloatType:
        """
        """
        random.seed(seed + self.seed_offset()) 

        height_layer = next(layer for layer in layers if layer.name() == "height")
        moisture_layer = next(layer for layer in layers if layer.name() == "moisture")
        sea_layer = next(layer for layer in layers if layer.name() == "sea")

        source_candidates = self._select_river_source_candidates(
            coords, 
            height_layer=height_layer, 
            sea_layer=sea_layer,
            moisture_layer=moisture_layer,
        )

        sources: list[CoordType] = []
        for coord, score in source_candidates.items():
            if random.random() < score * self.frequency():
                sources.append(coord)

        rivers = set()

        import math

        def find_path(source):
            path_list = [source]
            path_set = {source}

            current = source
            previous = None
            uphill_count = 0
            steps = 0

            MAX_STEPS = 1000
            T = 0.7  # slightly lower = less wandering

            while steps < MAX_STEPS:
                steps += 1

                current_height = height_layer.get_value_at(current)
                neighbours = height_layer.get_neighbours_of(current)

                if not neighbours:
                    return None

                # ✅ reach sea
                for n in neighbours:
                    if sea_layer.get_value_at(n):
                        return path_set | {n}

                # ✅ merge into existing river
                for n in neighbours:
                    if n in rivers:
                        return path_set | {n}

                # Prefer unvisited, but allow revisiting if needed
                unvisited = [n for n in neighbours if n not in path_set]
                candidates = unvisited if unvisited else neighbours

                # 🚫 avoid immediate backtracking
                if previous is not None:
                    candidates = [n for n in candidates if n != previous]

                if not candidates:
                    return None

                weights = []

                for n in candidates:
                    h = height_layer.get_value_at(n)
                    delta_h = h - current_height

                    # uphill limit
                    if delta_h > 0 and uphill_count >= 3:
                        weights.append(0)
                        continue

                    # base Boltzmann weight
                    w = math.exp(-delta_h / T)

                    # discourage flat wandering
                    if abs(delta_h) < 0.01:
                        w *= 0.3

                    # 🔥 MOMENTUM (directional bias)
                    if previous is not None:
                        dx1 = current[0] - previous[0]
                        dy1 = current[1] - previous[1]

                        dx2 = n[0] - current[0]
                        dy2 = n[1] - current[1]

                        alignment = dx1 * dx2 + dy1 * dy2  # dot product

                        if alignment > 0:
                            w *= 2.5   # strongly prefer forward
                        elif alignment < 0:
                            w *= 0.2   # strongly discourage turning back
                        else:
                            w *= 0.7   # slight penalty for sharp turns

                    # penalise revisiting (prevents thickness)
                    if n in path_set:
                        w *= 0.05

                    weights.append(w)

                total = sum(weights)
                if total == 0:
                    return None

                # 🎲 weighted random choice
                r = random.uniform(0, total)
                acc = 0

                for n, w in zip(candidates, weights):
                    acc += w
                    if acc >= r:
                        next_coord = n
                        break

                # update uphill count
                if height_layer.get_value_at(next_coord) > current_height:
                    uphill_count += 1
                else:
                    uphill_count = 0

                previous = current
                current = next_coord

                path_list.append(current)
                path_set.add(current)

            return None



        for source in sources:
            path = find_path(source)
            print('='*50)
            print(path)
            if path:
                rivers.update(path)

            


        for coord in coords:
            self._set_value_at(coord, False)
        for river_tile in rivers:
            self._set_value_at(river_tile, True)

        # sources: list[CoordType] = []
        # for coord, score in source_candidates.items():
        #     if random.random() < score * self.frequency():
        #         sources.append(coord)

        # print("SOURCES")
        # print(sources)

        # rivers = set()

        # for source in sources:
        #     current = source
        #     path = [current]

        #     current_height = height_layer.get_value_at(current)
        #     neighbours = self.get_neighbours_of(current)
            
        #     # skip tiles already in path to prevent loops
        #     neighbours = [n for n in neighbours if n not in path]
        #     neighbours.sort(key=lambda n: height_layer.get_value_at(n))

        #     if not neighbours:
        #         rivers.update(path)
        #         break

        #     # sort neighbors by height
            
        #     # try downhill first
        #     lower_neighbours = [n for n in neighbours if height_layer.get_value_at(n) < current_height]
            
        #     if not lower_neighbours:
        #         # allow flat or small uphill flow if blocked
        #         lower_neighbours = [n for n in neighbours if height_layer.get_value_at(n) <= current_height + 1]

        #     if not lower_neighbours:
        #         # completely stuck
        #         rivers.update(path)
        #         break

        #     # pick next tile
        #     choice = lower_neighbours[0]
        #     if len(lower_neighbours) > 1 and random.random() < MEANDERING_PROBABILITY:
        #         choice = lower_neighbours[1]

        #     # stop if reached sea
        #     if sea_layer.get_value_at(choice):
        #         path.append(choice)
        #         rivers.update(path)
        #         break

        #     path.append(choice)
        #     current = choice

        # reset layer and mark rivers

