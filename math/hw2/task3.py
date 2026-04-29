import math

# Кількість кандидатів
back_end_total = 8
front_end_total = 6
designer_total = 4

# Потрібна кількість від кожної групи
back_end_needed = 2
front_end_needed = 2
designer_needed = 1

# 1. Способи вибору Back-end розробників
back_end_combinations = math.comb(back_end_total, back_end_needed)
print(f"Способів вибрати {back_end_needed} Back-end розробників: {back_end_combinations}")

# 2. Способи вибору Front-end розробників
front_end_combinations = math.comb(front_end_total, front_end_needed)
print(f"Способів вибрати {front_end_needed} Front-end розробників: {front_end_combinations}")

# 3. Способи вибору дизайнера
designer_combinations = math.comb(designer_total, designer_needed)
print(f"Способів вибрати {designer_needed} Дизайнера: {designer_combinations}")

# 4. Загальна кількість унікальних складів команди (правило множення)
total_combinations = back_end_combinations * front_end_combinations * designer_combinations
print(f"\nЗагальна кількість можливих команд: {total_combinations}")
