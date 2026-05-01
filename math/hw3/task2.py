'''
# Adaptive Learning Model

1. Реалізація моделі
Функція правої частини рівняння:

The differential equation describing learning is:

$$
\frac{dK}{dt} = r (M - K)
$$

where:
- \\(K(t)\\) — knowledge level at time \\(t\\)
- \\(M = 100\\) — max knowledge level
- \\(r = 0.15\\) — learning rate

'''

def learning_rate(t, K, r=0.15, M=100):
    return r * (M - K)

'''
2. Чисельне розв’язання рівняння
Використаємо scipy.integrate.solve_ivp для розв’язання
на проміжку [0, 30] днів з початковою умовою K(0).
'''

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def learning_rate(t, K, r=0.15, M=100):
    return r * (M - K)

def solve_learning(K0):
    t_span = (0, 30)
    t_eval = np.linspace(0, 30, 300)
    sol = solve_ivp(learning_rate, t_span, [K0], args=(0.15, 100), t_eval=t_eval)
    return sol.t, sol.y[0]

# Приклад для K0=10
t, K = solve_learning(10)

plt.plot(t, K)
plt.xlabel('Час (дні)')
plt.ylabel('Рівень знань (%)')
plt.title('Навчання студента при K0=10')
plt.grid()
plt.show()



'''
3. Вплив початкового рівня
Обчислимо час досягнення 90% знань для трьох значень K(0)=5,10,20
'''

def time_to_reach_90(K0):
    t, K = solve_learning(K0)
    idx = np.where(K >= 90)[0]
    if idx.size > 0:
        return t[idx[0]]
    else:
        return None  # не досягається за 30 днів

initial_levels = [5, 10, 20]
for K0 in initial_levels:
    time_90 = time_to_reach_90(K0)
    print(f"Початковий рівень: {K0}, час до 90% знань: {time_90:.2f} днів")


'''
Висновок
Чим вищий початковий рівень знань, тим швидше студент досягає 90%.
Початкова підготовка суттєво впливає на швидкість оволодіння матеріалом — вона економить час навчання.
'''
