from matplotlib_venn import venn3
import matplotlib.pyplot as plt

# Множини користувачів
rock_fans = {101, 102, 103, 105, 107, 109, 110, 112, 115, 118}
pop_fans = {102, 104, 105, 106, 108, 110, 111, 113, 115, 117}
jazz_fans = {103, 105, 108, 110, 112, 114, 115, 116, 119, 120}

# 1. Загальне охоплення (унікальні користувачі)
all_users = rock_fans | pop_fans | jazz_fans
print(f"Загальне охоплення (унікальні користувачі): {len(all_users)}")

# 2. "Всеїдні меломани" (користувачі, які слухали усі три жанри)
all_three = rock_fans & pop_fans & jazz_fans
print(f"Всеїдні меломани (усі три жанри): {all_three}, кількість: {len(all_three)}")

# 3. "Чисті рокери" (слухали рок, але НЕ слухали поп і джаз)
pure_rockers = rock_fans - (pop_fans | jazz_fans)
print(f"Чисті рокери: {pure_rockers}")

# 4. Користувачі, які слухали рівно два жанри
two_genres = ((rock_fans & pop_fans) | (rock_fans & jazz_fans) | (pop_fans & jazz_fans)) - all_three
print(f"Користувачі, які слухали рівно два жанри: {two_genres}")

# 5. Візуалізація перетинів (Венн-дiаграма)
venn3([rock_fans, pop_fans, jazz_fans], ('Rock', 'Pop', 'Jazz'))
plt.title("Перетини аудиторій за жанрами")
plt.show()
