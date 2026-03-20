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
        return 4  # slightly higher frequency than height

    def seed_offset(self) -> int:
        return 1234  # different offset to produce independent noise

    def max_layer_value(self) -> float:
        return 100  # normalized 0..1 for moisture

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
        height_layer = prev_layers["height"]

        simplex = OpenSimplex(seed + self.seed_offset())
        freq = self.frequency() / radius
        result: Dict[Coord, float] = {}

        for coord in coords:
            # Height contribution normalized [0,1]
            h = height_layer[coord] / max(height_layer.values())

            # Noise contribution in [0,1]
            n = (simplex.noise2(coord[0] * freq, coord[1] * freq) + 1) / 2.0

            # Weighted blend: 70% noise, 30% height
            moisture = 0.7 * n + 0.3 * h

            # Clamp to [0,1]
            moisture = min(max(moisture, 0.0), 1.0)

            result[coord] = moisture

        return result
