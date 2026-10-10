from fastapi import APIRouter
from .deps import user_service, login_form
from .schemas import UserLogin, UserRegister

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.post('/login')
async def login(service: user_service, form: login_form):
    user_data = UserLogin(
        email=form.username, 
        password=form.password
    )
    return await service.authenticate_user(user_data)

@router.post('/register')
async def create_user(service: user_service, user_data: UserRegister):
    return await service.create_user(user_data)