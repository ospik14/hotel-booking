from fastapi import APIRouter
from deps import rooms_service
from schemas import RoomCreate

router = APIRouter(
    prefix='/rooms',
    tags=['rooms']
)

@router.post('/')
async def create_room(room: RoomCreate, service: rooms_service):
    return service.create_room(room)