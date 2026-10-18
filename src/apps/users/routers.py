from fastapi import APIRouter, status
from .deps import user_service, login_form, current_user
from .schemas import (
    UserLogin,
    UserRegister,
    UserResponse,
    UserUpdate,
    ChangePasswordRequest,
    Token,
)

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('/login', response_model=Token)
async def login(service: user_service, form: login_form):
    user_data = UserLogin(
        email=form.username,
        password=form.password,
    )
    return await service.authenticate_user(user_data)


@router.post(
    '/register',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(service: user_service, user_data: UserRegister):
    return await service.create_user(user_data)


@router.get('/me/', response_model=UserResponse)
async def get_me(service: user_service, user: current_user):
    return await service.get_me(user)


@router.patch('/me/', response_model=UserResponse)
async def update_me(
    service: user_service,
    user: current_user,
    data: UserUpdate,
):
    return await service.update_me(user, data)


@router.post(
    '/change-password/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_password(
    service: user_service,
    user: current_user,
    data: ChangePasswordRequest,
):
    await service.change_password(user, data)
