import math
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import CLIMATE_SCALE, CLIMATE_BIAS, LATITUDE
from opensimplex import OpenSimplex


class MoistureLayer(BaseLayer[float]):
    def name(self) -> str:
        return "moisture"

    def depends_on(self) -> list[str]:
        return ["height"]  # Moisture depends on HeightLayer

    def frequency(self) -> float:
        return 0.05

    def seed_offset(self) -> int:
        return 1234  # different offset to produce independent noise

    def max_layer_value(self) -> float:
        return 1.0

    def _latitude_moisture_bias(self, latitude: float) -> float:
        lat = math.radians(latitude)

        # Wet equator, dry subtropics (~30°), wetter mid-latitudes
        return 0.5 + 0.5 * (
            0.6 * math.cos(2 * lat) +
            0.4 * math.cos(lat)
        )

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
        freq = self.frequency()
        lat_bias = self._latitude_moisture_bias(LATITUDE)

        for coord in coords:
            # Height contribution normalized [0,1]
            h = height_layer.get_value_at(coord) / max_value

            # Noise contribution in [0,1]
            large_noise = (simplex.noise2(coord[0] * freq, coord[1] * freq) + 1) / 2.0
            small_noise = (simplex.noise2(coord[0] * freq * 3, coord[1] * freq * 3) + 1) / 2.0
            n = (large_noise * 0.7 + small_noise * 0.3 + 1) / 2.0

            base = (
                0.4 * n +        # local variation
                0.3 * (1 - h) +  # elevation drying
                0.3 * lat_bias ** 0.8   # global climate
            )
            moisture = base * CLIMATE_SCALE + CLIMATE_BIAS

            # Clamp to [0,max moisture]
            moisture = min(max(moisture, 0.0), self.max_layer_value())
            self._set_value_at(coord, moisture)
