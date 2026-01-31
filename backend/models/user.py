from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserInDB(UserBase):
    id: str
    createdAt: datetime
    updatedAt: datetime
    emailVerified: bool
    role: UserRole = UserRole.USER

class User(UserInDB):
    hashed_password: str