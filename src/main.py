from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.rooms.routers import router as room_router
from apps.bookings.routers import router as booking_router
from apps.users.routers import router as user_router
from core.exc_handlers import setup_exception_handlers

app = FastAPI(
    title='Hotel Booking API',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router=room_router)
app.include_router(router=booking_router)
app.include_router(router=user_router)

setup_exception_handlers(app)
