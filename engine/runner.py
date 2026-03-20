# engine/runner.py
from core.types import CoordType, LayerMapType
from core.base_layer import BaseLayer
from layers.height import HeightLayer
from layers.moisture import MoistureLayer
from layers.sea import SeaLayer
from layers.rivers import RiversLayer


def get_layer_sequence() -> list[BaseLayer]:
    """
    Hardcoded topological order for now.
    Later replace with actual topo sort based on depends_on().
    """
    return [HeightLayer(), MoistureLayer(), SeaLayer(), RiversLayer()]


def run_layers(coords: list[CoordType], radius: float, seed: int) -> dict[str, LayerMapType]:
    """
    Generate all layers for the grid, respecting dependencies,
    and populate tiles with layer values.
    """

    # Store results of each layer for dependency injection
    result_maps: dict[str, LayerMapType] = {}
    layers = get_layer_sequence()

    for layer in layers:
        # Generate layer using decoupled, functional pattern
        layer.generate(coords, seed, radius, layers)
        result_maps[layer.name()] = layer.get_result()

    return result_maps
