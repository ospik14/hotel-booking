from pydantic import BaseModel, Field

class RoomCreate(BaseModel):
    name: str = Field(max_length=255)
    capacity: int

class RoomResponse(RoomCreate):
    id: int

    class Config:
        from_attributes = True