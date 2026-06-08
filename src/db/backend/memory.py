from .record import Record
from .table import Table


class Memory:
    def __init__(self):
        self.table = Table()

    def create_meme(
        self,
        meme_id: int,
        name: str,
        origin: str,
        year: int,
        category: str,
    ) -> Record:
        return self.table.create_record(meme_id, name, origin, year, category)

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
        return self.table.update_record(meme_id, name, origin, year, category)

    def delete_meme(self, meme_id: int) -> Record:
        return self.table.delete_record(meme_id)
