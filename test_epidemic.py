import math_models_epidemic as epidemic
import sys

def runSIR(animate, transmit=3.5, remove=0.5):
    model = epidemic.SIRModel(transmitRate=transmit, removeRate=remove)
    t, sir = epidemic.solve(model, 15, 150)
    if animate:
        epidemic.animate(model, t, sir, legend='center right')
    else:
        epidemic.plot(model, t, sir)

def runSEIR(animate, transmit=3.5, reducedEI=0.0, infect=1.0, remove=0.5):
    model = epidemic.SEIRModel(transmitRate=transmit, reducedEIRate=reducedEI, infectRate=infect, removeRate=remove)
    t, seir = epidemic.solve(model, 20, 200)
    if animate:
        epidemic.animate(model, t, seir, legend='center right')
    else:
        epidemic.plot(model, t, seir)

def run(which, animate, modelArgs):
    if which == 'sir':
        runSIR(animate, *modelArgs)
    elif which == 'seir':
        runSEIR(animate, *modelArgs)

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else 'sir',
        sys.argv[2].lower() == 'anim' if len(sys.argv) > 2 else False,
        [float(arg) for arg in sys.argv[3:]] if len(sys.argv) > 3 else [])
