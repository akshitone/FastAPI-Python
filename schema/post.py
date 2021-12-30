from pydantic import BaseModel
from datetime import datetime

from schema.user import UserResponse


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value


# only the fields that are required from request
class PostRequest(Post):
    pass


# only the fields that are returned as response
class PostResponse(Post):
    id: int
    # user_id: int
    user: UserResponse  # many-to-one relationship with User
    created_at: datetime

    class Config:
        orm_mode = True
