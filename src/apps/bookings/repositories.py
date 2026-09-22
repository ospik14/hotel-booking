from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from .schemas import BookingCreate
from .models import Booking
from core.exceptions import BookingOverlapError, RoomNotExistsError

class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, booking: BookingCreate):
        try:
            stmt = insert(Booking) \
            .values(
                **booking.model_dump(), 
                user_id=1
            ) \
            .returning(Booking)
            
            result = await self.session.execute(stmt)
        except IntegrityError as e:
            error_msg = str(e.orig)
            
            if "violates foreign key constraint" in error_msg: 
                raise RoomNotExistsError()
            elif "violates exclude constraint" in error_msg: 
                raise BookingOverlapError()

        return result.scalar_one()