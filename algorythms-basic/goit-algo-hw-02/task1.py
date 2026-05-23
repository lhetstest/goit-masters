import queue
import itertools
from typing import Generator

# Створюємо чергу заявок
requests_queue: queue.Queue[str] = queue.Queue()

# Генератор унікальних номерів заявок
request_id_generator: Generator[int, None, None] = itertools.count(1)

def generate_request() -> None:
    """
    Генерує нову заявку з унікальним номером та додає її до черги.

    Заявка представлена рядком у форматі "Заявка #<номер>".
    """
    request_id: int = next(request_id_generator)
    request: str = f"Заявка #{request_id}"
    requests_queue.put(request)
    print(f"Створено: {request}")

def process_request() -> None:
    """
    Обробляє заявку з черги, якщо вона не порожня.

    Витягує заявку з черги та виводить інформацію про обробку.
    Якщо черга порожня, виводить відповідне повідомлення.
    """
    if not requests_queue.empty():
        request: str = requests_queue.get()
        print(f"Обробляється: {request}")
        print(f"Оброблено: {request}")
    else:
        print("Черга порожня, немає заявок для обробки.")

def main() -> None:
    """
    Головний цикл програми з керуванням користувача.

    Користувач вводить:
    - '1' для створення заявки,
    - '2' для обробки заявки,
    - 'x' для виходу з програми.
    """
    print("Система обробки заявок")
    print("Введіть '1' - створити заявку")
    print("Введіть '2' - обробити заявку")
    print("Введіть 'x' - вийти з програми")

    while True:
        user_input: str = input("Ваш вибір: ").strip().lower()
        if user_input == '1':
            generate_request()
        elif user_input == '2':
            process_request()
        elif user_input == 'x':
            print("Вихід з програми.")
            break
        else:
            print("Невірна команда. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
