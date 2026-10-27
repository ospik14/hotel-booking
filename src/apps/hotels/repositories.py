from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from .models import Hotel, HotelImage
from .schemas import HotelCreate

class HotelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_hotel(self, hotel: HotelCreate, user_id: int):
        stmt = insert(Hotel) \
        .values(
            name = hotel.name,
            address = hotel.address,
            owner_id = user_id
        ) \
        .returning(Hotel)
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def get_by_id(self, hotel_id: int):
        stmt = select(Hotel).where(Hotel.id == hotel_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def create_image(self, image_url: str, hotel_id: int):
        stmt = insert(HotelImage) \
        .values(
            url=image_url,
            hotel_id=hotel_id
        ) \
        .returning(HotelImage)

        result = await self.session.execute(stmt)

        return result.scalar_one()