from typing import Annotated
from fastapi import APIRouter, Depends, status
from apps.users.models import Role
from apps.users.schemas import CurrentUser
from .deps import room_service
from .schemas import (
    RoomCreate,
    RoomResponse,
    RoomFilters,
    RoomUpdate,
    AvailableRoomsFilters,
)
from apps.users.deps import current_user, RoleChecker

router = APIRouter(
    prefix='/rooms',
    tags=['rooms'],
)

require_admin = RoleChecker([Role.SUPER_ADMIN, Role.HOTEL_ADMIN])

@router.post(
    '/',
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_room(
    room_request: RoomCreate,
    service: room_service,
    user: Annotated[CurrentUser, Depends(require_admin)],
) -> RoomResponse:
    return await service.create_room(room_request)


@router.get('/available/', response_model=list[RoomResponse])
async def get_available_rooms(
    service: room_service,
    filters: AvailableRoomsFilters = Depends(),
):
    return await service.get_available_rooms(filters)


@router.get('/', response_model=list[RoomResponse])
async def get_rooms(
    service: room_service,
    filters: RoomFilters = Depends(),
):
    return await service.get_rooms(filters)


@router.get('/{id}/', response_model=RoomResponse)
async def get_room_by_id(
    id: int,
    service: room_service,
    user: current_user,
) -> RoomResponse:
    return await service.get_room_by_id(id)


@router.patch('/{id}/', response_model=RoomResponse)
async def update_room(
    id: int,
    room_upd: RoomUpdate,
    service: room_service,
    user: Annotated[CurrentUser, Depends(require_admin)],
) -> RoomResponse:
    return await service.update_room(id, room_upd)


@router.delete('/{id}/', response_model=RoomResponse)
async def deactivate_room(
    id: int,
    service: room_service,
    user: Annotated[CurrentUser, Depends(require_admin)],
) -> RoomResponse:
    return await service.deactivate_room(id)
