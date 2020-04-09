import math_models_util as util
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CompartmentModelBase:
    def __init__(self, initialConditions, labels, colors):
        self.numCompartments = len(initialConditions)
        self.initialConditions = initialConditions
        self.labels = labels
        self.colors = colors

class SIRModel(CompartmentModelBase):
    def __init__(self, transmitRate=3.5, removeRate=0.5, sir0=(0.99, 0.01, 0.0)):
        super().__init__(sir0, ['Susceptible', 'Infected', 'Removed'], ['b', 'r', 'g'])
        self.transmitRate = transmitRate
        self.removeRate = removeRate

    def __str__(self):
        return 'SIR: Transmit={} Remove={}'.format(self.transmitRate, self.removeRate)

    def __repr__(self):
        return 'SIR({}, {})'.format(self.transmitRate, self.removeRate)

    def __call__(self, sir, t):
        # S'(t) = - transmitRate * S(t) * I(t)
        # I'(t) = transmitRate * S(t) * I(t) - removeRate * I(t)
        # R'(t) = removeRate * I(t)

        transmitted = self.transmitRate * sir[0] * sir[1]
        removed = self.removeRate * sir[1]
        dS = - transmitted
        dI = transmitted - removed
        dR = removed
        return dS, dI, dR

class SEIRModel(CompartmentModelBase):
    def __init__(self, transmitRate=3.5, reducedEIRate=0.0, infectRate=1.0, removeRate=0.5, seir0=(0.99, 0.01, 0.0, 0.0)):
        super().__init__(seir0, ['Susceptible', 'Exposed', 'Infected', 'Removed'], ['b', 'c', 'r', 'g'])
        self.transmitRate = transmitRate
        self.reducedEIRate = reducedEIRate
        self.infectRate = infectRate
        self.removeRate = removeRate

    def __str__(self):
        return 'SEIR: Transmit={} ReduceEI={} Infect={} Remove={}'.format(self.transmitRate, self.reducedEIRate, self.infectRate, self.removeRate)

    def __repr__(self):
        return 'SIR({}, {}, {}, {})'.format(self.transmitRate, self.reducedEIRate, self.infectRate, self.removeRate)

    def __call__(self, seir, t):
        # S'(t) = - transmitRate * S(t) * (I(t) + reducedEIRate * E(t))
        # E'(t) = transmitRate * S(t) * (I(t) + reducedEIRate * E(t)) - infectRate * E(t)
        # I'(t) = infectRate * E(t) - removeRate * I(t)
        # R'(t) = removeRate * I(t)

        transmitted = self.transmitRate * seir[0] * (seir[2] + self.reducedEIRate * seir[1])
        infected = self.infectRate * seir[1]
        removed = self.removeRate * seir[2]
        dS = - transmitted
        dE = transmitted - infected
        dI = infected - removed
        dR = removed
        return dS, dE, dI, dR

def solve(model=SIRModel(), maxTime=10, timeSteps=100):
    t = np.linspace(0, maxTime, timeSteps)
    sir = odeint(model, model.initialConditions, t)
    return t, sir

def plotFinish_(title, legend=None):
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title(title)
    if legend is not None:
        plt.legend(loc=legend)
    plt.grid()
    plt.show()

def plot(model, t, ys):
    labels = model.labels
    colors = model.colors

    for i in range(model.numCompartments):
        plt.plot(t, ys[:, i], color=model.colors[i], label=labels[i])

    plotFinish_('{}'.format(model), legend='best')

def animate(model, t, ys, legend=None):
    labels = model.labels
    colors = model.colors
    gridSize = util.XYsMinMaxRange(t, ys)

    fig = plt.figure()
    ax = plt.axes(xlim=gridSize.xRange(), ylim=gridSize.yRange())

    lines = [ax.plot([], [], c, label=l)[0] for c, l in zip(colors, labels)]

    def initLines():
        for line in lines:
            line.set_data([], [])
        return lines

    def updateLines(i):
        x = t[:i]
        for line, j, in zip(lines, range(model.numCompartments)):
            line.set_data(x, ys[:i, j])
        return lines

    anim = FuncAnimation(fig, updateLines, init_func=initLines, frames=len(t), interval=25, blit=True, repeat=False)
    plotFinish_('{}'.format(model), legend=legend)
