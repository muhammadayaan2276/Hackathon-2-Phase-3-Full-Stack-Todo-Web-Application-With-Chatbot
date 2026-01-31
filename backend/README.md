# Todo Backend & Database

This is a secure, reliable backend API and database layer to support multi-user Todo operations using Python FastAPI, Neon Serverless PostgreSQL with SQLModel ORM, and JWT-based authentication. The backend provides full CRUD functionality for todo tasks with proper user isolation and concurrent request handling capabilities.

## Features

- Full CRUD operations for todo tasks
- JWT-based authentication and authorization
- User isolation - users can only access their own tasks
- RESTful API design
- Proper error handling
- Comprehensive logging

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel
- Pydantic
- Uvicorn
- PyJWT
- Neon Serverless PostgreSQL

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Secret key for JWT signing
6. Run database migrations: `alembic upgrade head`
7. Start the server: `uvicorn backend.src.main:app --reload`

## API Endpoints

- `GET /api/{user_id}/tasks` → List all tasks for a user
- `POST /api/{user_id}/tasks` → Create a new task
- `GET /api/{user_id}/tasks/{id}` → Get a specific task
- `PUT /api/{user_id}/tasks/{id}` → Update a specific task
- `DELETE /api/{user_id}/tasks/{id}` → Delete a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` → Toggle task completion status

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT signing
- `ENVIRONMENT`: Development environment (dev, staging, prod)

## Running Tests

To run the tests, use: `pytest`

## Docker

To run the application with Docker:

1. Build and run: `docker-compose up --build`
2. The API will be available at `http://localhost:8000`