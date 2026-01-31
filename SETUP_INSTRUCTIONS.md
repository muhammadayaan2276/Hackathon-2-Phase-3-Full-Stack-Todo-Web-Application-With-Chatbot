# Quick Setup Instructions

Follow these steps to get your Todo application running:

## Step 1: Start the Backend

1. Open a terminal and navigate to the backend folder:
```bash
cd backend
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 2: Start the Frontend

1. Open a NEW terminal and navigate to the frontend folder:
```bash
cd frontend
```

2. Start the Next.js development server:
```bash
npm run dev
```

You should see:
```
- Local:        http://localhost:3000
```

## Step 3: Use the Application

1. Open your browser and go to: `http://localhost:3000`

2. Click "Get Started" to create a new account

3. Fill in your email and password, then click "Create Account"

4. You'll be redirected to the todos page where you can:
   - Add new tasks
   - Mark tasks as complete
   - Delete tasks
   - Logout

## Troubleshooting

### Backend won't start
- Make sure you're in the backend directory
- Check if port 8000 is already in use
- Verify your .env file has the correct DATABASE_URL

### Frontend won't start
- Make sure you're in the frontend directory
- Check if port 3000 is already in use
- Run `npm install` if you haven't already

### Can't login or signup
- Make sure the backend is running on port 8000
- Check the browser console for errors
- Verify the .env.local file has `NEXT_PUBLIC_API_URL=http://localhost:8000`

### CORS errors
- Make sure both frontend and backend are running
- Check that the backend CORS settings include `http://localhost:3000`

## Testing the API

You can test the backend API directly:

1. Go to `http://localhost:8000/docs` to see the interactive API documentation

2. Try the signup endpoint:
```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## Next Steps

- Customize the UI colors and styling in the frontend
- Add more features like task categories or due dates
- Deploy to production (Vercel for frontend, Railway/Render for backend)

Enjoy your Todo app! 🎉
