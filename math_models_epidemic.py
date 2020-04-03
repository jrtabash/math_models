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
    def __init__(self, alpha=3.5, beta=0.5, sir0=(0.99, 0.01, 0.0)):
        super().__init__(sir0, ['Susceptible', 'Infected', 'Removed'], ['b', 'r', 'g'])
        self.alpha = alpha
        self.beta = beta

    def __str__(self):
        return 'SIR: Alpha={} Beta={}'.format(self.alpha, self.beta)

    def __repr__(self):
        return 'SIR({}, {})'.format(self.alpha, self.beta)

    def __call__(self, sir, t):
        # S'(t) = - alpha * S(t) * I(t)
        # I'(t) = alpha * S(t) * I(t) - beta * I(t)
        # R'(t) = beta * I(t)

        transmitted = self.alpha * sir[0] * sir[1]
        removed = self.beta * sir[1]
        dS = - transmitted
        dI = transmitted - removed
        dR = removed
        return dS, dI, dR

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
