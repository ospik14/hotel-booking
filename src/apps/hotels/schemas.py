from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class HotelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)

class HotelResponse(HotelCreate):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
