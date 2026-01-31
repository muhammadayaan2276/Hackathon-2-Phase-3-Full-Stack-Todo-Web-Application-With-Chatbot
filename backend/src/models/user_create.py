from sqlmodel import SQLModel
from typing import Optional


class UserBase(SQLModel):
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None