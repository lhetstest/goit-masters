"""
Завдання 2 — Фрактал «Дерево Піфагора»
=======================================
Програма будує фрактал «Дерево Піфагора» за допомогою рекурсії
та візуалізує результат через matplotlib.

Запуск:
    python task2.py          # рівень рекурсії за замовчуванням (10)
    python task2.py --level 7

Алгоритм:
    Кожна гілка — відрізок. На вершині відрізка рекурсивно
    малюються дві дочірні гілки, повернуті на кут ±angle відносно
    поточного напрямку та скорочені на коефіцієнт scale.
    Рекурсія зупиняється, коли досягнуто заданий рівень глибини.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field
from typing import NamedTuple

import matplotlib.pyplot as plt
import matplotlib.collections as mc


# ── Типи ────────────────────────────────────────────────────────────────────

class Point(NamedTuple):
    """Двовимірна точка."""
    x: float
    y: float


@dataclass
class Segment:
    """Відрізок між двома точками + глибина (для кольорування)."""
    start: Point
    end: Point
    depth: int


@dataclass
class FractalConfig:
    """Налаштування побудови фракталу."""
    max_depth: int = 10          # максимальна глибина рекурсії
    trunk_length: float = 120.0  # довжина стовбура (пікселі)
    scale: float = 0.71          # коефіцієнт скорочення дочірніх гілок
    angle_deg: float = 45.0      # кут нахилу лівої/правої гілки (у градусах)


@dataclass
class FractalTree:
    """Зберігає всі відрізки дерева, зібрані під час рекурсії."""
    config: FractalConfig
    segments: list[Segment] = field(default_factory=list)


# ── Рекурсивна побудова ──────────────────────────────────────────────────────

def _build_branch(
    tree: FractalTree,
    start: Point,
    length: float,
    angle_rad: float,
    depth: int,
) -> None:
    """
    Рекурсивно малює одну гілку і дві дочірні гілки.

    Параметри:
        tree       — об'єкт дерева, куди додаються відрізки
        start      — початкова точка поточної гілки
        length     — довжина поточної гілки
        angle_rad  — кут напрямку відносно осі X (у радіанах)
        depth      — поточна глибина рекурсії (відлік іде вниз до 0)
    """
    if depth < 0:
        return  # базовий випадок: глибина вичерпана

    # Кінцева точка поточної гілки
    end = Point(
        x=start.x + length * math.cos(angle_rad),
        y=start.y + length * math.sin(angle_rad),
    )

    # Зберігаємо відрізок разом із рівнем глибини (для кольору)
    tree.segments.append(Segment(start=start, end=end, depth=depth))

    cfg = tree.config
    child_length: float = length * cfg.scale
    angle_delta: float = math.radians(cfg.angle_deg)

    # Ліва дочірня гілка (поворот проти годинникової стрілки)
    _build_branch(tree, end, child_length, angle_rad + angle_delta, depth - 1)

    # Права дочірня гілка (поворот за годинниковою стрілкою)
    _build_branch(tree, end, child_length, angle_rad - angle_delta, depth - 1)


def build_tree(config: FractalConfig) -> FractalTree:
    """
    Будує «Дерево Піфагора» згідно з налаштуваннями.

    Повертає об'єкт FractalTree з усіма відрізками.
    """
    tree = FractalTree(config=config)

    # Початок стовбура — знизу по центру, напрямок — вертикально вгору (π/2)
    trunk_start = Point(x=0.0, y=0.0)
    _build_branch(
        tree,
        start=trunk_start,
        length=config.trunk_length,
        angle_rad=math.pi / 2,
        depth=config.max_depth,
    )

    return tree


# ── Візуалізація ─────────────────────────────────────────────────────────────

def _depth_to_color(depth: int, max_depth: int) -> tuple[float, float, float]:
    """
    Повертає RGB-колір для гілки залежно від її глибини.

    Стовбур і товсті гілки — темно-коричневі,
    тонкі верхні гілки — зелені.
    """
    # Нормалізація: 0.0 = верхівка (малий depth), 1.0 = стовбур (великий depth)
    t: float = depth / max_depth if max_depth > 0 else 0.0
    r: float = 0.13 + t * 0.42   # від зеленуватого до коричневого
    g: float = 0.55 - t * 0.30
    b: float = 0.13 - t * 0.10
    return (
        max(0.0, min(1.0, r)),
        max(0.0, min(1.0, g)),
        max(0.0, min(1.0, b)),
    )


def _branch_linewidth(depth: int, max_depth: int) -> float:
    """Товщина лінії: стовбур товстий, листя тонке."""
    if max_depth == 0:
        return 1.0
    return max(0.4, (depth / max_depth) * 3.5)


def visualize(tree: FractalTree) -> None:
    """
    Відображає фрактал за допомогою matplotlib.

    Кожен рівень глибини отримує окремий колір і товщину ліній.
    Використовується LineCollection для ефективного рендерингу
    великої кількості відрізків.
    """
    max_depth: int = tree.config.max_depth

    # Групуємо відрізки за глибиною для ефективного батчевого малювання
    groups: dict[int, list[tuple[tuple[float, float], tuple[float, float]]]] = {}
    for seg in tree.segments:
        groups.setdefault(seg.depth, []).append(
            ((seg.start.x, seg.start.y), (seg.end.x, seg.end.y))
        )

    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_facecolor("#0d1117")   # темний фон
    fig.patch.set_facecolor("#0d1117")

    for depth, lines in groups.items():
        color = _depth_to_color(depth, max_depth)
        lw = _branch_linewidth(depth, max_depth)
        collection = mc.LineCollection(lines, colors=[color], linewidths=lw)
        ax.add_collection(collection)

    ax.autoscale()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"Дерево Піфагора — рівень рекурсії: {max_depth}",
        color="white",
        fontsize=14,
        pad=12,
    )

    plt.tight_layout()
    output_path = "task2_pythagorean_tree.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Збережено: {output_path}")
    plt.show()


# ── Точка входу ──────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Розбирає аргументи командного рядка."""
    parser = argparse.ArgumentParser(
        description='Фрактал "Дерево Піфагора"',
    )
    parser.add_argument(
        "--level",
        type=int,
        default=10,
        metavar="N",
        help="Рівень рекурсії (за замовчуванням: 10)",
    )
    parser.add_argument(
        "--angle",
        type=float,
        default=45.0,
        metavar="DEG",
        help="Кут нахилу гілок у градусах (за замовчуванням: 45)",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=0.71,
        metavar="K",
        help="Коефіцієнт скорочення дочірніх гілок (за замовчуванням: 0.71)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Валідація введених значень
    if not (1 <= args.level <= 18):
        raise ValueError("Рівень рекурсії має бути від 1 до 18.")
    if not (1.0 <= args.angle <= 89.0):
        raise ValueError("Кут має бути від 1 до 89 градусів.")
    if not (0.1 <= args.scale <= 0.99):
        raise ValueError("Коефіцієнт скорочення має бути від 0.1 до 0.99.")

    config = FractalConfig(
        max_depth=args.level,
        angle_deg=args.angle,
        scale=args.scale,
    )

    print(f"Будуємо дерево: рівень={config.max_depth}, "
          f"кут={config.angle_deg}°, масштаб={config.scale}")

    tree = build_tree(config)
    print(f"Всього відрізків: {len(tree.segments)}")

    visualize(tree)


if __name__ == "__main__":
    main()