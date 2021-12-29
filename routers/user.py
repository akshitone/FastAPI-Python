from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException

from schema.user import UserRequest, UserResponse

import util.models as models
from util.hashing import hash_password
from util.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
