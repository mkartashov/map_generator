# engine/runner.py
from core.types import Coord, LayerFloatValues
from layers.height import HeightLayer
from layers.moisture import MoistureLayer

LayerClass = HeightLayer | MoistureLayer  # for type hints, extendable


def get_layer_sequence() -> list[LayerClass]:
    """
    Hardcoded topological order for now.
    Later replace with actual topo sort based on depends_on().
    """
    return [HeightLayer(), MoistureLayer()]


def run_layers(coords: list[Coord], radius: float, seed: int) -> dict[str, LayerFloatValues]:
    """
    Generate all layers for the grid, respecting dependencies,
    and populate tiles with layer values.
    """

    # Store results of each layer for dependency injection
    prev_layers: dict[str, LayerFloatValues] = {}

    for layer in get_layer_sequence():
        # Generate layer using decoupled, functional pattern
        layer_values = layer.generate(coords, seed, radius, prev_layers)
        prev_layers[layer.name()] = layer_values

    return prev_layers
