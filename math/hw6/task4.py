## Дослідження продуктивності


import numpy as np
from scipy.optimize import minimize_scalar
from scipy.integrate import quad
from scipy.interpolate import interp1d

# Функція продуктивності
def P(t):
    return 100 + 40*t - 4*t**2

# 1. Аналіз динаміки продуктивності: похідні в t=2,5,8
t_points = np.array([2,5,8])
dt = 1e-5

# Використаємо чисельне диференціювання (approximate derivative)
def approx_fprime(f, x, epsilon=1e-6):
    return (f(x + epsilon) - f(x - epsilon)) / (2 * epsilon)

for t in t_points:
    dP = approx_fprime(P, t)
    sign = "зростає" if dP > 0 else "спадає"
    print(f"P'({t}) = {dP:.3f}, продуктивність {sign}")

# 2. Знаходимо момент пікової продуктивності
res = minimize_scalar(lambda t: -P(t), bounds=(0,10), method='bounded')
t_star = res.x
P_max = P(t_star)
print(f"Момент пікової продуктивності t* = {t_star:.3f}, P(t*) = {P_max:.3f}")

# 3. Обчислюємо загальний обсяг виробництва (інтеграл)
total_production, _ = quad(P, 0, 10)
print(f"Загальний обсяг виробництва за зміну = {total_production:.3f}")


##  Оптимізація витрат

import numpy as np
from scipy.optimize import minimize

# 1. Визначаємо початкові параметри розв'язанням системи
A = np.array([[2, 1], [1, 3]])
b = np.array([20, 25])
x0, y0 = np.linalg.solve(A, b)
print(f"Початкові параметри: x0 = {x0:.3f}, y0 = {y0:.3f}")

# Функція вартості
def C(params):
    x, y = params
    return x**2 + y**2 - 10*x - 8*y + 50

# 2. Мінімізуємо вартість виробництва
res = minimize(C, [x0, y0], method='BFGS')
x_star, y_star = res.x
C_min = res.fun
print(f"Оптимальні параметри: x* = {x_star:.3f}, y* = {y_star:.3f}")
print(f"Мінімальна вартість виробництва: {C_min:.3f}")

## ФІНАЛ. Обчислюємо загальну вартість

total_cost = total_production * C_min
print(f"Загальна вартість виробництва за зміну: {total_cost:.3f}")
