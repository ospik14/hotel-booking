from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

async def get_session():
    yield