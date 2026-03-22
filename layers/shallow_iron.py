# layers/deep_iron.py
import random
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import (
    SEA_LEVEL,
    LOWLANDS_PEAK,
    HILLS_PEAK,
    SHALLOW_IRON_BASELINE_PROBABILITY,
    SHALLOW_IRON_BASELINE_TONNAGE_MEAN,
    SHALLOW_IRON_BASELINE_TONNAGE_SIGMA,
    # SHALLOW_IRON_ALLUVIAL_SPREAD_DIMINISHING_FACTOR,
    SHALLOW_IRON_HILL_SPAWN_PROBABILITY,
    SHALLOW_IRON_HILL_TONNAGE_MEAN,
    SHALLOW_IRON_HILL_TONNAGE_SIGMA,
    SHALLOW_IRON_FLOODPLAIN_SPAWN_PROBABILITY,
    SHALLOW_IRON_FLOODPLAIN_TONNAGE_MEAN,
    SHALLOW_IRON_FLOODPLAIN_TONNAGE_SIGMA,
    SHALLOW_IRON_RIVERBANK_SPAWN_PROBABILITY,
    SHALLOW_IRON_RIVERBANK_TONNAGE_MEAN,
    SHALLOW_IRON_RIVERBANK_TONNAGE_SIGMA,
    SHALLOW_IRON_FLOODPLAIN_RIVERS_DIMINISHER,
    SHALLOW_IRON_EXTRA_RICH_PROBABILITY,
    SHALLOW_IRON_EXTRA_RICH_TONNAGE_MULTIPLIER,
)


