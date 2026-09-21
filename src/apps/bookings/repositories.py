from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, insert
from .schemas import BookingCreate
from .models import Booking

class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.sesion = session

    async def check_overlap(self, start_time: datetime, end_time: datetime):
        stmt = select(Booking) \
        .where(
            and_(
                Booking.start_time <= end_time,
                Booking.end_time >= start_time         
            )    
        )
        result = await self.sesion.execute(stmt)

        if result.scalars().first() is not None:
            return True
        else:
            return False

    async def create(self, booking: BookingCreate):
        stmt = insert(Booking).values(
            **booking.model_dump(), 
            user_id=1
        ).returning(Booking)
        result = await self.sesion.execute(stmt)

        return result.scalar_one()