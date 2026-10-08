from apps.rooms.repositories import RoomRepository
from apps.bookings.repositories import BookingRepository
from apps.users.repositories import UserRepository


class UnitOfWork:
    def __init__(self, session_maker):
        self.session_maker = session_maker
        
    async def __aenter__(self):
        self.session = self.session_maker()
        self.rooms = RoomRepository(session=self.session)
        self.bookings = BookingRepository(session=self.session)
        self.users = UserRepository(session=self.session)
        return self 

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()