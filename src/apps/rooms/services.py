from core.db.uow import UnitOfWork
from .schemas import RoomCreate, RoomResponse
from .models import Room

class RoomService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_room(self, room_request: RoomCreate):
        room = Room(**room_request.model_dump())
        async with self.uow as uow:
            room_response = await uow.rooms.create(room=room)

        return RoomResponse.model_validate(room_response)