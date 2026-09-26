from core.db.uow import UnitOfWork
from .schemas import BookingCreate, BookingResponse, BookingFilters

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

    async def delete_booking(self, id: int, user_id: int):
        async with self.uow as uow:
            await uow.bookings.delete(id, user_id)