# layers/sea.py
from core.base_layer import BaseLayer
from core.types import CoordType, LayerMapBoolType


class SeaLayer(BaseLayer):
    """
    Marks ocean hexes based on height map and sea level.
    """
    def name(self) -> str:
        return "sea"

    def depends_on(self) -> list[str]:
        return ["height"]

    def frequency(self) -> float:
        raise NotImplementedError()

    def seed_offset(self) -> int:
        raise NotImplementedError()

    def max_layer_value(self) -> float:
        return 100.0  # meters

    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[BaseLayer]
    ) -> LayerMapBoolType:
        """
        Generate sea map: True for ocean hexes, False for land.
        """
        height = next(layer for layer in layers if layer.name() == "height").get_result()
        sea_level = self.max_layer_value()
        result: LayerMapBoolType = {}

        for coord in coords:
            result[coord] = height[coord] <= sea_level

        return result
