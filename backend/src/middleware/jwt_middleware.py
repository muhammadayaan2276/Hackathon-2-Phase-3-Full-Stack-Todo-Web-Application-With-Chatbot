import os
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from typing import Dict
from datetime import datetime, timedelta
import json

# Get secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
# Don't raise an error at import time, check when function is called
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()

def create_access_token(data: dict):
    """
    Create an access token with 15-minute expiration
    """
    global SECRET_KEY
    SECRET_KEY = SECRET_KEY or os.getenv("BETTER_AUTH_SECRET")
    if not SECRET_KEY:
        raise ValueError("BETTER_AUTH_SECRET environment variable not set")

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Use timestamp() method for consistency
    to_encode.update({"exp": expire.timestamp(), "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Create a refresh token with 7-day expiration
    """
    global SECRET_KEY
    SECRET_KEY = SECRET_KEY or os.getenv("BETTER_AUTH_SECRET")
    if not SECRET_KEY:
        raise ValueError("BETTER_AUTH_SECRET environment variable not set")

    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    # Use timestamp() method for consistency
    to_encode.update({"exp": expire.timestamp(), "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict:
    """
    Verify JWT token and return decoded payload
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="todo-app")

        # Verify that the token is meant for this audience
        # aud = payload.get("aud")
        # if aud != "todo-app":
        #     raise HTTPException(status_code=401, detail=f"Invalid token audience: {aud}")

        # Verify the issuer
        # iss = payload.get("iss")
        # if iss != "todo-app-auth-service":
        #     raise HTTPException(status_code=401, detail=f"Invalid token issuer: {iss}")

        # Verify token type (access token)
        # token_type = payload.get("type")
        # if token_type != "access":
        #     raise HTTPException(status_code=401, detail=f"Invalid token type: {token_type}")

        # Check if token is expired
        exp = payload.get("exp")
        if exp:
            # Compare timestamps properly
            current_timestamp = datetime.now().timestamp()
            # Allow a small tolerance for clock differences
            # Only consider expired if current time is more than 1 second past expiration
            if current_timestamp - exp > 1:
                raise HTTPException(status_code=401, detail="Token has expired")

        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"JWT Error: {str(e)}")

def decode_token_without_validation(token: str) -> Dict:
    """
    Decode token without validation - only for extracting user info
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token format")