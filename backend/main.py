from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel
from pydantic import BaseModel as PydanticBaseModel
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import re
import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./todo.db')
# Clean the database URL for asyncpg compatibility
if 'sslmode=' in DATABASE_URL or 'channel_binding=' in DATABASE_URL:
    DATABASE_URL = re.sub(r'[&?]sslmode=[^&]*', '', DATABASE_URL)
    DATABASE_URL = re.sub(r'[&?]channel_binding=[^&]*', '', DATABASE_URL)
    DATABASE_URL = DATABASE_URL.replace('?&', '?')
    DATABASE_URL = DATABASE_URL.rstrip('?&')

# Create async engine
engine = create_async_engine(DATABASE_URL)

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-strong-secret-key-here-32-characters-minimum")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Cleanup on shutdown
    await engine.dispose()

# Models
class TaskBase(PydanticBaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(PydanticBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime

# SQLModel for database
class TaskDB(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    user_id: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# User model for authentication
class UserBase(PydanticBaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(UserBase):
    pass

class User(UserBase):
    id: str
    created_at: datetime

class UserDB(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Dependency for database session
async def get_session():
    async with AsyncSession(engine) as session:
        yield session

# JWT security
security = HTTPBearer()

# Create access token
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Hash password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Get current user from token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        statement = select(UserDB).where(UserDB.id == user_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Create FastAPI app
app = FastAPI(title="Todo API", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

# AUTHENTICATION ENDPOINTS

# User signup
@app.post("/api/auth/signup", response_model=Dict[str, str])
async def signup(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check if user already exists
    statement = select(UserDB).where(UserDB.email == user_data.email)
    result = await session.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_data.password)

    new_user = UserDB(
        id=user_id,
        email=user_data.email,
        password_hash=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create access token
    access_token = create_access_token(data={"sub": user_id, "email": user_data.email})

    return {"access_token": access_token, "token_type": "bearer", "user_id": user_id}

# User signin
@app.post("/api/auth/signin", response_model=Dict[str, str])
async def signin(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    # Find user by email
    statement = select(UserDB).where(UserDB.email == user_data.email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create access token
    access_token = create_access_token(data={"sub": user.id, "email": user.email})

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

# PROTECTED ENDPOINTS (using existing user_id parameter but now authenticated via JWT)

# CREATE Single Todo (now protected by JWT)
@app.post("/api/todos", response_model=Task)
async def create_todo(task_data: TaskCreate, current_user: UserDB = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # Create new task from user input
    new_task = TaskDB(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=current_user.id
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    # Convert to response model
    return Task(
        id=new_task.id,
        title=new_task.title,
        description=new_task.description,
        completed=new_task.completed,
        user_id=new_task.user_id,
        created_at=new_task.created_at,
        updated_at=new_task.updated_at
    )


# GET all todos for current user
@app.get("/api/todos", response_model=List[Task])
async def get_todos(current_user: UserDB = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    statement = select(TaskDB).where(TaskDB.user_id == current_user.id)
    result = await session.execute(statement)
    tasks = result.scalars().all()

    return [
        Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]

# GET a specific todo (for current user)
@app.get("/api/todos/{todo_id}", response_model=Task)
async def get_todo(todo_id: str, current_user: UserDB = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    statement = select(TaskDB).where(TaskDB.id == uuid.UUID(todo_id)).where(TaskDB.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return Task(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

# UPDATE a todo (for current user)
@app.put("/api/todos/{todo_id}", response_model=Task)
async def update_todo(todo_id: str, task_data: TaskUpdate, current_user: UserDB = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    statement = select(TaskDB).where(TaskDB.id == uuid.UUID(todo_id)).where(TaskDB.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields that were provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return Task(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

# DELETE a todo (for current user)
@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str, current_user: UserDB = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    statement = select(TaskDB).where(TaskDB.id == uuid.UUID(todo_id)).where(TaskDB.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return {"message": f"Task {todo_id} successfully deleted"}

# TOGGLE completion status (for current user)
@app.put("/api/todos/{todo_id}/toggle", response_model=Task)
async def toggle_todo(todo_id: str, current_user: UserDB = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    statement = select(TaskDB).where(TaskDB.id == uuid.UUID(todo_id)).where(TaskDB.user_id == current_user.id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return Task(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )