# layers/moisture.py
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import CLIMATE_SCALE, CLIMATE_BIAS
from opensimplex import OpenSimplex


class MoistureLayer(BaseLayer[float]):
    def name(self) -> str:
        return "moisture"

    def depends_on(self) -> list[str]:
        return ["height"]  # Moisture depends on HeightLayer

    def frequency(self) -> float:
        return 4  # slightly higher frequency than height

    def seed_offset(self) -> int:
        return 1234  # different offset to produce independent noise

    def max_layer_value(self) -> float:
        return 1.0

    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[AnyBaseLayerType]
    ) -> None:
        """
        Generate moisture values for each coordinate.
        Moisture is influenced by height: higher terrain tends to be drier.
        Returns a dict mapping (q,r) coordinates to float 0..1.
        """
        height_layer = next(layer for layer in layers if layer.name() == "height")
        _, max_value = height_layer.get_range()

        simplex = OpenSimplex(seed + self.seed_offset())
        freq = self.frequency() / radius

        for coord in coords:
            # Height contribution normalized [0,1]
            h = height_layer.get_value_at(coord) / max_value

            # Noise contribution in [0,1]
            n = (simplex.noise2(coord[0] * freq, coord[1] * freq) + 1) / 2.0

            # Weighted blend: 70% noise, 30% height
            base = float(0.7 * n + 0.3 * h)
            moisture = base * CLIMATE_SCALE + CLIMATE_BIAS

            # Clamp to [0,max moisture]
            moisture = min(max(moisture, 0.0), self.max_layer_value())
            self._set_value_at(coord, moisture)
