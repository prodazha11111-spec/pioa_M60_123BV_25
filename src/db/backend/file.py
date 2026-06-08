import json
from pathlib import Path

from .database import Database
from .record import Record
from .table import Table


class FileDatabase(Database):
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
                "name": "Мемы",
                "fields": {
                    "id": "int",
                    "name": "str",
                    "origin": "str",
                    "year": "int",
                    "category": "str",
                },
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
            raise ValueError("Файл базы данных содержит некорректный JSON.") from error
        except OSError as error:
            raise ValueError("Не удалось прочитать файл базы данных.") from error

    def _get_records_from_json(self, data: dict) -> list:
        if not isinstance(data, dict):
            raise ValueError("Файл базы данных имеет неверную структуру.")

        table = data.get("table")
        if not isinstance(table, dict):
            raise ValueError("В файле базы данных не найдена таблица.")

        records = table.get("records")
        if not isinstance(records, list):
            raise ValueError("В файле базы данных неверный список записей.")

        return records

    def _load(self) -> None:
        data = self._load_json()
        records = self._get_records_from_json(data)
        self.table = Table()

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Запись в файле базы данных должна быть объектом.")

            try:
                self.table.create_record(
                    record["id"],
                    record["name"],
                    record["origin"],
                    record["year"],
                    record["category"],
                )
            except KeyError as error:
                raise ValueError("В записи файла базы данных не хватает полей.") from error
            except TypeError as error:
                raise ValueError("Запись в файле базы данных имеет неверный тип.") from error

    def _save(self) -> None:
        data = self._empty_data()
        data["table"]["records"] = [
            self._record_to_dict(record) for record in self.table.get_records()
        ]

        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            raise ValueError("Не удалось сохранить файл базы данных.") from error

    def create_meme(
        self,
        meme_id: int,
        name: str,
        origin: str,
        year: int,
        category: str,
    ) -> Record:
        record = self.table.create_record(meme_id, name, origin, year, category)
        self._save()
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
        record = self.table.update_record(meme_id, name, origin, year, category)
        self._save()
        return record

    def delete_meme(self, meme_id: int) -> Record:
        record = self.table.delete_record(meme_id)
        self._save()
        return record
