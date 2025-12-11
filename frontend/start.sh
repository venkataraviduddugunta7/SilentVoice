#!/bin/bash

# SilentVoice Startup Script
# This script starts both the backend and frontend servers

echo "🚀 Starting SilentVoice..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed."
    exit 1
fi

echo "✅ All prerequisites are installed."

# Setup backend
echo "🐍 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo "🚀 Starting FastAPI backend..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Setup frontend
echo "⚛️ Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install --legacy-peer-deps
fi

echo "🚀 Starting Next.js frontend..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 SilentVoice is starting up!"
echo ""
echo "📡 Backend: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - WebSocket: ws://localhost:8000/api/v1/ws/sign"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "🎭 Features:"
echo "   - Ready Player Me Avatar Integration"
echo "   - Real-time Sign Language Recognition"
echo "   - 3D Avatar Animations"
echo "   - Modern Light UI Design"
echo ""
echo "📚 Development Guide: ./DEVELOPMENT_GUIDE.md"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down SilentVoice..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped."
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT

# Wait for both processes
wait
