from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import date, datetime
from decimal import Decimal
from apps.rooms.schemas import RoomResponse
from apps.bookings.models import BookingStatus


class BookingCreate(BaseModel):
    room_id: int = Field(gt=0)
    check_in_date: date
    check_out_date: date
    guests: int = Field(gt=0)

    @model_validator(mode='after')
    def validate_dates(self):
        if self.check_out_date <= self.check_in_date:
            raise ValueError('check_out_date must be after check_in_date')
        return self


class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    guests: int
    status: BookingStatus
    price_per_night: Decimal
    total_price: Decimal
    created_at: datetime
    updated_at: datetime
    room: RoomResponse

    model_config = ConfigDict(from_attributes=True)


class BookingFilters(BaseModel):
    status: Optional[BookingStatus] = Field(default=None)
    room_id: Optional[int] = Field(default=None, gt=0)
    check_in_from: Optional[date] = Field(default=None)
    check_in_to: Optional[date] = Field(default=None)
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class AdminBookingFilters(BookingFilters):
    user_id: Optional[int] = Field(default=None, gt=0)


class BookingStatusUpdate(BaseModel):
    status: BookingStatus
