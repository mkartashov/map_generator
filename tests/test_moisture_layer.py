from layers.moisture import MoistureLayer
from layers.height import HeightLayer

def test_moisture_layer_deterministic():
    coords = [(0, 0), (1, 1)]
    seed = 99
    
    # generate height layer first (needed by moisture)
    height_layer = HeightLayer()
    height_layer.generate(coords, seed=seed, radius=5, layers=[])
    
    moisture_layer1 = MoistureLayer()
    moisture_layer2 = MoistureLayer()
    moisture_layer1.generate(coords, seed=seed, radius=5, layers=[height_layer])
    moisture_layer2.generate(coords, seed=seed, radius=5, layers=[height_layer])
    
    for coord in coords:
        assert moisture_layer1.get_value_at(coord) == moisture_layer2.get_value_at(coord)
    
    assert all(c1 in moisture_layer2.get_all_coords() for c1 in moisture_layer1.get_all_coords())
    assert all(c2 in moisture_layer1.get_all_coords() for c2 in moisture_layer2.get_all_coords())