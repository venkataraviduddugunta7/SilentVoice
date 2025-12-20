# SilentVoice Complete Setup & Training Guide

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Training the Model](#training-the-model)
4. [Database Setup](#database-setup)
5. [Deployment Guide](#deployment-guide)
6. [Making the App Functional](#making-the-app-functional)

## Overview

SilentVoice is a real-time bidirectional sign language translator that:
- Converts sign language to speech using computer vision and ML
- Converts speech to 3D sign language animations
- Works entirely in the browser with a Python backend

## Architecture

```
Frontend (Next.js)          Backend (FastAPI)
    |                            |
    ├── WebCam Feed ──────────> Hand Detection (MediaPipe)
    ├── Speech Input             |
    ├── 3D Avatar                ├── LSTM Model
    └── WebSocket Client ←─────> WebSocket Server
                                 |
                                 ├── Sign Detection
                                 ├── Text-to-Sign Mapping
                                 └── Database (SQLite/PostgreSQL)
```

## Training the Model

### Step 1: Collect Training Data

The model needs labeled video data of sign language gestures. Run the data collection script:

```bash
cd backend
python collect_training_data.py
```

This will:
- Open your webcam
- Record hand landmarks for each sign
- Save data to `backend/training_data/`

### Step 2: Prepare Dataset

Create a structured dataset with signs:

```python
# backend/prepare_dataset.py
import numpy as np
import json
import os
from pathlib import Path

SIGNS_TO_COLLECT = [
    'hello', 'thank_you', 'please', 'yes', 'no',
    'help', 'sorry', 'goodbye', 'love', 'friend',
    'eat', 'drink', 'sleep', 'work', 'home',
    'good', 'bad', 'happy', 'sad', 'angry'
]

def collect_sign_data():
    """
    Collect 30 samples of each sign
    Each sample = 30 frames of hand landmarks
    """
    data_path = Path('training_data')
    data_path.mkdir(exist_ok=True)
    
    for sign in SIGNS_TO_COLLECT:
        sign_path = data_path / sign
        sign_path.mkdir(exist_ok=True)
        print(f"Collecting data for sign: {sign}")
        # Collect 30 samples, 30 frames each
        # This creates the training dataset structure

if __name__ == "__main__":
    collect_sign_data()
```

### Step 3: Train the LSTM Model

```bash
cd backend
python train_model.py
```

The trained model will be saved to:
- `backend/models/sign_language_model.h5` (Keras model)
- `backend/models/model_metadata.json` (labels and config)

### Step 4: Training Configuration

Edit `backend/train_config.py`:

```python
TRAINING_CONFIG = {
    'epochs': 100,
    'batch_size': 32,
    'learning_rate': 0.001,
    'sequence_length': 30,  # frames per sign
    'num_landmarks': 21,     # hand keypoints
    'num_features': 3,       # x, y, z coordinates
    'test_split': 0.2,
    'validation_split': 0.1
}
```

## Database Setup

### SQLite (Development - Default)

The app uses SQLite by default for development. The database is automatically created at:
- `backend/data/silentvoice.db`

### PostgreSQL (Production)

For production deployment, use PostgreSQL:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres psql
CREATE DATABASE silentvoice;
CREATE USER silentvoice_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE silentvoice TO silentvoice_user;
```

### Database Schema

```sql
-- Signs dictionary table
CREATE TABLE signs (
    id INTEGER PRIMARY KEY,
    word VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    difficulty VARCHAR(20),
    description TEXT,
    hand_landmarks JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Training data table
CREATE TABLE training_samples (
    id INTEGER PRIMARY KEY,
    sign_id INTEGER REFERENCES signs(id),
    landmarks JSON NOT NULL,
    user_id VARCHAR(100),
    quality_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User progress table
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(100),
    sign_id INTEGER REFERENCES signs(id),
    practice_count INTEGER DEFAULT 0,
    accuracy FLOAT,
    last_practiced TIMESTAMP
);
```

## Deployment Guide

### Where Trained Data is Stored

1. **Model Files**:
   - `backend/models/sign_language_model.h5` - The trained neural network
   - `backend/models/model_metadata.json` - Labels and configuration
   - `backend/models/scaler.pkl` - Data normalization parameters

2. **Training Data**:
   - `backend/training_data/` - Raw collected samples
   - `backend/processed_data/` - Preprocessed numpy arrays

3. **Database**:
   - `backend/data/silentvoice.db` - SQLite database (development)
   - PostgreSQL database (production)

### Deployment Steps

1. **Prepare for deployment**:
```bash
# Create requirements file
cd backend
pip freeze > requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost/silentvoice
MODEL_PATH=./models/sign_language_model.h5
SECRET_KEY=$(openssl rand -hex 32)
ENVIRONMENT=production
EOF
```

2. **Deploy to cloud (e.g., Railway, Render, Heroku)**:
```bash
# Add to your repository
git add .
git commit -m "Add trained model and deployment config"
git push origin main

# Deploy backend (FastAPI)
# Deploy frontend (Next.js/Vercel)
```

## Making the App Functional

### Current Issues to Fix:

1. **Sign Detection Not Working**
2. **3D Avatar Not Human-like**
3. **WebSocket Connection Issues**
4. **Model Not Loaded Properly**

### Quick Fixes:

1. **Enable Sign Detection**:
   - Ensure MediaPipe is properly initialized
   - Check WebSocket connection
   - Verify model is loaded

2. **Improve 3D Avatar**:
   - Use Ready Player Me or other human avatar services
   - Implement proper hand pose animations
   - Sync with detected/spoken words

3. **Test the Pipeline**:
   - Record sample signs
   - Verify landmark extraction
   - Check model predictions
   - Ensure text-to-speech works

## Testing Instructions

### Test Sign-to-Speech:
1. Open http://localhost:3000/translate
2. Click "Start Camera"
3. Make a sign (e.g., "Hello" - open palm wave)
4. Check if text appears and speech is generated

### Test Speech-to-Sign:
1. Switch to "Speech → Sign" mode
2. Click microphone and say "Hello"
3. Avatar should show the sign

## Troubleshooting

### Common Issues:

1. **"Model not found"**:
   - Train the model first: `python train_model.py`
   - Check model path in `backend/model_service.py`

2. **"WebSocket disconnected"**:
   - Ensure backend is running: `uvicorn main:app --reload`
   - Check CORS settings in `backend/main.py`

3. **"No signs detected"**:
   - Ensure good lighting
   - Hand should be clearly visible
   - Check MediaPipe initialization

## Next Steps

1. Collect more training data (at least 30 samples per sign)
2. Train the model with your collected data
3. Test with real users
4. Deploy to production
5. Add more signs to the dictionary