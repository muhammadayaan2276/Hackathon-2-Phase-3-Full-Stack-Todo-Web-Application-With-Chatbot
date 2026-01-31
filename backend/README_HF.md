# Todo API - Hugging Face Deployment

## FastAPI Todo Application with JWT Authentication

This is a RESTful API for managing todos with user authentication.

## Features
- User signup and signin with JWT authentication
- Create, read, update, delete todos
- Toggle todo completion status
- SQLite database (auto-created on startup)

## API Endpoints

### Authentication
- POST `/api/auth/signup` - Create new user account
- POST `/api/auth/signin` - Login and get JWT token

### Todos (Protected - Requires JWT)
- GET `/api/todos` - Get all todos for current user
- POST `/api/todos` - Create new todo
- GET `/api/todos/{id}` - Get specific todo
- PUT `/api/todos/{id}` - Update todo
- DELETE `/api/todos/{id}` - Delete todo
- PUT `/api/todos/{id}/toggle` - Toggle completion status

## Environment Variables

Set these in Hugging Face Space settings:
- `BETTER_AUTH_SECRET` - JWT secret key (minimum 32 characters)
- `DATABASE_URL` - Database connection string (optional, defaults to SQLite)

## Running Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Tech Stack
- FastAPI
- SQLModel
- JWT Authentication
- Async SQLite/PostgreSQL support
