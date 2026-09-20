from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import insert, select, update
from .models import Room
from .schemas import RoomCreate, RoomUpdate, RoomFilters
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

    async def get_list(self, filters: RoomFilters):
        conditions = []
        if filters.capacity_gte is not None:
            conditions.append(Room.capacity >= filters.capacity_gte)
        if filters.capacity_lte is not None:
            conditions.append(Room.capacity <= filters.capacity_lte)
        if filters.name_contains is not None:
            conditions.append(Room.name.ilike(f'%{filters.name_contains}%'))

        stmt = select(Room).where(*conditions)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def update(self, id: int, room_upd: RoomUpdate):
        try:
            stmt = update(Room) \
            .where(Room.id == id) \
            .values(**room_upd.model_dump(exclude_unset=True)) \
            .returning(Room)
            result = await self.session.execute(stmt)

            return result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundError()
        except IntegrityError:
            raise RoomAlreadyExistsError()