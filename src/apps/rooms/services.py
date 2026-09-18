from core.db.uow import UnitOfWork
from .schemas import RoomCreate, RoomResponse

class RoomService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_room(self, room_request: RoomCreate):
        async with self.uow as uow:
            room = await uow.rooms.create(room_request)

        return RoomResponse.model_validate(room)

    async def get_room(self, id: int):
        async with self.uow as uow:
            room = await uow.rooms.get(id)

        return RoomResponse.model_validate(room)