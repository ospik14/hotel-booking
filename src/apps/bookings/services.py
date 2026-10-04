from datetime import date
from core.db.uow import UnitOfWork
from .schemas import BookingCreate, BookingResponse
from core.exceptions import BookingNotFoundError, CancelBookingTimeExpiredError

class BookingService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_booking(self, booking_request: BookingCreate):
        async with self.uow as uow:
            booking = await uow.bookings.create(booking_request)

        return BookingResponse.model_validate(booking)

    async def get_bookings(self, user_id: int):
        async with self.uow as uow:
            bookings = await uow.bookings.get_list(user_id)  

        return [
            BookingResponse.model_validate(booking) for booking in bookings
        ]

    async def cancel_booking(self, id: int, user_id: int):
        async with self.uow as uow:
            booking = await uow.bookings.get(id, user_id)

            if not booking:
                raise BookingNotFoundError()
            if booking.check_in_date <= date.today():
                raise CancelBookingTimeExpiredError()
            
            await uow.bookings.delete(id, user_id)