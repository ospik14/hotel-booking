from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date
from core.exceptions import IncompleteDataError

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
    check_in: Optional[date] = Field(default=None)
    check_out: Optional[date] = Field(default=None)

    @model_validator(mode='after')
    def check_both_or_none(self):
        if (self.check_in is None) != (self.check_out is None):
            raise IncompleteDataError

        return self

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    capacity: Optional[int] = Field(default=None)