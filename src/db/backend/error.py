class DatabaseError(ValueError):
    pass


class BusinessLogicError(DatabaseError):
    pass


class InvalidNameError(BusinessLogicError):
    pass


class InvalidYearError(BusinessLogicError):
    pass


class InvalidRecordIdError(BusinessLogicError):
    pass


class InvalidRecordFieldError(BusinessLogicError):
    pass


class DuplicateRecordError(BusinessLogicError):
    pass


class RecordNotFoundError(BusinessLogicError):
    pass


class StorageError(DatabaseError):
    pass


class InvalidStorageDataError(StorageError):
    pass


class StorageIOError(StorageError):
    pass
