"""
Завдання 6 — Жадібні алгоритми та динамічне програмування
===========================================================
Задача: вибрати страви з максимальною сумарною калорійністю,
не перевищуючи бюджет.

Реалізовано два підходи:
  1. greedy_algorithm   — жадібний алгоритм (сортування за співвідношенням
                          калорії/вартість, вибір найвигідніших страв)
  2. dynamic_programming — динамічне програмування (точний оптимум,
                          класична задача про рюкзак з цілими вагами)

Запуск:
    python task6.py
    python task6.py --budget 100
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import TypedDict


# ── Типи ────────────────────────────────────────────────────────────────────

class FoodItem(TypedDict):
    """Структура одного запису у словнику страв."""
    cost:     int   # вартість страви (грн)
    calories: int   # калорійність страви (ккал)


# Словник страв: назва → {cost, calories}
FoodMenu = dict[str, FoodItem]


@dataclass(frozen=True)
class SelectionResult:
    """Результат вибору страв будь-яким алгоритмом."""
    chosen_items: list[str]   # назви обраних страв
    total_cost:   int         # загальна витрачена сума
    total_calories: int       # загальна калорійність


# ── Вхідні дані ───────────────────────────────────────────────────────────────

ITEMS: FoodMenu = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}


# ── Жадібний алгоритм ─────────────────────────────────────────────────────────

def greedy_algorithm(menu: FoodMenu, budget: int) -> SelectionResult:
    """
    Жадібний алгоритм вибору страв.

    Стратегія:
        Сортуємо страви за спаданням питомої калорійності
        (calories / cost) і жадібно беремо кожну страву,
        якщо вона вписується у залишок бюджету.

    Переваги: простота, швидкість O(n log n).
    Недоліки: не гарантує глобального оптимуму —
              може пропустити вигідніші комбінації дешевших страв.

    Параметри:
        menu   — словник страв
        budget — максимально доступна сума (грн)

    Повертає:
        SelectionResult з обраними стравами, витратами і калорійністю.
    """
    # Обчислюємо питому калорійність (ккал на 1 грн) для кожної страви
    # і сортуємо за спаданням — найвигідніші страви ідуть першими
    sorted_items: list[tuple[str, FoodItem]] = sorted(
        menu.items(),
        key=lambda item: item[1]["calories"] / item[1]["cost"],
        reverse=True,
    )

    chosen:          list[str] = []
    remaining_budget: int      = budget
    total_calories:   int      = 0

    for name, data in sorted_items:
        # Якщо страва вписується у залишок бюджету — беремо її
        if data["cost"] <= remaining_budget:
            chosen.append(name)
            remaining_budget -= data["cost"]
            total_calories   += data["calories"]

    return SelectionResult(
        chosen_items    = chosen,
        total_cost      = budget - remaining_budget,
        total_calories  = total_calories,
    )


# ── Динамічне програмування ───────────────────────────────────────────────────

def dynamic_programming(menu: FoodMenu, budget: int) -> SelectionResult:
    """
    Алгоритм динамічного програмування (задача про рюкзак 0/1).

    Ідея:
        Будуємо таблицю dp розміром (n+1) × (budget+1), де
        dp[i][w] = максимальна калорійність, яку можна отримати,
        розглядаючи перші i страв при бюджеті w.

    Рекурентне співвідношення:
        dp[i][w] = dp[i-1][w]                               якщо cost[i] > w
        dp[i][w] = max(dp[i-1][w],
                       dp[i-1][w - cost[i]] + calories[i])  інакше

    Відновлення відповіді:
        Йдемо по таблиці у зворотному напрямку (від n до 1),
        визначаючи, чи була взята кожна страва.

    Складність: O(n × budget) часу та пам'яті.
    Гарантує точний оптимум.

    Параметри:
        menu   — словник страв
        budget — максимально доступна сума (грн)

    Повертає:
        SelectionResult з оптимальним набором страв.
    """
    names:     list[str] = list(menu.keys())
    costs:     list[int] = [menu[n]["cost"]     for n in names]
    calories:  list[int] = [menu[n]["calories"] for n in names]
    n: int = len(names)

    # ── Побудова таблиці DP ──────────────────────────────────
    # dp[i][w] — найкраща калорійність для перших i страв і бюджету w
    # Використовуємо список списків (рядок 0 — базовий випадок, всі нулі)
    dp: list[list[int]] = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item_cost     = costs[i - 1]      # вартість i-ї страви (1-індексація)
        item_calories = calories[i - 1]   # калорійність i-ї страви

        for w in range(budget + 1):
            # Варіант 1: не беремо i-ту страву
            dp[i][w] = dp[i - 1][w]

            # Варіант 2: беремо i-ту страву (якщо вона вміщується у бюджет w)
            if item_cost <= w:
                with_item = dp[i - 1][w - item_cost] + item_calories
                if with_item > dp[i][w]:
                    dp[i][w] = with_item

    # ── Відновлення набору страв ──────────────────────────────
    # Йдемо від dp[n][budget] назад і перевіряємо, чи змінилось значення
    # порівняно з рядком вище — якщо так, страва була взята
    chosen:     list[str] = []
    w: int = budget

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            # i-та страва увійшла до оптимального рішення
            chosen.append(names[i - 1])
            w -= costs[i - 1]

    chosen.reverse()   # відновлюємо порядок (від першої до останньої)

    total_cost     = budget - w
    total_calories = dp[n][budget]

    return SelectionResult(
        chosen_items   = chosen,
        total_cost     = total_cost,
        total_calories = total_calories,
    )


# ── Виведення результатів ─────────────────────────────────────────────────────

def print_result(label: str, result: SelectionResult, menu: FoodMenu) -> None:
    """Красиво виводить результат вибору страв."""
    width = 52
    print(f"\n{'─' * width}")
    print(f"  {label}")
    print(f"{'─' * width}")
    print(f"  {'Страва':<14} {'Вартість':>9} {'Калорії':>9}  {'ккал/грн':>9}")
    print(f"  {'─'*14} {'─'*9} {'─'*9}  {'─'*9}")

    for name in result.chosen_items:
        c = menu[name]["cost"]
        k = menu[name]["calories"]
        ratio = k / c
        print(f"  {name:<14} {c:>8} ₴ {k:>8} ккал  {ratio:>8.2f}")

    print(f"  {'─'*14} {'─'*9} {'─'*9}")
    print(f"  {'РАЗОМ':<14} {result.total_cost:>8} ₴ {result.total_calories:>8} ккал")
    print(f"{'─' * width}")


# ── Точка входу ──────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Вибір страв у межах бюджету")
    parser.add_argument(
        "--budget", type=int, default=100,
        metavar="N", help="Бюджет у гривнях (за замовчуванням: 100)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    budget: int = args.budget

    print("╔══════════════════════════════════════════════════════╗")
    print("║   Жадібний алгоритм vs Динамічне програмування       ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"\n  Бюджет: {budget} ₴")
    print("\n  Меню:")
    print(f"  {'Страва':<14} {'Вартість':>9} {'Калорії':>9}  {'ккал/грн':>9}")
    print(f"  {'─'*14} {'─'*9} {'─'*9}  {'─'*9}")
    for name, data in ITEMS.items():
        ratio = data["calories"] / data["cost"]
        print(f"  {name:<14} {data['cost']:>8} ₴ {data['calories']:>8} ккал  {ratio:>8.2f}")

    greedy_result = greedy_algorithm(ITEMS, budget)
    dp_result     = dynamic_programming(ITEMS, budget)

    print_result("ЖАДІБНИЙ АЛГОРИТМ", greedy_result, ITEMS)
    print_result("ДИНАМІЧНЕ ПРОГРАМУВАННЯ", dp_result, ITEMS)

    # Порівняння
    diff = dp_result.total_calories - greedy_result.total_calories
    print(f"\n  Різниця в калорійності: {diff:+d} ккал "
          f"({'DP точніший' if diff > 0 else 'результати збігаються'})")


if __name__ == "__main__":
    main()