from datetime import timedelta
from core.db.uow import UnitOfWork
from .schemas import UserLogin
from core.exceptions import WrongCredentialsError
from core.security import verify_password, create_token

class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def authenticate_user(self, user_data: UserLogin):
        async with self.uow as uow:
            user = uow.users.get(user_data.username)

        if user is None:
            raise WrongCredentialsError()

        if not verify_password(user.hashed_password, user_data.password):
            raise WrongCredentialsError()

        token_data = {
            'sub': user.id,
            'type': 'access'
        }
        token = create_token(token_data, timedelta(minutes=20))

        return {
        'access_token': token,
        'token_type': 'bearer'
    }

            