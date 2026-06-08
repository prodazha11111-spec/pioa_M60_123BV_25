type MemeRecord = tuple[int, str, str, int, str]

Memes: list[MemeRecord] = []


def _meme_exists(meme_id: int) -> bool:
    return any(record[0] == meme_id for record in Memes)


def create_meme(
        meme_id: int,
        name: str,
        origin: str,
        year: int,
        category: str,
) -> MemeRecord:
    if meme_id < 0:
        raise ValueError("ID должен быть неотрицательным числом.")
    if _meme_exists(meme_id):
        raise ValueError(f"Мем с ID = {meme_id} уже существует.")
    if not name.strip():
        raise ValueError("Название мема не может быть пустым.")
    if year <= 0 or year > 2100:
        raise ValueError("Год должен быть положительным числом и не превышать 2100.")

    record: MemeRecord = (meme_id, name.strip(), origin.strip(), year, category.strip())
    Memes.append(record)
    return record


def select_memes(
        meme_id: int | None = None,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
) -> list[MemeRecord]:
    if meme_id is None and name is None and origin is None and year is None and category is None:
        return Memes.copy()

    return [
        r for r in Memes
        if (meme_id is None or r[0] == meme_id)
           and (name is None or r[1] == name)
           and (origin is None or r[2] == origin)
           and (year is None or r[3] == year)
           and (category is None or r[4] == category)
    ]


def update_meme(
        meme_id: int,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
) -> MemeRecord:
    for i, record in enumerate(Memes):
        if record[0] == meme_id:
            new_name = name.strip() if name is not None else record[1]
            new_origin = origin.strip() if origin is not None else record[2]
            new_year = year if year is not None else record[3]
            new_category = category.strip() if category is not None else record[4]

            if name is not None and not new_name:
                raise ValueError("Название мема не может быть пустым.")
            if year is not None and (year <= 0 or year > 2100):
                raise ValueError("Год должен быть положительным числом и не превышать 2100.")

            updated: MemeRecord = (meme_id, new_name, new_origin, new_year, new_category)
            Memes[i] = updated
            return updated

    raise ValueError(f"Мем с ID = {meme_id} не найден.")


def delete_meme(meme_id: int) -> MemeRecord:
    for i, record in enumerate(Memes):
        if record[0] == meme_id:
            return Memes.pop(i)

    raise ValueError(f"Мем с id={meme_id} не найден.")
