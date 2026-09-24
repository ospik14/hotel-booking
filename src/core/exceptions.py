class RoomAlreadyExistsError(Exception):
    pass

class RoomNotFoundError(Exception):
    pass

class EmptyRequestForUpdateError(Exception):
    pass

class BookingOverlapError(Exception):
    pass

class RoomNotExistsError(Exception):
    pass

class IncompleteDataError(Exception):
    pass