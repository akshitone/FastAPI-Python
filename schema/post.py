from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value


# only the fields that are required from request
class PostCreate(Post):
    pass


# only the fields that are returned as response
class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
