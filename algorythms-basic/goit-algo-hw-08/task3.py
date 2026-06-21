import heapq
from typing import List, Tuple


def min_cost_cable_merge(cables: List[float]) -> Tuple[float, List[Tuple[float, float, float]]]:
    """
    Знаходить мінімальні витрати на з'єднання всіх кабелів у один.

    Алгоритм (жадібний підхід із мін-купою):
      1. Поміщаємо всі довжини у мін-купу.
      2. Поки в купі більше одного елемента:
         - Витягуємо два найкоротших кабелі.
         - З'єднуємо їх → витрати = сума двох довжин.
         - Отриманий кабель повертаємо у купу.
      3. Загальні витрати = сума витрат усіх з'єднань.

    Чому саме мін-купа?
      Щоразу обираємо два найменших кабелі — це гарантує,
      що довші кабелі додаються до суми якомога рідше.
      Жадібний вибір тут є глобально оптимальним (аналог алгоритму Хаффмана).

    Складність:
      Час:    O(n log n) — n витягувань і вставок у купу, кожна O(log n).
      Пам'ять: O(n) — розмір купи.

    Args:
        cables: список довжин кабелів (невід'ємні числа)

    Returns:
        Кортеж (загальні_витрати, кроки), де кроки — список
        кортежів (кабель_1, кабель_2, витрати_на_з'єднання)

    Raises:
        ValueError: якщо список порожній або містить від'ємні значення
    """
    if not cables:
        raise ValueError("Список кабелів не може бути порожнім.")
    if any(c < 0 for c in cables):
        raise ValueError("Довжина кабелю не може бути від'ємною.")
    if len(cables) == 1:
        return 0.0, []

    heap: List[float] = cables.copy()
    heapq.heapify(heap)  # O(n) — побудова купи

    total_cost: float = 0.0
    steps: List[Tuple[float, float, float]] = []

    while len(heap) > 1:
        first: float = heapq.heappop(heap)   # найменший
        second: float = heapq.heappop(heap)  # другий найменший

        cost: float = first + second
        total_cost += cost
        steps.append((first, second, cost))

        heapq.heappush(heap, cost)  # новий кабель повертаємо у купу

    return total_cost, steps


# -------------------------------------------------------
# Тест
# -------------------------------------------------------
if __name__ == "__main__":
    # Приклад 1: базовий
    cables = [4, 3, 2, 6]
    print("=" * 45)
    print(f"Кабелі: {cables}")

    total, steps = min_cost_cable_merge(cables)

    print("\nПокроковe з'єднання:")
    for i, (a, b, cost) in enumerate(steps, start=1):
        print(f"  Крок {i}: {a} + {b} = {cost}")

    print(f"\nЗагальні витрати: {total}")

    # Приклад 2: однакові кабелі
    cables2 = [3, 1, 8, 1]
    print("\n" + "=" * 45)
    print(f"Кабелі: {cables2}")

    total2, steps2 = min_cost_cable_merge(cables2)

    print("\nПокрокове з'єднання:")
    for i, (a, b, cost) in enumerate(steps2, start=1):
        print(f"  Крок {i}: {a} + {b} = {cost}")

    print(f"\nЗагальні витрати: {total2}")

    # Приклад 3: один кабель — з'єднання не потрібне
    cables3 = [7.5]
    print("\n" + "=" * 45)
    print(f"Кабелі: {cables3}")
    total3, steps3 = min_cost_cable_merge(cables3)
    print(f"Загальні витрати: {total3}  (з'єднання не потрібне)")
