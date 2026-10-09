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

class BookingNotFoundError(Exception):
    pass

class CancelBookingTimeExpiredError(Exception):
    pass

class WrongCredentialsError(Exception):
    pass