from .types import Coord, LayerFloatValues


class BaseLayer:

    def name(self) -> str:
        """Used as a key for Tile layers"""
        raise NotImplementedError()

    def depends_on(self) -> list[str]:
        """Used for topological sort"""
        raise NotImplementedError()

    def frequency(self) -> float:
        raise NotImplementedError()

    def seed_offset(self) -> int:
        raise NotImplementedError()

    def max_layer_value(self) -> float:
        """For scaling the actual values, for example, to meters for height"""
        raise NotImplementedError()

    def generate(
        self,
        coords: list[Coord],
        seed: int,
        radius: float,
        prev_layers: dict[str, LayerFloatValues] = {}
    ) -> LayerFloatValues:
        # check dependencies before running actual logic
        missing = [dep for dep in self.depends_on() if dep not in prev_layers]
        if missing:
            raise ValueError(f"Missing dependent layers for {self.name()}: {missing}")
        return self._generate(coords, seed, radius, prev_layers)

    def _generate(
        self,
        coords: list[Coord],
        seed: int,
        radius: float,
        prev_layers: dict[str, LayerFloatValues]
    ) -> LayerFloatValues:
        raise NotImplementedError()

