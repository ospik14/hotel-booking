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


class InvalidCredentialsError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class InvalidBookingDatesError(Exception):
    pass


class RoomNotAvailableError(Exception):
    pass


class CapacityExceededError(Exception):
    pass


class BookingAlreadyCancelledError(Exception):
    pass


class InvalidBookingStatusError(Exception):
    pass


class RoomHasActiveBookingsError(Exception):
    pass


class WrongPasswordError(Exception):
    pass
