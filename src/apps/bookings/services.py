from core.db.uow import UnitOfWork
from .schemas import BookingCreate, BookingResponse

class BookingService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_booking(self, booking_request: BookingCreate):
        async with self.uow as uow:
            booking = await uow.bookings.create(booking_request)

        return BookingResponse.model_validate(booking)
