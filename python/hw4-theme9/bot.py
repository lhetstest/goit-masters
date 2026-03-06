from typing import Callable, Dict, Tuple
from collections import UserDict
import re


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


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not re.fullmatch(r"\d{12}", value):
            raise ValueError("Phone must be exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone: str) -> bool:
        phone = phone.strip()
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> bool:
        old_phone = old_phone.strip()
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone: str) -> Phone | None:
        phone = phone.strip()
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name.strip().capitalize())

    def delete(self, name: str) -> bool:
        name = name.strip().capitalize()
        if name in self.data:
            del self.data[name]
            return True
        return False


@input_error
def add_contact(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    if len(args) < 2:
        raise ValueError
    name = args[0].capitalize()
    phone = args[1]
    if name in contacts:
        return f"Контакт {name} вже існує. Використайте change для зміни номера."
    record = Record(name)
    record.add_phone(phone)
    contacts[name] = record
    return f"Контакт {name} з номером {phone} додано."


@input_error
def change_contact(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    if len(args) < 2:
        raise ValueError
    name = args[0].capitalize()
    phone = args[1]
    if name not in contacts:
        raise KeyError
    record = contacts[name]
    # Якщо є хоча б один телефон - змінюємо перший, інакше додаємо
    if record.phones:
        record.edit_phone(record.phones[0].value, phone)
    else:
        record.add_phone(phone)
    return f"Номер контакту {name} змінено на {phone}."


@input_error
def show_phone(args: Tuple[str, ...], contacts: Dict[str, str]) -> str:
    if len(args) < 1:
        raise ValueError
    name = args[0].capitalize()
    if name not in contacts:
        raise KeyError
    record = contacts[name]
    if not record.phones:
        return f"У контакту {name} немає номерів."
    phones_str = "; ".join(p.value for p in record.phones)
    return f"{name}: {phones_str}"


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
    contacts: Dict[str, Record] = {}
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

