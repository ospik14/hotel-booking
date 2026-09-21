from core.db.uow import UnitOfWork
from .schemas import BookingCreate, BookingResponse
from core.exceptions import BookingOverlapError

class BookingService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_booking(self, booking_request: BookingCreate):
        async with self.uow as uow:
            if await uow.bookings.check_overlap(
                booking_request.start_time,
                booking_request.end_time
            ):
                raise BookingOverlapError()

            booking = await uow.bookings.create(booking_request)

            return BookingResponse.model_validate(booking)
