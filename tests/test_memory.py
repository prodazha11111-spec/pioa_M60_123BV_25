import unittest

from src.db.backend.database import Database
from src.db.backend.error import (
    DuplicateRecordError,
    InvalidNameError,
    InvalidRecordFieldError,
    InvalidRecordIdError,
    InvalidYearError,
    RecordNotFoundError,
)
from src.db.backend.memory import Memory
from src.db.backend.record import Record
from src.db.backend.table import Table


class TestRecord(unittest.TestCase):
    def test_record_matches(self):
        record = Record(2, "Кот", "Форум", 2015, "Фото")

        self.assertTrue(record.matches(name="Кот"))
        self.assertTrue(record.matches(record_id=2, year=2015))
        self.assertFalse(record.matches(category="Видео"))

    def test_record_is_immutable(self):
        record = Record(2, "Кот", "Форум", 2015, "Фото")

        with self.assertRaises(AttributeError):
            record.name = "Новое имя"

    def test_record_rejects_invalid_types(self):
        with self.assertRaises(InvalidRecordIdError):
            Record(2.5, "Кот", "Форум", 2015, "Фото")

        with self.assertRaises(InvalidNameError):
            Record(2, 123, "Форум", 2015, "Фото")

        with self.assertRaises(InvalidRecordFieldError):
            Record(2, "Кот", 123, 2015, "Фото")

        with self.assertRaises(InvalidYearError):
            Record(2, "Кот", "Форум", 2015.5, "Фото")

        with self.assertRaises(InvalidRecordFieldError):
            Record(2, "Кот", "Форум", 2015, 123)


class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table()

    def test_create_record_positive(self):
        record = self.table.create_record(1, "Мем", "Сайт", 2010, "Шутка")

        self.assertEqual(record.name, "Мем")
        self.assertEqual(len(self.table.get_records()), 1)

    def test_create_record_negative_id(self):
        with self.assertRaises(InvalidRecordIdError):
            self.table.create_record(-1, "Мем", "Сайт", 2010, "Шутка")

    def test_create_record_non_integer_id(self):
        with self.assertRaises(InvalidRecordIdError):
            self.table.create_record(1.5, "Мем", "Сайт", 2010, "Шутка")

        with self.assertRaises(InvalidRecordIdError):
            self.table.create_record(True, "Мем", "Сайт", 2010, "Шутка")

    def test_create_record_duplicate_id(self):
        self.table.create_record(1, "Мем", "Сайт", 2010, "Шутка")

        with self.assertRaises(DuplicateRecordError):
            self.table.create_record(1, "Другой мем", "Сайт", 2011, "Шутка")

    def test_create_record_empty_name(self):
        with self.assertRaises(InvalidNameError):
            self.table.create_record(1, "   ", "Сайт", 2010, "Шутка")

    def test_create_record_non_string_name(self):
        with self.assertRaises(InvalidNameError):
            self.table.create_record(1, 123, "Сайт", 2010, "Шутка")

    def test_create_record_invalid_year(self):
        with self.assertRaises(InvalidYearError):
            self.table.create_record(1, "Мем", "Сайт", 0, "Шутка")

    def test_create_record_non_integer_year(self):
        with self.assertRaises(InvalidYearError):
            self.table.create_record(1, "Мем", "Сайт", 2020.5, "Шутка")

        with self.assertRaises(InvalidYearError):
            self.table.create_record(1, "Мем", "Сайт", True, "Шутка")

    def test_create_record_non_string_text_fields(self):
        with self.assertRaises(InvalidRecordFieldError):
            self.table.create_record(1, "Мем", 123, 2010, "Шутка")

        with self.assertRaises(InvalidRecordFieldError):
            self.table.create_record(1, "Мем", "Сайт", 2010, 123)

    def test_select_records_by_filter(self):
        self.table.create_record(1, "Кот", "Форум", 2010, "Фото")
        self.table.create_record(2, "Пес", "Форум", 2011, "Фото")

        records = self.table.select_records(origin="Форум")

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].name, "Кот")

    def test_update_record_positive(self):
        self.table.create_record(1, "Кот", "Форум", 2010, "Фото")

        record = self.table.update_record(1, name="Котик", year=2012)

        self.assertEqual(record.name, "Котик")
        self.assertEqual(record.year, 2012)

    def test_update_record_missing(self):
        with self.assertRaises(RecordNotFoundError):
            self.table.update_record(99, name="Нет")

    def test_update_record_invalid_types(self):
        self.table.create_record(1, "Кот", "Форум", 2010, "Фото")

        with self.assertRaises(InvalidRecordIdError):
            self.table.update_record("1", name="Котик")

        with self.assertRaises(InvalidNameError):
            self.table.update_record(1, name=123)

        with self.assertRaises(InvalidRecordFieldError):
            self.table.update_record(1, origin=123)

        with self.assertRaises(InvalidYearError):
            self.table.update_record(1, year=2020.5)

        with self.assertRaises(InvalidRecordFieldError):
            self.table.update_record(1, category=123)

    def test_delete_record_positive(self):
        self.table.create_record(1, "Кот", "Форум", 2010, "Фото")

        record = self.table.delete_record(1)

        self.assertEqual(record.id, 1)
        self.assertEqual(self.table.get_records(), [])

    def test_delete_record_missing(self):
        with self.assertRaises(RecordNotFoundError):
            self.table.delete_record(7)

    def test_delete_record_invalid_id_type(self):
        with self.assertRaises(InvalidRecordIdError):
            self.table.delete_record("7")

    def test_select_records_invalid_filter_types(self):
        with self.assertRaises(InvalidRecordIdError):
            self.table.select_records(record_id=1.5)

        with self.assertRaises(InvalidNameError):
            self.table.select_records(name=123)

        with self.assertRaises(InvalidRecordFieldError):
            self.table.select_records(origin=123)

        with self.assertRaises(InvalidYearError):
            self.table.select_records(year=2020.5)

        with self.assertRaises(InvalidRecordFieldError):
            self.table.select_records(category=123)


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_memory_is_database(self):
        self.assertIsInstance(self.memory, Database)

    def test_create_and_select(self):
        self.memory.create_meme(1, "Мем", "Сайт", 2010, "Шутка")

        memes = self.memory.select_memes()

        self.assertEqual(memes[0].name, "Мем")

    def test_update(self):
        self.memory.create_meme(1, "Мем", "Сайт", 2010, "Шутка")

        meme = self.memory.update_meme(1, category="Обновление")

        self.assertEqual(meme.category, "Обновление")

    def test_delete(self):
        self.memory.create_meme(1, "Мем", "Сайт", 2010, "Шутка")

        meme = self.memory.delete_meme(1)

        self.assertEqual(meme.name, "Мем")
        self.assertEqual(self.memory.select_memes(), [])

    def test_select_returns_independent_copy(self):
        self.memory.create_meme(1, "Мем", "Сайт", 2010, "Шутка")

        memes = self.memory.select_memes()
        memes.append(Record(2, "Лишний", "Нет", 2020, "Нет"))

        self.assertEqual(len(self.memory.select_memes()), 1)
