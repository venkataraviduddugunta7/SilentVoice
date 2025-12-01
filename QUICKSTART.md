# 🚀 SilentVoice Quick Start Guide

## One-Command Setup

```bash
cd silent-voice
./start.sh
```

This will automatically:
- ✅ Set up Python virtual environment
- ✅ Install all backend dependencies
- ✅ Install all frontend dependencies  
- ✅ Start both servers simultaneously

## Manual Setup (Alternative)

### Backend Only
```bash
cd backend
chmod +x setup_venv.sh
./setup_venv.sh
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Only
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

## 🎯 Testing the Connection

1. **Open your browser** to `http://localhost:3000`
2. **Allow camera permissions** when prompted
3. **Click the "Start" button** to begin recording
4. **Show your hands** to the camera
5. **Check the browser console** (F12) for detected landmarks
6. **Monitor the connection status** in the top-right corner

### Expected Behavior
- 🟢 Green dot = Backend connected
- 📹 Red recording indicator when active
- 🖐️ Hand landmarks logged to console
- 📡 WebSocket messages in browser network tab

## 🔧 Troubleshooting

### Camera Not Working
```bash
# Check if camera is available
# In browser console:
navigator.mediaDevices.getUserMedia({video: true})
```

### Backend Connection Failed
```bash
# Check if backend is running
curl http://localhost:8000/api/v1/health
```

### Dependencies Issues
```bash
# Clean install
npm run clean
npm run setup
```

## 🎨 What You'll See

### Frontend (localhost:3000)
- **Left Panel**: Live camera feed with hand tracking
- **Right Panel**: 3D avatar placeholder (animated cube)
- **Header**: Connection status and recording controls
- **Footer**: Real-time status information

### Backend (localhost:8000)
- **API Docs**: Interactive documentation at `/docs`
- **Health Check**: Status endpoint at `/api/v1/health`
- **WebSocket**: Real-time endpoint at `/api/v1/ws/sign`

## 🚀 Ready for Development

The scaffold is complete and ready for:
- 🤖 Adding ML sign language models
- 🎭 Implementing 3D avatar animations
- 🔄 Building bidirectional translation
- 📱 Adding mobile support
- 👥 Implementing user profiles

Happy hacking! 🎉
