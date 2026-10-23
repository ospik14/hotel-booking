from fastapi import APIRouter
from schemas import HotelCreate
from deps import get_hotel_service

router = APIRouter(
    prefix='/hotels',
    tags=['hotels']
)

@router.post('/')
async def create_hotel(services: get_hotel_service, hotel: HotelCreate):
    return