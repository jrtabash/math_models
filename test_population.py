import sys
import math_models_population as population
import math_models_util as util

def runPiecewiseChange(animate):
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
    if animate:
        population.animate(model, t, p, legend='lower right')
    else:
        population.plot(model, t, p)

def runContinuousChange(animate):
    space = population.Dimension(
        'space',
        [util.PolyChangeFtn(0.2, 100),
         util.PolyChangeFtn(-0.35, 10)])

    water = population.Dimension(
        'water',
        [util.PolyChangeFtn(0.2, 50),
         util.PolyChangeFtn(-0.25, 20)])

    food = population.Dimension(
        'food',
        [util.PolyChangeFtn(0.10, 100),
         util.PolyChangeFtn(-0.15, 20)])

    capacity = population.CarryingCapacity(10000000, [space, water, food])
    model = population.LogisticModel(0.02, 4500000, capacity)

    t, p = population.solve(model, maxTime=250)
    if animate:
        population.animate(model, t, p, legend='lower right')
    else:
        population.plot(model, t, p)

def run(which, animate):
    if which == 'piece':
        runPiecewiseChange(animate)
    elif which == 'cont':
        runContinuousChange(animate)

if __name__ == '__main__':
    run(sys.argv[1].lower() if len(sys.argv) > 1 else 'piece',
        sys.argv[2].lower() == 'anim' if len(sys.argv) > 2 else False)
