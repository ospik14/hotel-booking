from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select
from .models import Room
from .schemas import RoomCreate
from core.exceptions import RoomAlreadyExistsError

class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, room_request: RoomCreate): 
        try:
            stmt = insert(Room).values(**room_request.model_dump()).returning(Room)
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise RoomAlreadyExistsError()

        return result.scalar_one()

    async def get(self, id: int):
        stmt = select(Room).where(Room.id == id)
        result = await self.session.execute(stmt)

        return result.scalar_one()