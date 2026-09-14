from sqlalchemy.ext.asyncio import AsyncSession

class RoomsRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session
        pass 