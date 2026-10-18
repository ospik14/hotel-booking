from fastapi import APIRouter, Depends, status
from .schemas import (
    BookingCreate,
    BookingResponse,
    BookingFilters,
    AdminBookingFilters,
    BookingStatusUpdate,
)
from .deps import booking_service
from apps.users.deps import current_user, current_admin

router = APIRouter(
    prefix='/booking',
    tags=['booking'],
)


@router.post(
    '/',
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    booking: BookingCreate,
    service: booking_service,
    user: current_user,
):
    return await service.create_booking(booking, user)


@router.get('/my/', response_model=list[BookingResponse])
async def get_bookings(
    service: booking_service,
    user: current_user,
    filters: BookingFilters = Depends(),
):
    return await service.get_bookings(user, filters)


@router.get('/', response_model=list[BookingResponse])
async def get_all_bookings(
    service: booking_service,
    user: current_admin,
    filters: AdminBookingFilters = Depends(),
):
    return await service.get_admin_bookings(filters)


@router.get('/{id}/', response_model=BookingResponse)
async def get_booking(
    id: int,
    service: booking_service,
    user: current_user,
):
    return await service.get_booking(id, user)


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    service: booking_service,
    id: int,
    user: current_user,
):
    await service.cancel_booking(id, user)


@router.patch('/{id}/status/', response_model=BookingResponse)
async def update_booking_status(
    id: int,
    status_update: BookingStatusUpdate,
    service: booking_service,
    user: current_admin,
):
    return await service.update_status(id, status_update)
