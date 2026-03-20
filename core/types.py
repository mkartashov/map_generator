CoordType = tuple[int, int]

LayerMapFloatType = dict[CoordType, float]
LayerMapBoolType = dict[CoordType, bool]
LayerMapType = LayerMapFloatType | LayerMapBoolType
