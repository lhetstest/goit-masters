import numpy as np

# 1. Вектори користувача та фільмів
u = np.array([8, 2, 5])
v_A = np.array([9, 1, 2])
v_B = np.array([1, 9, 8])
v_C = np.array([7, 2, 6])

# 2. Функція косинусної схожості
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 3. Обчислюємо схожість для кожного фільму
sim_A = cosine_similarity(u, v_A)
sim_B = cosine_similarity(u, v_B)
sim_C = cosine_similarity(u, v_C)

# 4. Вивід коефіцієнтів схожості та вибір найбільш схожого
similarities = {
    'Action Movie (A)': sim_A,
    'Comedy Movie (B)': sim_B,
    'Drama Movie (C)': sim_C
}

for movie, sim in similarities.items():
    print(f"Схожість з {movie}: {sim:.3f}")

best_match = max(similarities, key=similarities.get)
print(f"\nНайбільш підходить користувачу фільм: {best_match} з косинусною схожістю {similarities[best_match]:.3f}")
