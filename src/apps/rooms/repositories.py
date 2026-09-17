from sqlalchemy.ext.asyncio import AsyncSession
from .models import Room

class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, room: Room): 
        self.session.add(room)
        await self.session.flush()
        await self.session.refresh(room)

        return room
