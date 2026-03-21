from __future__ import annotations
from .types import CoordType
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, TypeAlias


T = TypeVar("T", float, bool)


class BaseLayer(ABC, Generic[T]):

    def __init__(self) -> None:
        self.__result: dict[CoordType, T] = {}
        self.ready = False

    def get_range(self) -> tuple[T, T]:
        if not self.ready:
            raise RuntimeError("This layer is not ready: " + self.__class__.__name__)
        all_values = self.__result.values()
        return min(all_values), max(all_values)

    def get_all_coords(self) -> list[CoordType]:
        if not self.ready:
            raise RuntimeError("This layer is not ready: " + self.__class__.__name__)
        return list(self.__result.keys())

    def get_value_at(self, coord: CoordType) -> T:
        return self.__result[coord]

    def get_neighbours_of(self, coord: CoordType) -> list[CoordType]:
        # flat-top directions
        DIRECTIONS = [
            (+1, 0), (+1, -1), (0, -1),
            (-1, 0), (-1, +1), (0, +1)
        ]
        existing_coords = list(self.__result.keys())
        neighbours = []
        for dq, dr in DIRECTIONS:
            new_coord = (coord[0] + dq, coord[1] + dr)
            if new_coord in existing_coords:
                neighbours.append(new_coord)
        return neighbours

    def _set_value_at(self, coord: CoordType, value: T) -> None:
        self.__result[coord] = value

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
        layers: list[BaseLayer[Any]]
    ) -> None:
        self._generate(coords, seed, radius, layers)
        self.ready = True
        # ready_layers = [x.name() for x in layers if x.ready]
        # missing = [dep for dep in self.depends_on() if dep not in ready_layers]
        # if missing:
        #     raise ValueError(f"Missing dependent layers for {self.name()}: {missing}")
        # self.__result = self._generate(coords, seed, radius, layers)
        # self.ready = True
        # return

    @abstractmethod
    def _generate(
        self,
        coords: list[CoordType],
        seed: int,
        radius: float,
        layers: list[BaseLayer[Any]]
    ) -> None:
        raise NotImplementedError()


AnyBaseLayerType: TypeAlias = BaseLayer[Any]
