# layers/sea.py
from core.base_layer import BaseLayer, AnyBaseLayerType
from core.types import CoordType


SEA_LEVEL = 200.0


class SeaLayer(BaseLayer[bool]):
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

        for coord in coords:
            self._set_value_at(coord, height_layer.get_value_at(coord) <= SEA_LEVEL)
