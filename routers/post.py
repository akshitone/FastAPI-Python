from fastapi import status, Depends, APIRouter, HTTPException
from typing import List
from sqlalchemy.orm import Session

from schema.post import PostRequest, PostResponse

import util.models as models
from util.database import get_db
from util.oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("", response_model=List[PostResponse])
# auth_user is a dependency which will be passed to this function and it will be used to get user id
# that is used for authorization
def get_posts(db: Session = Depends(get_db), auth_user: int = Depends(get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostRequest, db: Session = Depends(get_db), auth_user: int = Depends(get_current_user)):
    post = models.Post(**post.dict())
    db.add(post)  # add to session
    db.commit()  # commit to database
    db.refresh(post)  # refresh post from database
    return post


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), auth_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        # raise exception with custom status code and message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), auth_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post.delete(synchronize_session=False)
    db.commit()


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, updated_post: PostRequest, db: Session = Depends(get_db), auth_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post.first()

    return updated_post
