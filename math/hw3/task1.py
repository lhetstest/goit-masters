import numpy as np

def f(t):
    return 1000 * t * np.exp(-0.2 * t)

def numerical_derivative(func, x, h=1e-5):
    return (func(x + h) - func(x - h)) / (2 * h)

points = [2, 6, 10]

for t in points:
    dfdt = numerical_derivative(f, t)
    print(f"f'({t}) ≈ {dfdt:.2f}")
