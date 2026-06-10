class Record:
    def __init__(self, record_id: int, name: str, origin: str, year: int, category: str):
        self.id = record_id
        self.name = name.strip()
        self.origin = origin.strip()
        self.year = year
        self.category = category.strip()

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
