from datetime import date
from core.db.uow import UnitOfWork
from apps.users.schemas import CurrentUser
from .schemas import (
    RoomCreate,
    RoomResponse,
    RoomFilters,
    RoomUpdate,
    AvailableRoomsFilters,
)
from core.exceptions import (
    EmptyRequestForUpdateError,
    RoomHasActiveBookingsError,
    AccessDeniedError,
)


class RoomService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_room(
            self, 
            room_request: RoomCreate, 
            user: CurrentUser
    ) -> RoomResponse:
        async with self.uow as uow:
            hotel = await uow.hotels.get_by_id(room_request.hotel_id)
            if not hotel.owner_id == user.id or not hotel:
                raise AccessDeniedError()

            room = await uow.rooms.create(room_request)

        return RoomResponse.model_validate(room)

    async def get_room_by_id(self, id: int) -> RoomResponse:
        async with self.uow as uow:
            room = await uow.rooms.get(id)

        return RoomResponse.model_validate(room)

    async def get_rooms(self, filters: RoomFilters) -> list[RoomResponse]:
        async with self.uow as uow:
            rooms = await uow.rooms.get_list(filters)

        return [RoomResponse.model_validate(room) for room in rooms]

    async def get_available_rooms(
        self, filters: AvailableRoomsFilters
    ) -> list[RoomResponse]:
        async with self.uow as uow:
            rooms = await uow.rooms.get_available(filters)

        return [RoomResponse.model_validate(room) for room in rooms]

    async def update_room(self, id: int, room_upd: RoomUpdate) -> RoomResponse:
        if not room_upd.model_dump(exclude_unset=True):
            raise EmptyRequestForUpdateError()

        async with self.uow as uow:
            if room_upd.capacity is not None:
                conflicting = await uow.rooms.count_future_confirmed_with_guests_gt(
                    id, room_upd.capacity, date.today()
                )
                if conflicting:
                    raise RoomHasActiveBookingsError()

            room = await uow.rooms.update(id, room_upd)

        return RoomResponse.model_validate(room)

    async def deactivate_room(self, id: int) -> RoomResponse:
        async with self.uow as uow:
            room = await uow.rooms.deactivate(id)

        return RoomResponse.model_validate(room)
