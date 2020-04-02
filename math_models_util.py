import numpy as np

class PopulationUtilException(Exception):
    pass

class ApplyToCallablesFtn:
    def __init__(self, applyFtn, callables):
        self.applyFtn = applyFtn
        self.callables = callables

    def __call__(self, x):
        return self.applyFtn([f(x) for f in self.callables])

class SumCallablesFtn(ApplyToCallablesFtn):
    def __init__(self, ftns):
        super().__init__(sum, ftns)

class MinCallablesFtn(ApplyToCallablesFtn):
    def __init__(self, ftns):
        super().__init__(min, ftns)

class PiecewiseFtn:
    def __init__(self, limits, values):
        if len(values) != (len(limits) + 1):
            raise(PopulationUtilException(
                "PiecewiseFtn: invalid lengths - values ({}) not equal to limits ({}) + 1".format(
                    len(values),
                    len(limits))))

        self.limits = np.array(limits)
        self.values = np.array(values)
        self.isFunction = callable(values[0])

    def __call__(self, x):
        for i in range(len(self.limits)):
            if self.check_(x, i):
                return self.value_(x, i)
        return self.value_(x, -1)

    def check_(self, x, i):
        if i > 0:
            return x > self.limits[i - 1] and x <= self.limits[i]
        else:
            return x <= self.limits[0]

    def value_(self, x, i):
        return self.values[i](x) if self.isFunction else self.values[i]

class FunctionPoints:
    def __init__(self, ftn, x):
        self.y = ftn(x) if type(ftn) == np.vectorize else np.vectorize(ftn)(x)
        self.yMin = np.min(self.y)
        self.yMax = np.max(self.y)

    def minLine(self):
        return np.full(len(self.y), self.yMin)

    def maxLine(self):
        return np.full(len(self.y), self.yMax)
