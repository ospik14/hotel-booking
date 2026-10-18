from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError
from core.exceptions import UserAlreadyExistsError, EmptyRequestForUpdateError
from .models import User
from .schemas import UserUpdate


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
        except IntegrityError as exc:
            raise UserAlreadyExistsError() from exc

        return result.scalar_one()

    async def update_profile(self, user_id: int, data: UserUpdate):
        values = data.model_dump(exclude_unset=True)
        if not values:
            raise EmptyRequestForUpdateError()

        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**values)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update_password(self, user_id: int, hashed_password: str):
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(hashed_password=hashed_password)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
