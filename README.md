# Mathematical Models

## Population Growth
Logistic Model

```
p' = rate * p(t) * (1 - p(t) / K(t))
```

* Model defined in math_models_population.py
* Sample application in sample_population.py

## Epidemiology
SIR Model

```
S' = - transmitRate * S(t) * I(t) / N
I' = (transmitRate * S(t) * I(t) / N) - (removeRate * I(t))
R' = removeRate * I(t)
```

* Model defined in math_models_epidemic.py
* Sample application in sample_epidemic.py
