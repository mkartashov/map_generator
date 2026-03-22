SEA_LEVEL = 300.0  # meters
MAXIMUM_HEIGHT = 1500.0

CLIMATE_BIAS = 0.2  # positive => wetter; negative => dryer
CLIMATE_SCALE = 1.2 # >1 - stronger extremes, more variery; <1 = more samey

# where the probability for deep iron deposit is highest (high hills / low mountains)
DEEP_IRON_MOST_PROBABLE_ELEVATION = 500.0
DEEP_IRON_ELEVATION_SIGMA_FALLOFF = 100.0
# No deep iron deposits below this elevation
DEEP_IRON_LOWEST_ELEVATION = 0.0 
# probability for a deep vein to still randomly appear anywhere
DEEP_IRON_BASELINE_PROBABILITY = 0.02 
DEEP_IRON_PEAK_PROBABILITY = 0.05
DEEP_IRON_ORE_GRADE_MEDIAN = 0.45
DEEP_IRON_ORE_GRADE_VARIABILITY = 0.1
DEEP_IRON_ORE_GRADE_EXTRA_RICH_PROBABILITY = 0.05
DEEP_IRON_ORE_GRADE_EXTRA_RICH_MEDIAN = 0.9
DEEP_IRON_ORE_GRADE_EXTRA_RICH_VARIABILITY = 0.1