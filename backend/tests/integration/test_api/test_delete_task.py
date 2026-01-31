import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from unittest.mock import patch
import uuid


client = TestClient(app)


def test_delete_task():
    # Mock user ID and task ID for testing
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())
    
    # Mock the JWT middleware to simulate an authenticated user
    with patch('backend.src.middleware.auth_middleware.JWTBearer.__call__') as mock_jwt:
        mock_jwt.return_value = user_id
        
        # Make the request
        response = client.delete(f"/api/{user_id}/tasks/{task_id}")
        
        # Since the task doesn't exist, we expect a 404
        assert response.status_code == 404