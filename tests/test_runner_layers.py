from engine.runner import run_layers

def test_run_layers_deterministic():
    coords = [(0, 0), (1, -1)]
    seed = 123
    radius = 3
    
    result1 = run_layers(coords=coords, radius=radius, seed=seed)
    result2 = run_layers(coords=coords, radius=radius, seed=seed)
    
    # output must be exactly the same
    assert result1 == result2

    assert all(result1_layer in result2.keys() for result1_layer in result1.keys())
    assert all(result2_layer in result1.keys() for result2_layer in result2.keys())

    for layer_name, layer_values in result1.items():
        for coord, value in result2[layer_name].items():
            assert abs(layer_values[coord] - value) < 1e-6
