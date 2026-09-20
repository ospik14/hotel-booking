from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    room_id: int
    booking_start_at: datetime
    booking_end_at: datetime
