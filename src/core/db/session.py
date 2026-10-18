from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)

session_maker = async_sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)


class Base(DeclarativeBase):
    pass
