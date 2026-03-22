# layers/height.py
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import MAXIMUM_HEIGHT
from opensimplex import OpenSimplex


class HeightLayer(BaseLayer[float]):
    def name(self) -> str:
        return "height"

    def depends_on(self) -> list[str]:
        return []

    def frequency(self) -> float:
        return 4

    def seed_offset(self) -> int:
        return 0

    def max_layer_value(self) -> float:
        return MAXIMUM_HEIGHT

    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[AnyBaseLayerType]
    ) -> None:
        """
        Internal pure function to generate height values.
        Returns a dict mapping (q,r) coordinates to normalized height 0..1.
        """
        simplex = OpenSimplex(seed + self.seed_offset())
        freq = self.frequency() / radius  # scale the frequency for proportionality

        for q, r in coords:
            # Perlin/simplex noise
            n = simplex.noise2(q * freq, r * freq)
            n = (n + 1) / 2

            # optional radial falloff for island shape
            distance = (abs(q) + abs(r) + abs(-q-r)) / 2
            falloff = max(0, 1 - (distance / radius))
            normalised_height = float(n * falloff)

            self._set_value_at((q, r), normalised_height * self.max_layer_value())
