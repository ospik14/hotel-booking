from datetime import timedelta
from core.db.uow import UnitOfWork
from .schemas import UserLogin, UserRegister, UserResponse
from core.exceptions import InvalidCredentialsError
from core.security import verify_password, create_token, hash_password, \
decode_token

class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def authenticate_user(self, user_data: UserLogin):
        async with self.uow as uow:
            user = await uow.users.get_by_email(user_data.email)

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(user.hashed_password, user_data.password):
           raise InvalidCredentialsError()

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

    async def verify_user(self, token: str):
        try:
            token_payload = decode_token(token)
        except ValueError:
            raise InvalidCredentialsError()
        
        user_id = token_payload.get('sub')
        async with self.uow as uow:
            current_user = await uow.users.get_by_id(int(user_id))

        if not current_user:
            raise InvalidCredentialsError()

        return UserResponse.model_validate(current_user)