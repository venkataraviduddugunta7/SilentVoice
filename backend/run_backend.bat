@echo off
REM SilentVoice Backend Startup Script for Windows

echo 🚀 Starting SilentVoice Backend...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ⚠️  Virtual environment not found. Setting up...
    call setup_venv.bat
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Create models directory if it doesn't exist
if not exist "models" mkdir models

REM Create training_data directory if it doesn't exist
if not exist "training_data" mkdir training_data

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing requirements...
    pip install -r requirements.txt
)

echo.
echo ✅ Starting backend server...
echo 📍 Server will be available at: http://localhost:8000
echo 📡 WebSocket endpoint: ws://localhost:8000/api/v1/ws/sign
echo 📚 API docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the backend
python main.py

