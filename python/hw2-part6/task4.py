def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):
    if len(args) < 2:
        return "Помилка: команда add потребує ім'я та номер телефону."
    name = args[0].capitalize()
    phone = args[1]
    if name in contacts:
        return f"Контакт {name} вже існує. Використайте change для зміни номера."
    contacts[name] = phone
    return f"Контакт {name} з номером {phone} додано."

def change_contact(args, contacts):
    if len(args) < 2:
        return "Помилка: команда change потребує ім'я та новий номер телефону."
    name = args[0].capitalize()
    phone = args[1]
    if name not in contacts:
        return f"Контакт {name} не знайдено."
    contacts[name] = phone
    return f"Номер контакту {name} змінено на {phone}."

def show_phone(args, contacts):
    if len(args) < 1:
        return "Помилка: команда phone потребує ім'я."
    name = args[0].capitalize()
    if name not in contacts:
        return f"Контакт {name} не знайдено."
    return f"{name}: {contacts[name]}"

def show_all(contacts):
    if not contacts:
        return "Книга контактів порожня."
    result = "Контакти:\n"
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result.strip()

def main():
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
    contacts = {}
    print("Бот-помічник запущено. Введіть команду або 'exit'/'close' для виходу.")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Invalid command.")
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in ["close", "exit"]:
            print("Вихід з програми.")
            break
        elif command == "hello" and not args:
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args,contacts))
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
