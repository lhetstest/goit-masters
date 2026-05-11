### Знайдемо оптимум чисельно (Python)

import numpy as np
from scipy.optimize import minimize

def f(v):
    x, y = v
    return x**2 + x*y + y**2 - 6*x - 9*y + 20

start = (0, 0)
res = minimize(f, start, method='BFGS')

print(f"Оптимум чисельно: {res.x}")
print(f"Значення функції в оптимумі: {res.fun}")


### 4. Перевіримо стійкість розв’язку

starting_points = [(0, 0), (10, 10), (-5, 15)]

for sp in starting_points:
    res = minimize(f, sp, method='BFGS')
    print(f"Старт: {sp} -> Оптимум: {res.x}, Значення: {res.fun}")

# Всі запуски мають сходитися до точки (1,4) зі значенням функції:
# f(1,4) = 1^2 + 1 \cdot 4 + 4^2 - 6 \cdot 1 - 9 \cdot 4 + 20 = 1 + 4 + 16 - 6 - 36 + 20 = -1

