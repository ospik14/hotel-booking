from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .services import RoomService
from .repositories import RoomRepository
from core.db.session import get_session

def get_room_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
):
    return RoomRepository(session=session)

def get_room_service(
    repo: Annotated[RoomRepository, Depends(get_room_repository)]
):
    return RoomService(repo=repo)

room_service = Annotated[RoomService, Depends(get_room_service)]