import math_models_epidemic as epidemic
import sys

def runSIR(transmit=3.5, remove=0.5):
    model = epidemic.SIRModel(transmitRate=transmit, removeRate=remove)
    t, sir = epidemic.solve(model, 15, 150)
    epidemic.plot(model, t, sir)

def runSEIR(transmit=3.5, reducedEI=0.0, infect=1.0, remove=0.5):
    model = epidemic.SEIRModel(transmitRate=transmit, reducedEIRate=reducedEI, infectRate=infect, removeRate=remove)
    t, seir = epidemic.solve(model, 20, 200)
    epidemic.plot(model, t, seir)

def run(which, modelArgs):
    if which == 'sir':
        runSIR(*modelArgs)
    elif which == 'seir':
        runSEIR(*modelArgs)

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else 'sir',
        [float(arg) for arg in sys.argv[2:]] if len(sys.argv) > 2 else [])
