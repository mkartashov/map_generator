from layers.height import HeightLayer

def test_height_layer_deterministic():
    layer1 = HeightLayer()
    layer2 = HeightLayer()
    coords = [(0, 0), (1, 1), (2, -1)]
    
    # Use a fixed seed
    seed = 42
    layer1.generate(coords, seed=seed, radius=5, layers=[])
    layer2.generate(coords, seed=seed, radius=5, layers=[])

    for coord in coords:
        assert layer1.get_value_at(coord) == layer2.get_value_at(coord)

    assert all(c1 in layer2.get_all_coords() for c1 in layer1.get_all_coords())
    assert all(c2 in layer1.get_all_coords() for c2 in layer2.get_all_coords())
