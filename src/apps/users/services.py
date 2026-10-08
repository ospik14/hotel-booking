from core.db.uow import UnitOfWork
from .schemas import UserLogin

class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def login(self, user_login: UserLogin):
        async with self.uow as uow:
            user = uow.users.get(user_login.email)
