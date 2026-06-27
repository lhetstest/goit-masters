# ============================================================
# Task 1 — Singly Linked List: Reverse · Sort · Merge
# ============================================================

from __future__ import annotations
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar("T")

# ── Types ────────────────────────────────────────────────────

Comparator = Callable[[T, T], int]
"""
A comparator function: returns a negative int if a < b,
zero if a == b, and a positive int if a > b.
"""


class ListNode(Generic[T]):
    """A single node in a singly linked list."""

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: Optional[ListNode[T]] = None

    def __repr__(self) -> str:
        return f"ListNode({self.value!r})"


class LinkedList(Generic[T]):
    """A singly linked list."""

    def __init__(self) -> None:
        self.head: Optional[ListNode[T]] = None

    # ── helpers ──────────────────────────────────────────────

    @classmethod
    def from_list(cls, values: list[T]) -> LinkedList[T]:
        """Build a LinkedList from a plain Python list."""
        ll: LinkedList[T] = cls()
        if not values:
            return ll

        ll.head = ListNode(values[0])
        current = ll.head
        for value in values[1:]:
            current.next = ListNode(value)
            current = current.next

        return ll

    def to_list(self) -> list[T]:
        """Convert the linked list to a plain Python list."""
        result: list[T] = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()!r})"


# ── 1. Reverse ────────────────────────────────────────────────

def reverse_list(ll: LinkedList[T]) -> LinkedList[T]:
    """
    Reverse a singly linked list **in-place** by re-wiring the ``next``
    pointers — no extra memory, O(n) time.

    Args:
        ll: The list to reverse (mutated in place).

    Returns:
        The same LinkedList object with its head updated.
    """
    prev: Optional[ListNode[T]] = None
    current: Optional[ListNode[T]] = ll.head

    while current is not None:
        next_node: Optional[ListNode[T]] = current.next  # save successor
        current.next = prev                               # flip pointer
        prev = current                                    # advance prev
        current = next_node                              # advance current

    ll.head = prev  # new head is the old tail
    return ll


# ── 2. Sort (insertion sort) ──────────────────────────────────

def _default_comparator(a: T, b: T) -> int:
    """Default comparator using Python's built-in ordering."""
    if a < b:   # type: ignore[operator]
        return -1
    if a > b:   # type: ignore[operator]
        return 1
    return 0


def sort_list(
    ll: LinkedList[T],
    comparator: Comparator[T] = _default_comparator,
) -> LinkedList[T]:
    """
    Sort a singly linked list using **insertion sort**.

    Insertion sort suits linked lists well: inserting a node into a sorted
    prefix costs O(1) pointer operations once the position is found, and
    there is no array shifting.

    Time complexity: O(n²) — good for small or nearly-sorted lists.

    Args:
        ll:          The list to sort (mutated in place).
        comparator:  Ordering function (default: natural ordering).

    Returns:
        The same LinkedList object with its head updated.
    """
    # A sentinel dummy node simplifies insertion at the front.
    dummy: ListNode[T] = ListNode(None)  # type: ignore[arg-type]
    dummy.next = None

    unsorted: Optional[ListNode[T]] = ll.head

    while unsorted is not None:
        current: ListNode[T] = unsorted
        unsorted = unsorted.next

        # Find the correct insertion point inside the sorted section.
        prev: ListNode[T] = dummy
        while prev.next is not None and comparator(prev.next.value, current.value) <= 0:
            prev = prev.next

        # Splice `current` after `prev`.
        current.next = prev.next
        prev.next = current

    ll.head = dummy.next
    return ll


# ── 3. Merge two sorted lists ─────────────────────────────────

def merge_sorted_lists(
    list_a: LinkedList[T],
    list_b: LinkedList[T],
    comparator: Comparator[T] = _default_comparator,
) -> LinkedList[T]:
    """
    Merge two **already-sorted** singly linked lists into one sorted list.

    Nodes are re-linked (not copied), so both input lists are consumed.
    Time complexity: O(n + m) where n and m are the lengths of the lists.

    Args:
        list_a:      First sorted list.
        list_b:      Second sorted list.
        comparator:  Ordering function (default: natural ordering).

    Returns:
        A new LinkedList whose head points to the merged sequence.
    """
    dummy: ListNode[T] = ListNode(None)  # type: ignore[arg-type]
    tail: ListNode[T] = dummy

    a: Optional[ListNode[T]] = list_a.head
    b: Optional[ListNode[T]] = list_b.head

    while a is not None and b is not None:
        if comparator(a.value, b.value) <= 0:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next  # type: ignore[assignment]

    # Attach any remaining nodes from whichever list is not exhausted.
    tail.next = a if a is not None else b

    result: LinkedList[T] = LinkedList()
    result.head = dummy.next
    return result


# ── Demo ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Task 1: Singly Linked List ===\n")

    # — Reverse —
    original: LinkedList[int] = LinkedList.from_list([1, 2, 3, 4, 5])
    print("Original:        ", original.to_list())
    reverse_list(original)
    print("Reversed:        ", original.to_list())

    # — Sort —
    unsorted: LinkedList[int] = LinkedList.from_list([4, 2, 7, 1, 9, 3])
    print("\nUnsorted:        ", unsorted.to_list())
    sort_list(unsorted)
    print("Sorted (ins):    ", unsorted.to_list())

    # — Merge —
    sorted_a: LinkedList[int] = LinkedList.from_list([1, 3, 5, 7])
    sorted_b: LinkedList[int] = LinkedList.from_list([2, 4, 6, 8, 9])
    print("\nList A:          ", sorted_a.to_list())
    print("List B:          ", sorted_b.to_list())
    merged: LinkedList[int] = merge_sorted_lists(sorted_a, sorted_b)
    print("Merged:          ", merged.to_list())

    # — String example with custom comparator —
    words_1: LinkedList[str] = LinkedList.from_list(["apple", "cherry", "fig"])
    words_2: LinkedList[str] = LinkedList.from_list(["banana", "date", "grape"])
    str_cmp: Comparator[str] = lambda a, b: (a > b) - (a < b)
    merged_words: LinkedList[str] = merge_sorted_lists(words_1, words_2, str_cmp)
    print("\nMerged strings:  ", merged_words.to_list())