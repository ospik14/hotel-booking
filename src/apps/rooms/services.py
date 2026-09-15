from .repositories import RoomRepository
from .schemas import RoomCreate

class RoomService:
    def __init__(self, repo: RoomRepository):
        self.repo = repo

    async def create_room(self, room: RoomCreate):
        return await self.repo.create(room)