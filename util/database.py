from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from util.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.fastapi_db_username}:{settings.fastapi_db_password}@{settings.fastapi_db_port}/{settings.fastapi_db_name}"

# connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base class for all models
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
