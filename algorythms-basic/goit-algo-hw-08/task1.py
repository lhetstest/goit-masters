from __future__ import annotations
from typing import Optional


class AVLNode:
    def __init__(self, key: int) -> None:
        self.key: int = key
        self.height: int = 1
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None

    def __str__(self, level: int = 0, prefix: str = "Root: ") -> str:
        ret = "\t" * level + prefix + str(self.key) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


def get_height(node: Optional[AVLNode]) -> int:
    if not node:
        return 0
    return node.height


def get_balance(node: Optional[AVLNode]) -> int:
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)


def left_rotate(z: AVLNode) -> AVLNode:
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def right_rotate(y: AVLNode) -> AVLNode:
    x = y.left
    T3 = x.right
    x.right = y
    y.left = T3
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def insert(root: Optional[AVLNode], key: int) -> AVLNode:
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1:
        if key < root.left.key:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)

    if balance < -1:
        if key > root.right.key:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)

    return root


# -------------------------------------------------------
# Функція пошуку мінімального значення у AVL-дереві
# -------------------------------------------------------
def find_min(root: Optional[AVLNode]) -> Optional[AVLNode]:
    """
    Знаходить вузол з найменшим ключем у двійковому дереві пошуку.

    У BST / AVL-дереві найменший елемент завжди знаходиться
    у крайньому лівому вузлі — ідемо вліво доти, доки є куди.

    Складність: O(h), де h — висота дерева.
    Для збалансованого AVL-дерева h = O(log n).

    Args:
        root: кореневий вузол дерева (AVLNode або None)

    Returns:
        AVLNode з мінімальним ключем, або None якщо дерево порожнє
    """
    if root is None:
        return None

    current: AVLNode = root
    while current.left is not None:
        current = current.left

    return current


# -------------------------------------------------------
# Тест
# -------------------------------------------------------
root = None
keys = [10, 20, 30, 25, 28, 27, -1]

for key in keys:
    root = insert(root, key)

print("AVL-дерево після вставки", keys)
print(root)

min_node = find_min(root)
print(f"Мінімальне значення у дереві: {min_node.key}")

# Додатковий тест: дерево з одного вузла
single = AVLNode(42)
print(f"\nДерево з одного вузла (42). Мінімум: {find_min(single).key}")

# Тест на порожнє дерево
print(f"Порожнє дерево. Мінімум: {find_min(None)}")
