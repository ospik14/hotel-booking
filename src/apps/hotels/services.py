from core.db.uow import UnitOfWork
from schemas import HotelCreate, HotelResponse
from apps.users.schemas import CurrentUser

class HotelService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_hotel(self, hotel_request: HotelCreate, user: CurrentUser):
        async with self.uow as uow:
            hotel = await uow.hotels.create(hotel_request, user.id)

        return HotelResponse.model_validate(hotel)
    