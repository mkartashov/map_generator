# layers/height.py
from core.base_layer import BaseLayer
from core.types import CoordType, LayerMapFloatType
from opensimplex import OpenSimplex


class HeightLayer(BaseLayer):
    def name(self) -> str:
        return "height"

    def depends_on(self) -> list[str]:
        return []

    def frequency(self) -> float:
        return 5

    def seed_offset(self) -> int:
        return 0

    def max_layer_value(self) -> float:
        return 600.0  # meters

    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[BaseLayer]
    ) -> LayerMapFloatType:
        """
        Internal pure function to generate height values.
        Returns a dict mapping (q,r) coordinates to normalized height 0..1.
        """
        simplex = OpenSimplex(seed + self.seed_offset())
        freq = self.frequency() / radius  # scale the frequency for proportionality
        result: LayerMapFloatType = {}

        for q, r in coords:
            # Perlin/simplex noise
            n = simplex.noise2(q * freq, r * freq)
            n = (n + 1) / 2

            # optional radial falloff for island shape
            distance = (abs(q) + abs(r) + abs(-q-r)) / 2
            falloff = max(0, 1 - (distance / radius))
            normalised_height = n * falloff

            result[(q, r)] = normalised_height * self.max_layer_value()

        return result
