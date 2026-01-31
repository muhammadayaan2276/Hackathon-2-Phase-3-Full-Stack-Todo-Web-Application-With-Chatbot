# Todo Full-Stack Web Application

A modern, secure todo application built with Next.js (frontend) and FastAPI (backend), featuring JWT authentication and PostgreSQL database.

## Features

- ✅ **User Authentication**: Secure signup and login with JWT tokens
- 📝 **Task Management**: Create, read, update, delete, and toggle tasks
- 🔒 **Security**: JWT-based authentication with user isolation
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile
- 🎨 **Modern UI**: Clean interface built with Tailwind CSS
- 🚀 **Fast Backend**: Python FastAPI with async support
- 💾 **Database**: PostgreSQL (Neon Serverless)

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt

## Project Structure

```
.
├── frontend/                 # Next.js frontend application
│   ├── app/                 # Next.js app router pages
│   │   ├── login/          # Login page
│   │   ├── signup/         # Signup page
│   │   ├── todos/          # Todo management page
│   │   └── page.tsx        # Home/landing page
│   ├── components/         # React components
│   │   ├── TodoList.tsx    # Todo list component
│   │   ├── AddTaskModal.tsx # Add task modal
│   │   └── EditTaskModal.tsx # Edit task modal
│   └── lib/                # Utility functions
│       ├── api.ts          # API client
│       └── auth.ts         # Authentication utilities
│
└── backend/                 # FastAPI backend application
    ├── main.py             # Main application file
    ├── requirements.txt    # Python dependencies
    └── .env                # Environment variables

```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- PostgreSQL database (or use Neon Serverless)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key-here
```

5. Start the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Login with credentials

### Todos (Protected)
- `GET /api/todos` - Get all todos for authenticated user
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get specific todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `PUT /api/todos/{id}/toggle` - Toggle todo completion status

## Usage

1. **Sign Up**: Create a new account on the signup page
2. **Login**: Sign in with your credentials
3. **Add Tasks**: Click "Add New Task" to create todos
4. **Manage Tasks**:
   - Click the checkbox to mark tasks as complete
   - Click the delete icon to remove tasks
5. **Logout**: Click the logout button to end your session

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- User isolation (users can only access their own tasks)
- CORS protection
- Secure token storage

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
npm start
```

Backend:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT signing

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Troubleshooting

### CORS Issues
Make sure the backend CORS middleware includes your frontend URL:
```python
allow_origins=["http://localhost:3000"]
```

### Database Connection
Verify your DATABASE_URL is correct and the database is accessible.

### JWT Token Issues
Ensure BETTER_AUTH_SECRET is the same value in both frontend and backend configurations.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.
