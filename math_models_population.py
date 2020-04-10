import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import math_models_animate as anim
import math_models_util as util

class Dimension(util.SumCallablesFtn):
    def __init__(self, name, factors):
        super().__init__(factors)
        self.name = name

class CarryingCapacity:
    def __init__(self, capacity0, dimensions):
        self.capacity0 = capacity0
        self.minDimFtn = util.MinCallablesFtn(dimensions)

    def __call__(self, t):
        return (1 + self.minDimFtn(t)) * self.capacity0

    def __str__(self):
        return "CarryingCapacity({})".format(self.capacity0)

    def __repr__(self):
        return str(self)

class LogisticModel:
    def __init__(self, rate, population0, capacity):
        self.rate = rate               # Growth rate
        self.population0 = population0 # Initial population size
        self.capacity = capacity       # Carrying Capacity function

    def __str__(self):
        return 'LogisticModel({}, {}, {})'.format(
            self.rate,
            self.population0,
            self.capacity)

    def __repr__(self):
        return str(self)

    def __call__(self, p, t):
        # P'(t) = rate * p(t) * (1 - p(t) / capacity(t))
        return self.rate * p * (1 - p / self.capacity(t))

def solve(model, maxTime=10):
    t = np.linspace(0, maxTime, maxTime + 1)
    p = odeint(model, model.population0, t)
    return t, p

def plotConstLines_(t, cPoints):
    plt.plot(t, cPoints.minLine(), 'c', label='Min Capacity')
    plt.plot(t, cPoints.maxLine(), 'g', label='Max Capacity')

def plotFinish_(legend=None):
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title('Population Forecast')
    if legend is not None:
        plt.legend(loc=legend)
    plt.grid(True)
    plt.show()

def plot(model, t, p):
    cPoints = util.FunctionPoints(model.capacity, t)
    plotConstLines_(t, cPoints)
    plt.plot(t, cPoints.y, 'r', label='Carrying Capacity')
    plt.plot(t, p, 'b', label='Population')
    plotFinish_(legend='best')

def animate(model, t, p, legend=None):
    cPoints = util.FunctionPoints(model.capacity, t)
    animation = anim.Animate(t,
                             [p, cPoints.y],
                             labels=['Population', 'Carrying Capacity'],
                             colors=['b', 'r'],
                             preFtn=lambda: plotConstLines_(t, cPoints))
    animation.run(interval=20)
    plotFinish_(legend=legend)
