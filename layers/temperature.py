import math
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import (
    LATITUDE,
    MAXIMUM_HEIGHT, 
    TEMPERATURE_LAPSE_RATE, 
    TEMPERATURE_NOISE_AMPLITUDE,
    TEMPERATURE_EQUATOR,
    TEMPERATURE_POLE,
)
from opensimplex import OpenSimplex


class TemperatureLayer(BaseLayer[float]):
    def name(self) -> str:
        return "temperature"

    def depends_on(self) -> list[str]:
        return ["height"]

    def frequency(self) -> float:
        return 0.1  # appx every 10 tiles

    def seed_offset(self) -> int:
        return 5678

    def max_layer_value(self) -> float:
        return 1.0

    def _temp_at_latitude(self, latitude: float) -> float:
        lat = math.radians(latitude)
        return (
            TEMPERATURE_EQUATOR - 
            (TEMPERATURE_EQUATOR - TEMPERATURE_POLE) * (math.sin(lat) ** 2)
        )

    def _generate(self, coords, seed, radius, layers):
        height_layer = next(l for l in layers if l.name() == "height")
        max_height = height_layer.max_layer_value()

        simplex = OpenSimplex(seed + self.seed_offset())
        freq = self.frequency()

        for coord in coords:
            # Normalize height → convert to meters
            h_norm = height_layer.get_value_at(coord) / max_height
            height_m = h_norm * MAXIMUM_HEIGHT

            base_temperature = self._temp_at_latitude(LATITUDE)

            # Temperature drop with elevation
            temp_height = base_temperature - (height_m * TEMPERATURE_LAPSE_RATE)

            # Local variation (weather, terrain, etc.)
            n = simplex.noise2(coord[0] * freq, coord[1] * freq)
            temp_noise = n * TEMPERATURE_NOISE_AMPLITUDE

            # Final temperature in °C
            temp_c = temp_height + temp_noise

            self._set_value_at(coord, min(temp_c, TEMPERATURE_EQUATOR))