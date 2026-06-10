from dataclasses import dataclass


@dataclass(frozen=True, slots=True, init=False)
class Record:
    id: int
    name: str
    origin: str
    year: int
    category: str

    def __init__(self, record_id: int, name: str, origin: str, year: int, category: str):
        object.__setattr__(self, "id", record_id)
        object.__setattr__(self, "name", name.strip())
        object.__setattr__(self, "origin", origin.strip())
        object.__setattr__(self, "year", year)
        object.__setattr__(self, "category", category.strip())

    def matches(
        self,
        record_id: int | None = None,
        name: str | None = None,
        origin: str | None = None,
        year: int | None = None,
        category: str | None = None,
    ) -> bool:
        return (
            (record_id is None or self.id == record_id)
            and (name is None or self.name == name)
            and (origin is None or self.origin == origin)
            and (year is None or self.year == year)
            and (category is None or self.category == category)
        )
