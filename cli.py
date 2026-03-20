# cli.py
import argparse
from engine.hex_generator import generate_hex_grid
from engine.runner import run_layers
from renderer.hex_renderer import render_layer

def main():
    parser = argparse.ArgumentParser(description="Generate a hex map with procedural layers")
    parser.add_argument("radius", type=int, help="Radius of the hex map (in hexes)")
    args = parser.parse_args()

    radius = args.radius
    print(f"Generating hex grid with radius {radius}...")
    
    # Create the grid
    grid = generate_hex_grid(radius)
    
    # Generate layers
    print("Running layers...")
    tiles = run_layers(grid, seed=42)
    
    # Render layers
    print("Rendering Height Layer...")
    render_layer(tiles, layer_name="height", filename="height.png")
    print("Rendering Moisture Layer...")
    render_layer(tiles, layer_name="moisture", filename="moisture.png")
    
    print("Done! Check height.png and moisture.png.")

if __name__ == "__main__":
    main()