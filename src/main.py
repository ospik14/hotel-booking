from fastapi import FastAPI
from apps.rooms.routers import router as room_router
from core.exc_handlers import setup_exception_handlers

app = FastAPI()

app.include_router(router=room_router)

setup_exception_handlers(app)
