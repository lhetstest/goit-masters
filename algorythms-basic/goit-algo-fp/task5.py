"""
Завдання 5 — Візуалізація обходів бінарного дерева
====================================================
Програма будує бінарне дерево з купи (код task4.py),
а потім візуалізує два обходи:
  • DFS (обхід у глибину) — використовує стек (collections.deque)
  • BFS (обхід у ширину) — використовує чергу (collections.deque)

Кожен вузол при відвідуванні отримує унікальний колір:
градієнт від темного (#1A1A7E — темно-синій) до світлого (#E8F4FD — блакитний),
відповідно до порядку обходу (крок 1 — найтемніший, останній — найсвітліший).

⚠️ Рекурсія НЕ використовується — тільки стек і черга.
"""

from __future__ import annotations

import heapq
import uuid
from collections import deque
from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx


# ── Типи ────────────────────────────────────────────────────────────────────

class Node:
    """Вузол бінарного дерева (взятий із task4.py без змін)."""

    def __init__(self, key: int, color: str = "skyblue") -> None:
        self.left:  Optional[Node] = None
        self.right: Optional[Node] = None
        self.val:   int = key
        self.color: str = color
        self.id:    str = str(uuid.uuid4())


# ── Функції побудови дерева (з task4.py) ─────────────────────────────────────

def heap_to_tree(
    heap: list[int],
    index: int = 0,
    total_nodes: Optional[int] = None,
) -> Optional[Node]:
    """
    Рекурсивно перетворює масив-купу на дерево вузлів Node.

    Властивість індексів бінарної купи:
        • лівий нащадок  → 2*i + 1
        • правий нащадок → 2*i + 2
    """
    if total_nodes is None:
        total_nodes = len(heap)
    if index >= total_nodes:
        return None

    node = Node(key=heap[index])
    node.left  = heap_to_tree(heap, 2 * index + 1, total_nodes)
    node.right = heap_to_tree(heap, 2 * index + 2, total_nodes)
    return node


