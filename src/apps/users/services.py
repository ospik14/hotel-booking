from datetime import timedelta
from core.db.uow import UnitOfWork
from .schemas import UserLogin, UserRegister, UserResponse
from core.exceptions import WrongCredentialsError
from core.security import verify_password, create_token, hash_password

class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def authenticate_user(self, user_data: UserLogin):
        async with self.uow as uow:
            user = await uow.users.get(user_data.username)

        if user is None:
            raise WrongCredentialsError()

        if not verify_password(user.hashed_password, user_data.password):
           raise WrongCredentialsError()

        token_data = {
            'sub': str(user.id),
            'type': 'access'
        }
        token = create_token(token_data, timedelta(minutes=20))

        return {
        'access_token': token,
        'token_type': 'bearer'
        }

    async def create_user(self, user_data: UserRegister):
        hashed_password = hash_password(user_data.password)

        async with self.uow as uow:
            user = await uow.users.create(
                {
                    'first_name': user_data.first_name,
                    'last_name': user_data.last_name,
                    'email': user_data.email,
                    'hashed_password': hashed_password
                }
            )

        return UserResponse.model_validate(user)

            