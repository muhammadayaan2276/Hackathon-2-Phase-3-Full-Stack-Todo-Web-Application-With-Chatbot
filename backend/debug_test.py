import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

print("Environment loaded")

# Initialize database
import asyncio
from src.database import init_db_and_tables
asyncio.run(init_db_and_tables())
print("Database initialized")

# Import app
from main import app
print("App imported")

# Test calling signup function directly
from routes.auth import signup
from src.models.user_create import UserCreate
from src.database import get_session
from sqlmodel import Session

async def test_direct_call():
    print("Testing signup function directly...")
    
    # Create a test user
    user_data = UserCreate(email='test@example.com', name='Test User', password='password123')
    
    # Get a session
    gen = get_session()
    session = await gen.__anext__()
    
    try:
        result = await signup(user_data, session)
        print(f"Signup successful: {result}")
    except Exception as e:
        print(f"Signup failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await gen.aclose()

asyncio.run(test_direct_call())