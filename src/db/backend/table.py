from .record import Record


class Table:
    def __init__(self):
        self._records: list[Record] = []

    def get_records(self) -> list[Record]:
        return self._records.copy()

    def _find_index(self, record_id: int) -> int:
        for index, record in enumerate(self._records):
            if record.id == record_id:
                return index
        return -1

    @staticmethod
    def _check_name(name: str) -> None:
        if not name.strip():
            raise ValueError("Название мема не может быть пустым.")

    @staticmethod
    def _check_year(year: int) -> None:
        if year <= 0 or year > 2026:
            raise ValueError("Год должен быть положительным числом и не превышать 2026.")

    def create_record(
        self,
        record_id: int,
        name: str,
        origin: str,
        year: int,
        category: str,
    ) -> Record:
        if record_id < 0:
            raise ValueError("ID должен быть неотрицательным числом.")
        if self._find_index(record_id) != -1:
            raise ValueError(f"Мем с ID = {record_id} уже существует.")

        self._check_name(name)
        self._check_year(year)

        record = Record(record_id, name, origin, year, category)
        self._records.append(record)
        return record

    def select_records(
        self,
        record_id: int | None = None,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
    ) -> list[Record]:
        if (
            record_id is None
            and name is None
            and origin is None
            and year is None
            and category is None
        ):
            return self.get_records()

        return [
            record
            for record in self._records
            if record.matches(record_id, name, origin, year, category)
        ]

    def update_record(
        self,
        record_id: int,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
    ) -> Record:
        index = self._find_index(record_id)
        if index == -1:
            raise ValueError(f"Мем с ID = {record_id} не найден.")

        current = self._records[index]
        new_name = current.name if name is None else name.strip()
        new_origin = current.origin if origin is None else origin.strip()
        new_year = current.year if year is None else year
        new_category = current.category if category is None else category.strip()

        if name is not None:
            self._check_name(new_name)
        if year is not None:
            self._check_year(new_year)

        updated = Record(record_id, new_name, new_origin, new_year, new_category)
        self._records[index] = updated
        return updated

    def delete_record(self, record_id: int) -> Record:
        index = self._find_index(record_id)
        if index == -1:
            raise ValueError(f"Мем с ID = {record_id} не найден.")
        return self._records.pop(index)
