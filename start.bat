@echo off
echo Starting Todo Application...
echo.

REM Check if backend virtual environment exists
if not exist "backend\venv" (
    echo Backend virtual environment not found!
    echo Please run: cd backend ^&^& python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo Frontend dependencies not installed!
    echo Please run: cd frontend ^&^& npm install
    exit /b 1
)

REM Start backend
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo Application started successfully!
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers
