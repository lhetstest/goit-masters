from typing import List, Dict, Any


def get_cats_info(path: str) -> List[Dict[str, Any]]:
    """
    Читає файл з інформацією про котів і повертає список словників.

    Кожен рядок файлу повинен містити унікальний ідентифікатор кота,
    ім'я та вік, розділені комою.

    Args:
        path (str): Шлях до текстового файлу з даними про котів.

    Returns:
        List[Dict[str, Any]]: Список словників з ключами "id", "name", "age".

    Example:
        >>> cats_info = get_cats_info("cats_file.txt")
        >>> print(cats_info)
        [
            {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": 3},
            {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": 1},
            {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": 2},
            {"id": "60b90c3b13067a15887e1ae4", "name": "Simon", "age": 12},
            {"id": "60b90c4613067a15887e1ae5", "name": "Tessi", "age": 5}
        ]
    """
    cats: List[Dict[str, Any]] = []
    try:
        with open(path, encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) != 3:
                    continue
                cat_id, name, age_str = parts
                try:
                    age = int(age_str)
                except ValueError:
                    continue
                cats.append({"id": cat_id, "name": name, "age": age})
    except (IOError, OSError):
        print(f"Помилка при відкритті файлу: {path}")
    return cats


if __name__ == "__main__":
    cats_info = get_cats_info("cats_file.txt")
    print(cats_info)
