from typing import List
from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException

from schema.post import PostCreate, PostResponse

import util.models as models
from util.database import get_db, engine
from sqlalchemy.orm import Session

# Create tables if not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project!"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**post.dict())
    db.add(post)  # add to session
    db.commit()  # commit to database
    db.refresh(post)  # refresh post from database
    return post


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        # raise exception with custom status code and message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    post.delete(synchronize_session=False)
    db.commit()


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
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
