from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from core.exceptions import UserAlreadyExistsError
from .models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_id(self, id: int):
            stmt = select(User).where(User.id == id)
            result = await self.session.execute(stmt)
    
            return result.scalar_one_or_none()

    async def create(self, user_data: dict):
        try:
            stmt = insert(User).values(**user_data).returning(User)
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise UserAlreadyExistsError()

        return result.scalar_one()