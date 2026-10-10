from fastapi import FastAPI
from apps.rooms.routers import router as room_router
from apps.bookings.routers import router as booking_router
from apps.users.routers import router as user_router
from core.exc_handlers import setup_exception_handlers

app = FastAPI()

app.include_router(router=room_router)
app.include_router(router=booking_router)
app.include_router(router=user_router)

setup_exception_handlers(app)
