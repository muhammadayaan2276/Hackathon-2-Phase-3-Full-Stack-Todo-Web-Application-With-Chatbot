from fastapi import APIRouter, Depends, HTTPException, status
from middleware.jwt_middleware import create_access_token, create_refresh_token, decode_token_without_validation
from typing import Dict
import uuid
from datetime import datetime

router = APIRouter()

# In-memory storage for revoked tokens (in production, use Redis or database)
revoked_tokens = {}

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh the access token using a refresh token"""
    try:
        # Decode the refresh token without validation to get its data
        payload = decode_token_without_validation(refresh_token)
        
        # Check if the token type is refresh
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Check if the refresh token is expired
        exp = payload.get("exp")
        if exp and datetime.now().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Check if the refresh token has been revoked
        jti = payload.get("jti")
        if jti and revoked_tokens.get(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )
        
        # Create new access token with the same user data
        new_access_data = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "aud": "todo-app",
            "iss": "todo-app-auth-service"
        }
        
        new_access_token = create_access_token(data=new_access_data)
        
        # Optionally, create a new refresh token (token rotation)
        new_refresh_data = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "aud": "todo-app",
            "iss": "todo-app-auth-service"
        }
        
        new_refresh_token = create_refresh_token(data=new_refresh_data)
        
        # Revoke the old refresh token (if using token rotation)
        if jti:
            revoked_tokens[jti] = {
                "revoked_at": datetime.now().isoformat(),
                "reason": "token_rotation"
            }
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not refresh token: {str(e)}"
        )

@router.post("/revoke")
async def revoke_token(refresh_token: str):
    """Revoke a refresh token"""
    try:
        # Decode the refresh token without validation to get its jti
        payload = decode_token_without_validation(refresh_token)
        
        jti = payload.get("jti") or str(uuid.uuid4())
        
        # Store the revoked token
        revoked_tokens[jti] = {
            "revoked_at": datetime.now().isoformat(),
            "reason": "user_logout"
        }
        
        return {"message": "Token successfully revoked"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not revoke token: {str(e)}"
        )