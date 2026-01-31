import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.src.models.task import Task
from backend.src.services.task_service import delete_task
import uuid


def test_delete_task_success():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Create a mock task to return from get_task_by_id
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    existing_task = Task(
        id=task_id,
        title="Task to Delete",
        description="This task will be deleted", 
        completed=False,
        user_id=user_id
    )
    
    # Mock the get_task_by_id function to return the existing task
    with patch('backend.src.services.task_service.get_task_by_id', return_value=existing_task):
        # Call the delete function
        result = delete_task(mock_session, task_id)
        
        # Assertions
        assert result is True
        mock_session.delete.assert_called_once_with(existing_task)
        mock_session.commit.assert_called_once()


def test_delete_task_not_found():
    # Mock session
    mock_session = MagicMock(spec=Session)
    
    # Mock the get_task_by_id function to return None (task not found)
    with patch('backend.src.services.task_service.get_task_by_id', return_value=None):
        # Call the delete function
        result = delete_task(mock_session, uuid.uuid4())
        
        # Assertions
        assert result is False
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()