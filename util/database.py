from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://root:root@172.19.0.1/fastapi"

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
