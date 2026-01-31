from sqlmodel import select, Session
from ..models.task import Task, TaskBase
from ..models.task_create import TaskCreate
from typing import List, Optional
import uuid
from ..exceptions import TaskNotFoundException


async def create_task(session: Session, task_data: TaskCreate, user_id: uuid.UUID) -> Task:
    """
    Creates a new task in the database
    """
    from ..models.task import Task
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task_by_id(session: Session, task_id: uuid.UUID) -> Optional[Task]:
    """
    Retrieves a task by its ID
    """
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    return task


async def get_task_by_id_or_raise(session: Session, task_id: uuid.UUID) -> Task:
    """
    Retrieves a task by its ID or raises an exception if not found
    """
    task = await get_task_by_id(session, task_id)
    if not task:
        raise TaskNotFoundException(task_id)
    return task


async def get_tasks_for_user(session: Session, user_id: uuid.UUID, completed: Optional[bool] = None) -> List[Task]:
    """
    Retrieves all tasks for a specific user
    Optionally filter by completion status
    """
    statement = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    result = await session.execute(statement)
    tasks = result.scalars().all()
    return tasks


async def update_task(session: Session, task_id: uuid.UUID, title: str = None, description: str = None, completed: bool = None) -> Optional[Task]:
    """
    Updates an existing task
    """
    try:
        task = await get_task_by_id_or_raise(session, task_id)
        # Update task attributes with provided data
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    except TaskNotFoundException:
        return None


async def delete_task(session: Session, task_id: uuid.UUID) -> bool:
    """
    Deletes a task by its ID
    """
    try:
        task = await get_task_by_id_or_raise(session, task_id)
        session.delete(task)
        session.commit()
        return True
    except TaskNotFoundException:
        return False


async def toggle_task_completion(session: Session, task_id: uuid.UUID) -> Optional[Task]:
    """
    Toggles the completion status of a task
    """
    try:
        task = await get_task_by_id_or_raise(session, task_id)
        task.completed = not task.completed
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except TaskNotFoundException:
        return None