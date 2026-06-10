from abc import ABC, abstractmethod

from .record import Record


class Database(ABC):
    @abstractmethod
    def create_meme(
        self,
        meme_id: int,
        name: str,
        origin: str,
        year: int,
        category: str,
    ) -> Record:
        raise NotImplementedError

    @abstractmethod
    def select_memes(
        self,
        meme_id: int | None = None,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
    ) -> list[Record]:
        raise NotImplementedError

    @abstractmethod
    def update_meme(
        self,
        meme_id: int,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
    ) -> Record:
        raise NotImplementedError

    @abstractmethod
    def delete_meme(self, meme_id: int) -> Record:
        raise NotImplementedError
