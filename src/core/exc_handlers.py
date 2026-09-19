from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .exceptions import RoomAlreadyExistsError, RoomNotFoundError

async def room_alredy_exists(request, exc):
    return JSONResponse(status_code=409, content={'detail': 'room alredy exists'})

async def room_not_found(request, exc):
    return JSONResponse(status_code=404, content={'detail': 'room not found'})

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RoomAlreadyExistsError, room_alredy_exists)
    app.add_exception_handler(RoomNotFoundError, room_not_found)