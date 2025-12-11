# 🚀 SilentVoice - Quick Start Guide

## Start the Application

### 1. Backend (Terminal 1)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### 3. Open Browser
```
http://localhost:3000
```

## Learn the Codebase

**Start with these files in order:**

1. **`frontend/src/app/page.tsx`** - Main application entry point
2. **`frontend/src/PROJECT_STRUCTURE.md`** - Complete architecture guide
3. **`frontend/src/components/CameraView.tsx`** - Hand tracking implementation
4. **`frontend/src/hooks/useRecognizer.ts`** - WebSocket communication
5. **`frontend/src/utils/websocket.ts`** - Low-level WebSocket client
6. **`frontend/src/components/GLBViewer.tsx`** - 3D avatar rendering

Each file has comprehensive comments explaining how it works!

## Key Concepts

- **MediaPipe Hands**: Detects hands and extracts 21 landmarks per hand
- **WebSocket**: Real-time communication with backend LSTM model
- **Three.js**: 3D rendering for avatar animations
- **Gesture Recognition**: Backend LSTM model processes landmarks → predicts gestures

Happy coding! 🎉

