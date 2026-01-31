from models.user import User, UserCreate, UserUpdate, UserInDB
import hashlib
from typing import Optional
import uuid
from datetime import datetime
from middleware.jwt_middleware import create_access_token, create_refresh_token

# Simple password hashing using SHA-256 (for demo purposes only)
# In production, use a proper password hashing library like bcrypt or argon2
def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(plain_password) == hashed_password

class UserService:
    def __init__(self):
        # In a real application, this would connect to a database
        self.users_db = {}
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address"""
        for user_id, user in self.users_db.items():
            if user.email == email:
                return user
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID"""
        return self.users_db.get(user_id)
    
    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        
        # Hash the password
        hashed_password = hash_password(user_create.password)
        
        # Create the user object
        user = User(
            id=user_id,
            email=user_create.email,
            name=user_create.name,
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
            emailVerified=False,  # In a real app, this would be verified via email
            role="user",
            hashed_password=hashed_password
        )
        
        # Save to "database"
        self.users_db[user_id] = user
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
            
        # Update fields if provided
        if user_update.name is not None:
            user.name = user_update.name
        if user_update.email is not None:
            user.email = user_update.email
            
        user.updatedAt = datetime.now()

        # Update the user in the database
        self.users_db[user_id] = user

        return user
    
    def generate_tokens(self, user: UserInDB):
        """Generate access and refresh tokens for a user"""
        # Create data to encode in the token
        access_data = {
            "sub": user.id,
            "email": user.email,
            "name": user.name,
            "aud": "todo-app",
            "iss": "todo-app-auth-service"
        }
        
        refresh_data = {
            "sub": user.id,
            "email": user.email,
            "aud": "todo-app",
            "iss": "todo-app-auth-service"
        }
        
        # Create tokens
        access_token = create_access_token(data=access_data)
        refresh_token = create_refresh_token(data=refresh_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }