from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from services import RoomsService
from repositories import RoomsRepositories
from core.db.session import get_session

def get_rooms_repositories(
    session = Annotated(AsyncSession, Depends(get_session))
):
    return RoomsRepositories(session=session)

def get_rooms_service(
    repo = Annotated[RoomsRepositories, Depends(get_rooms_repositories)]
):
    return RoomsService(repo=repo)

rooms_service = Annotated[RoomsService, Depends(get_rooms_service)]