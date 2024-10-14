from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    is_active: bool
    created_at: datetime
    id: int


class LoginResponse(UserResponse):
    access_token: str
    token_type: str
