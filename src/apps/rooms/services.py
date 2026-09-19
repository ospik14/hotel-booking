from core.db.uow import UnitOfWork
from .schemas import RoomCreate, RoomResponse, RoomFilters, RoomUpdate

class RoomService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_room(self, room_request: RoomCreate) -> RoomResponse:
        async with self.uow as uow:
            room = await uow.rooms.create(room_request)

        return RoomResponse.model_validate(room)

    async def get_room_by_id(self, id: int) -> RoomResponse:
        async with self.uow as uow:
            room = await uow.rooms.get(id)

        return RoomResponse.model_validate(room)

    async def get_rooms(self, filters: RoomFilters):
        async with self.uow as uow:
            rooms = await uow.rooms.get_list()

    async def update_room(self, id: int, room_upd: RoomUpdate):
        async with self.uow as uow:
            room = uow.rooms.get(id)
            