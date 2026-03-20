import math
from renderer.hex_renderer import coord_to_pixel

def test_coord_to_pixel_consistent():
    # two different coords should be distinct pixel positions
    p1 = coord_to_pixel(0, 0)
    p2 = coord_to_pixel(1, 0)
    assert p1 != p2

    # check basic ratio: x increases roughly by 1.5x size
    # so p2.x > p1.x
    assert p2[0] > p1[0]