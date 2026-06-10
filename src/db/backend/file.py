import json
import os
from pathlib import Path

from .database import Database
from .error import (
    BusinessLogicError,
    InvalidStorageDataError,
    StorageIOError,
)
from .record import Record
from .table import Table


class FileDatabase(Database):
    TABLE_NAME = "Мемы"
    TABLE_FIELDS = {
        "id": "int",
        "name": "str",
        "origin": "str",
        "year": "int",
        "category": "str",
    }
    DATA_KEYS = {"table"}
    TABLE_KEYS = {"name", "fields", "records"}
    RECORD_KEYS = set(TABLE_FIELDS)

    def __init__(self, file_path: str = "data/memes.json"):
        self.file_path = Path(file_path)
        self.table = Table()
        self._load()

    def _record_to_dict(self, record: Record) -> dict:
        return {
            "id": record.id,
            "name": record.name,
            "origin": record.origin,
            "year": record.year,
            "category": record.category,
        }

    def _empty_data(self) -> dict:
        return {
            "table": {
                "name": self.TABLE_NAME,
                "fields": self.TABLE_FIELDS.copy(),
                "records": [],
            }
        }

    def _load_json(self) -> dict:
        if not self.file_path.exists():
            return self._empty_data()

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            raise InvalidStorageDataError(
                "Файл базы данных содержит некорректный JSON."
            ) from error
        except OSError as error:
            raise StorageIOError("Не удалось прочитать файл базы данных.") from error

    @staticmethod
    def _check_keys(data: dict, expected_keys: set[str], message: str) -> None:
        if set(data) != expected_keys:
            raise InvalidStorageDataError(message)

    def _get_records_from_json(self, data: dict) -> list:
        if not isinstance(data, dict):
            raise InvalidStorageDataError("Файл базы данных имеет неверную структуру.")
        self._check_keys(data, self.DATA_KEYS, "Файл базы данных имеет неверную структуру.")

        table = data.get("table")
        if not isinstance(table, dict):
            raise InvalidStorageDataError("В файле базы данных не найдена таблица.")
        self._check_keys(
            table,
            self.TABLE_KEYS,
            "В файле базы данных указана неверная структура таблицы.",
        )

        if table.get("name") != self.TABLE_NAME:
            raise InvalidStorageDataError(
                "В файле базы данных указано неверное название таблицы."
            )

        if table.get("fields") != self.TABLE_FIELDS:
            raise InvalidStorageDataError(
                "В файле базы данных указана неверная структура полей таблицы."
            )

        records = table.get("records")
        if not isinstance(records, list):
            raise InvalidStorageDataError(
                "В файле базы данных неверный список записей."
            )

        return records

    def _load(self) -> None:
        data = self._load_json()
        records = self._get_records_from_json(data)
        self.table = Table()

        for record in records:
            if not isinstance(record, dict):
                raise InvalidStorageDataError(
                    "Запись в файле базы данных должна быть объектом."
                )
            self._check_keys(
                record,
                self.RECORD_KEYS,
                "Запись в файле базы данных имеет неверную структуру.",
            )

            try:
                self.table.create_record(
                    record["id"],
                    record["name"],
                    record["origin"],
                    record["year"],
                    record["category"],
                )
            except KeyError as error:
                raise InvalidStorageDataError(
                    "В записи файла базы данных не хватает полей."
                ) from error
            except (AttributeError, TypeError) as error:
                raise InvalidStorageDataError(
                    "Запись в файле базы данных имеет неверный тип."
                ) from error
            except BusinessLogicError as error:
                raise InvalidStorageDataError(
                    "Запись в файле базы данных содержит недопустимые значения."
                ) from error

    def _save_table(self, table: Table) -> None:
        data = self._empty_data()
        data["table"]["records"] = [
            self._record_to_dict(record) for record in table.get_records()
        ]
        temp_path = self.file_path.with_name(f".{self.file_path.name}.tmp")

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2, allow_nan=False)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temp_path, self.file_path)
        except (OSError, TypeError, ValueError) as error:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass
            raise StorageIOError("Не удалось сохранить файл базы данных.") from error

    def _save(self) -> None:
        self._save_table(self.table)

    def create_meme(
        self,
        meme_id: int,
        name: str,
        origin: str,
        year: int,
        category: str,
    ) -> Record:
        table = self.table.copy()
        record = table.create_record(meme_id, name, origin, year, category)
        self._save_table(table)
        self.table = table
        return record

    def select_memes(
        self,
        meme_id: int | None = None,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
    ) -> list[Record]:
        return self.table.select_records(meme_id, name, origin, year, category)

    def update_meme(
        self,
        meme_id: int,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
    ) -> Record:
        table = self.table.copy()
        record = table.update_record(meme_id, name, origin, year, category)
        self._save_table(table)
        self.table = table
        return record

    def delete_meme(self, meme_id: int) -> Record:
        table = self.table.copy()
        record = table.delete_record(meme_id)
        self._save_table(table)
        self.table = table
        return record
