from datetime import datetime


def get_days_from_today(date: str) -> int:
    """
    Обчислює кількість днів між сьогоднішньою датою та заданою датою.

    Args:
        date (str): Дата у форматі 'РРРР-ММ-ДД'.

    Returns:
        int: Різниця у днях (сьогодні - задана дата).

    Raises:
        ValueError: Якщо формат дати неправильний.
    """
    try:
        input_date = datetime.strptime(date, '%Y-%m-%d')
        today = datetime.today()
        delta = today - input_date
        return delta.days

    except ValueError:
        raise ValueError("Неправильний формат дати. Використовуйте 'РРРР-ММ-ДД'.")


if __name__ == "__main__":
    try:
        print(get_days_from_today("2026-03-13"))  # Припустимо, сьогодні 3 березня 2026 року
    except ValueError as e:
        print(e)
