from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schema.like import LikeRequest

import util.models as models
from util.database import get_db
from util.oauth2 import get_current_user


router = APIRouter(prefix="/likes", tags=['Likes'])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_like(like: LikeRequest, db: Session = Depends(get_db), auth_user=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    like_query = db.query(models.Like).filter(models.Like.user_id == auth_user.id).\
        filter(models.Like.post_id == like.post_id)
    liked_post = like_query.first()

    if like.direction == 1:
        if liked_post:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already liked")

        like = models.Like(user_id=auth_user.id, post_id=like.post_id)
        db.add(like)
        db.commit()
        return {"message": "Liked"}
    else:
        if not liked_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")

        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Unliked"}
