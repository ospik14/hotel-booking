from fastapi import APIRouter
from .deps import room_service
from .schemas import RoomCreate

router = APIRouter(
    prefix='/rooms',
    tags=['rooms']
)

@router.post('/')
async def create_room(room_request: RoomCreate, service: room_service):
    return await service.create_room(room_request)

@router.get('/{id}/')
async def get_room(id: int, servise: room_service):
    return await servise.get_room(id)