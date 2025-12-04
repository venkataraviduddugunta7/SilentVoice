#!/bin/bash

# SilentVoice Backend Startup Script

echo "🚀 Starting SilentVoice Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Setting up..."
    bash setup_venv.sh
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Create models directory if it doesn't exist
mkdir -p models

# Create training_data directory if it doesn't exist
mkdir -p training_data

# Check if requirements are installed
echo "🔍 Checking dependencies..."
pip show fastapi > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "📥 Installing requirements..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Starting backend server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📡 WebSocket endpoint: ws://localhost:8000/api/v1/ws/sign"
echo "📚 API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the backend
python main.py

