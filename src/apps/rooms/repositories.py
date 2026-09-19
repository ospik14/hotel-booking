from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import insert, select
from .models import Room
from .schemas import RoomCreate
from core.exceptions import RoomAlreadyExistsError, RoomNotFoundError

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
        try:
            stmt = select(Room).where(Room.id == id)
            result = await self.session.execute(stmt)

            return result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundError()

    async def get_list(self, filters):
        return