from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File
from .schemas import HotelCreate
from apps.users.schemas import CurrentUser
from apps.users.deps import RoleChecker
from .deps import hotel_service
from apps.users.models import Role

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)

require_admin = RoleChecker([Role.SUPER_ADMIN, Role.HOTEL_ADMIN])

@router.post('/')
async def create_hotel(
    service: hotel_service, 
    hotel: HotelCreate, 
    user: Annotated[CurrentUser, Depends(require_admin)]
):
    return await service.create_hotel(hotel, user)

@router.post('/{id}/images/')
async def upload_image(
    service: hotel_service,
    id: int,
    is_main: bool,
    file: Annotated[UploadFile, File()], 
    user: Annotated[CurrentUser, Depends(require_admin)]
):
    file_bytes = await file.read()
    filename = file.filename
    return await service.upload_image(file_bytes, is_main, filename, id)

@router.get('/')
async def get_hotels(service: hotel_service):
    return await service.get_hotels()