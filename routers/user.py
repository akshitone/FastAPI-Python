from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schema.user import UserRequest, UserResponse

import util.models as models
from util.hashing import hash_password
from util.database import get_db
from util.oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=['Users'])

USER = models.User


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    user = USER(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), auth_user: int = Depends(get_current_user)):
    user = db.query(USER).filter(USER.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
