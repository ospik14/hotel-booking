from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import RoomCreate, RoomResponse

class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, room: RoomCreate): 
        return RoomResponse(**room.model_dump(), id=1) 