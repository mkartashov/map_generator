# layers/moisture.py
from typing import Dict, List
from core.base_layer import BaseLayer
from core.types import Coord
from opensimplex import OpenSimplex

class MoistureLayer(BaseLayer):
    def name(self) -> str:
        return "moisture"

    def depends_on(self) -> List[str]:
        return ["height"]  # Moisture depends on HeightLayer

    def frequency(self) -> float:
        return 0.08  # slightly higher frequency than height

    def seed_offset(self) -> int:
        return 1234  # different offset to produce independent noise

    def max_layer_value(self) -> float:
        return 1.0  # normalized 0..1 for moisture

    def _generate(
        self,
        coords: list[Coord],
        seed: int,
        radius: float,
        prev_layers: Dict[str, Dict[Coord, float]]
    ) -> Dict[Coord, float]:
        """
        Generate moisture values for each coordinate.
        Moisture is influenced by height: higher terrain tends to be drier.
        Returns a dict mapping (q,r) coordinates to float 0..1.
        """
        # Assert dependent layers are present (wrapper in BaseLayer handles this)
        height_layer = prev_layers["height"]

        simplex = OpenSimplex(seed + self.seed_offset())
        freq = self.frequency() / radius
        result: Dict[Coord, float] = {}

        for q, r in coords:
            n = simplex.noise2(q * freq, r * freq)
            n = (n + 1) / 2  # normalize 0..1

            # radial falloff for island edges
            distance = (abs(q) + abs(r) + abs(-q-r)) / 2
            falloff = max(0, 1 - (distance / radius))

            # combine noise with height influence
            height = height_layer[(q, r)] / 600.0  # normalize height 0..1 using HeightLayer max value
            height_factor = max(0, 1 - height)     # higher = drier

            moisture = (n * 0.7 + height_factor * 0.3) * falloff
            result[(q, r)] = min(max(moisture, 0.0), 1.0)  # clamp 0..1

        return result