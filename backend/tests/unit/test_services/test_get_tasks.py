import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.src.models.task import Task
from backend.src.services.task_service import get_tasks_for_user, get_task_by_id
import uuid


def test_get_tasks_for_user():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Create mock tasks
    user_id = uuid.uuid4()
    mock_task1 = Task(id=uuid.uuid4(), title="Task 1", user_id=user_id, completed=False)
    mock_task2 = Task(id=uuid.uuid4(), title="Task 2", user_id=user_id, completed=True)
    mock_tasks = [mock_task1, mock_task2]
    
    # Mock the exec method to return the mock tasks
    mock_session.exec.return_value.all.return_value = mock_tasks
    
    # Call the function
    result = get_tasks_for_user(mock_session, user_id)
    
    # Assertions
    assert len(result) == 2
    assert result[0].title == "Task 1"
    assert result[1].title == "Task 2"
    assert all(task.user_id == user_id for task in result)


def test_get_task_by_id_found():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Create mock task
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    mock_task = Task(id=task_id, title="Test Task", user_id=user_id, completed=False)
    
    # Mock the exec method to return the mock task
    mock_session.exec.return_value.first.return_value = mock_task
    
    # Call the function
    result = get_task_by_id(mock_session, task_id)
    
    # Assertions
    assert result is not None
    assert result.id == task_id
    assert result.title == "Test Task"


def test_get_task_by_id_not_found():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Mock the exec method to return None
    mock_session.exec.return_value.first.return_value = None
    
    # Call the function
    result = get_task_by_id(mock_session, uuid.uuid4())
    
    # Assertions
    assert result is None