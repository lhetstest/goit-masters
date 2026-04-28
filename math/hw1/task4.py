import numpy as np

# Дані
t = np.array([1, 2, 3, 4, 5])
y = np.array([22, 28, 37, 45, 53])

# 1. Створення матриці A з стовпцем t та стовпцем одиниць
A = np.vstack([t, np.ones(len(t))]).T  # форма (5,2)

# 2. Знаходження коефіцієнтів k та b (нахил і зсув) методом найменших квадратів
k, b = np.linalg.lstsq(A, y, rcond=None)[0]

print(f"Коефіцієнти прямої тренду: k = {k:.3f}, b = {b:.3f}")

# 3. Прогноз навантаження на 6-ту годину
t_pred = 6
y_pred = k * t_pred + b

print(f"Прогнозоване навантаження на {t_pred}-ту годину: {y_pred:.2f}")

# Опціонально: ручне розв’язання через нормальне рівняння

# Обчислення A.T @ A та A.T @ y
ATA = A.T @ A
ATy = A.T @ y

# Рішення системи рівнянь
x = np.linalg.solve(ATA, ATy)
k_manual, b_manual = x

print(f"\nРучне рішення (нормальне рівняння): k = {k_manual:.3f}, b = {b_manual:.3f}")

# Перевірка збіжності
assert np.allclose([k, b], [k_manual, b_manual]), "Результати не співпадають!"
