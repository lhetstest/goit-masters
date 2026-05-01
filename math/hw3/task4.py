import numpy as np
from scipy.optimize import approx_fprime

def f(vars):
    x, y = vars
    return 0.5*x**2 + 0.3*y**2 + 0.2*x*y + 10*x + 5*y

point = np.array([10.0, 20.0])
epsilon = np.sqrt(np.finfo(float).eps)

grad_numeric = approx_fprime(point, f, epsilon)
print("Чисельний градієнт:", grad_numeric)


def delta_f(x, y, dx, dy):
    dfdx = 1.0*x + 0.2*y + 10
    dfdy = 0.6*y + 0.2*x + 5
    return dfdx*dx + dfdy*dy

approx_change = delta_f(10, 20, 0.5, -0.3)
exact_change = f([10.5, 19.7]) - f([10, 20])

print(f"Наближена зміна Δf ≈ {approx_change:.4f}")
print(f"Точна зміна Δf = {exact_change:.4f}")
