from layers.moisture import MoistureLayer
from layers.height import HeightLayer

def test_moisture_layer_deterministic():
    coords = [(0, 0), (1, 1)]
    seed = 99
    
    # generate height layer first (needed by moisture)
    height_layer = HeightLayer()
    height_values = height_layer._generate(coords, seed=seed, radius=5, prev_layers={})
    
    moisture_layer = MoistureLayer()
    out1 = moisture_layer._generate(coords, seed=seed, radius=5, prev_layers={'height': height_values})
    out2 = moisture_layer._generate(coords, seed=seed, radius=5, prev_layers={'height': height_values})
    
    assert out1 == out2
    
    expected_values = {coord: out1[coord] for coord in coords}

    for coord, expected in expected_values.items():
        assert abs(out2[coord] - expected) < 1e-6