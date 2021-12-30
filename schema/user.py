from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str


class UserLogin(User):
    pass


class UserRequest(User):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserTokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserTokenRequest(BaseModel):
    id: Optional[str] = None
