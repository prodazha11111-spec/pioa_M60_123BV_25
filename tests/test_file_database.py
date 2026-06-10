import json
import tempfile
import unittest
from pathlib import Path

from src.db.backend.database import Database
from src.db.backend.error import InvalidStorageDataError, StorageIOError
from src.db.backend.file import FileDatabase


class TestFileDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "memes.json"
        self.database = FileDatabase(str(self.file_path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_database_is_database(self):
        self.assertIsInstance(self.database, Database)

    def test_create_record_saves_file(self):
        self.database.create_meme(1, "Мем", "Сайт", 2010, "Шутка")

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data["table"]["name"], "Мемы")
        self.assertEqual(data["table"]["fields"]["name"], "str")
        self.assertEqual(data["table"]["records"][0]["name"], "Мем")

    def test_records_are_loaded_from_file(self):
        self.database.create_meme(1, "Кот", "Форум", 2015, "Фото")

        new_database = FileDatabase(str(self.file_path))
        memes = new_database.select_memes()

        self.assertEqual(len(memes), 1)
        self.assertEqual(memes[0].name, "Кот")

    def test_update_record_saves_changes(self):
        self.database.create_meme(1, "Кот", "Форум", 2015, "Фото")

        self.database.update_meme(1, category="Картинка")
        new_database = FileDatabase(str(self.file_path))

        self.assertEqual(new_database.select_memes()[0].category, "Картинка")

    def test_delete_record_saves_changes(self):
        self.database.create_meme(1, "Кот", "Форум", 2015, "Фото")

        self.database.delete_meme(1)
        new_database = FileDatabase(str(self.file_path))

        self.assertEqual(new_database.select_memes(), [])

    def test_invalid_json_raises_error(self):
        self.file_path.write_text("{ плохой json", encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_wrong_file_structure_raises_error(self):
        self.file_path.write_text(json.dumps({"table": {"records": {}}}), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_extra_top_level_key_raises_error(self):
        data = self.database._empty_data()
        data["extra"] = "value"
        self.file_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_extra_table_key_raises_error(self):
        data = self.database._empty_data()
        data["table"]["extra"] = "value"
        self.file_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_missing_record_field_raises_error(self):
        data = self.database._empty_data()
        data["table"]["records"] = [{"id": 1, "name": "Мем"}]
        self.file_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_wrong_table_name_raises_error(self):
        data = self.database._empty_data()
        data["table"]["name"] = "Другая таблица"
        self.file_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_wrong_table_fields_raises_error(self):
        data = self.database._empty_data()
        data["table"]["fields"]["year"] = "str"
        self.file_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_wrong_record_value_type_raises_error(self):
        data = self.database._empty_data()
        data["table"]["records"] = [
            {
                "id": 1,
                "name": 123,
                "origin": "Сайт",
                "year": 2010,
                "category": "Шутка",
            }
        ]
        self.file_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_extra_record_key_raises_error(self):
        data = self.database._empty_data()
        data["table"]["records"] = [
            {
                "id": 1,
                "name": "Мем",
                "origin": "Сайт",
                "year": 2010,
                "category": "Шутка",
                "extra": "value",
            }
        ]
        self.file_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(InvalidStorageDataError):
            FileDatabase(str(self.file_path))

    def test_wrong_record_id_and_year_types_raise_error(self):
        for field, value in (("id", 1.5), ("id", True), ("year", 2020.5)):
            data = self.database._empty_data()
            record = {
                "id": 1,
                "name": "Мем",
                "origin": "Сайт",
                "year": 2010,
                "category": "Шутка",
            }
            record[field] = value
            data["table"]["records"] = [record]
            self.file_path.write_text(json.dumps(data), encoding="utf-8")

            with self.assertRaises(InvalidStorageDataError):
                FileDatabase(str(self.file_path))

    def test_failed_save_keeps_file_and_state_unchanged(self):
        self.database.create_meme(1, "Кот", "Форум", 2015, "Фото")
        before_file = json.loads(self.file_path.read_text(encoding="utf-8"))
        before_records = self.database.select_memes()

        def broken_record_to_dict(_record):
            return {"bad": object()}

        self.database._record_to_dict = broken_record_to_dict

        with self.assertRaises(StorageIOError):
            self.database.update_meme(1, name="Котик")

        after_file = json.loads(self.file_path.read_text(encoding="utf-8"))

        self.assertEqual(after_file, before_file)
        self.assertEqual(self.database.select_memes(), before_records)
