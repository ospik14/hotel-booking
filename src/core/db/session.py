import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.apps.rooms.repositories import RoomRepository

SQLALCHEMY_DATABASE_URL = os.getenv(
    'DATABASE_URL', 
    'postgresql+asyncpg://postgres:password@localhost:5432/repair_hub'
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(autoflush=False, expire_on_commit=False, class_=AsyncSession, bind=engine)

class Base(DeclarativeBase):
    pass

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

async def get_session():
    yield