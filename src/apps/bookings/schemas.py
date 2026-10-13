from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from apps.rooms.schemas import RoomResponse

class BookingCreate(BaseModel):
    room_id: int
    check_in_date: date
    check_out_date: date

class BookingResponse(BaseModel):
    id: int
    user_id: int
    check_in_date: date
    check_out_date: date
    created_at: datetime
    room: RoomResponse

    model_config = ConfigDict(from_attributes=True)

class BookingFilters(BaseModel):
    user_id: Optional[int] = Field(default=None)
    room_id: Optional[int] = Field(default=None)