def add_edges(
    graph: nx.DiGraph,
    node: Optional[Node],
    pos: dict[str, tuple[float, float]],
    x: float = 0.0,
    y: float = 0.0,
    layer: int = 1,
) -> nx.DiGraph:
    """Додає вузли та ребра до графа networkx (з task4.py без змін)."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


# ── Кольоровий градієнт ───────────────────────────────────────────────────────

def make_color_gradient(n: int) -> list[str]:
    """
    Генерує список із n кольорів у форматі '#RRGGBB'.

    Градієнт: від темно-синього (#1A1A7E) до світло-блакитного (#E8F4FD).
    Крок 1 (перший відвіданий вузол) — найтемніший,
    крок n (останній відвіданий) — найсвітліший.

    Інтерполяція виконується лінійно для кожного каналу RGB окремо.
    """
    # Початковий (темний) і кінцевий (світлий) кольори
    start_rgb: tuple[int, int, int] = (0x1A, 0x1A, 0x7E)   # #1A1A7E
    end_rgb:   tuple[int, int, int] = (0xE8, 0xF4, 0xFD)   # #E8F4FD

    colors: list[str] = []
    for step in range(n):
        # t: 0.0 — перший вузол (темний), 1.0 — останній (світлий)
        t: float = step / max(n - 1, 1)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")

    return colors


# ── Обходи (без рекурсії) ─────────────────────────────────────────────────────

def dfs_iterative(root: Node) -> list[Node]:
    """
    Обхід у глибину (DFS) за допомогою явного стеку.

    Алгоритм:
        1. Кладемо корінь у стек.
        2. Поки стек не порожній:
           а. Дістаємо вузол з вершини стеку (pop з правого кінця deque).
           б. Фіксуємо порядок відвідування.
           в. Кладемо спочатку правого, потім лівого нащадка —
              щоб лівий опинився на вершині і був оброблений першим.
    """
    if root is None:
        return []

    order: list[Node] = []
    stack: deque[Node] = deque()
    stack.append(root)               # початковий стан: корінь у стеку

    while stack:
        node: Node = stack.pop()     # беремо з вершини стеку (LIFO)
        order.append(node)

        # Правий — першим у стек, щоб лівий оброблявся першим
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


def bfs_iterative(root: Node) -> list[Node]:
    """
    Обхід у ширину (BFS) за допомогою черги.

    Алгоритм:
        1. Кладемо корінь у чергу.
        2. Поки черга не порожня:
           а. Дістаємо вузол з початку черги (popleft — FIFO).
           б. Фіксуємо порядок відвідування.
           в. Додаємо лівого, потім правого нащадка в кінець черги.
    """
    if root is None:
        return []

    order: list[Node] = []
    queue: deque[Node] = deque()
    queue.append(root)               # початковий стан: корінь у черзі

    while queue:
        node: Node = queue.popleft() # беремо з початку черги (FIFO)
        order.append(node)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return order


# ── Візуалізація одного обходу ────────────────────────────────────────────────

def draw_traversal(
    root: Node,
    traversal_order: list[Node],
    title: str,
    output_path: Optional[str] = None,
) -> None:
    """
    Малює дерево, де колір кожного вузла відповідає його порядку обходу.

    Параметри:
        root             — корінь дерева
        traversal_order  — список вузлів у порядку відвідування
        title            — заголовок графіку
        output_path      — якщо вказано, зберігає PNG
    """
    # Призначаємо кольори відповідно до порядку обходу
    n = len(traversal_order)
    gradient = make_color_gradient(n)
    color_map: dict[str, str] = {
        node.id: gradient[step]
        for step, node in enumerate(traversal_order)
    }

    # Застосовуємо кольори до вузлів дерева
    def apply_colors(node: Optional[Node]) -> None:
        """Обхід дерева стеком для присвоєння кольорів (без рекурсії)."""
        if node is None:
            return
        stack: deque[Node] = deque([node])
        while stack:
            current = stack.pop()
            current.color = color_map.get(current.id, "skyblue")
            if current.right:
                stack.append(current.right)
            if current.left:
                stack.append(current.left)

    apply_colors(root)

    # Будуємо граф
    graph = nx.DiGraph()
    pos: dict[str, tuple[float, float]] = {root.id: (0.0, 0.0)}
    graph = add_edges(graph, root, pos)

    node_colors = [data["color"] for _, data in graph.nodes(data=True)]
    labels      = {nid: data["label"] for nid, data in graph.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)

    nx.draw(
        graph,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=node_colors,
        font_size=11,
        font_weight="bold",
        font_color="white",
        ax=ax,
    )

    # Кольорова шкала — показує градієнт від першого до останнього кроку
    legend_handles = [
        mpatches.Patch(color=gradient[0],    label=f"Крок 1 (перший)"),
        mpatches.Patch(color=gradient[n//4], label=f"Крок ~{n//4 + 1}"),
        mpatches.Patch(color=gradient[n//2], label=f"Крок ~{n//2 + 1}"),
        mpatches.Patch(color=gradient[-1],   label=f"Крок {n} (останній)"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        fontsize=9,
        title="Порядок відвідування",
        title_fontsize=9,
    )

    # Підписи з номерами кроків під вузлами
    step_labels: dict[str, str] = {
        node.id: str(step + 1)
        for step, node in enumerate(traversal_order)
    }
    step_pos = {nid: (x, y - 0.18) for nid, (x, y) in pos.items()}
    nx.draw_networkx_labels(
        graph, step_pos, labels=step_labels,
        font_size=8, font_color="#555555", ax=ax,
    )

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Збережено: {output_path}")
    plt.show()
    plt.close(fig)


# ── Точка входу ──────────────────────────────────────────────────────────────

def main() -> None:
    print("=== Завдання 5: Візуалізація обходів бінарного дерева ===\n")

    # Будуємо мін-купу і перетворюємо на дерево
    raw: list[int] = [10, 6, 8, 4, 3, 7, 2, 9, 1, 5]
    heapq.heapify(raw)
    print(f"Масив купи: {raw}\n")

    # DFS ──────────────────────────────────────────────────────
    root_dfs = heap_to_tree(raw)
    assert root_dfs is not None

    dfs_order = dfs_iterative(root_dfs)
    print("DFS порядок:", [n.val for n in dfs_order])

    draw_traversal(
        root_dfs,
        dfs_order,
        title="DFS — обхід у глибину (стек)\nТемний = перший відвіданий, світлий = останній",
        output_path="task5_dfs.png",
    )

    # BFS ──────────────────────────────────────────────────────
    root_bfs = heap_to_tree(raw)   # нове дерево, бо кольори змінились у першому
    assert root_bfs is not None

    bfs_order = bfs_iterative(root_bfs)
    print("BFS порядок:", [n.val for n in bfs_order])

    draw_traversal(
        root_bfs,
        bfs_order,
        title="BFS — обхід у ширину (черга)\nТемний = перший відвіданий, світлий = останній",
        output_path="task5_bfs.png",
    )

    print("\nГотово!")


if __name__ == "__main__":
    main()