from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .exceptions import RoomAlreadyExistsError, RoomNotFoundError, EmptyRequestForUpdateError

async def room_alredy_exists(request, exc):
    return JSONResponse(status_code=409, content={'detail': 'room alredy exists'})

async def room_not_found(request, exc):
    return JSONResponse(status_code=404, content={'detail': 'room not found'})

async def empty_request(request, exc):
    return JSONResponse(status_code=400, content={'detail': 'empty update request'})

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RoomAlreadyExistsError, room_alredy_exists)
    app.add_exception_handler(RoomNotFoundError, room_not_found)
    app.add_exception_handler(EmptyRequestForUpdateError, empty_request)