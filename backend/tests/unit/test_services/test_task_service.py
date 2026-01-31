import pytest
from unittest.mock import MagicMock
from sqlmodel import Session
from backend.src.models.task import Task, TaskBase
from backend.src.services.task_service import create_task
import uuid


def test_create_task():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Create test data
    user_id = uuid.uuid4()
    task_data = TaskBase(
        title="Test Task",
        description="This is a test task",
        completed=False,
        user_id=user_id
    )
    
    # Call the function
    result = create_task(mock_session, task_data, user_id)
    
    # Assertions
    assert isinstance(result, Task)
    assert result.title == "Test Task"
    assert result.description == "This is a test task"
    assert result.completed is False
    assert result.user_id == user_id
    
    # Verify session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()