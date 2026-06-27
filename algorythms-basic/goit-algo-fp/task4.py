"""
Завдання 4 — Візуалізація бінарної купи
========================================
Базовий код будує довільне бінарне дерево вручну (вузол за вузлом).
Наше завдання — перетворити список-купу (heap) на таке дерево
автоматично і намалювати його.

Ключова ідея:
    Бінарна купа зберігається у масиві так, що для вузла з індексом i:
        • лівий нащадок  → індекс 2*i + 1
        • правий нащадок → індекс 2*i + 2
    Ми рекурсивно проходимо масив і будуємо дерево вузлів Node,
    після чого малюємо його за допомогою networkx/matplotlib.
"""

from __future__ import annotations

import uuid
from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx


# ── Типи ────────────────────────────────────────────────────────────────────

class Node:
    """Вузол бінарного дерева (незмінений з базового коду)."""

    def __init__(self, key: int, color: str = "skyblue") -> None:
        self.left:  Optional[Node] = None
        self.right: Optional[Node] = None
        self.val:   int = key
        self.color: str = color
        # Унікальний ідентифікатор — потрібен networkx для розрізнення вузлів
        self.id: str = str(uuid.uuid4())


# ── Базові функції (з умови, без змін) ───────────────────────────────────────

def add_edges(
    graph: nx.DiGraph,
    node: Optional[Node],
    pos: dict[str, tuple[float, float]],
    x: float = 0,
    y: float = 0,
    layer: int = 1,
) -> nx.DiGraph:
    """
    Рекурсивно додає вузли та ребра до графа networkx.
    Обчислює координати (pos) для кожного вузла.
    """
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


def draw_tree(
    tree_root: Node,
    title: str = "Бінарна купа",
    output_path: Optional[str] = None,
) -> None:
    """
    Малює бінарне дерево за допомогою networkx + matplotlib.
    Розширено відносно базового коду: заголовок і збереження у файл.
    """
    tree = nx.DiGraph()
    pos: dict[str, tuple[float, float]] = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2500,
        node_color=colors,
        font_size=12,
        font_weight="bold",
        font_color="black",
    )

    # Легенда
    legend_handles = [
        mpatches.Patch(color="#4CAF50", label="Корінь (максимум)"),
        mpatches.Patch(color="skyblue", label="Внутрішній вузол"),
        mpatches.Patch(color="#FFB74D", label="Листок"),
    ]
    plt.legend(handles=legend_handles, loc="upper right", fontsize=9)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"Збережено: {output_path}")
    plt.show()


# ── Головна функція: купа → дерево ───────────────────────────────────────────

def heap_to_tree(
    heap: list[int],
    index: int = 0,
    total_nodes: Optional[int] = None,
) -> Optional[Node]:
    """
    Рекурсивно перетворює масив-купу на дерево вузлів Node.

    Властивість бінарної купи у масиві:
        • батько з індексом i
        • лівий нащадок  → 2*i + 1
        • правий нащадок → 2*i + 2

    Параметри:
        heap        — список значень (у порядку купи)
        index       — поточний індекс у масиві (початок: 0)
        total_nodes — загальна кількість вузлів (передається для визначення листків)

    Повертає:
        Корінь піддерева або None, якщо index виходить за межі.
    """
    if total_nodes is None:
        total_nodes = len(heap)

    # Базовий випадок: індекс поза масивом
    if index >= total_nodes:
        return None

    # Визначаємо колір вузла залежно від його ролі
    left_child_idx  = 2 * index + 1
    right_child_idx = 2 * index + 2

    is_root: bool = index == 0
    is_leaf: bool = left_child_idx >= total_nodes  # немає нащадків у масиві

    if is_root:
        color = "#4CAF50"    # зелений — корінь (максимальний елемент у макс-купі)
    elif is_leaf:
        color = "#FFB74D"    # жовтогарячий — листок
    else:
        color = "skyblue"    # блакитний — внутрішній вузол

    node = Node(key=heap[index], color=color)

    # Рекурсивно будуємо ліве і праве піддерева
    node.left  = heap_to_tree(heap, left_child_idx,  total_nodes)
    node.right = heap_to_tree(heap, right_child_idx, total_nodes)

    return node


def visualize_heap(
    heap: list[int],
    title: str = "Бінарна купа",
    output_path: Optional[str] = None,
) -> None:
    """
    Головна функція: приймає масив-купу та візуалізує її як дерево.

    Параметри:
        heap        — список цілих чисел, що утворюють купу
        title       — заголовок на графіку
        output_path — якщо вказано, зберігає зображення у файл

    Приклад:
        import heapq
        data = [3, 1, 9, 7, 4, 8, 2]
        heapq.heapify(data)          # перетворює список на мін-купу
        visualize_heap(data)
    """
    if not heap:
        raise ValueError("Купа порожня — нема що відображати.")

    print(f"Масив купи: {heap}")
    print(f"Кількість елементів: {len(heap)}")

    root: Optional[Node] = heap_to_tree(heap)
    if root is None:
        raise RuntimeError("Не вдалось побудувати дерево.")

    draw_tree(root, title=title, output_path=output_path)


# ── Демонстрація ──────────────────────────────────────────────────────────────

import heapq  # стандартний модуль Python — реалізує мін-купу через масив

if __name__ == "__main__":

    # ── Приклад 1: мін-купа через heapq ──────────────────────
    print("=== Мін-купа (heapq) ===")
    min_data: list[int] = [3, 1, 9, 7, 4, 8, 2, 6, 5]
    heapq.heapify(min_data)   # O(n): перебудовує список у мін-купу на місці
    visualize_heap(
        min_data,
        title="Мін-купа (heapq.heapify)",
        output_path="task4_min_heap.png",
    )

    # ── Приклад 2: макс-купа (інвертуємо знаки) ───────────────
    print("\n=== Макс-купа ===")
    raw: list[int] = [3, 1, 9, 7, 4, 8, 2, 6, 5]
    # heapq підтримує лише мін-купу; для макс-купи зберігаємо від'ємні значення
    max_heap_neg: list[int] = [-x for x in raw]
    heapq.heapify(max_heap_neg)
    max_heap: list[int] = [-x for x in max_heap_neg]  # повертаємо оригінальні значення
    visualize_heap(
        max_heap,
        title="Макс-купа",
        output_path="task4_max_heap.png",
    )

    # ── Приклад 3: той самий граф, що в умові задачі ──────────
    print("\n=== Дерево з умови задачі (побудоване вручну) ===")
    root_manual = Node(0)
    root_manual.left = Node(4)
    root_manual.left.left = Node(5)
    root_manual.left.right = Node(10)
    root_manual.right = Node(1)
    root_manual.right.left = Node(3)
    draw_tree(root_manual, title="Дерево з умови задачі", output_path="task4_original_tree.png")