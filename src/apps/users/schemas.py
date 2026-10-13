from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class UserLogin(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(max_length=255)

class UserRegister(UserLogin):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CurrentUser(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    