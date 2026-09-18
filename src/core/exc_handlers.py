from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .exceptions import RoomAlreadyExistsError

async def room_alredy_exists(request, exc):
    return JSONResponse(status_code=409, content={'detail': 'room alredy exists'})

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RoomAlreadyExistsError, room_alredy_exists)