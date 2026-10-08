from pydantic.types import Annotated
from fastapi import Depends
from core.db.uow import UnitOfWork
from core.global_deps import get_uow
from .services import UserService

def get_user_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
):
    return UserService(uow=uow)

user_service = Annotated[UserService, Depends(get_user_service)]