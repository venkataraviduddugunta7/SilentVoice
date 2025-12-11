#!/bin/bash

# SilentVoice Setup Script
# This script sets up the complete development environment

echo "🚀 Setting up SilentVoice - Breaking Communication Barriers with AI"
echo "================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check for Node.js
print_status "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js not found. Please install Node.js 18+ first."
    exit 1
fi

# Check for Python
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.9+ first."
    exit 1
fi

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
if npm install; then
    print_success "Frontend dependencies installed successfully"
else
    print_warning "Some frontend packages may have failed. Trying with legacy peer deps..."
    npm install --legacy-peer-deps
fi
cd ..

# Setup Python virtual environment
print_status "Setting up Python virtual environment..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
if pip install -r requirements.txt; then
    print_success "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p models
mkdir -p storage/dataset
mkdir -p storage/logs
print_success "Directories created"

cd ..

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating environment file..."
    cat > .env << EOL
# SilentVoice Environment Configuration
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
MODEL_PATH=models/silentvoice.h5
EOL
    print_success "Environment file created"
else
    print_warning "Environment file already exists"
fi

# Final instructions
echo ""
echo "================================================================="
print_success "🎉 Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "  1. Start the backend:  cd backend && source venv/bin/activate && python main.py"
echo "  2. Start the frontend: cd frontend && npm run dev"
echo "  3. Open browser:       http://localhost:3000"
echo ""
echo "🚀 Quick start:"
echo "  Run: npm run dev (from root directory)"
echo ""
echo "📚 Documentation:"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - README: ./HACKATHON_README.md"
echo ""
print_status "Happy coding! 🤟"