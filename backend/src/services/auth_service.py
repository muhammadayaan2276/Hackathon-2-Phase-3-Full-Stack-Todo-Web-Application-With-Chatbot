import jwt
from datetime import datetime, timedelta
from ..config.settings import settings
from typing import Optional
import uuid


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_secret, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=[settings.algorithm])
        user_id: str = payload.get("user_id")
        if user_id is None:
            return None
        return uuid.UUID(user_id)
    except jwt.PyJWTError:
        return None