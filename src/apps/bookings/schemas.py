from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime

class BookingResponse(BookingCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
