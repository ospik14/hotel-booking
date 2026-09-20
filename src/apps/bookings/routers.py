from fastapi import APIRouter
from .schemas import BookingCreate

router = APIRouter(
    prefix='/booking',
    tags=['booking']
)

@router.post('/')
async def create_booking(booking: BookingCreate):
    return booking