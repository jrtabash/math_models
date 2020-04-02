import math_models_util as util
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

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

class LogisticModel:
    def __init__(self, rate, population0, capacity):
        self.rate = rate               # Growth rate
        self.population0 = population0 # Initial population size
        self.capacity = capacity       # Carrying Capacity function

    def __str__(self):
        return 'LogisticModel({}, {}, {})'.format(self.rate, self.population0, self.capacity.capacity0)

    def __repr__(self):
        return str(self)

    def __call__(self, p, t):
        # P'(t) = rate * p(t) * (1 - p(t) / capacity(t))
        return self.rate * p * (1 - p / self.capacity(t))

def solve(model, maxTime=10):
    t = np.linspace(0, maxTime, maxTime + 1)
    p = odeint(model, model.population0, t)
    return t, p

def plot(model, t, p):
    cPoints = util.FunctionPoints(model.capacity, t)
    plt.plot(t, cPoints.minLine(), 'c', label='Min Capacity')
    plt.plot(t, cPoints.maxLine(), 'g', label='Max Capacity')
    plt.plot(t, cPoints.y, 'r', label='Carrying Capacity')
    plt.plot(t, p, 'b', label='Population')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title('Population Forecast')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()
