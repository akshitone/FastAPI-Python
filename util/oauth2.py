from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from jose import jwt, JWTError
from datetime import datetime, timedelta

from schema.user import UserTokenRequest

from util.database import get_db
from util.config import settings
import util.models as models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.fastapi_secret_key
ALGORITHM = settings.fastapi_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.fastapi_access_token_expire_minutes


def create_access_token(data: dict):
    # copy data to avoid modifying the original
    to_encode = data.copy()
    # add expire time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # add expire time to data
    to_encode.update({"exp": expire})
    # encode jwt token with secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# this method verify token and return user id
def verify_access_token(token: str, credentials_exception):
    try:
        # decode token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # get user id from token
        id: str = decoded_token.get("user_id")

        # if user id is not found
        if not id:
            # raise credentials exception
            raise credentials_exception

        # create token data
        token_data = UserTokenRequest(id=id)

    # if token is not valid
    except JWTError:
        raise credentials_exception

    return token_data


# this method get token from header and verify it
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # create credentials exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
