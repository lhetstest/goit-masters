from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """
    Створює функцію fibonacci(n) з кешем для збереження обчислених значень.

    Returns:
        function: fibonacci(n) — рекурсивна функція для обчислення n-го числа Фібоначчі з кешуванням.

    Example:
        >>> fib = caching_fibonacci()
        >>> fib(7)
        13
        >>> fib(10)
        55
    """
    cache: dict[int, int] = {}

    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    n = 10
    print(f"Fibonacci number для {n} це {fib(n)}")
