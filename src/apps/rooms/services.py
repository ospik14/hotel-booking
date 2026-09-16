from core.db.uow import UnitOfWork
from .schemas import RoomCreate

class RoomService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_room(self, room: RoomCreate):
        return await self.uow.rooms.create(room)