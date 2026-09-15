from fastapi import FastAPI
from apps.rooms.routers import router as room_router

app = FastAPI()

app.include_router(router=room_router)