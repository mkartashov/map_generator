# cli.py
import argparse
from core.grid import generate_all_coordinates
from engine.runner import run_layers
from renderer.hex_renderer import render_layer

def main():
    parser = argparse.ArgumentParser(description="Generate a hex map with procedural layers")
    parser.add_argument("radius", type=int, help="Radius of the hex map (in hexes)")
    args = parser.parse_args()

    radius = args.radius
    print(f"Generating hex grid with radius {radius}...")

    coords = generate_all_coordinates(radius)

    # Generate layers
    print("Running layers...")
    layers = run_layers(coords, radius, seed=42)

    for layer_name, layer_values in layers.items():
        print("Rendering " + layer_name + " layer...")
        render_layer(layer_values, layer_name, filename=layer_name+'.png')


    print("Done!")

if __name__ == "__main__":
    main()