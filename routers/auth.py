from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schema.user import UserTokenResponse

import util.models as models
from util.hashing import verify_password
from util.database import get_db
from util.oauth2 import create_access_token


router = APIRouter(prefix="/auth", tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserTokenResponse)
# OAuth2PasswordRequestForm is a class from fastapi.security. It is a wrapper for the data
# It will convert email to username and it required data using form not json
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    def invalid_credential_exception():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user:
        raise invalid_credential_exception()

    if not verify_password(user_credentials.password, user.password):
        raise invalid_credential_exception()

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
