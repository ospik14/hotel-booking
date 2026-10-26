from typing import Annotated
from fastapi import APIRouter, Depends
from schemas import HotelCreate
from apps.users.schemas import CurrentUser
from apps.users.deps import RoleChecker
from deps import hotel_service
from apps.users.models import Role

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)

require_admin = RoleChecker([Role.SUPER_ADMIN, Role.HOTEL_ADMIN])
\
@router.post('/')
async def create_hotel(
    service: hotel_service, 
    hotel: HotelCreate, 
    user: Annotated[CurrentUser, Depends(require_admin)]
):
    return await service.create_hotel(hotel, user)