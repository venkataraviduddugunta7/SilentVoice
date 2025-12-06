# SilentVoice Codebase Structure

This document describes the refined codebase structure for SilentVoice.

## Frontend Structure

### App Routes (`frontend/src/app/`)

- **`(landing)/page.tsx`** - Marketing/landing page
- **`live/page.tsx`** - Main live translation interface
- **`train/page.tsx`** - Gesture data collection for training
- **`avatar/page.tsx`** - Standalone 3D avatar viewer

### Components (`frontend/src/components/`)

- **`WebcamFeed.tsx`** - Webcam capture with MediaPipe hand tracking
- **`GestureVisualizer.tsx`** - Visual feedback for hand landmarks
- **`PredictionOverlay.tsx`** - Display recognized gestures and confidence
- **`SpeechToTextPanel.tsx`** - Speech recognition interface
- **`AvatarRenderer.tsx`** - 3D avatar for sign language visualization

### Hooks (`frontend/src/hooks/`)

- **`useHandTracking.ts`** - MediaPipe hand tracking with frame extraction
- **`useWebSocket.ts`** - WebSocket connection to backend for inference
- **`useSpeech.ts`** - Web Speech API integration

### Utils (`frontend/src/utils/`)

- **`normalize.ts`** - Data cleaning and landmark normalization
- **`fileExport.ts`** - Export training data utilities
- **`gestureConfig.ts`** - Sign vocabulary and text-to-sign mapping

### Extension (`frontend/extension/`)

- **`manifest.json`** - Chrome extension manifest
- **`contentScript.js`** - Content script for web page injection
- **`overlay.css`** - Extension overlay styles

## Backend Structure

### Main Files

- **`main.py`** - FastAPI application entry point
- **`api.py`** - REST and WebSocket API routes
- **`websocket_manager.py`** - WebSocket connection management

### Model (`backend/model/`)

- **`lstm_model.py`** - LSTM model architecture for gesture recognition
- **`silentvoice.h5`** - Trained model file (generated after training)

### Services (`backend/services/`)

- **`preprocess.py`** - Landmark normalization and feature extraction
- **`inference.py`** - Model inference service
- **`text2sign.py`** - Text-to-sign language mapping

### Storage (`backend/storage/`)

- **`dataset/`** - Raw and processed training data
- **`logs/`** - Application logs

## Shared Structure

### Types (`shared/types/`)

- **`index.ts`** - Shared TypeScript type definitions

### Protocol (`shared/`)

- **`protocol.md`** - WebSocket and API communication protocol

## Data Flow

### Sign → Speech Flow

1. **Webcam Feed** (`WebcamFeed.tsx`)
   - Captures video stream
   - Uses MediaPipe Hands for landmark extraction

2. **Hand Tracking** (`useHandTracking.ts`)
   - Processes MediaPipe results
   - Extracts 21 landmarks per hand

3. **Normalization** (`normalize.ts`)
   - Cleans and normalizes landmark data
   - Prepares data for model input

4. **WebSocket** (`useWebSocket.ts`)
   - Sends landmarks to backend
   - Receives predictions

5. **Backend Inference** (`services/inference.py`)
   - Processes landmarks with LSTM model
   - Returns gesture prediction + confidence

6. **Display** (`PredictionOverlay.tsx`)
   - Shows recognized gesture
   - Displays confidence score
   - Triggers text-to-speech

### Speech → Sign Flow

1. **Speech Input** (`SpeechToTextPanel.tsx`)
   - Captures microphone input
   - Uses Web Speech API

2. **Text Processing** (`useSpeech.ts`)
   - Transcribes speech to text
   - Handles interim results

3. **Text-to-Sign Mapping** (`gestureConfig.ts`, `services/text2sign.py`)
   - Maps text to sign gestures
   - Handles vocabulary lookup

4. **Avatar Animation** (`AvatarRenderer.tsx`)
   - Displays 3D avatar
   - Animates sign gestures

## Key Technologies

- **Frontend**: Next.js 14, React, TypeScript, MediaPipe, Three.js
- **Backend**: FastAPI, TensorFlow/Keras, WebSockets
- **ML**: LSTM neural networks for gesture recognition
- **3D**: Three.js for avatar rendering

## Development Workflow

1. **Training Data Collection**: Use `/train` page or `collect_training_data.py`
2. **Model Training**: Run `train_model.py` to train LSTM model
3. **Testing**: Use `/live` page for real-time testing
4. **Deployment**: Build frontend and deploy backend separately

