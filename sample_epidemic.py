import math_models_epidemic as epidemic

model = epidemic.SIRModel(3.5, 0.5, N=1000000, sir0=(990000, 10000, 0))

t, sir = epidemic.solve(model, 20, 200)
epidemic.plot(model, t, sir)
