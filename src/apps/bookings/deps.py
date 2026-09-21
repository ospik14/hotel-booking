from fastapi import Depends
from typing import Annotated
from .services import BookingService
from core.global_deps import get_uow
from core.db.uow import UnitOfWork

def get_booking_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> BookingService:
    return BookingService(uow=uow)

booking_service = Annotated[BookingService, Depends(get_booking_service)]