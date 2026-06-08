from .backend.database import Database
from .backend.file import FileDatabase
from .backend.memory import Memory


database: Database


def _select_database() -> Database:
    while True:
        print("\nВыберите способ хранения данных:")
        print("1. В памяти")
        print("2. В JSON-файле")
        choice = input("Выберите вариант: ").strip()

        if choice == "1":
            return Memory()
        if choice == "2":
            try:
                return FileDatabase()
            except ValueError as error:
                print(f"Ошибка: {error}")
                continue

        print("Неверный ввод. Выберите 1 или 2.")


def _read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число.")


def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _read_nonempty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def _print_memes(meme_list: list) -> None:
    if not meme_list:
        print("Мемы не найдены.")
        return
    for meme in meme_list:
        print(
            f"{meme.id}, {meme.name}, {meme.origin}, "
            f"{meme.year}, {meme.category}"
        )


def _add_meme() -> None:
    print("\n  Добавление мема  ")
    meme_id = _read_int("ID мема: ")
    name = _read_nonempty_string("Название: ")
    origin = input("Источник (откуда пошёл мем): ").strip()
    year = _read_int("Год появления: ")
    category = input("Категория: ").strip()
    try:
        _print_memes([database.create_meme(meme_id, name, origin, year, category)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _find_memes() -> None:
    print("\n  Поиск мемов  ")
    print("Введите критерии поиска (пустое поле = пропустить фильтр):")
    meme_id = _read_optional_int("ID мема: ")
    name = input("Название: ").strip() or None
    origin = input("Источник: ").strip() or None
    year = _read_optional_int("Год: ")
    category = input("Категория: ").strip() or None
    _print_memes(database.select_memes(meme_id, name, origin, year, category))


def _update_meme() -> None:
    print("\n  Обновление мема  ")
    meme_id = _read_int("ID мема для обновления: ")
    print("Введите новые значения (пустое поле — без изменений):")
    name = input("Новое название: ").strip() or None
    origin = input("Новый источник: ").strip() or None
    year = _read_optional_int("Новый год: ")
    category = input("Новая категория: ").strip() or None
    try:
        _print_memes([database.update_meme(meme_id, name, origin, year, category)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def _delete_meme() -> None:
    print("\n  Удаление мема  ")
    meme_id = _read_int("ID мема для удаления: ")
    try:
        _print_memes([database.delete_meme(meme_id)])
    except ValueError as e:
        print(f"Ошибка: {e}")


def run() -> None:
    global database
    database = _select_database()

    actions = {
        "1": _add_meme,
        "2": _find_memes,
        "3": _update_meme,
        "4": _delete_meme,
        "5": lambda: _print_memes(database.select_memes()),
    }
    while True:
        print("\n= База данных мемов =")
        print("1. Добавить мем")
        print("2. Найти мемы")
        print("3. Обновить мем")
        print("4. Удалить мем")
        print("5. Показать все мемы")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("Выход из программы.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный ввод. Пожалуйста, выберите пункт из меню.")
