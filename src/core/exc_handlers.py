from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .exceptions import (
    RoomAlreadyExistsError,
    RoomNotFoundError,
    EmptyRequestForUpdateError,
    BookingOverlapError,
    RoomNotExistsError,
    IncompleteDataError,
    BookingNotFoundError,
    CancelBookingTimeExpiredError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    AccessDeniedError,
    InvalidBookingDatesError,
    RoomNotAvailableError,
    CapacityExceededError,
    BookingAlreadyCancelledError,
    InvalidBookingStatusError,
    RoomHasActiveBookingsError,
    WrongPasswordError,
)


async def room_already_exists(request, exc):
    return JSONResponse(
        status_code=409,
        content={'detail': 'room already exists'},
    )


async def room_not_found(request, exc):
    return JSONResponse(
        status_code=404,
        content={'detail': 'room not found'},
    )


async def empty_request(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': 'empty update request'},
    )


async def booking_overlap(request, exc):
    return JSONResponse(
        status_code=409,
        content={'detail': 'booking overlap'},
    )


async def room_not_exists(request, exc):
    return JSONResponse(
        status_code=404,
        content={'detail': 'this room does not exist'},
    )


async def incomplete_data(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': 'incomplete data in filters'},
    )


async def booking_not_found(request, exc):
    return JSONResponse(
        status_code=404,
        content={'detail': 'booking not found'},
    )


async def cancel_booking_time_expired(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': 'the time for canceling has expired'},
    )


async def invalid_credentials(request, exc):
    return JSONResponse(
        status_code=401,
        content={'detail': 'wrong credentials'},
    )


async def user_already_exists(request, exc):
    return JSONResponse(
        status_code=409,
        content={'detail': 'user already exists'},
    )


async def access_denied(request, exc):
    return JSONResponse(
        status_code=403,
        content={'detail': 'access denied'},
    )


async def invalid_booking_dates(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc) or 'invalid booking dates'},
    )


async def room_not_available(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': 'room is not available for booking'},
    )


async def capacity_exceeded(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': 'number of guests exceeds room capacity'},
    )


async def booking_already_cancelled(request, exc):
    return JSONResponse(
        status_code=409,
        content={'detail': 'booking is already cancelled'},
    )


async def invalid_booking_status(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': str(exc) or 'invalid booking status transition'},
    )


async def room_has_active_bookings(request, exc):
    return JSONResponse(
        status_code=409,
        content={'detail': 'room has active future bookings that conflict with this change'},
    )


async def wrong_password(request, exc):
    return JSONResponse(
        status_code=400,
        content={'detail': 'current password is incorrect'},
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RoomAlreadyExistsError, room_already_exists)
    app.add_exception_handler(RoomNotFoundError, room_not_found)
    app.add_exception_handler(EmptyRequestForUpdateError, empty_request)
    app.add_exception_handler(BookingOverlapError, booking_overlap)
    app.add_exception_handler(RoomNotExistsError, room_not_exists)
    app.add_exception_handler(IncompleteDataError, incomplete_data)
    app.add_exception_handler(BookingNotFoundError, booking_not_found)
    app.add_exception_handler(CancelBookingTimeExpiredError, cancel_booking_time_expired)
    app.add_exception_handler(InvalidCredentialsError, invalid_credentials)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists)
    app.add_exception_handler(AccessDeniedError, access_denied)
    app.add_exception_handler(InvalidBookingDatesError, invalid_booking_dates)
    app.add_exception_handler(RoomNotAvailableError, room_not_available)
    app.add_exception_handler(CapacityExceededError, capacity_exceeded)
    app.add_exception_handler(BookingAlreadyCancelledError, booking_already_cancelled)
    app.add_exception_handler(InvalidBookingStatusError, invalid_booking_status)
    app.add_exception_handler(RoomHasActiveBookingsError, room_has_active_bookings)
    app.add_exception_handler(WrongPasswordError, wrong_password)
