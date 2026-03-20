from layers.height import HeightLayer

def test_height_layer_deterministic():
    layer = HeightLayer()
    coords = [(0, 0), (1, 1), (2, -1)]
    
    # Use a fixed seed
    seed = 42
    out1 = layer._generate(coords, seed=seed, radius=5, layers=[])
    out2 = layer._generate(coords, seed=seed, radius=5, layers=[])
    
    # deterministic: outputs must match exactly
    assert out1 == out2
    
    expected_values = {coord: out1[coord] for coord in coords}

    for coord, expected in expected_values.items():
        assert abs(out2[coord] - expected) < 1e-6