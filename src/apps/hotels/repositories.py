from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from .models import Hotel
from .schemas import HotelCreate

class HotelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, hotel: HotelCreate, user_id: int):
        stmt = insert(Hotel) \
        .values(
            name = hotel.name,
            address = hotel.address,
            owner_id = user_id
        ) \
        .returning(Hotel)
        result = await self.session.execute(stmt)

        return result.scalar_one()