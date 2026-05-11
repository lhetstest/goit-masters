##  Розв’язок задачі програмно

import numpy as np
from scipy.optimize import linprog

# Коєфіцієнти для мінімізації -P(x,y)
c = [-500, -800]

# Матриця коефіцієнтів обмежень (ліва частина)
A = [
    [2, 4],
    [3, 2]
]

# Права частина обмежень
b = [120, 90]

# Межі змінних (x,y >= 0)
x_bounds = (0, None)
y_bounds = (0, None)

res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds])

print("Оптимальна кількість стільців:", res.x[0])
print("Оптимальна кількість столів:", res.x[1])
print("Максимальний прибуток:", -res.fun)



## Аналіз використання ресурсів

wood_used = 2*res.x[0] + 4*res.x[1]
time_used = 3*res.x[0] + 2*res.x[1]

wood_left = 120 - wood_used
time_left = 90 - time_used

print(f"Використано деревини: {wood_used} (залишок: {wood_left})")
print(f"Використано робочого часу: {time_used} (залишок: {time_left})")
