"""
Завдання 3 — Алгоритм Дейкстри з бінарною купою
=================================================
Програма реалізує алгоритм Дейкстри для знаходження найкоротших
шляхів від початкової вершини до всіх інших у зваженому графі.

Ключові рішення:
  • Граф зберігається у вигляді списку суміжності (dict[Node, list[Edge]]).
  • Для вибору вершини з мінімальною відстанню використовується
    бінарна мін-купа через стандартний модуль heapq.
  • Підтримується відновлення повного шляху до будь-якої вершини.

Запуск:
    python task3.py
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field
from typing import Optional

# ── Типи ────────────────────────────────────────────────────────────────────

# Вершина графа — довільний рядок-мітка
Node = str


@dataclass(frozen=True)
class Edge:
    """Ребро графа: куди веде та яка вага."""
    to: Node          # вершина призначення
    weight: float     # вага ребра (невід'ємна)


@dataclass
class Graph:
    """
    Зважений орієнтований граф на основі списку суміжності.

    Для неорієнтованого графа кожне ребро додається в обох напрямках
    за допомогою add_edge(..., bidirectional=True).
    """
    _adj: dict[Node, list[Edge]] = field(default_factory=dict)

    def add_node(self, node: Node) -> None:
        """Додає вершину (якщо вона ще не існує)."""
        if node not in self._adj:
            self._adj[node] = []

    def add_edge(
        self,
        frm: Node,
        to: Node,
        weight: float,
        bidirectional: bool = False,
    ) -> None:
        """
        Додає ребро frm → to з вагою weight.

        Якщо bidirectional=True — додається також зворотне ребро to → frm.
        """
        if weight < 0:
            raise ValueError(f"Від'ємна вага ребра ({frm}→{to}): {weight}. "
                             "Алгоритм Дейкстри вимагає невід'ємних ваг.")
        self.add_node(frm)
        self.add_node(to)
        self._adj[frm].append(Edge(to=to, weight=weight))
        if bidirectional:
            self._adj[to].append(Edge(to=frm, weight=weight))

    @property
    def nodes(self) -> list[Node]:
        """Список усіх вершин графа."""
        return list(self._adj.keys())

    def neighbors(self, node: Node) -> list[Edge]:
        """Список ребер, що виходять з вершини node."""
        return self._adj.get(node, [])


@dataclass
class DijkstraResult:
    """Результат роботи алгоритму Дейкстри."""
    source: Node                        # початкова вершина
    dist: dict[Node, float]            # найкоротша відстань до кожної вершини
    prev: dict[Node, Optional[Node]]   # попередник на найкоротшому шляху

    def path_to(self, target: Node) -> Optional[list[Node]]:
        """
        Відновлює найкоротший шлях від source до target.

        Повертає список вершин або None, якщо target недосяжний.
        """
        if self.dist.get(target, math.inf) == math.inf:
            return None  # вершина недосяжна

        path: list[Node] = []
        current: Optional[Node] = target
        while current is not None:
            path.append(current)
            current = self.prev.get(current)

        path.reverse()
        return path

    def distance_to(self, target: Node) -> float:
        """Повертає найкоротшу відстань до target (або inf, якщо недосяжна)."""
        return self.dist.get(target, math.inf)


# ── Алгоритм Дейкстри ────────────────────────────────────────────────────────

# Елемент бінарної купи: (відстань, вершина).
# Кортеж порівнюється лексикографічно — спочатку за відстанню.
_HeapItem = tuple[float, Node]


def dijkstra(graph: Graph, source: Node) -> DijkstraResult:
    """
    Алгоритм Дейкстри з мін-купою (heapq).

    Складність: O((V + E) · log V), де V — кількість вершин, E — ребер.

    Параметри:
        graph  — зважений граф (ваги мають бути невід'ємними)
        source — початкова вершина

    Повертає:
        DijkstraResult з відстанями та попередниками для відновлення шляху.

    Кроки алгоритму:
        1. Ініціалізуємо відстань до source = 0, до решти = ∞.
        2. Кладемо (0, source) у мін-купу.
        3. Поки купа не порожня:
           а. Дістаємо вершину u з мінімальною відстанню.
           б. Якщо вона вже оброблена — пропускаємо (стара запис у купі).
           в. Для кожного ребра u → v: якщо dist[u] + вага < dist[v],
              оновлюємо dist[v] і кладемо (dist[v], v) у купу.
    """
    if source not in graph.nodes:
        raise ValueError(f"Вершина «{source}» відсутня у графі.")

    # Ініціалізація: відстань до всіх вершин = ∞
    dist: dict[Node, float] = {node: math.inf for node in graph.nodes}
    dist[source] = 0.0

    # Попередники для відновлення шляху
    prev: dict[Node, Optional[Node]] = {node: None for node in graph.nodes}

    # Множина вже оброблених (фіналізованих) вершин
    visited: set[Node] = set()

    # Мін-купа: починаємо з початкової вершини
    heap: list[_HeapItem] = [(0.0, source)]

    while heap:
        # Крок 3а: беремо вершину з найменшою поточною відстанню
        current_dist, u = heapq.heappop(heap)

        # Крок 3б: якщо вже оброблена — пропускаємо застарілий запис
        if u in visited:
            continue
        visited.add(u)

        # Крок 3в: релаксація ребер
        for edge in graph.neighbors(u):
            v: Node = edge.to
            if v in visited:
                continue  # вершина вже фіналізована — не можна покращити

            new_dist: float = current_dist + edge.weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                # Кладемо оновлену відстань у купу
                # (старий запис залишається, але буде пропущений як visited)
                heapq.heappush(heap, (new_dist, v))

    return DijkstraResult(source=source, dist=dist, prev=prev)


# ── Виведення результатів ─────────────────────────────────────────────────────

def print_results(result: DijkstraResult, graph: Graph) -> None:
    """Виводить таблицю відстаней і найкоротші шляхи до кожної вершини."""
    print(f"\n{'─'*55}")
    print(f"  Початкова вершина: «{result.source}»")
    print(f"{'─'*55}")
    print(f"  {'Вершина':<12} {'Відстань':>10}   Шлях")
    print(f"{'─'*55}")

    for node in sorted(graph.nodes):
        d = result.distance_to(node)
        path = result.path_to(node)
        dist_str = f"{d:.1f}" if d != math.inf else "∞"
        path_str = " → ".join(path) if path else "недосяжна"
        print(f"  {node:<12} {dist_str:>10}   {path_str}")

    print(f"{'─'*55}\n")


# ── Демонстрація ──────────────────────────────────────────────────────────────

def build_demo_graph() -> Graph:
    """
    Будує демонстраційний граф з 7 містами України.

    Схема (відстані умовні, у км):

           Київ
          / |  \\
        4  10   7
        /   |    \\
    Рівне Житомир Полтава
       \\    |   /    |
        3   2  6     9
         \\  | /      |
         Вінниця   Харків
              \\     /
               8   5
                \\ /
               Дніпро
    """
    g = Graph()

    edges: list[tuple[Node, Node, float]] = [
        ("Київ",     "Житомир",  10.0),
        ("Київ",     "Рівне",     4.0),
        ("Київ",     "Полтава",   7.0),
        ("Житомир",  "Вінниця",   2.0),
        ("Рівне",    "Вінниця",   3.0),
        ("Полтава",  "Вінниця",   6.0),
        ("Полтава",  "Харків",    9.0),
        ("Вінниця",  "Дніпро",    8.0),
        ("Харків",   "Дніпро",    5.0),
    ]

    for frm, to, w in edges:
        g.add_edge(frm, to, w, bidirectional=True)

    return g


def main() -> None:
    print("╔══════════════════════════════════════════════════════╗")
    print("║        Алгоритм Дейкстри — найкоротші шляхи          ║")
    print("╚══════════════════════════════════════════════════════╝")

    graph = build_demo_graph()

    # ── Приклад 1: старт з Києва ──────────────────────────────
    result_kyiv = dijkstra(graph, source="Київ")
    print_results(result_kyiv, graph)

    # ── Приклад 2: старт з Вінниці ───────────────────────────
    result_vinnytsia = dijkstra(graph, source="Вінниця")
    print_results(result_vinnytsia, graph)

    # ── Перевірка конкретного шляху ───────────────────────────
    target = "Харків"
    path = result_kyiv.path_to(target)
    dist = result_kyiv.distance_to(target)
    print(f"Найкоротший шлях Київ → {target}:")
    print(f"  {' → '.join(path) if path else 'недосяжно'}")
    print(f"  Відстань: {dist:.1f} км\n")


if __name__ == "__main__":
    main()