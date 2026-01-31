import os
import json
from datetime import datetime

# Set the environment variable
os.environ['BETTER_AUTH_SECRET'] = 'your-super-secret-key-here'

# Import the modules
from models.user import UserCreate
from services.user_service import UserService
from routes.auth import signup
import asyncio

# Create a test user
test_user = UserCreate(email="test@example.com", password="password123", name="Test User")

print(f"Test user created: {test_user}")

async def test_signup():
    try:
        result = await signup(test_user)
        print(f"Signup successful: {result}")
        
        # Try to serialize the result to JSON to check for serialization issues
        json_result = json.dumps(result, default=str)
        print("JSON serialization successful!")
        print(f"Serialized result length: {len(json_result)}")
        return result
    except Exception as e:
        print(f"Error during signup: {e}")
        import traceback
        traceback.print_exc()
        return None

# Run the async function
result = asyncio.run(test_signup())

if result:
    print("SUCCESS: Signup function works correctly!")
else:
    print("FAILURE: Signup function failed")