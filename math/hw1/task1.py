import numpy as np

# Початкові матриці
M = np.array([[100, 150, 200],
              [50, 100, 150],
              [0, 50, 100]])

E = np.array([[20, 30, 40],
              [10, 20, 30],
              [5, 10, 15]])

# 1. Зміна контрасту (множення на 0.5)
contrast_changed = 0.5 * M

# 2. Корекція яскравості (додавання 25)
brightness_corrected = M + 25

# 3. Змішування (Blending)
blended = 0.8 * M + 0.2 * E

# Вивід результатів
print("Зміна контрасту:")
print(contrast_changed)
print("\nКорекція яскравості:")
print(brightness_corrected)
print("\nЗмішування (Blending):")
print(blended)
