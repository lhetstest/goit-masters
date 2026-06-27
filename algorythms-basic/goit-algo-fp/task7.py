"""
Завдання 7 — Метод Монте-Карло: симуляція кидків двох кубиків
==============================================================
Програма імітує велику кількість кидків двох кубиків,
обчислює ймовірність кожної суми (2–12) і порівнює
результати симуляції з аналітичними значеннями.

Метод Монте-Карло:
    Замість аналітичного підрахунку комбінацій — генеруємо
    N випадкових дослідів і рахуємо частоти. При N → ∞
    відносна частота прямує до теоретичної ймовірності
    (закон великих чисел).

Запуск:
    python task7.py
    python task7.py --rolls 100000
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from fractions import Fraction

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np


# ── Типи ────────────────────────────────────────────────────────────────────

# Сума двох кубиків: від 2 до 12
DiceSum = int

# Словник: сума → кількість появ / ймовірність
FrequencyMap    = dict[DiceSum, int]
ProbabilityMap  = dict[DiceSum, float]


@dataclass(frozen=True)
class SimulationResult:
    """Результати симуляції методом Монте-Карло."""
    n_rolls:       int             # кількість кидків
    frequencies:   FrequencyMap    # скільки разів випала кожна сума
    mc_probs:      ProbabilityMap  # ймовірності з симуляції (відносні частоти)
    exact_probs:   ProbabilityMap  # точні аналітичні ймовірності


# ── Аналітичні ймовірності ────────────────────────────────────────────────────

def compute_exact_probabilities() -> ProbabilityMap:
    """
    Обчислює точні ймовірності кожної суми двох кубиків.

    Для двох кубиків існує 6×6 = 36 рівноймовірних результатів.
    Підраховуємо, скільки пар (d1, d2) дають кожну суму.

    Повертає словник {сума: ймовірність}.
    """
    counts: FrequencyMap = {s: 0 for s in range(2, 13)}

    for d1 in range(1, 7):       # грані першого кубика
        for d2 in range(1, 7):   # грані другого кубика
            counts[d1 + d2] += 1

    total = 36  # загальна кількість комбінацій
    return {s: count / total for s, count in counts.items()}


# ── Симуляція Монте-Карло ─────────────────────────────────────────────────────

def monte_carlo_simulation(n_rolls: int, seed: int | None = None) -> SimulationResult:
    """
    Симулює n_rolls кидків двох кубиків методом Монте-Карло.

    Алгоритм:
        1. Для кожного кидка генеруємо два випадкових числа від 1 до 6.
        2. Рахуємо суму та збільшуємо лічильник для цієї суми.
        3. Після всіх кидків ділимо лічильники на n_rolls — отримуємо
           відносні частоти (емпіричні ймовірності).

    Параметри:
        n_rolls — кількість кидків
        seed    — зерно генератора (для відтворюваності результатів)

    Повертає:
        SimulationResult з частотами та ймовірностями.
    """
    if seed is not None:
        random.seed(seed)

    # Ініціалізуємо лічильники нулями для всіх можливих сум
    frequencies: FrequencyMap = {s: 0 for s in range(2, 13)}

    for _ in range(n_rolls):
        d1: int = random.randint(1, 6)   # кидок першого кубика
        d2: int = random.randint(1, 6)   # кидок другого кубика
        frequencies[d1 + d2] += 1        # рахуємо суму

    # Відносна частота = кількість появ / загальна кількість кидків
    mc_probs: ProbabilityMap = {
        s: count / n_rolls
        for s, count in frequencies.items()
    }

    exact_probs = compute_exact_probabilities()

    return SimulationResult(
        n_rolls     = n_rolls,
        frequencies = frequencies,
        mc_probs    = mc_probs,
        exact_probs = exact_probs,
    )


# ── Таблиця результатів ───────────────────────────────────────────────────────

def print_table(result: SimulationResult) -> None:
    """Виводить порівняльну таблицю у консоль."""
    print(f"\n{'═'*68}")
    print(f"  Метод Монте-Карло — {result.n_rolls:,} кидків".replace(",", " "))
    print(f"{'═'*68}")
    print(f"  {'Сума':^5} │ {'Частота':>8} │ {'МК %':>9} │ {'Точна %':>9} │ {'Відхилення':>11}")
    print(f"  {'─'*5}─┼─{'─'*8}─┼─{'─'*9}─┼─{'─'*9}─┼─{'─'*11}")

    for s in range(2, 13):
        freq   = result.frequencies[s]
        mc_p   = result.mc_probs[s] * 100
        ex_p   = result.exact_probs[s] * 100
        delta  = mc_p - ex_p
        # Дріб у форматі "k/36" для точної ймовірності
        frac   = Fraction(round(ex_p * 36 / 100), 36)
        frac_s = f"({frac.numerator}/{frac.denominator})"
        print(
            f"  {s:^5} │ {freq:>8,} │ {mc_p:>8.2f}% │ "
            f"{ex_p:>7.2f}% {frac_s:<7} │ {delta:>+10.3f}%"
            .replace(",", " ")
        )

    print(f"{'═'*68}\n")


# ── Візуалізація ──────────────────────────────────────────────────────────────

def visualize(result: SimulationResult, output_path: str = "task7_monte_carlo.png") -> None:
    """
    Будує графік із трьома панелями:
      1. Стовпчаста діаграма порівняння МК та точних ймовірностей.
      2. Графік відхилення МК від теоретичних значень.
      3. Конвергенція МК (як ймовірність суми 7 наближається до 1/6
         зі збільшенням кількості кидків).
    """
    sums   = list(range(2, 13))
    mc_pct = [result.mc_probs[s] * 100   for s in sums]
    ex_pct = [result.exact_probs[s] * 100 for s in sums]
    deltas = [mc_pct[i] - ex_pct[i]      for i in range(len(sums))]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        f"Метод Монте-Карло: два кубики ({result.n_rolls:,} кидків)".replace(",", "\u00a0"),
        fontsize=14, fontweight="bold", y=1.02,
    )

    # ── Панель 1: порівняння ймовірностей ────────────────────
    ax1 = axes[0]
    x = np.arange(len(sums))
    width = 0.38

    bars_mc = ax1.bar(x - width/2, mc_pct, width, label="Монте-Карло",
                      color="#4C72B0", alpha=0.85, zorder=3)
    bars_ex = ax1.bar(x + width/2, ex_pct, width, label="Аналітично",
                      color="#DD8452", alpha=0.85, zorder=3)

    ax1.set_title("Ймовірності сум (МК vs Аналіт.)", fontsize=11)
    ax1.set_xlabel("Сума двох кубиків")
    ax1.set_ylabel("Ймовірність (%)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(sums)
    ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f%%"))
    ax1.legend(fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
    ax1.set_axisbelow(True)

    # Підписи значень на стовпцях МК
    for bar in bars_mc:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.1,
                 f"{h:.1f}", ha="center", va="bottom", fontsize=7, color="#4C72B0")

    # ── Панель 2: відхилення МК від теоретичних значень ──────
    ax2 = axes[1]
    colors_delta = ["#E74C3C" if d > 0 else "#2ECC71" for d in deltas]
    ax2.bar(sums, deltas, color=colors_delta, alpha=0.85, zorder=3)
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax2.set_title("Відхилення МК від аналітичних значень", fontsize=11)
    ax2.set_xlabel("Сума двох кубиків")
    ax2.set_ylabel("Δ (%)")
    ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter("%+.2f%%"))
    ax2.set_xticks(sums)
    ax2.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
    ax2.set_axisbelow(True)

    # ── Панель 3: конвергенція для суми = 7 ──────────────────
    ax3 = axes[2]
    # Симулюємо знову з меншою кількістю кроків для демонстрації збіжності
    checkpoints = [10, 50, 100, 500, 1_000, 5_000, 10_000,
                   50_000, min(result.n_rolls, 1_000_000)]
    checkpoints = sorted(set(c for c in checkpoints if c <= result.n_rolls))

    random.seed(42)
    running_count = 0
    running_rolls = 0
    conv_probs: list[float] = []

    for target in checkpoints:
        # Докидаємо до наступного чекпоінту
        extra = target - running_rolls
        for _ in range(extra):
            running_rolls += 1
            if random.randint(1, 6) + random.randint(1, 6) == 7:
                running_count += 1
        conv_probs.append(running_count / running_rolls * 100)

    exact_7 = result.exact_probs[7] * 100
    ax3.semilogx(checkpoints, conv_probs, "o-", color="#4C72B0",
                 linewidth=1.8, markersize=5, label="МК (сума=7)", zorder=3)
    ax3.axhline(exact_7, color="#DD8452", linewidth=1.5,
                linestyle="--", label=f"Точне ({exact_7:.2f}%)", zorder=2)
    ax3.set_title("Конвергенція МК (сума = 7)", fontsize=11)
    ax3.set_xlabel("Кількість кидків (лог. шкала)")
    ax3.set_ylabel("Ймовірність (%)")
    ax3.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f%%"))
    ax3.legend(fontsize=9)
    ax3.grid(linestyle="--", alpha=0.5, zorder=0)
    ax3.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Графік збережено: {output_path}")
    plt.show()
    plt.close(fig)


# ── Точка входу ──────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Симуляція кидків кубиків (Монте-Карло)")
    parser.add_argument(
        "--rolls", type=int, default=1_000_000,
        metavar="N", help="Кількість кидків (за замовчуванням: 1 000 000)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        metavar="S", help="Зерно генератора для відтворюваності",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("╔══════════════════════════════════════════════════════╗")
    print("║         Метод Монте-Карло — два кубики               ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"\n  Запускаємо симуляцію: {args.rolls:,} кидків...".replace(",", "\u00a0"))

    result = monte_carlo_simulation(n_rolls=args.rolls, seed=args.seed)

    print_table(result)
    visualize(result)


if __name__ == "__main__":
    main()