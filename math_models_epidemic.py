import math_models_util as util
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class SIRModel:
    # alpha := transmit rate
    #  beta := remove rate
    #     N := population size
    #  sir0 := initial susceptible, infected and removed
    def __init__(self, alpha=3.5, beta=0.5, N=1, sir0=(0.99, 0.01, 0.0)):
        self.N = N
        self.alpha = alpha
        self.beta = beta
        self.sir0 = sir0

    def __str__(self):
        return 'SIR: Alpha={} Beta={} N={}'.format(self.alpha, self.beta, self.N)

    def __repr__(self):
        return 'SIR({}, {}, N={})'.format(self.alpha, self.beta, self.N)

    def __call__(self, sir, t):
        # S'(t) = - alpha * S * I / N
        # I'(t) = alpha * S * I / N - beta * I
        # R'(t) = beta * I

        transmitted = self.alpha * sir[0] * sir[1] / self.N
        removed = self.beta * sir[1]
        dS = - transmitted
        dI = transmitted - removed
        dR = removed
        return dS, dI, dR

def solve(model=SIRModel(), maxTime=10, timeSteps=100):
    t = np.linspace(0, maxTime, timeSteps)
    sir = odeint(model, model.sir0, t)
    return t, sir

def plot(model, t, sir):
    plt.plot(t, sir[:, 0], 'b', label='Susceptible')
    plt.plot(t, sir[:, 1], 'r', label='Infected')
    plt.plot(t, sir[:, 2], 'g', label='Removed')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title('{}'.format(model))
    plt.legend(loc='best')
    plt.grid()
    plt.show()
