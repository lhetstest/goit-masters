from typing import Callable, Dict, Tuple


def input_error(handler: Callable) -> Callable:
    """
    Декоратор для обробки помилок введення користувача.

    Обробляє KeyError, ValueError, IndexError і повертає
    відповідні повідомлення замість помилки.

    Args:
        handler (Callable): Функція-обробник команди.

    Returns:
        Callable: Обгорнута функція з обробкою помилок.
    """

    def wrapper(*args, **kwargs) -> str:
        try:
            return handler(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."

    return wrapper


def parse_input(user_input: str) -> Tuple[str, ...]:
    """
    Розбирає введений рядок на команду та аргументи.

    Args:
        user_input (str): Рядок введення користувача.

    Returns:
        Tuple[str, ...]: Кортеж з команди та аргументів.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return (cmd, *args)


@input_error
def add_contact(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    if len(args) < 2:
        raise ValueError
    name = args[0].capitalize()
    phone = args[1]
    if name in contacts:
        return f"Контакт {name} вже існує. Використайте change для зміни номера."
    contacts[name] = phone
    return f"Контакт {name} з номером {phone} додано."


@input_error
def change_contact(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    if len(args) < 2:
        raise ValueError
    name = args[0].capitalize()
    phone = args[1]
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return f"Номер контакту {name} змінено на {phone}."


@input_error
def show_phone(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    if len(args) < 1:
        raise ValueError
    name = args[0].capitalize()
    if name not in contacts:
        raise KeyError
    return f"{name}: {contacts[name]}"


def show_all(contacts: Dict[str, str]) -> str:
    if not contacts:
        return "Книга контактів порожня."
    result = "Контакти:\n"
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result.strip()


def main() -> None:
    """
    Основна функція, що запускає цикл взаємодії з користувачем.

    Приймає команди:
    - hello
    - add username phone
    - change username phone
    - phone username
    - showall
    - close / exit

    Виводить відповіді у консоль.
    """
    contacts: Dict[str, str] = {}
    print("Бот-помічник запущено. Введіть команду або 'exit'/'close' для виходу.")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Invalid command.")
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = tuple(parts[1:])

        if command in ["close", "exit"]:
            print("Вихід з програми.")
            break
        elif command == "hello" and not args:
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "showall" and not args:
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

