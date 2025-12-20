#!/bin/bash

# Silent Voice - Start Script
# This script starts both frontend and backend servers

echo "🚀 Starting Silent Voice Application..."
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to kill processes on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set up trap to catch Ctrl+C
trap cleanup INT

# Start Backend
echo -e "${GREEN}Starting Backend Server...${NC}"
cd backend
python3 main.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
cd ..

# Wait for backend to start
sleep 3

# Start Frontend
echo -e "${GREEN}Starting Frontend Server...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"
cd ..

# Display access information
echo ""
echo "=================================="
echo -e "${GREEN}✅ Silent Voice is running!${NC}"
echo "=================================="
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Keep script running
wait