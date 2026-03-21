from engine.runner import run_layers
from layers.height import HeightLayer
from layers.moisture import MoistureLayer

def test_run_layers_deterministic():
    coords = [(0, 0), (1, -1)]
    seed = 123
    radius = 3

    height1 = HeightLayer()
    height2 = HeightLayer()
    moisture1 = MoistureLayer()
    moisture2 = MoistureLayer()    
    layers1 = run_layers(coords=coords, radius=radius, seed=seed)
    layers2 = run_layers(coords=coords, radius=radius, seed=seed)
    
    for i, first_layer in enumerate(layers1):
        for coord in coords:
            assert first_layer.get_value_at(coord) == layers2[i].get_value_at(coord)

        assert all(c1 in layers2[i].get_all_coords() for c1 in first_layer.get_all_coords())
        assert all(c2 in first_layer.get_all_coords() for c2 in layers2[i].get_all_coords())
