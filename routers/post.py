from fastapi import status, Depends, APIRouter, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from schema.post import PostLikeResponse, PostRequest, PostResponse

import util.models as models
from util.database import get_db
from util.oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=['Posts'])

POST = models.Post
LIKE = models.Like


@router.get("", response_model=List[PostLikeResponse])
# auth_user is a dependency which will be passed to this function and it will be used to get user id
# that is used for authorization
def get_posts(db: Session = Depends(get_db), auth_user=Depends(get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    # get limited number of posts in descending order of creation time
    # offset is used to skip number of posts
    # posts = db.query(POST).\
    #     filter(POST.user_id == auth_user.id).\
    #     filter(POST.title.contains(search)).\
    #     order_by(POST.created_at.desc()).\
    #     limit(limit).offset(offset).all()

    posts_with_likes = db.query(POST, func.count(LIKE.post_id).label("likes")).\
        filter(POST.user_id == auth_user.id).\
        filter(POST.title.contains(search)).\
        join(LIKE, POST.id == LIKE.post_id, isouter=True).\
        group_by(POST.id).\
        order_by(POST.created_at.desc()).\
        limit(limit).offset(offset).all()

    return posts_with_likes


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostRequest, db: Session = Depends(get_db), auth_user=Depends(get_current_user)):
    # set user_id to the current user id and post data to the database
    post = POST(user_id=auth_user.id, **post.dict())
    db.add(post)  # add to session
    db.commit()  # commit to database
    db.refresh(post)  # refresh post from database
    return post


@router.get("/{post_id}", response_model=PostLikeResponse)
def get_post(post_id: int, db: Session = Depends(get_db), auth_user=Depends(get_current_user)):
    post = db.query(POST, func.count(LIKE.post_id).label("likes")).\
        filter(POST.id == post_id).\
        join(LIKE, POST.id == LIKE.post_id, isouter=True).\
        group_by(POST.id).first()

    if not post:
        # raise exception with custom status code and message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), auth_user=Depends(get_current_user)):
    post_query = db.query(POST).filter(POST.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.user_id != auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this post"
        )

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, updated_post: PostRequest, db: Session = Depends(get_db), auth_user=Depends(get_current_user)):
    post_query = db.query(POST).filter(POST.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.user_id != auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this post"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()

    return updated_post
