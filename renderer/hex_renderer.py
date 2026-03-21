# renderer/hex_renderer.py
import math
from PIL import Image, ImageDraw

from core.base_layer import AnyBaseLayerType

HEX_SIZE = 20  # pixels per hex
SEA_LEVEL_ENABLED = True
SEA_LEVEL_FACTOR = 0.3


def coord_to_pixel(q: int, r: int, size: int = HEX_SIZE) -> tuple[float, float]:
    """Convert axial (q,r) to pixel coordinates for flat-top hexes."""
    x = size * 3/2 * q
    y = size * (3**0.5) * (r + q / 2)  # stagger for flat-top
    return x, y


def draw_hex(draw: ImageDraw.ImageDraw, x: float, y: float, size: int, color: tuple[int, int, int]) -> None:
    """Draw a flat-top hex centered at (x,y)."""
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        px = x + size * math.cos(angle_rad)
        py = y + size * math.sin(angle_rad)
        points.append((px, py))
    draw.polygon(points, fill=color, outline=(0, 0, 0))


def render_layer(layer: AnyBaseLayerType) -> None:
    """Render a layer to a PNG image with normalization and optional sea level."""

    filename = layer.name() + '.png'

    # Extract values
    min_val, max_val = [float(x) for x in layer.get_range()]

    # Precompute all pixel positions
    pixel_coords = {}
    for (q, r) in layer.get_all_coords():
        x, y = coord_to_pixel(q, r)
        pixel_coords[(q, r)] = (x, y)

    # Determine image bounds
    xs = [x for x, y in pixel_coords.values()]
    ys = [y for x, y in pixel_coords.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    padding = HEX_SIZE  # optional padding around edges
    img_width = int(max_x - min_x + 2 * padding)
    img_height = int(max_y - min_y + 2 * padding)

    # Create image
    image = Image.new("RGB", (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw hexes
    for coord in layer.get_all_coords():
        value = float(layer.get_value_at(coord))
        x, y = pixel_coords[coord]

        # Shift so min_x/min_y is at padding
        x_shifted = x - min_x + padding
        y_shifted = y - min_y + padding

        normalized = (value - min_val) / max(max_val - min_val, 1e-6)
        gray = int(normalized * 255)
        color = (gray, gray, gray)

        draw_hex(draw, x_shifted, y_shifted, HEX_SIZE, color)

    image.save(filename)
