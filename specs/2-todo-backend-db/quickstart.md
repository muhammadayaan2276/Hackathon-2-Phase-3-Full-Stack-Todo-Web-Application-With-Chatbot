# Quickstart Guide: Todo Backend & Database

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Neon Serverless PostgreSQL instance
- Environment variables configured

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project root with the following variables:
```env
DATABASE_URL=postgresql://<username>:<password>@<neon-project>.aws-neon.tech/<database-name>
BETTER_AUTH_SECRET=<your-jwt-secret-key>
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

### 6. Start the Server
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage Examples

### Authentication
All API requests require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Create a Task
```bash
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "title": "Sample Task",
    "description": "This is a sample task",
    "completed": false
  }'
```

### List User's Tasks
```bash
curl -X GET http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer <jwt-token>"
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/{user_id}/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "title": "Updated Task Title",
    "description": "Updated description",
    "completed": true
  }'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/{user_id}/tasks/{task_id} \
  -H "Authorization: Bearer <jwt-token>"
```

### Toggle Task Completion
```bash
curl -X PATCH http://localhost:8000/api/{user_id}/tasks/{task_id}/complete \
  -H "Authorization: Bearer <jwt-token>"
```

## Running Tests
```bash
pytest
```

## Docker Deployment (Optional)
```bash
docker-compose up --build
```