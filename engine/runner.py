# engine/runner.py
from core.types import CoordType
from core.base_layer import AnyBaseLayerType
from layers.height import HeightLayer
from layers.moisture import MoistureLayer
from layers.sea import SeaLayer
from layers.rivers import RiversLayer
from layers.deep_iron import DeepIronLayer
from layers.lakes import LakesLayer
from layers.shallow_iron import ShallowIronLayer


def get_layer_sequence() -> list[AnyBaseLayerType]:
    """
    Hardcoded topological order for now.
    Later replace with actual topo sort based on depends_on().
    """
    return [
        HeightLayer(),
        MoistureLayer(),
        SeaLayer(),
        LakesLayer(),
        DeepIronLayer(),
        RiversLayer(),
        ShallowIronLayer(),
    ]


def run_layers(coords: list[CoordType], radius: float, seed: int) -> list[AnyBaseLayerType]:
    """
    Generate all layers for the grid, respecting dependencies,
    and populate tiles with layer values.
    """
    layers = get_layer_sequence()

    for layer in layers:
        layer.generate(coords, seed, radius, layers)

    # validity check - check that each layer produces the same coords
    for layer in layers:
        assert set(layer.get_all_coords()) == set(coords)
    print("Coords are identical")

    return layers
