from datetime import datetime, timedelta
import hashlib
import base64
import os
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session
from config import get_settings
from models.models import User
from schemas.userschema import DecodedToken, UserCreate

ALGORITHM = "HS256"
SECRET_KEY = get_settings().secret_key
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_user(db: Session, user_create: UserCreate):
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", user_create.password.encode(), salt, 1000
    ).hex()
    new_user = User(
        username=user_create.username,
        password=hashed_password,
        salt=salt.decode(),
    )
    db.add(new_user)
    db.commit()
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).one_or_none()
    if not user:
        return False
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), user.salt.encode(), 1000
    ).hex()
    if user.password != hashed_password:
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return DecodedToken(username=username, user_id=user_id)
    except ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token has expired") from exc
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
