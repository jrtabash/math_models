import math_models_epidemic as epidemic
import sys

def runSIR():
    model = epidemic.SIRModel(transmitRate=3.5, removeRate=0.5)
    t, sir = epidemic.solve(model, 15, 150)
    epidemic.plot(model, t, sir)

def runSEIR():
    model = epidemic.SEIRModel(exposeRate=3.5, infectRate=1.0, removeRate=0.5)
    t, seir = epidemic.solve(model, 20, 200)
    epidemic.plot(model, t, seir)

def run(which):
    if which == 'sir':
        runSIR()
    elif which == 'seir':
        runSEIR()

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else 'sir')
