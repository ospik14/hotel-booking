from datetime import timedelta
from core.db.uow import UnitOfWork
from .schemas import (
    UserLogin,
    UserRegister,
    UserResponse,
    CurrentUser,
    UserUpdate,
    ChangePasswordRequest,
)
from .models import Role
from core.exceptions import InvalidCredentialsError, WrongPasswordError
from core.security import verify_password, create_token, hash_password, decode_token
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def authenticate_user(self, user_data: UserLogin):
        async with self.uow as uow:
            user = await uow.users.get_by_email(user_data.email)

        if user is None or not user.is_active:
            raise InvalidCredentialsError()

        if not verify_password(user.hashed_password, user_data.password):
            raise InvalidCredentialsError()

        token_data = {
            'sub': str(user.id),
            'type': 'access',
        }
        token = create_token(
            token_data,
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return {
            'access_token': token,
            'token_type': 'bearer',
        }

    async def create_user(self, user_data: UserRegister):
        hashed_password = hash_password(user_data.password)

        async with self.uow as uow:
            user = await uow.users.create(
                {
                    'first_name': user_data.first_name,
                    'last_name': user_data.last_name,
                    'email': user_data.email,
                    'hashed_password': hashed_password,
                    'role': Role.USER,
                }
            )

        return UserResponse.model_validate(user)

    async def verify_user(self, token: str):
        try:
            token_payload = decode_token(token)
        except ValueError as exc:
            raise InvalidCredentialsError() from exc

        if token_payload.get('type') != 'access':
            raise InvalidCredentialsError()

        user_id = token_payload.get('sub')
        async with self.uow as uow:
            current_user = await uow.users.get_by_id(int(user_id))

        if not current_user or not current_user.is_active:
            raise InvalidCredentialsError()

        return CurrentUser.model_validate(current_user)

    async def get_me(self, user: CurrentUser) -> UserResponse:
        async with self.uow as uow:
            db_user = await uow.users.get_by_id(user.id)

        if not db_user:
            raise InvalidCredentialsError()

        return UserResponse.model_validate(db_user)

    async def update_me(self, user: CurrentUser, data: UserUpdate) -> UserResponse:
        async with self.uow as uow:
            db_user = await uow.users.update_profile(user.id, data)

        return UserResponse.model_validate(db_user)

    async def change_password(
        self,
        user: CurrentUser,
        data: ChangePasswordRequest,
    ) -> None:
        async with self.uow as uow:
            db_user = await uow.users.get_by_id(user.id)
            if not db_user:
                raise InvalidCredentialsError()

            if not verify_password(db_user.hashed_password, data.current_password):
                raise WrongPasswordError()

            await uow.users.update_password(
                user.id,
                hash_password(data.new_password),
            )

    async def create_admin(self, user_data: UserRegister) -> UserResponse:
        """Internal/script helper — not exposed via public API."""
        hashed_password = hash_password(user_data.password)

        async with self.uow as uow:
            user = await uow.users.create(
                {
                    'first_name': user_data.first_name,
                    'last_name': user_data.last_name,
                    'email': user_data.email,
                    'hashed_password': hashed_password,
                    'role': Role.ADMIN,
                }
            )

        return UserResponse.model_validate(user)
