from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
# from fastapi.params import Body

from util.db_connect import CURSOR, CONN
from model.post import Post
# from util.posts import add_post, find_post, modify_post, posts

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project!"}


@app.get("/posts")
def get_posts():
    CURSOR.execute("SELECT * FROM posts")
    posts = CURSOR.fetchall()  # it returns a list of dicts from DB
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    CURSOR.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    CONN.commit()  # save changes to DB without it the new post will not be saved
    post = CURSOR.fetchone()  # get the new post from DB
    return {"message": f"Successfully created {post['title']}"}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    CURSOR.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = CURSOR.fetchone()
    if not post:
        # raise exception with custom status code and message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    CURSOR.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
    CONN.commit()
    deleted_post = CURSOR.fetchone()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    CURSOR.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, post_id))
    CONN.commit()
    updated_post = CURSOR.fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return {"message": f"Successfully updated {updated_post['title']}"}
