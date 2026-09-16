from fastapi import Depends
from typing import Annotated
from .services import RoomService
from .repositories import RoomRepository
from core.db.session import session_maker
from core.db.uow import UnitOfWork

def get_uow() -> UnitOfWork:
    return UnitOfWork(session_maker=session_maker)

def get_room_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> RoomService:
    return RoomService(uow=uow)

room_service = Annotated[RoomService, Depends(get_room_service)]