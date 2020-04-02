import math_models_population as population
import math_models_util as util

space = population.Dimension(
    'space',
    [util.PiecewiseFtn([50, 100], [0.0, 0.10, 0.20]),
     util.PiecewiseFtn([10, 25, 40], [0.0, -0.15, -0.30, -0.35])])

water = population.Dimension(
    'water',
    [util.PiecewiseFtn([25, 50], [0.0, 0.10, 0.20]),
     util.PiecewiseFtn([10, 20, 30], [-0.05, -0.10, -0.20, -0.25])])

food = population.Dimension(
    'food',
    [util.PiecewiseFtn([70, 100], [0.0, 0.05, 0.10]),
     util.PiecewiseFtn([20, 30, 40], [0.0, -0.05, -0.10, -0.15])])

capacity = population.CarryingCapacity(10000000, [space, water, food])

model = population.LogisticModel(0.02, 4500000, capacity)

t, p = population.solve(model, maxTime=250)
population.plot(model, t, p)
