#!/bin/bash

# SilentVoice Application Startup Script
# This script installs dependencies and starts both frontend and backend

echo "======================================"
echo "   SilentVoice - Sign Language App   "
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Kill processes on ports if they're in use
if check_port 3000; then
    echo -e "${YELLOW}Port 3000 is in use. Killing existing process...${NC}"
    lsof -ti:3000 | xargs kill -9 2>/dev/null
fi

if check_port 8000; then
    echo -e "${YELLOW}Port 8000 is in use. Killing existing process...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

echo -e "${GREEN}Step 1: Setting up Backend${NC}"
echo "================================"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn websockets numpy tensorflow scikit-learn opencv-python-headless mediapipe

# Create necessary directories
mkdir -p models
mkdir -p training_data
mkdir -p storage/dataset
mkdir -p storage/logs

# Start backend server in background
echo -e "${GREEN}Starting Backend Server...${NC}"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Check if backend started successfully
if check_port 8000; then
    echo -e "${GREEN}✓ Backend server started successfully on port 8000${NC}"
else
    echo -e "${RED}✗ Failed to start backend server${NC}"
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}Step 2: Setting up Frontend${NC}"
echo "================================"

cd frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install

# Build the frontend
echo "Building frontend..."
npm run build

# Start frontend server
echo -e "${GREEN}Starting Frontend Server...${NC}"
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 10

# Check if frontend started successfully
if check_port 3000; then
    echo -e "${GREEN}✓ Frontend server started successfully on port 3000${NC}"
else
    echo -e "${RED}✗ Failed to start frontend server${NC}"
    kill $BACKEND_PID
    exit 1
fi

cd ..

echo ""
echo "======================================"
echo -e "${GREEN}✓ SilentVoice is now running!${NC}"
echo "======================================"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "WebSocket: ws://localhost:8000/api/v1/ws/sign"
echo ""
echo "Available Pages:"
echo "  - Translation: http://localhost:3000/translate"
echo "  - Training: http://localhost:3000/train"
echo "  - Learn: http://localhost:3000/learn"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Function to handle cleanup
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down servers...${NC}"
    kill $FRONTEND_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    echo -e "${GREEN}✓ Servers stopped${NC}"
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup INT

# Keep script running
while true; do
    sleep 1
done
