from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class RoomCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    capacity: int = Field(gt=0)
    price_per_night: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    is_active: bool = True


class RoomResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    capacity: int
    price_per_night: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoomFilters(BaseModel):
    name_contains: Optional[str] = Field(default=None)
    capacity_gte: Optional[int] = Field(default=None, gt=0)
    capacity_lte: Optional[int] = Field(default=None, gt=0)
    price_gte: Optional[Decimal] = Field(default=None, ge=0)
    price_lte: Optional[Decimal] = Field(default=None, ge=0)
    guests: Optional[int] = Field(default=None, gt=0)
    is_active: Optional[bool] = Field(default=None)
    check_in: Optional[date] = Field(default=None)
    check_out: Optional[date] = Field(default=None)
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @model_validator(mode='after')
    def check_both_or_none(self):
        if (self.check_in is None) != (self.check_out is None):
            raise ValueError('both check_in and check_out must be provided together')
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValueError('check_out must be after check_in')
        return self


class AvailableRoomsFilters(BaseModel):
    check_in: date
    check_out: date
    guests: Optional[int] = Field(default=None, gt=0)
    price_gte: Optional[Decimal] = Field(default=None, ge=0)
    price_lte: Optional[Decimal] = Field(default=None, ge=0)
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @model_validator(mode='after')
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError('check_out must be after check_in')
        return self


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    capacity: Optional[int] = Field(default=None, gt=0)
    price_per_night: Optional[Decimal] = Field(
        default=None, ge=0, max_digits=10, decimal_places=2
    )
    is_active: Optional[bool] = Field(default=None)
