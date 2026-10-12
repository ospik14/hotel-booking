from fastapi import APIRouter, status
from .schemas import BookingCreate, BookingFilters
from .deps import booking_service
from apps.users.deps import current_user

router = APIRouter(
    prefix='/booking',
    tags=['booking']
)

@router.post('/')
async def create_booking(
    booking: BookingCreate, 
    service: booking_service, 
    user: current_user
):
    return await service.create_booking(booking, user)

@router.get('/my/')
async def get_bookings(service: booking_service, user: current_user): 
    return await service.get_bookings(user)

@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(service: booking_service, id: int, user: current_user):
    await service.cancel_booking(id, user)