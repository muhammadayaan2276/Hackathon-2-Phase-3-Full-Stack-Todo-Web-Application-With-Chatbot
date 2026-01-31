import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("Testing signup endpoint...")

try:
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 500:
        print("Error details:", response.json())
except Exception as e:
    print(f"Exception occurred: {e}")
    import traceback
    traceback.print_exc()