from src.apps.rooms.repositories import RoomRepository

class UnitOfWork:
    def __init__(self, session_maker):
        self.session_maker = session_maker
        
    async def __aenter__(self):
        self.session = self.session_maker()
        self.rooms = RoomRepository(session=self.session)

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
            raise 
        else:
            await self.session.commit()
        await self.session.close()