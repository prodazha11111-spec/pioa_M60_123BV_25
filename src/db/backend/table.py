from .error import (
    DuplicateRecordError,
    InvalidNameError,
    InvalidRecordFieldError,
    InvalidRecordIdError,
    InvalidYearError,
    RecordNotFoundError,
)
from .record import Record


class Table:
    def __init__(self):
        self._records: list[Record] = []

    def get_records(self) -> list[Record]:
        return self._records.copy()

    def copy(self) -> "Table":
        table = Table()
        table._records = self._records.copy()
        return table

    def _find_index(self, record_id: int) -> int:
        for index, record in enumerate(self._records):
            if record.id == record_id:
                return index
        return -1

    @staticmethod
    def _check_record_id(record_id: int) -> None:
        if type(record_id) is not int:
            raise InvalidRecordIdError("ID должен быть целым числом.")
        if record_id < 0:
            raise InvalidRecordIdError("ID должен быть неотрицательным числом.")

    @staticmethod
    def _check_name(name: str) -> None:
        if not isinstance(name, str):
            raise InvalidNameError("Название мема должно быть строкой.")
        if not name.strip():
            raise InvalidNameError("Название мема не может быть пустым.")

    @staticmethod
    def _check_year(year: int) -> None:
        if type(year) is not int:
            raise InvalidYearError("Год должен быть целым числом.")
        if year <= 0 or year > 2026:
            raise InvalidYearError(
                "Год должен быть положительным числом и не превышать 2026."
            )

    @staticmethod
    def _check_optional_text(value: str | None, field_name: str) -> None:
        if value is not None and not isinstance(value, str):
            raise InvalidRecordFieldError(f"{field_name} должен быть строкой.")

    @staticmethod
    def _check_text(value: str, field_name: str) -> None:
        if not isinstance(value, str):
            raise InvalidRecordFieldError(f"{field_name} должен быть строкой.")

    def create_record(
        self,
        record_id: int,
        name: str,
        origin: str,
        year: int,
        category: str,
    ) -> Record:
        self._check_record_id(record_id)
        if self._find_index(record_id) != -1:
            raise DuplicateRecordError(f"Мем с ID = {record_id} уже существует.")

        self._check_name(name)
        self._check_text(origin, "Источник")
        self._check_year(year)
        self._check_text(category, "Категория")

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
        if record_id is not None:
            self._check_record_id(record_id)
        if name is not None:
            self._check_name(name)
        self._check_optional_text(origin, "Источник")
        if year is not None:
            self._check_year(year)
        self._check_optional_text(category, "Категория")

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
        self._check_record_id(record_id)
        index = self._find_index(record_id)
        if index == -1:
            raise RecordNotFoundError(f"Мем с ID = {record_id} не найден.")

        current = self._records[index]
        new_name = current.name if name is None else name
        new_origin = current.origin if origin is None else origin
        new_year = current.year if year is None else year
        new_category = current.category if category is None else category

        if name is not None:
            self._check_name(new_name)
        if origin is not None:
            self._check_text(new_origin, "Источник")
        if year is not None:
            self._check_year(new_year)
        if category is not None:
            self._check_text(new_category, "Категория")

        updated = Record(record_id, new_name, new_origin, new_year, new_category)
        self._records[index] = updated
        return updated

    def delete_record(self, record_id: int) -> Record:
        self._check_record_id(record_id)
        index = self._find_index(record_id)
        if index == -1:
            raise RecordNotFoundError(f"Мем с ID = {record_id} не найден.")
        return self._records.pop(index)
