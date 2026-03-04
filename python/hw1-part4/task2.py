import random


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    """
    Генерує унікальний відсортований список випадкових чисел у заданому діапазоні.

    Args:
        min (int): Мінімальне число (включно).
        max (int): Максимальне число (включно).
        quantity (int): Кількість чисел для генерації.

    Returns:
        list[int]: Відсортований список унікальних випадкових чисел.
                    Порожній список, якщо вхідні параметри некоректні.
    """
    if min < 1 or max > 1000 or quantity < 1 or quantity > (max - min + 1):
        return []

    numbers = set()
    while len(numbers) < quantity:
        number = random.randint(min, max)
        numbers.add(number)

    return sorted(numbers)


if __name__ == "__main__":
    lottery_numbers = get_numbers_ticket(1, 49, 6)
    print("Ваші лотерейні числа:", lottery_numbers)
