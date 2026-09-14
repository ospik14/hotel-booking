from repositories import RoomsRepositories
from schemas import RoomCreate

class RoomsService:
    def __init__(self, repo: RoomsRepositories):
        self.repo = repo
        pass

    async def create_room(self, room: RoomCreate):
        return RoomsRepositories.create()