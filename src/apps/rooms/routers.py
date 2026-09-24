from fastapi import APIRouter, Depends
from .deps import room_service
from .schemas import RoomCreate, RoomResponse, RoomFilters, RoomUpdate

router = APIRouter(
    prefix='/rooms',
    tags=['rooms']
)

@router.post('/')
async def create_room(
    room_request: RoomCreate, 
    service: room_service
) -> RoomResponse:
    return await service.create_room(room_request)

@router.get('/{id}/')
async def get_room_by_id(
    id: int, 
    serviсe: room_service
) -> RoomResponse:
    return await serviсe.get_room_by_id(id)

@router.get('/')
async def get_rooms(
    service: room_service,
    filters: RoomFilters = Depends()
):
    return await service.get_rooms(filters)

@router.patch('/{id}/')
async def update_room(
    id: int, 
    room_upd: RoomUpdate, 
    service: room_service
) -> RoomResponse:
    return await service.update_room(id, room_upd)
