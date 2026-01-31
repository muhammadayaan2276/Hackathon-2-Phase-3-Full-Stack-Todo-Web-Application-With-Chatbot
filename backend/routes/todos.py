from fastapi import APIRouter, Depends, HTTPException, status, Body
from middleware.jwt_middleware import verify_jwt_token
from typing import Dict, List
import uuid

# Import the proper models and services - using absolute imports from the project root
from src.models.task import Task
from src.models.task_create import TaskCreate, TaskUpdate
from src.services.task_service import create_task, get_tasks_for_user, update_task, delete_task, toggle_task_completion
from src.database import get_session
from sqlmodel import Session

router = APIRouter()

# Service function to verify user ownership of tasks
def verify_user_owns_task(user_id: str, task_user_id: str) -> bool:
    """Verify that the authenticated user owns the task"""
    return user_id == task_user_id

@router.get("/users/{user_id}/todos", response_model=List[Task])
async def get_user_todos(user_id: str, payload: Dict = Depends(verify_jwt_token), session: Session = Depends(get_session)):
    """Retrieve user's todos"""
    # Verify that the authenticated user matches the requested user_id
    if payload.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Fetch the user's todos from the database
    todos = await get_tasks_for_user(session, user_uuid)
    return todos

@router.post("/users/{user_id}/todos", response_model=Task)
async def create_user_todo(user_id: str, task_data: TaskCreate, payload: Dict = Depends(verify_jwt_token), session: Session = Depends(get_session)):
    """Create a new todo for the user"""
    # Verify that the authenticated user matches the requested user_id
    if payload.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    # Convert user_id string to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Create a new todo in the database with user-provided title and description
    todo = await create_task(session, task_data, user_uuid)
    return todo

@router.put("/users/{user_id}/todos/{todo_id}", response_model=Task)
async def update_user_todo(user_id: str, todo_id: str, todo_data: TaskUpdate, payload: Dict = Depends(verify_jwt_token), session: Session = Depends(get_session)):
    """Update a specific todo"""
    # Verify that the authenticated user matches the requested user_id
    if payload.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    # Convert IDs to UUIDs
    try:
        user_uuid = uuid.UUID(user_id)
        todo_uuid = uuid.UUID(todo_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

    # Update the todo in the database with user-provided data
    updated_todo = await update_task(
        session,
        todo_uuid,
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed
    )

    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return updated_todo

@router.delete("/users/{user_id}/todos/{todo_id}")
async def delete_user_todo(user_id: str, todo_id: str, payload: Dict = Depends(verify_jwt_token), session: Session = Depends(get_session)):
    """Delete a specific todo"""
    # Verify that the authenticated user matches the requested user_id
    if payload.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    # Convert IDs to UUIDs
    try:
        user_uuid = uuid.UUID(user_id)
        todo_uuid = uuid.UUID(todo_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

    # Delete the todo from the database
    success = await delete_task(session, todo_uuid)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return {"message": f"Todo {todo_id} successfully deleted"}

@router.put("/users/{user_id}/todos/{todo_id}/toggle", response_model=Task)
async def toggle_user_todo(user_id: str, todo_id: str, payload: Dict = Depends(verify_jwt_token), session: Session = Depends(get_session)):
    """Toggle completion status of a todo"""
    # Verify that the authenticated user matches the requested user_id
    if payload.get("sub") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    # Convert IDs to UUIDs
    try:
        user_uuid = uuid.UUID(user_id)
        todo_uuid = uuid.UUID(todo_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

    # Toggle the completion status in the database
    toggled_todo = await toggle_task_completion(session, todo_uuid)

    if not toggled_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return toggled_todo