# layers/deep_iron.py
import random
from math import exp
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import (
    SEA_LEVEL,
    DEEP_IRON_MOST_PROBABLE_ELEVATION,
    DEEP_IRON_ELEVATION_SIGMA_FALLOFF,
    DEEP_IRON_LOWEST_ELEVATION,
    DEEP_IRON_BASELINE_PROBABILITY,
    DEEP_IRON_PEAK_PROBABILITY,
    DEEP_IRON_ORE_GRADE_MEDIAN,
    DEEP_IRON_ORE_GRADE_VARIABILITY,
    DEEP_IRON_ORE_GRADE_EXTRA_RICH_PROBABILITY,
    DEEP_IRON_ORE_GRADE_EXTRA_RICH_MEDIAN,
    DEEP_IRON_ORE_GRADE_EXTRA_RICH_VARIABILITY,
)
from opensimplex import OpenSimplex


class DeepIronLayer(BaseLayer[float]):
    def name(self) -> str:
        return "deep_iron"

    def depends_on(self) -> list[str]:
        return ["height", "sea"]  

    def frequency(self) -> float:
        raise NotImplementedError()  

    def seed_offset(self) -> int:
        return 100

    def max_layer_value(self) -> float:
        raise NotImplementedError()

    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[AnyBaseLayerType]
    ) -> None:
        """
        Generate iron potential values for each coordinate.
        This will modulate the probability and the amount of iron 
        that will appear in the tile. The modulator potential offers
        realistic clustering, without revealing the whole map 
        by just one discovery.
        """
        random.seed(seed + self.seed_offset())
        height_layer = next(layer for layer in layers if layer.name() == "height")
        sea_layer = next(layer for layer in layers if layer.name() == "sea")

        for coord in coords:
            self._set_value_at(coord, 0.0)

        print("ORE GRADES")
        for coord in coords:
            elevation = height_layer.get_value_at(coord) - SEA_LEVEL

            if sea_layer.get_value_at(coord) or elevation < DEEP_IRON_LOWEST_ELEVATION:
                continue

            prob = (
                DEEP_IRON_BASELINE_PROBABILITY +
                (DEEP_IRON_PEAK_PROBABILITY - DEEP_IRON_BASELINE_PROBABILITY) *
                exp(
                    -(elevation - DEEP_IRON_MOST_PROBABLE_ELEVATION) /
                    (2 * DEEP_IRON_ELEVATION_SIGMA_FALLOFF**2)
                )
            )


            if random.random() < prob:
                ore_grade = random.gauss(
                    DEEP_IRON_ORE_GRADE_MEDIAN, 
                    DEEP_IRON_ORE_GRADE_VARIABILITY
                )
                if random.random() < DEEP_IRON_ORE_GRADE_EXTRA_RICH_PROBABILITY:
                    ore_grade = random.gauss(
                        DEEP_IRON_ORE_GRADE_EXTRA_RICH_MEDIAN, 
                        DEEP_IRON_ORE_GRADE_EXTRA_RICH_VARIABILITY
                    )
                    print("extra rich!!!!!")
                ore_grade = max(min(ore_grade, 1.0), 0.0)
                mining_yield = (
                    ore_grade + # base
                    0.2 * ore_grade**3 + # smoothing
                    0.1 * exp(5*(ore_grade-0.75)) # reward high yield
                    - 0.05 * exp(-40 * (ore_grade - 0.125)**2) # punish low yield
                )
                print( int(100*ore_grade) / 100.0, int(100*mining_yield)/100.0)

                self._set_value_at(coord, ore_grade)





