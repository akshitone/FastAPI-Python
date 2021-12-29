from fastapi import FastAPI

import util.models as models

from util.database import engine
from routers import user, post

# Create tables if not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project!"}
