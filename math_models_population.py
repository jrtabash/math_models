import math_models_util as util
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

def plotConstLines_(t, cPoints):
    plt.plot(t, cPoints.minLine(), 'c', label='Min Capacity')
    plt.plot(t, cPoints.maxLine(), 'g', label='Max Capacity')

def plotFinish_(t, cPoints, legend=None):
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
    plotFinish_(t, cPoints, legend='best')

def animate(model, t, p, legend=None):
    cPoints = util.FunctionPoints(model.capacity, t)
    gridSize = util.XYsMinMaxRange(t, [p, cPoints.y])

    fig = plt.figure()
    ax = plt.axes(xlim=gridSize.xRange(), ylim=gridSize.yRange())

    plotConstLines_(t, cPoints)
    cline, = ax.plot([], [], 'r', label='Carrying Capacity')
    pline, = ax.plot([], [], 'b', label='Population')

    def initLines():
        pline.set_data([], [])
        cline.set_data([], [])
        return [pline, cline]

    def updateLines(i):
        x = t[:i]
        py = p[:i]
        cy = cPoints.y[:i]
        pline.set_data(x, py)
        cline.set_data(x, cy)
        return [pline, cline]

    anim = FuncAnimation(fig, updateLines, init_func=initLines, frames=len(t), interval=20, blit=True, repeat=False)
    plotFinish_(t, cPoints, legend=legend)
