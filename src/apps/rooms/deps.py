from fastapi import Depends
from typing import Annotated
from .services import RoomService
from core.global_deps import get_uow
from core.db.uow import UnitOfWork

def get_room_service(
    uow: Annotated[UnitOfWork, Depends(get_uow)]
) -> RoomService:
    return RoomService(uow=uow)

room_service = Annotated[RoomService, Depends(get_room_service)]