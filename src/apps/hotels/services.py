from core.db.uow import UnitOfWork
from schemas import HotelCreate, HotelResponse
from apps.users.schemas import CurrentUser
from core.s3_client import upload_image_to_cloud

class HotelService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_hotel(self, hotel_request: HotelCreate, user: CurrentUser):
        async with self.uow as uow:
            hotel = await uow.hotels.create_hotel(hotel_request, user.id)

        return HotelResponse.model_validate(hotel)

    async def upload_image(self, 
        file: bytes, 
        user: CurrentUser, 
        filename: str, 
        hotel_id: int
    ):
        image_url = await upload_image_to_cloud(file, filename)

        async with self.uow as uow:
            hotel = await uow.hotels.get_by_id(hotel_id)

            if not hotel:
                raise #!!!!

            image = await uow.hotels.create_image(image_url, hotel_id)

        return image