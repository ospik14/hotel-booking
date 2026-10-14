from pydantic.types import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from core.db.uow import UnitOfWork
from core.global_deps import get_uow
from .services import UserService
from .schemas import CurrentUser
from core.exceptions import AccessDeniedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

def get_user_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
):
    return UserService(uow=uow)

async def get_current_user(
        service: Annotated[UserService, Depends(get_user_service)],
        token: Annotated[str, Depends(oauth2_scheme)]
    ):
    return await service.verify_user(token)


user_service = Annotated[UserService, Depends(get_user_service)]
login_form = Annotated[OAuth2PasswordRequestForm, Depends()]
current_user = Annotated[CurrentUser, Depends(get_current_user)]

async def get_current_admin(user: current_user):
    if not user.role == 'admin':
        raise AccessDeniedError()

    return user

current_admin = Annotated[CurrentUser, Depends(get_current_admin)]