# cli.py
import argparse
from core.grid import generate_all_coordinates
from engine.runner import run_layers
from renderer.hex_renderer import render_layer


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate a hex map with procedural layers")

    parser.add_argument(
        "--radius",
        type=int,
        default=40,
        help="Radius of the hex map (in hexes, default 40)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for map generation (default 42)"
    )

    args = parser.parse_args()
    return args 

def main():
    args = parse_arguments()
    radius = args.radius
    seed = args.seed

    print(f"Generating hex grid with radius {radius} and seed {seed}...")

    coords = generate_all_coordinates(radius)

    # Generate layers
    print("Running layers...")
    layers = run_layers(coords, radius, seed=seed)

    for layer in layers:
        print(f"Rendering {layer.name()} layer...")
        render_layer(layer)

    print("Done!")

if __name__ == "__main__":
    main()