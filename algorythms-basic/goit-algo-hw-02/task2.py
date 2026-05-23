from collections import deque

def is_palindrome(s: str) -> bool:
    """
    Перевіряє, чи є рядок паліндромом.

    Ігнорує регістр та пробіли.

    Args:
        s (str): Вхідний рядок.

    Returns:
        bool: True, якщо рядок є паліндромом, інакше False.
    """
    # Нормалізуємо рядок: видаляємо пробіли, переводимо в нижній регістр
    normalized_str = ''.join(ch.lower() for ch in s if ch.isalnum())

    # Додаємо символи до двосторонньої черги
    char_deque = deque(normalized_str)

    # Порівнюємо символи з обох кінців
    while len(char_deque) > 1:
        if char_deque.popleft() != char_deque.pop():
            return False
    return True

# Приклад використання
if __name__ == "__main__":
    test_str = "А роза упала на лапу Азора"
    print(f"Рядок: {test_str}")
    print("Рядок є паліндромом" if is_palindrome(test_str) else "Не паліндром")
