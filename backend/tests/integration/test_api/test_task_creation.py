import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database import engine
from sqlmodel import Session, SQLModel
from unittest.mock import patch
import uuid


client = TestClient(app)


def test_create_task_integration():
    # Mock user ID for testing
    user_id = str(uuid.uuid4())
    
    # Mock the JWT middleware to simulate an authenticated user
    with patch('backend.src.middleware.auth_middleware.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = user_id
        
        # Prepare test data
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False,
            "user_id": user_id
        }
        
        # Make the request
        response = client.post(
            f"/api/{user_id}/tasks",
            json=task_data
        )
        
        # Assertions
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "This is a test task"
        assert data["completed"] is False
        assert "id" in data