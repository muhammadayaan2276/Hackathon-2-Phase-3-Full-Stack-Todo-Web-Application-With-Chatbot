from sqlmodel import select, Session
from ..models.user import User
from ..models.user_create import UserCreate
from typing import Optional
import uuid
from datetime import datetime
from passlib.context import CryptContext
from ..config.settings import settings
from ..middleware.jwt_middleware import create_access_token, create_refresh_token


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


async def create_user(session: Session, user_create: UserCreate):
    """Create a new user in the database"""
    # Check if user already exists
    existing_user = await get_user_by_email(session, user_create.email)
    if existing_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user object
    user = User(
        email=user_create.email,
        name=getattr(user_create, 'name', ''),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        email_verified=False,  # In a real app, this would be verified via email
        hashed_password=hashed_password
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by their email address"""
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    return user


async def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    """Get a user by their ID"""
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    return user


async def authenticate_user(session: Session, email: str, password: str):
    """Authenticate a user with email and password"""
    user = await get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def generate_tokens(user: User):
    """Generate access and refresh tokens for a user"""
    # Create data to encode in the token
    access_data = {
        "sub": str(user.id),  # Convert UUID to string
        "email": user.email,
        "name": getattr(user, 'name', ''),
        "aud": "todo-app",
        "iss": "todo-app-auth-service"
    }

    refresh_data = {
        "sub": str(user.id),  # Convert UUID to string
        "email": user.email,
        "aud": "todo-app",
        "iss": "todo-app-auth-service"
    }

    # Create tokens
    access_token = create_access_token(data=access_data)
    refresh_token = create_refresh_token(data=refresh_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }