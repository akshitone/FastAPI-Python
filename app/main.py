from fastapi import FastAPI, Response, status
from fastapi.exceptions import HTTPException
# from fastapi.params import Body

from model.post import Post
from util.posts import add_post, find_post, modify_post, posts

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project!"}


@app.get("/posts")
def get_posts():
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    add_post(post)  # add new post to list
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
        # raise exception with custom status code and message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post = find_post(post_id)  # find post
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    posts.remove(post)  # remove post from list


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    updated_post = modify_post(post_id, post)  # update post
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return {"message": f"Successfully updated {post.title}"}
