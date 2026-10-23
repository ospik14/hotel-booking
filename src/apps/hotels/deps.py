from fastapi import Depends
from typing import Annotated
from .services import HotelService
from core.global_deps import get_uow
from core.db.uow import UnitOfWork

def get_hotel_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> HotelService:
    return HotelService(uow=uow)

booking_service = Annotated[HotelService, Depends(get_hotel_service)]