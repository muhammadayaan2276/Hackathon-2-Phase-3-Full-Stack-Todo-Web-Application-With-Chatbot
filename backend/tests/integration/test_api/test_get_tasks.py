import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from unittest.mock import patch
import uuid


client = TestClient(app)


def test_get_user_tasks():
    # Mock user ID for testing
    user_id = str(uuid.uuid4())
    
    # Mock the JWT middleware to simulate an authenticated user
    with patch('backend.src.middleware.auth_middleware.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = user_id
        
        # Make the request
        response = client.get(f"/api/{user_id}/tasks")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        # The response will be an empty list since no tasks exist yet
        assert isinstance(data, list)


def test_get_specific_task():
    # Mock user ID and task ID for testing
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    
    # Mock the JWT middleware to simulate an authenticated user
    with patch('backend.src.middleware.auth_middleware.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = user_id
        
        # Make the request
        response = client.get(f"/api/{user_id}/tasks/{task_id}")
        
        # Since the task doesn't exist, we expect a 404
        assert response.status_code == 404