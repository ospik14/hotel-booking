from pydantic import BaseModel, Field
from typing import Optional

class RoomCreate(BaseModel):
    name: str = Field(max_length=255)
    capacity: int = Field(gt=0)

class RoomResponse(RoomCreate):
    id: int

    class Config:
        from_attributes = True

class RoomFilters(BaseModel):
    name_contains: Optional[str] = Field(default=None)
    capacity_gte: Optional[int] = Field(default=None)
    capacity_lte: Optional[int] = Field(default=None)

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    capacity: Optional[str] = Field(default=None)