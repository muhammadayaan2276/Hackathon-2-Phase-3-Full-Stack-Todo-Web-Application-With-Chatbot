import os
import sys
import traceback

# Set the environment variable
os.environ['BETTER_AUTH_SECRET'] = 'your-super-secret-key-here'

# Add the current directory to the path
sys.path.insert(0, '.')

try:
    # Import the modules
    from models.user import UserCreate
    from services.user_service import UserService
    from routes.auth import signup
    from main import app
    
    print("All imports successful!")
    
    # Create a test user
    test_user = UserCreate(email="test@example.com", password="password123", name="Test User")
    
    print(f"Test user created: {test_user}")
    
    # Try to call the signup function directly
    import asyncio
    
    async def test_signup():
        try:
            result = await signup(test_user)
            print(f"Signup successful: {result}")
            return result
        except Exception as e:
            print(f"Error during signup: {e}")
            traceback.print_exc()
            return None
    
    # Run the async function
    result = asyncio.run(test_signup())
    
    if result:
        print("SUCCESS: Signup function works correctly!")
    else:
        print("FAILURE: Signup function failed")
        
except Exception as e:
    print(f"General error: {e}")
    traceback.print_exc()