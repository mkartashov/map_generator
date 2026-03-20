# renderer/hex_renderer.py
from typing import Dict
from PIL import Image, ImageDraw

HEX_SIZE = 20  # pixels per hex
SEA_LEVEL_ENABLED = True
SEA_LEVEL_FACTOR = 0.3

def coord_to_pixel(q: int, r: int, size: int = HEX_SIZE) -> tuple[int, int]:
    """Convert axial (q,r) to pixel coordinates for flat-top hexes."""
    x = size * 3/2 * q
    y = size * (3**0.5) * (r + q / 2)  # stagger for flat-top
    return x, y

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

def render_layer(layer_values: Dict[tuple[int,int], float], layer_name: str, filename: str):
    """Render a layer to a PNG image with normalization and optional sea level."""

    # Extract values
    values = list(layer_values.values())
    min_val = min(values)
    max_val = max(values)

    # Sea-level for height layer
    if layer_name == "height" and SEA_LEVEL_ENABLED:
        sea_level = SEA_LEVEL_FACTOR * max_val
    else:
        sea_level = None

    # Precompute all pixel positions
    pixel_coords = {}
    for (q, r) in layer_values.keys():
        x, y = coord_to_pixel(q, r)
        pixel_coords[(q,r)] = (x, y)

    # Determine image bounds
    xs = [x for x, y in pixel_coords.values()]
    ys = [y for x, y in pixel_coords.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    padding = HEX_SIZE  # optional padding around edges
    img_width = int(max_x - min_x + 2 * padding)
    img_height = int(max_y - min_y + 2 * padding)

    # Create image
    image = Image.new("RGB", (img_width, img_height), (255,255,255))
    draw = ImageDraw.Draw(image)

    # Draw hexes
    for coord, value in layer_values.items():
        x, y = pixel_coords[coord]

        # Shift so min_x/min_y is at padding
        x_shifted = x - min_x + padding
        y_shifted = y - min_y + padding

        # Sea-level coloring
        if sea_level is not None and value < sea_level:
            gray = 0
        else:
            normalized = (value - min_val) / max(max_val - min_val, 1e-6)
            gray = int(normalized * 255)
        color = (gray, gray, gray)

        draw_hex(draw, x_shifted, y_shifted, HEX_SIZE, color)

    image.save(filename)