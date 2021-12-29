from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str


class UserRequest(User):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
