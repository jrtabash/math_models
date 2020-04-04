import math_models_util as util
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

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
    def __init__(self, transmitRate=3.5, exposedTransmitRate=0.0, infectRate=1.0, removeRate=0.5, seir0=(0.99, 0.01, 0.0, 0.0)):
        super().__init__(seir0, ['Susceptible', 'Exposed', 'Infected', 'Removed'], ['b', 'c', 'r', 'g'])
        self.transmitRate = transmitRate
        self.exposedTransmitRate = exposedTransmitRate
        self.infectRate = infectRate
        self.removeRate = removeRate

    def __str__(self):
        return 'SEIR: Transmit={} ExposedTransmit={} Infect={} Remove={}'.format(self.transmitRate, self.exposedTransmitRate, self.infectRate, self.removeRate)

    def __repr__(self):
        return 'SIR({}, {}, {}, {})'.format(self.transmitRate, self.exposedTransmitRate, self.infectRate, self.removeRate)

    def __call__(self, seir, t):
        # S'(t) = - transmitRate * S(t) * (I(t) + exposedTransmitRate * E(t))
        # E'(t) = transmitRate * S(t) * (I(t) + exposedTransmitRate * E(t)) - infectRate * E(t)
        # I'(t) = infectRate * E(t) - removeRate * I(t)
        # R'(t) = removeRate * I(t)

        exposed = self.transmitRate * seir[0] * (seir[2] + self.exposedTransmitRate * seir[1])
        infected = self.infectRate * seir[1]
        removed = self.removeRate * seir[2]
        dS = - exposed
        dE = exposed - infected
        dI = infected - removed
        dR = removed
        return dS, dE, dI, dR

def solve(model=SIRModel(), maxTime=10, timeSteps=100):
    t = np.linspace(0, maxTime, timeSteps)
    sir = odeint(model, model.initialConditions, t)
    return t, sir

def plot(model, t, ys):
    labels = model.labels
    colors = model.colors

    for i in range(model.numCompartments):
        plt.plot(t, ys[:, i], color=model.colors[i], label=labels[i])

    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title('{}'.format(model))
    plt.legend(loc='best')
    plt.grid()
    plt.show()
