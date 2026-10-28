from datetime import date
from decimal import Decimal
from core.db.uow import UnitOfWork
from .schemas import (
    BookingCreate,
    BookingResponse,
    BookingFilters,
    AdminBookingFilters,
    BookingStatusUpdate,
)
from .models import BookingStatus
from core.exceptions import (
    BookingNotFoundError,
    CancelBookingTimeExpiredError,
    InvalidBookingDatesError,
    RoomNotAvailableError,
    CapacityExceededError,
    BookingAlreadyCancelledError,
    InvalidBookingStatusError,
    AccessDeniedError,
)
from apps.users.schemas import CurrentUser
from apps.users.models import Role


class BookingService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def _validate_dates(self, check_in: date, check_out: date) -> None:
        if check_out <= check_in:
            raise InvalidBookingDatesError('check_out_date must be after check_in_date')
        if check_in < date.today():
            raise InvalidBookingDatesError('check_in_date cannot be in the past')

    async def create_booking(
        self,
        booking_request: BookingCreate,
        user: CurrentUser,
    ):
        if not user.is_active:
            raise AccessDeniedError()

        self._validate_dates(
            booking_request.check_in_date,
            booking_request.check_out_date,
        )

        async with self.uow as uow:
            room = await uow.rooms.get_for_update(booking_request.room_id)

            if not room.is_active:
                raise RoomNotAvailableError()
            if booking_request.guests > room.capacity:
                raise CapacityExceededError()

            nights = (booking_request.check_out_date - booking_request.check_in_date).days
            price_per_night = Decimal(room.price_per_night)
            total_price = price_per_night * nights

            booking = await uow.bookings.create(
                booking_request,
                user.id,
                price_per_night=price_per_night,
                total_price=total_price,
            )

        return BookingResponse.model_validate(booking)

    async def get_bookings(self, user: CurrentUser, filters: BookingFilters):
        async with self.uow as uow:
            bookings = await uow.bookings.get_list(user.id, filters)

        return [
            BookingResponse.model_validate(booking) for booking in bookings
        ]

    async def get_booking(self, id: int, user: CurrentUser):
        async with self.uow as uow:
            if user.role == Role.HOTEL_ADMIN:
                booking = await uow.bookings.get_by_id(id)
            else:
                booking = await uow.bookings.get_for_user(id, user.id)

            if not booking:
                raise BookingNotFoundError()

        return BookingResponse.model_validate(booking)

    async def get_admin_bookings(self, filters: AdminBookingFilters):
        async with self.uow as uow:
            bookings = await uow.bookings.get_admin_list(filters)

        return [
            BookingResponse.model_validate(booking) for booking in bookings
        ]

    async def cancel_booking(self, id: int, user: CurrentUser):
        async with self.uow as uow:
            if user.role == Role.HOTEL_ADMIN:
                booking = await uow.bookings.get_by_id(id)
            else:
                booking = await uow.bookings.get_for_user(id, user.id)

            if not booking:
                raise BookingNotFoundError()
            if booking.status == BookingStatus.CANCELLED:
                raise BookingAlreadyCancelledError()
            if booking.status == BookingStatus.COMPLETED:
                raise InvalidBookingStatusError('completed booking cannot be cancelled')
            if user.role != Role.HOTEL_ADMIN and booking.check_in_date <= date.today():
                raise CancelBookingTimeExpiredError()

            await uow.bookings.set_status(id, BookingStatus.CANCELLED)

    async def update_status(
        self,
        id: int,
        status_update: BookingStatusUpdate,
    ):
        async with self.uow as uow:
            booking = await uow.bookings.get_by_id(id)
            if not booking:
                raise BookingNotFoundError()

            new_status = status_update.status
            current = booking.status

            allowed = {
                BookingStatus.CONFIRMED: {
                    BookingStatus.CANCELLED,
                    BookingStatus.COMPLETED,
                },
                BookingStatus.CANCELLED: set(),
                BookingStatus.COMPLETED: set(),
            }
            if new_status not in allowed[current]:
                raise InvalidBookingStatusError(
                    f'cannot change status from {current.value} to {new_status.value}'
                )

            updated = await uow.bookings.set_status(id, new_status)

        return BookingResponse.model_validate(updated)
