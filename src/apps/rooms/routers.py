from fastapi import APIRouter
from .deps import room_service
from .schemas import RoomCreate

router = APIRouter(
    prefix='/rooms',
    tags=['rooms']
)

@router.post('/')
async def create_room(room: RoomCreate, service: room_service):
    return await service.create_room(room)