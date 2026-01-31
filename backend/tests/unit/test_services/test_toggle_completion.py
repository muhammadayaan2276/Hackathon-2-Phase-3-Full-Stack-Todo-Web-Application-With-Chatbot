import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.src.models.task import Task
from backend.src.services.task_service import toggle_task_completion
import uuid


def test_toggle_task_completion_success():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Create a mock task to return from get_task_by_id
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    existing_task = Task(
        id=task_id,
        title="Task to Toggle",
        description="This task completion will be toggled", 
        completed=False,  # Initially not completed
        user_id=user_id
    )
    
    # Mock the get_task_by_id function to return the existing task
    with patch('backend.src.services.task_service.get_task_by_id', return_value=existing_task):
        # Call the toggle function
        result = toggle_task_completion(mock_session, task_id)
        
        # Assertions
        assert result is not None
        assert result.completed is True  # Should be toggled to True
        mock_session.add.assert_called_once_with(existing_task)
        mock_session.commit.assert_called_once()


def test_toggle_task_completion_not_found():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Mock the get_task_by_id function to return None (task not found)
    with patch('backend.src.services.task_service.get_task_by_id', return_value=None):
        # Call the toggle function
        result = toggle_task_completion(mock_session, uuid.uuid4())
        
        # Assertions
        assert result is None
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()