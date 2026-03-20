# renderer/hex_renderer.py
from typing import Dict
from PIL import Image, ImageDraw
from core.grid import Tile
from core.types import Coord

HEX_SIZE = 20  # pixels per hex, adjust as needed
SEA_LEVEL_ENABLED = True  # hardcoded sea-level cutoff for height layer
SEA_LEVEL_FACTOR = 0.2   # 20% of max_layer_value

def coord_to_pixel(q: int, r: int, size: int = HEX_SIZE) -> tuple[int, int]:
    """Convert axial (q,r) to pixel coordinates for flat-top hexes."""
    x = size * 3/2 * q
    y = size * (3**0.5 / 2 * q + (3**0.5) * r)
    return int(x), int(y)

def draw_hex(draw: ImageDraw.Draw, x: int, y: int, size: int, color: tuple[int,int,int]):
    """Draw a flat-top hex centered at (x,y)."""
    import math
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        px = x + size * math.cos(angle_rad)
        py = y + size * math.sin(angle_rad)
        points.append((px, py))
    draw.polygon(points, fill=color, outline=(0,0,0))

def render_layer(tiles: Dict[Coord, Tile], layer_name: str, filename: str):
    """Render a layer to a PNG image with normalization and optional sea level."""
    # Extract layer values
    values = [tile.layers[layer_name] for tile in tiles.values()]
    min_val = min(values)
    max_val = max(values)

    # Special handling for height layer sea-level cutoff
    if layer_name == "height" and SEA_LEVEL_ENABLED:
        max_layer_val = max(values)
        sea_level = SEA_LEVEL_FACTOR * max_layer_val
    else:
        sea_level = None

    # Determine image size
    coords = tiles.keys()
    min_q = min(q for q, r in coords)
    max_q = max(q for q, r in coords)
    min_r = min(r for q, r in coords)
    max_r = max(r for q, r in coords)

    img_width = int(HEX_SIZE * 3/2 * (max_q - min_q + 3))
    img_height = int(HEX_SIZE * (3**0.5) * (max_r - min_r + 3))
    image = Image.new("RGB", (img_width, img_height), (255,255,255))
    draw = ImageDraw.Draw(image)

    # Draw each hex
    for coord, tile in tiles.items():
        q, r = coord
        x, y = coord_to_pixel(q - min_q, r - min_r)

        val = tile.layers[layer_name]

        # Apply sea-level cutoff if enabled
        if sea_level is not None and val < sea_level:
            gray = 0
        else:
            # normalize to 0..255
            normalized = (val - min_val) / max(max_val - min_val, 1e-6)
            gray = int(normalized * 255)
        color = (gray, gray, gray)

        draw_hex(draw, x, y, HEX_SIZE, color)

    image.save(filename)