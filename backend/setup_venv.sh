#!/bin/bash

# Virtual environment setup script for SilentVoice backend

echo "Setting up Python virtual environment for SilentVoice backend..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Virtual environment setup complete!"
echo "To activate the environment, run: source venv/bin/activate"
echo "To start the server, run: uvicorn main:app --reload --host 0.0.0.0 --port 8000"
