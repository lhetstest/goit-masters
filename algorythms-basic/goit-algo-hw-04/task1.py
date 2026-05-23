import os
import shutil
import sys
from typing import Optional

def copy_and_sort_files(src_dir: str, dest_dir: str) -> None:
    """
    Рекурсивно копіює файли з src_dir до dest_dir, сортує їх у піддиректорії за розширенням.

    Args:
        src_dir (str): Шлях до вихідної директорії.
        dest_dir (str): Шлях до директорії призначення.
    """
    try:
        for entry in os.scandir(src_dir):
            if entry.is_dir(follow_symlinks=False):
                # Рекурсивний виклик для піддиректорії
                copy_and_sort_files(entry.path, dest_dir)
            elif entry.is_file(follow_symlinks=False):
                try:
                    # Отримуємо розширення файлу без крапки, або "no_ext" якщо немає розширення
                    ext = os.path.splitext(entry.name)[1][1:].lower() or "no_ext"
                    target_dir = os.path.join(dest_dir, ext)
                    os.makedirs(target_dir, exist_ok=True)

                    target_path = os.path.join(target_dir, entry.name)

                    # Копіюємо файл
                    shutil.copy2(entry.path, target_path)
                    print(f"Скопійовано: {entry.path} -> {target_path}")

                except (PermissionError, OSError) as e:
                    print(f"Помилка копіювання файлу {entry.path}: {e}")
    except (PermissionError, OSError) as e:
        print(f"Помилка доступу до директорії {src_dir}: {e}")

def parse_args() -> Optional[tuple[str, str]]:
    """
    Парсить аргументи командного рядка.

    Повертає кортеж (src_dir, dest_dir) або None, якщо аргументи некоректні.
    """
    argc = len(sys.argv)
    if argc < 2:
        print("Використання: python script.py <шлях_до_вихідної_директорії> [шлях_до_директорії_призначення]")
        return None

    src_dir = sys.argv[1]
    dest_dir = sys.argv[2] if argc > 2 else "dist"

    if not os.path.isdir(src_dir):
        print(f"Вихідна директорія не існує або недоступна: {src_dir}")
        return None

    return src_dir, dest_dir

def main() -> None:
    args = parse_args()
    if args is None:
        return

    src_dir, dest_dir = args
    os.makedirs(dest_dir, exist_ok=True)
    copy_and_sort_files(src_dir, dest_dir)
    print("Копіювання завершено.")

if __name__ == "__main__":
    main()
