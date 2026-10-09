from fastapi import APIRouter
from .deps import user_service, login_form

router = APIRouter(
    prefix='/users',
    tags='users'
)

async def login(service: user_service, user_data: login_form):
    return await service.login(user_data)