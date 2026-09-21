class RoomAlreadyExistsError(Exception):
    pass

class RoomNotFoundError(Exception):
    pass

class EmptyRequestForUpdateError(Exception):
    pass

class BookingOverlapError(Exception):
    pass