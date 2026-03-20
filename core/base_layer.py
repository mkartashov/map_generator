from .types import CoordType, LayerMapType
from abc import ABC, abstractmethod


class BaseLayer(ABC):

    def __init__(self) -> None:
        self.__result: LayerMapType | None = None
        self.ready = False

    def get_result(self) -> LayerMapType:
        if self.__result is None:
            raise RuntimeError("This layer is not ready: " + self.__class__.__name__)
        return self.__result

    @abstractmethod
    def name(self) -> str:
        """Used as a key for Tile layers"""
        raise NotImplementedError()

    @abstractmethod
    def depends_on(self) -> list[str]:
        """Used for topological sort"""
        raise NotImplementedError()

    @abstractmethod
    def frequency(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def seed_offset(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def max_layer_value(self) -> float:
        """For scaling the actual values, for example, to meters for height"""
        raise NotImplementedError()

    def generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list["BaseLayer"]
    ) -> None:
        ready_layers = [x.name() for x in layers if x.ready]
        missing = [dep for dep in self.depends_on() if dep not in ready_layers]
        if missing:
            raise ValueError(f"Missing dependent layers for {self.name()}: {missing}")
        self.__result = self._generate(coords, seed, radius, layers)
        self.ready = True
        return

    @abstractmethod
    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list["BaseLayer"]
    ) -> LayerMapType:
        raise NotImplementedError()
