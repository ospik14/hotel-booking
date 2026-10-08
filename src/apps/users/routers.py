from fastapi import APIRouter
from .deps import user_service

router = APIRouter(
    prefix='/users',
    tags='users'
)

async def login(service: user_service, user_login):
    return await service.login(user_login)