# layers/sea.py
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType
from core.config import SEA_LEVEL


class LakesLayer(BaseLayer[bool]):
    """
    Marks ocean hexes based on height map and sea level.
    """
    def name(self) -> str:
        return "lakes"

    def depends_on(self) -> list[str]:
        return ["height", "sea"]

    def frequency(self) -> float:
        raise NotImplementedError()

    def seed_offset(self) -> int:
        raise NotImplementedError()

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
        Generate sea map: True for ocean hexes, False for land.
        """
        height_layer = next(layer for layer in layers if layer.name() == "height")
        sea_layer = next(layer for layer in layers if layer.name() == "sea")

        for coord in coords:
            is_lake = False
            is_below_sea_level = height_layer.get_value_at(coord) <= SEA_LEVEL
            is_sea = sea_layer.get_value_at(coord)
            is_lake = is_below_sea_level and not is_sea
            self._set_value_at(coord, is_lake)
