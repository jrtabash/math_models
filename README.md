# Mathematical Models

## Population Growth
Logistic Model

```
p'(t) = rate * p(t) * (1 - p(t) / K(t))
```

* Model defined in [math_models_population.py](math_models_population.py)
* Sample application in [sample_population.ipynb](sample_population.ipynb)

## Epidemiology
SIR Model

```
S'(t) = - transmitRate * S(t) * I(t)
I'(t) = transmitRate * S(t) * I(t) - removeRate * I(t)
R'(t) = removeRate * I(t)
```

SEIR Model

```
S'(t) = - transmitRate * S(t) * (I(t) + reducedEIRate * E(t))
E'(t) = transmitRate * S(t) * (I(t) + reducedEIRate * E(t)) - infectRate * E(t)
I'(t) = infectRate * E(t) - removeRate * I(t)
R'(t) = removeRate * I(t)
```

* Models defined in [math_models_epidemic.py](math_models_epidemic.py)
* Sample applications in [sample_epidemic.ipynb](sample_epidemic.ipynb)
