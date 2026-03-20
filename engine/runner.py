# engine/runner.py
from typing import Dict, List
from core.types import Coord
from core.grid import HexGrid, Tile
from layers.height import HeightLayer
from layers.moisture import MoistureLayer

LayerClass = HeightLayer | MoistureLayer  # for type hints, extendable

def get_layer_sequence() -> List[LayerClass]:
    """
    Hardcoded topological order for now.
    Later replace with actual topo sort based on depends_on().
    """
    return [HeightLayer(), MoistureLayer()]


def run_layers(coords: list[Coord], radius, seed: int = 42) -> Dict[Coord, Tile]:
    """
    Generate all layers for the grid, respecting dependencies,
    and populate tiles with layer values.
    """


    # Store results of each layer for dependency injection
    prev_layers: Dict[str, Dict[Coord, float]] = {}

    for layer in get_layer_sequence():
        # Generate layer using decoupled, functional pattern
        layer_values = layer.generate(coords, seed, radius, prev_layers)
        prev_layers[layer.name()] = layer_values

        # # Apply layer values to tiles
        # for coord, value in layer_values.items():
        #     tiles[coord].layers[layer.name()] = value

    return prev_layers