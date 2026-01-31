import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.src.models.task import Task, TaskBase
from backend.src.services.task_service import update_task, create_task
import uuid


def test_update_task_success():
    # Mock session
    mock_session = MagicMock(spec=Session)

    # Create a mock task to return from get_task_by_id
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    existing_task = Task(
        id=task_id,
        title="Old Title",
        description="Old Description",
        completed=False,
        user_id=user_id
    )

    # Mock the get_task_by_id function to return the existing task
    with patch('backend.src.services.task_service.get_task_by_id', return_value=existing_task):
        # Call the update function
        updated_task = update_task(
            mock_session,
            task_id,
            title="New Title",
            description="New Description",
            completed=True
        )

        # Assertions
        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed is True


def test_update_task_not_found():
    # Mock session
    mock_session = MagicMock(spec=Session)

    # Mock the get_task_by_id function to return None (task not found)
    with patch('backend.src.services.task_service.get_task_by_id', return_value=None):
        # Call the update function
        result = update_task(
            mock_session,
            uuid.uuid4(),
            title="New Title"
        )

        # Assertions
        assert result is None