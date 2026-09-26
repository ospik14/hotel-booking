from fastapi import APIRouter, status
from .schemas import BookingCreate, BookingFilters
from .deps import booking_service

router = APIRouter(
    prefix='/booking',
    tags=['booking']
)

@router.post('/')
async def create_booking(booking: BookingCreate, service: booking_service):
    return await service.create_booking(booking)

@router.get('/my/')
async def get_bookings(service: booking_service, user_id: int): # temporarily
    return await service.get_bookings(user_id)

@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(service: booking_service, id: int, user_id: int): # temporarily
    await service.delete_booking(id, user_id)