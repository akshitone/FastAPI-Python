from typing import List
from fastapi import FastAPI
# from fastapi.params import Body

from model.post import Post
from util import add_post, find_post, posts

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project!"}


@app.get("/posts")
def get_posts():
    return posts


@app.post("/posts")
def create_post(post: Post):
    add_post(post)  # add new post to list
    return {"message": f"Successfully created {post.title}"}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = find_post(post_id)  # find post
    if post:
        return post
    return {"message": f"Post with id {post_id} not found"}
