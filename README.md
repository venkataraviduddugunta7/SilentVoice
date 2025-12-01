# SilentVoice 🤟

A real-time bidirectional sign language translator with 3D avatars, built for hackathons. This monorepo contains both the backend (Python FastAPI) and frontend (Next.js 14) components with Ready Player Me integration.

## 🚀 Quick Start

### One-Command Setup
```bash
chmod +x start.sh && ./start.sh
```

This will automatically:
- Set up Python virtual environment
- Install all dependencies
- Start both backend and frontend servers
- Open the app at http://localhost:3000

### Prerequisites
- Python 3.9+ 
- Node.js 18+
- npm

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Run the setup script:
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- WebSocket endpoint: `ws://localhost:8000/api/v1/ws/sign`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🏗️ Architecture

### Backend (FastAPI + WebSockets)
- **FastAPI**: High-performance web framework
- **WebSockets**: Real-time bidirectional communication
- **MediaPipe**: Hand landmark detection (ready for integration)
- **TensorFlow**: ML model support (ready for sign language models)

### Frontend (Next.js 14 + React)
- **Next.js 14**: App Router with TypeScript
- **Ready Player Me**: 3D avatar creation and integration
- **MediaPipe Hands**: Real-time hand tracking
- **Tailwind CSS**: Modern light theme with gradients
- **Framer Motion**: Smooth animations and transitions

## 📁 Project Structure

```
silent-voice/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── api.py               # WebSocket endpoints
│   ├── websocket_manager.py # WebSocket connection management
│   ├── requirements.txt     # Python dependencies
│   └── setup_venv.sh       # Virtual environment setup script
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx     # Main application page
    │   │   └── globals.css  # Global styles
    │   ├── components/
    │   │   ├── CameraCapture.tsx  # Webcam + MediaPipe integration
    │   │   └── AvatarViewer.tsx   # 3D avatar display
    │   └── hooks/
    │       └── useSignWebSocket.ts # WebSocket communication hook
    ├── package.json
    └── tailwind.config.ts
```

## 🔧 Features

### ✅ Current Implementation
- **Real-time webcam capture** with MediaPipe hand tracking
- **WebSocket communication** between frontend and backend
- **Ready Player Me avatar integration** with customization
- **Gesture-based avatar animations** and expressions
- **Modern light UI design** with gradients and animations
- **Real-time gesture recognition** display
- **Avatar persistence** with localStorage
- **Connection status monitoring** and error handling
- **Responsive design** for desktop and mobile

### 🔄 Ready for Extension
- Advanced sign language recognition models (LSTM/Transformer)
- Real-time 3D avatar lip sync and facial expressions
- Text-to-sign translation with avatar demonstrations
- Multiple sign language support (ASL, BSL, etc.)
- User authentication and avatar profiles
- Voice synthesis for translated text
- Mobile app with React Native

## 🎯 Usage

### Getting Started
1. **Run the start script**: `./start.sh`
2. **Open your browser**: Navigate to `http://localhost:3000`
3. **Create your avatar**: Click "Create Avatar" to open Ready Player Me
4. **Customize your avatar**: Choose gender, appearance, clothing
5. **Allow camera permissions** when prompted
6. **Start recording**: Click "Start Recording" button
7. **Perform gestures**: Show hand signs to the camera
8. **Watch your avatar**: See real-time gesture recognition and avatar reactions

### Avatar Features
- **Personalized 3D avatars** created with Ready Player Me
- **Real-time gesture animations** based on sign recognition
- **Facial expressions** that match gesture emotions
- **Avatar persistence** - your avatar is saved for future sessions
- **Easy avatar switching** - create multiple avatars anytime

### Development Guide
For detailed development instructions, model training, and deployment guide, see: **[DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)**

## 🛠️ Development

### Adding Sign Language Models
1. Install your ML framework in `requirements.txt`
2. Add model loading in `api.py`
3. Process landmarks in the WebSocket endpoint
4. Return translation results to frontend

### Customizing the 3D Avatar
1. Replace the placeholder box in `AvatarViewer.tsx`
2. Load 3D models using `@react-three/drei`
3. Animate based on received sign data
4. Add facial expressions and lip sync

### Extending the UI
1. Modify `page.tsx` for layout changes
2. Update `globals.css` for styling
3. Add new components in `src/components/`
4. Use Framer Motion for animations

## 🐛 Troubleshooting

### Backend Issues
- **Port 8000 in use**: Change port in `main.py`
- **Dependencies fail**: Ensure Python 3.8+ and pip are updated
- **WebSocket connection fails**: Check CORS settings in `main.py`

### Frontend Issues
- **Camera not working**: Check browser permissions
- **3D scene not loading**: Ensure WebGL is supported
- **WebSocket connection fails**: Verify backend is running on port 8000

### Common Issues
- **MediaPipe loading slowly**: First load downloads models from CDN
- **High CPU usage**: MediaPipe processing is intensive
- **WebSocket disconnections**: Check network stability

## 📝 License

MIT License - feel free to use this for your hackathon projects!

## 🤝 Contributing

This is a hackathon starter template. Fork it, extend it, and build something amazing! 

---

Built with ❤️ for the sign language community
