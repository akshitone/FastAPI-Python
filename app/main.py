from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import util.models as models

from util.database import engine
from routers import user, post, auth, like


# Create tables if not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]  # every origin is allowed

# add CORS support to the API server, it's used to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(like.router)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project!"}
