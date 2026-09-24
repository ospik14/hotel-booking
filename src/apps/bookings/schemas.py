from typing import Optional

from pydantic import BaseModel, Field
from datetime import date, datetime

class BookingCreate(BaseModel):
    room_id: int
    check_in_date: date
    check_out_date: date

class BookingResponse(BookingCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BookingFilters(BaseModel):
    user_id: Optional[int] = Field(default=None)
    room_id: Optional[int] = Field(default=None)