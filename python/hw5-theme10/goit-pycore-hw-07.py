from typing import Callable, Dict, Tuple, List, Optional
from datetime import datetime, timedelta
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
        except ValueError as e:
            return str(e) if str(e) else "Invalid input."
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
    parts = user_input.strip().split()
    if not parts:
        return ("",)
    cmd = parts[0]
    args = parts[1:]
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
            raise ValueError("Phone must be exactly 12 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            date_obj = datetime.strptime(value.strip(), "%d.%m.%Y")
        except ValueError:
            raise ValueError("Невірний формат дати, використовуйте DD.MM.YYYY")
        super().__init__(date_obj)

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None

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

    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def days_to_birthday(self) -> Optional[int]:
        if not self.birthday:
            return None
        today = datetime.now().date()
        bday = self.birthday.value.date()
        next_birthday = bday.replace(year=today.year)
        if next_birthday < today:
            next_birthday = bday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

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

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> Dict[str, int]:
        """
        Повертає словник контактів з кількістю днів до дня народження,
        якщо день народження буде протягом наступних days_ahead днів.
        """
       # today = datetime.now().date()
        upcoming = {}
        for record in self.data.values():
            days = record.days_to_birthday()
            if days is not None and 0 <= days <= days_ahead:
                upcoming[record.name.value] = days
        return dict(sorted(upcoming.items(), key=lambda x: x[1]))


@input_error
def add_contact(args: Tuple[str, ...], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Додайте імʼя та номер телефону")
    name, phone, *_ = args
    name = name.strip().capitalize()
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Контакт {name} додано."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: Tuple[str, ...], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Назвіть імʼя та новий номер телефону")
    name, new_phone, *_ = args
    name = name.strip().capitalize()
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.phones:
        # Замінимо перший телефон на новий
        record.edit_phone(record.phones[0].value, new_phone)
    else:
        # Якщо телефонів немає, додамо новий
        record.add_phone(new_phone)
    return f"Телефон для {name} оновлено."


@input_error
def show_phone(args: Tuple[str, ...],  book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Введіть імʼя")
    name = args[0].strip().capitalize()
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return f"У контакту {name.capitalize()} немає номерів."
    phones_str = "; ".join(p.value for p in record.phones)
    return f"{name.capitalize()}: {phones_str}"


def show_all(book: AddressBook) -> str:
    if not book.data:
        return "Книга контактів порожня."
    result = "Контакти:\n"
    for record in book.data.values():
        result += f"{record}\n"
    return result.strip()


@input_error
def add_birthday(args: Tuple[str, ...], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Запишить імʼя і день народження, в форматі DD.MM.YYYY. ")
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday_str)
    return f"Birthday for {name.capitalize()} added/updated."


@input_error
def show_birthday(args: Tuple[str, ...], book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Enter user name.")
    name = args[0].strip().capitalize()
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.birthday:
        return f"No birthday set for {name.capitalize()}."
    return f"{name.capitalize()}'s birthday is {record.birthday}"


@input_error
def birthdays(args: Tuple[str, ...], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    result_lines = ["Upcoming birthdays:"]
    for name, days in upcoming.items():
        day_text = "today" if days == 0 else f"in {days} day{'s' if days > 1 else ''}"
        result_lines.append(f"{name} - {day_text}")
    return "\n".join(result_lines)


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
    book = AddressBook()
    print("Бот-помічник запущено. Введіть команду або 'exit'/'close' для виходу.")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Invalid command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Вихід з програми.")
            break

        elif command == "hello" and not args:
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "showall" and not args:
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

