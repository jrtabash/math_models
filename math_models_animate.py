import math_models_util as util
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Animate:
    def __init__(self, x, ys, labels=None, colors=None, preFtn=None):
        self.x = x
        self.ys = ys
        self.labels = labels
        self.colors = colors
        self.preFtn = preFtn
        self.lines = None

    def reset(self):
        self.lines = None

    def run(self, interval=20):
        if self.lines is not None:
            return

        gridSize = util.XYsMinMaxRange(self.x, self.ys)

        fig = plt.figure()
        ax = plt.axes(xlim=gridSize.xRange(), ylim=gridSize.yRange())

        if callable(self.preFtn):
            self.preFtn()

        self.lines = [ax.plot([], [], c, label=l)[0] for c, l in zip(self.colors, self.labels)]

        FuncAnimation(fig,
                      lambda i: self.updateLines_(i),
                      init_func = lambda: self.initLines_(),
                      frames=len(self.x),
                      interval=interval,
                      blit=True,
                      repeat=False)

    def initLines_(self):
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def updateLines_(self, i):
        for line, y in zip(self.lines, self.ys):
            line.set_data(self.x[:i], y[:i])
        return self.lines
