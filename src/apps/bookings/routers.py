from fastapi import APIRouter
from .schemas import BookingCreate
from .deps import booking_service

router = APIRouter(
    prefix='/booking',
    tags=['booking']
)

@router.post('/')
async def create_booking(booking: BookingCreate, service: booking_service):
    return await service.create_booking(booking)