class ShallowIronLayer(BaseLayer[float]):
    def name(self) -> str:
        return "shallow_iron"

    def depends_on(self) -> list[str]:
        return ["height", "sea", "lakes", "rivers", "moisture"]

    def frequency(self) -> float:
        raise NotImplementedError()

    def seed_offset(self) -> int:
        return 103

    def max_layer_value(self) -> float:
        raise NotImplementedError()

    def _calculate_probability_and_size(
        self,
        coord: CoordType,
        height_layer: AnyBaseLayerType,
        sea_layer: AnyBaseLayerType,
        lakes_layer: AnyBaseLayerType,
        rivers_layer: AnyBaseLayerType,
        moisture_layer: AnyBaseLayerType,
    ) -> tuple[float, float]:
        if (
            sea_layer.get_value_at(coord) or
            lakes_layer.get_value_at(coord)
        ):
            return 0.0, 0.0

        neighbours = height_layer.get_neighbours_of(coord)
        rivers_around = sum(int(rivers_layer.get_value_at(n)) for n in neighbours)
        is_next_to_land = any(
            not sea_layer.get_value_at(n) and
            not rivers_layer.get_value_at(n) and
            not lakes_layer.get_value_at(n)
            for n in neighbours
        )
        norm_moisture = moisture_layer.get_value_at(coord) / moisture_layer.max_layer_value()

        if rivers_layer.get_value_at(coord) and is_next_to_land:
            prob = SHALLOW_IRON_RIVERBANK_SPAWN_PROBABILITY
            deposit_size = random.gauss(
                SHALLOW_IRON_RIVERBANK_TONNAGE_MEAN,
                SHALLOW_IRON_RIVERBANK_TONNAGE_SIGMA,
            )
        elif rivers_around:
            prob = SHALLOW_IRON_FLOODPLAIN_SPAWN_PROBABILITY * (0.5 + norm_moisture ** 2)
            deposit_size = random.gauss(
                SHALLOW_IRON_FLOODPLAIN_TONNAGE_MEAN,
                SHALLOW_IRON_FLOODPLAIN_TONNAGE_SIGMA,
            ) * (rivers_around ** SHALLOW_IRON_FLOODPLAIN_RIVERS_DIMINISHER)
        elif LOWLANDS_PEAK <= height_layer.get_value_at(coord) - SEA_LEVEL < HILLS_PEAK:
            prob = SHALLOW_IRON_HILL_SPAWN_PROBABILITY
            deposit_size = random.gauss(
                SHALLOW_IRON_HILL_TONNAGE_MEAN,
                SHALLOW_IRON_HILL_TONNAGE_SIGMA,
            )
        else:
            prob = SHALLOW_IRON_BASELINE_PROBABILITY
            deposit_size = random.gauss(
                SHALLOW_IRON_BASELINE_TONNAGE_MEAN,
                SHALLOW_IRON_BASELINE_TONNAGE_SIGMA,
            )

        return prob, deposit_size

    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[AnyBaseLayerType]
    ) -> None:
        """
        Generate shallow iron deposits on the map.
        """
        random.seed(seed + self.seed_offset())
        height_layer = next(layer for layer in layers if layer.name() == "height")
        sea_layer = next(layer for layer in layers if layer.name() == "sea")
        lakes_layer = next(layer for layer in layers if layer.name() == "lakes")
        rivers_layer = next(layer for layer in layers if layer.name() == "rivers")
        moisture_layer = next(layer for layer in layers if layer.name() == "moisture")

        for coord in coords:
            self._set_value_at(coord, 0.0)

        count = 0
        total_tonnage = 0.0
        existing_deposits: dict[CoordType, tuple[float, float]] = {}

        # first pass - create primary deposits
        for coord in coords:
            prob, deposit_size = self._calculate_probability_and_size(
                coord=coord,
                height_layer=height_layer,
                sea_layer=sea_layer,
                lakes_layer=lakes_layer,
                rivers_layer=rivers_layer,
                moisture_layer=moisture_layer,
            )

            if random.random() > prob:
                continue
            if random.random() < SHALLOW_IRON_EXTRA_RICH_PROBABILITY:
                deposit_size *= SHALLOW_IRON_EXTRA_RICH_TONNAGE_MULTIPLIER
            existing_deposits[coord] = (prob, deposit_size)
            if deposit_size > 0.0:
                count += 1
                total_tonnage += deposit_size

        # TODO: logic of second pass
        # deposited_coords = set(existing_deposits.keys())
        # secondary passes - extenuate the veins
        # multiplier = SHALLOW_IRON_ALLUVIAL_SPREAD_DIMINISHING_FACTOR
        # for coord, (prob, deposit_size) in existing_deposits.items():
        #     neighbours = [
        #         x for x in height_layer.get_neighbours_of(coord)
        #         if x not in existing_deposits.keys()
        #     ]
        #     for n in neighbours:
        #         prob, deposit_size = self._calculate_probability_and_size(
        #             coord=coord,
        #             height_layer=height_layer,
        #             sea_layer=sea_layer,
        #             lakes_layer=lakes_layer,
        #             rivers_layer=rivers_layer,
        #             moisture_layer=moisture_layer,
        #         )
        #         prob *= multiplier

        # new_deposits_created = True
        # multiplier = SHALLOW_IRON_EXTRA_RICH_TONNAGE_MULTIPLIER
        # neighbours_to_consider = set([])
        # while new_deposits_created:
        #     new_deposits_created = False
        #     for coord, (prob, deposit_size) in existing_deposits.items():
        #         neighbours = [
        #             x for x in height_layer.get_neighbours_of(coord)
        #             if x not in existing_deposits.keys()
        #         ]
        #         for n in neighbours:
        #             prob, deposit_size = self._calculate_probability_and_size(
        #                 coord=coord,
        #                 height_layer=height_layer,
        #                 sea_layer=sea_layer,
        #                 lakes_layer=lakes_layer,
        #                 rivers_layer=rivers_layer,
        #                 moisture_layer=moisture_layer,
        #             )
        #             prob *= multiplier
        #             if random.random() > prob:
        #                 continue
        #             new_deposits_created = True

            self._set_value_at(coord, max(deposit_size, 0.0))

        print(f"shallow deposits found: {count}; size: {total_tonnage}")
