import sys
from pathlib import Path
from colorama import Fore, Style, init

def print_tree(path: Path, prefix=""):
    """
    Рекурсивно обходить директорію і виводить її структуру кольорово:
    - директорії — синім
    - файли — зеленим
    """
    # Сортуємо елементи: спочатку директорії, потім файли
    try:
        entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        print(Fore.RED + f"{prefix} [Permission Denied]" + Style.RESET_ALL)
        return

    for i, entry in enumerate(entries):
        connector = "┣━ " if i < len(entries) - 1 else "┗━ "
        if entry.is_dir():
            print(f"{prefix}{connector}{Fore.BLUE}{entry.name}/" + Style.RESET_ALL)
            # Збільшуємо відступ
            extension = "┃  " if i < len(entries) - 1 else "   "
            print_tree(entry, prefix + extension)
        else:
            print(f"{prefix}{connector}{Fore.GREEN}{entry.name}" + Style.RESET_ALL)


def main():
    init(autoreset=True)  # Ініціалізація colorama

    if len(sys.argv) != 2:
        print(f"{Fore.RED}Помилка: потрібно вказати шлях до директорії у якості аргументу{Style.RESET_ALL}")
        print("Приклад використання:")
        print("python3 task3.py /шлях/до/директорії")
        sys.exit(1)

    dir_path = Path(sys.argv[1])

    if not dir_path.exists():
        print(f"{Fore.RED}Помилка: шлях не існує{Style.RESET_ALL}")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"{Fore.RED}Помилка: вказаний шлях не є директорією{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.BLUE}{dir_path.name}/" + Style.RESET_ALL)
    print_tree(dir_path)


if __name__ == "__main__":
    main()

