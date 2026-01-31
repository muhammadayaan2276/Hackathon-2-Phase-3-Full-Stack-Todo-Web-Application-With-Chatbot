from sqlmodel import SQLModel
from typing import Optional


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None