from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from .models import Hotel

class HotelRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, hotel: dict):
        stmt = insert(Hotel).values(hotel).returning(Hotel)
        result = await self.session.execute(stmt)

        return result.scalar_one()