from fastapi import FastAPI, Response, status
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
def create_post(post: Post, response: Response):
    add_post(post)  # add new post to list
    response.status_code = status.HTTP_201_CREATED  # set response status code
    return {"message": f"Successfully created {post.title}"}


# Optional function
@app.get("/posts/latest")
def get_latest_posts():
    latest_post_id = posts[-1]["id"]  # get id of last post
    return find_post(latest_post_id)


@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    post = find_post(post_id)  # find post
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND  # set status code
        return {"message": f"Post with id {post_id} not found"}
    return post
