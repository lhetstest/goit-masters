import timeit
from typing import Final

COINS: Final[list[int]] = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int) -> dict[int, int]:
    """
    Жадібний алгоритм видачі решти.

    На кожному кроці обирає найбільший доступний номінал і бере
    максимально можливу кількість таких монет, потім переходить
    до наступного номіналу.

    Складність: O(k), де k — кількість номіналів (константа = 6) → O(1).

    Args:
        amount: Сума, яку потрібно видати (невід'ємне ціле число).

    Returns:
        Словник {номінал: кількість монет} у порядку спадання номіналу.
    """
    result: dict[int, int] = {}
    for coin in COINS:
        if amount >= coin:
            count: int = amount // coin
            result[coin] = count
            amount -= coin * count
    return result


def find_min_coins(amount: int) -> dict[int, int]:
    """
    Алгоритм динамічного програмування для мінімальної кількості монет.

    Будує таблицю dp[i] — мінімальна кількість монет для суми i,
    від 0 до заданої суми. Для відновлення складу зберігає coin_used[i].

    Складність: O(amount × k), де k — кількість номіналів.
    Пам'ять:    O(amount).

    Args:
        amount: Сума, яку потрібно видати (невід'ємне ціле число).

    Returns:
        Словник {номінал: кількість монет} із мінімальною загальною кількістю.
    """
    coins: list[int] = sorted(COINS)
    dp: list[float] = [float("inf")] * (amount + 1)
    dp[0] = 0
    coin_used: list[int] = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                coin_used[i] = coin

    result: dict[int, int] = {}
    remaining: int = amount
    while remaining > 0:
        coin = coin_used[remaining]
        result[coin] = result.get(coin, 0) + 1
        remaining -= coin

    return result


def _benchmark(amounts: list[int], repeats: int = 3) -> None:
    """
    Вимірює та виводить час виконання обох алгоритмів для заданих сум.

    Для кожної суми запускає кожен алгоритм `repeats` разів і бере
    мінімальний результат (щоб зменшити вплив фонових процесів).

    Args:
        amounts: Список сум для тестування.
        repeats: Кількість повторів вимірювання для кожної суми.
    """
    header = (
        f"{'Сума':>12} | {'Жадібний (мс)':>15} | {'ДП (мс)':>13} | "
        f"{'Монет (жад)':>12} | {'Монет (ДП)':>11} | {'Швидше у разів':>15}"
    )
    print(header)
    print("-" * len(header))

    for amount in amounts:
        # Жадібний: константна кількість ітерацій → багато повторів
        t_greedy: float = min(
            timeit.timeit(lambda: find_coins_greedy(amount), number=1_000)
            for _ in range(repeats)
        ) / 1_000 * 1_000  # → мілісекунди

        # ДП: час зростає з сумою → менше повторів для великих значень
        n_dp: int = max(1, 500 // (1 + amount // 10_000))
        t_dp: float = min(
            timeit.timeit(lambda: find_min_coins(amount), number=n_dp)
            for _ in range(repeats)
        ) / n_dp * 1_000  # → мілісекунди

        g_coins: dict[int, int] = find_coins_greedy(amount)
        d_coins: dict[int, int] = find_min_coins(amount)
        g_total: int = sum(g_coins.values())
        d_total: int = sum(d_coins.values())
        ratio: float = t_dp / t_greedy if t_greedy > 0 else float("inf")

        print(
            f"{amount:>12,} | {t_greedy:>15.4f} | {t_dp:>13.2f} | "
            f"{g_total:>12} | {d_total:>11} | {ratio:>14.0f}x"
        )


if __name__ == "__main__":
    # --- Базова демонстрація ---
    demo_amount: int = 113
    print(f"Демо (сума = {demo_amount}):")
    print(f"  Жадібний : {find_coins_greedy(demo_amount)}")
    print(f"  ДП       : {find_min_coins(demo_amount)}")
    print()

    # --- Бенчмарк ---
    print("Бенчмарк на зростаючих сумах:")
    _benchmark([113, 1000, 10000, 100000, 1000000])