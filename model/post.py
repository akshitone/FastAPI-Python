from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    rating: Optional[int] = None  # default value
