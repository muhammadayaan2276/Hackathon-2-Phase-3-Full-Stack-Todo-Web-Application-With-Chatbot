from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import List
from ..models.task import Task
from ..models.task_create import TaskCreate, TaskUpdate
from ..services.task_service import create_task, get_task_by_id, get_tasks_for_user, update_task, delete_task, toggle_task_completion
from ..database import get_session
from ..middleware.auth_middleware import JWTBearer
from ..exceptions import TaskNotFoundException, UnauthorizedAccessException
import uuid


task_router = APIRouter()


@task_router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    request: Request,
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    # Get user_id from the request state (set by JWT middleware)
    user_id = request.state.user_id
    task = create_task(session, task_data, user_id)
    return task


@task_router.get("/tasks", response_model=List[Task])
async def get_user_tasks(
    request: Request,
    completed: bool = None,
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user
    Optionally filter by completion status
    """
    user_id = request.state.user_id
    tasks = get_tasks_for_user(session, user_id, completed)
    return tasks


@task_router.get("/tasks/{id}", response_model=Task)
async def get_specific_task(
    id: uuid.UUID,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user
    """
    user_id = request.state.user_id
    task = get_task_by_id(session, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return task


@task_router.put("/tasks/{id}", response_model=Task)
async def update_existing_task(
    id: uuid.UUID,
    task_data: TaskUpdate,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the authenticated user
    """
    user_id = request.state.user_id
    task = get_task_by_id(session, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    updated_task = update_task(
        session,
        id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@task_router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(
    id: uuid.UUID,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the authenticated user
    """
    user_id = request.state.user_id
    task = get_task_by_id(session, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    success = delete_task(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return


@task_router.patch("/tasks/{id}/complete", response_model=Task)
async def toggle_completion(
    id: uuid.UUID,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    user_id = request.state.user_id
    task = get_task_by_id(session, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the authenticated user
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    toggled_task = toggle_task_completion(session, id)
    if not toggled_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return toggled_task