from pydantic import BaseModel
from pydantic.types import conint


class LikeRequest(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1)  # 0: like, 1: dislike
