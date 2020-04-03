import math_models_util as util
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class ModelBase:
    def __init__(self, labels, colors):
        self.numCompartments = len(labels)
        self.labels = labels
        self.colors = colors

class SIRModel(ModelBase):
    def __init__(self, transmitRate=3.5, removeRate=0.5, sir0=(0.99, 0.01, 0.0)):
        super().__init__(['Susceptible', 'Infected', 'Removed'], ['b', 'r', 'g'])
        self.transmitRate = transmitRate
        self.removeRate = removeRate
        self.sir0 = sir0

    def __str__(self):
        return 'SIR: TransmitRate={} RemoveRate={}'.format(self.transmitRate, self.removeRate)

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

def solve(model=SIRModel(), maxTime=10, timeSteps=100):
    t = np.linspace(0, maxTime, timeSteps)
    sir = odeint(model, model.sir0, t)
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
