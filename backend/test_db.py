import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

print("Environment variables loaded.")

# Test database connection
import asyncio
from src.database import get_session
from sqlmodel import Session

async def test_db_connection():
    try:
        print("Testing database connection...")
        gen = get_session()
        session = await gen.__anext__()
        print("Database connection successful.")
        
        # Close the session
        await gen.aclose()
    except Exception as e:
        print(f"Database connection failed: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_db_connection())