# Дані
employees = ['Анна', 'Богдан', 'Віктор', 'Ганна', 'Дмитро', 'Євген']
contacts = {
    'Анна': ['Богдан', 'Віктор', 'Ганна'],
    'Богдан': ['Анна', 'Віктор', 'Дмитро'],
    'Віктор': ['Анна', 'Богдан', 'Ганна', 'Дмитро'],
    'Ганна': ['Анна', 'Віктор', 'Євген'],
    'Дмитро': ['Богдан', 'Віктор', 'Євген'],
    'Євген': ['Ганна', 'Дмитро']
}

n = len(employees)

# 1. Представлення графа

# а) Матриця суміжності (вкладені списки)
adj_matrix = [[0]*n for _ in range(n)]
index = {name:i for i, name in enumerate(employees)}

for person, neighbors in contacts.items():
    i = index[person]
    for neighbor in neighbors:
        j = index[neighbor]
        adj_matrix[i][j] = 1

print("Матриця суміжності:")
for row in adj_matrix:
    print(row)

# б) Список суміжності (словник)
print("\nСписок суміжності:")
for person in employees:
    print(f"{person}: {contacts[person]}")

# в) Список ребер (список кортежів)
edges = set()
for person, neighbors in contacts.items():
    for neighbor in neighbors:
        # додаємо пару у множину, щоб уникнути дублювань у неорієнтованому графі
        edge = tuple(sorted((person, neighbor)))
        edges.add(edge)

edges = list(edges)
print("\nСписок ребер:")
print(edges)

# 2. Ступені вершин
degrees = {person: len(neighbors) for person, neighbors in contacts.items()}
max_person = max(degrees, key=degrees.get)
min_person = min(degrees, key=degrees.get)

print("\nСтупінь вершин:")
for person, deg in degrees.items():
    print(f"{person}: {deg}")

print(f"\nНайбільш комунікабельний: {max_person} зі ступенем {degrees[max_person]}")
print(f"Найменш комунікабельний: {min_person} зі ступенем {degrees[min_person]}")

# 3. Перевірка теореми про суму степенів
sum_degrees = sum(degrees.values())
num_edges = len(edges)
print(f"\nСума степенів вершин: {sum_degrees}")
print(f"Подвійна кількість ребер: {2 * num_edges}")
print("Перевірка теореми: ", sum_degrees == 2 * num_edges)
