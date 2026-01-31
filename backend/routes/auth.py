from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Optional
from src.models.user_create import UserCreate
from src.services.user_service import create_user, get_user_by_email, authenticate_user, generate_tokens
from middleware.jwt_middleware import verify_jwt_token
from src.database import get_session
from sqlmodel import Session

router = APIRouter()
security = HTTPBearer()

@router.post("/signup")
async def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user account"""
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(session, user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create the new user
        user = await create_user(session, user_create)

        # Generate tokens for the new user
        tokens = generate_tokens(user)

        # In a real application, we would set HttpOnly cookies here
        # For now, we'll return the tokens in the response
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
            "user": {
                "id": str(user.id),  # Convert UUID to string
                "email": user.email,
                "name": user.name,
                "createdAt": user.created_at.isoformat() if hasattr(user.created_at, 'isoformat') else str(user.created_at),
                "updatedAt": user.updated_at.isoformat() if hasattr(user.updated_at, 'isoformat') else str(user.updated_at),
                "emailVerified": user.email_verified
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/signin")
async def signin(user_create: UserCreate, session: Session = Depends(get_session)):
    """Authenticate existing user"""
    email = user_create.email
    password = user_create.password

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    # Authenticate the user
    user = await authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate tokens for the authenticated user
    tokens = generate_tokens(user)

    # In a real application, we would set HttpOnly cookies here
    # For now, we'll return the tokens in the response
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user": {
            "id": str(user.id),  # Convert UUID to string
            "email": user.email,
            "name": user.name,
            "createdAt": user.created_at.isoformat() if hasattr(user.created_at, 'isoformat') else str(user.created_at),
            "updatedAt": user.updated_at.isoformat() if hasattr(user.updated_at, 'isoformat') else str(user.updated_at),
            "emailVerified": user.email_verified
        }
    }

@router.post("/signout")
async def signout(credentials=Depends(security)):
    """Invalidate current session"""
    # In a real application, we would invalidate the refresh token here
    # For now, we'll just return a success message
    return {"message": "Successfully signed out"}