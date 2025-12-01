# SilentVoice Development Guide 🚀

## 🎯 Project Overview

SilentVoice is a real-time sign language to speech translator featuring:
- **Frontend**: Next.js + React Three Fiber + Ready Player Me avatars
- **Backend**: FastAPI + LSTM model for gesture recognition
- **Real-time Communication**: WebSocket for live predictions

---

## 🛠️ Development Setup

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.9+
- **Git**

### 1. Clone & Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd silent-voice

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start Development Servers

#### Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate
python main.py
# Server runs on http://localhost:8000
```

#### Frontend (Terminal 2)
```bash
cd frontend
npm run dev
# App runs on http://localhost:3000
```

---

## 🎨 Ready Player Me Avatar Integration

### How It Works
1. **Avatar Creation**: Users click "Create Avatar" → Opens Ready Player Me iframe
2. **Avatar Loading**: VRM file loaded via Three.js GLTFLoader + VRMLoaderPlugin
3. **Gesture Animation**: Real-time gesture recognition triggers avatar expressions

### Avatar Features
- **Gender Selection**: Male/Female avatar options
- **Customization**: Full Ready Player Me customization suite
- **Persistence**: Avatar URL saved in localStorage
- **Real-time Animation**: Gesture-based expressions and hand movements

### Code Structure
```
src/components/ReadyPlayerMeAvatar.tsx
├── AvatarScene (Three.js scene management)
├── VRM Loading (GLTFLoader + VRMLoaderPlugin)
├── Gesture Mapping (gestureLabel → animations)
└── UI Controls (Create/Change avatar buttons)
```

---

## 🤖 Sign Language Training Setup

### Current Model Architecture
- **Input**: Hand landmarks from MediaPipe (21 points × 2 hands × 3 coordinates)
- **Model**: LSTM neural network for sequence classification
- **Output**: Gesture labels (HELLO, THANK_YOU, YES, NO, etc.)

### Training Data Structure
```
training_data/
├── gestures/
│   ├── hello/
│   │   ├── sequence_001.json
│   │   ├── sequence_002.json
│   │   └── ...
│   ├── thank_you/
│   └── ...
└── labels.json
```

### Data Collection Process

#### 1. Record Training Data
```bash
cd backend
python data_collector.py --gesture HELLO --samples 50
```

#### 2. Data Format (JSON)
```json
{
  "gesture": "HELLO",
  "sequence": [
    {
      "timestamp": 1234567890,
      "landmarks": [
        {"x": 0.5, "y": 0.3, "z": 0.1},  // Hand 1, Point 1
        {"x": 0.6, "y": 0.4, "z": 0.2},  // Hand 1, Point 2
        // ... 21 points for hand 1
        {"x": 0.3, "y": 0.5, "z": 0.0},  // Hand 2, Point 1
        // ... 21 points for hand 2
      ]
    }
    // ... sequence frames
  ]
}
```

#### 3. Train Model
```bash
python train_model.py --epochs 100 --batch_size 32
```

### Adding New Gestures

#### Step 1: Collect Data
```bash
# Record 50+ samples per gesture
python data_collector.py --gesture NEW_GESTURE --samples 50
```

#### Step 2: Update Gesture Mapping
```typescript
// In ReadyPlayerMeAvatar.tsx
const gestureAnimations = {
  HELLO: 'wave',
  THANK_YOU: 'thankYou',
  NEW_GESTURE: 'newAnimation',  // Add here
  // ...
};
```

#### Step 3: Retrain Model
```bash
python train_model.py --include_new_gestures
```

---

## 🎭 Avatar Animation System

### Gesture → Animation Mapping
```typescript
const gestureAnimations = {
  HELLO: 'wave',           // Wave hand animation
  THANK_YOU: 'thankYou',   // Bow + hand gesture
  YES: 'nod',              // Head nod
  NO: 'shake',             // Head shake
  PLEASE: 'please',        // Polite gesture
  SORRY: 'sorry',          // Apologetic expression
  GOOD: 'thumbsUp',        // Thumbs up
  BAD: 'thumbsDown',       // Thumbs down
};
```

### Expression System
```typescript
// VRM Expression Manager
const expressionManager = vrm.expressionManager;

// Apply emotions based on gestures
switch (gestureLabel) {
  case 'HELLO':
    expressionManager.setValue('happy', 0.8);
    break;
  case 'SORRY':
    expressionManager.setValue('sad', 0.5);
    break;
  case 'GOOD':
    expressionManager.setValue('happy', 1.0);
    break;
}
```

---

## 🚀 Deployment Guide

### Frontend Deployment (Vercel)
```bash
cd frontend
npm run build
# Deploy to Vercel/Netlify
```

### Backend Deployment (Railway/Heroku)
```bash
cd backend
# Add Procfile: web: uvicorn main:app --host 0.0.0.0 --port $PORT
# Deploy to Railway/Heroku
```

### Environment Variables
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://your-backend-url.com

# Backend (.env)
CORS_ORIGINS=https://your-frontend-url.com
```

---

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test
npm run test:e2e
```

### Backend Testing
```bash
cd backend
pytest tests/
```

### Manual Testing Checklist
- [ ] Camera feed displays correctly
- [ ] WebSocket connection established
- [ ] Avatar loads from Ready Player Me
- [ ] Gesture recognition works
- [ ] Avatar animations trigger
- [ ] UI responsive on mobile

---

## 📈 Performance Optimization

### Frontend Optimizations
- **Three.js**: Use `useFrame` efficiently, dispose unused objects
- **Avatar Loading**: Implement loading states and error handling
- **WebSocket**: Throttle gesture data sending (max 30fps)

### Backend Optimizations
- **Model Inference**: Use GPU acceleration if available
- **WebSocket**: Implement connection pooling
- **Caching**: Cache model predictions for repeated gestures

---

## 🔧 Troubleshooting

### Common Issues

#### Avatar Not Loading
```typescript
// Check console for CORS errors
// Verify Ready Player Me URL format
// Ensure VRM loader is properly registered
```

#### WebSocket Connection Failed
```bash
# Check backend is running on correct port
# Verify CORS settings in FastAPI
# Test WebSocket endpoint directly
```

#### Gesture Recognition Poor
```python
# Collect more training data
# Increase model complexity
# Improve hand landmark detection
```

---

## 🎯 Roadmap

### Phase 1 (Current - Hackathon MVP) ✅
- [x] Ready Player Me integration
- [x] Basic gesture recognition
- [x] Real-time avatar animation
- [x] Modern UI design

### Phase 2 (Post-Hackathon)
- [ ] Advanced facial expressions
- [ ] Lip-sync for speech output
- [ ] Custom avatar creation
- [ ] Multi-language support

### Phase 3 (Production)
- [ ] Real motion capture integration
- [ ] Personalized avatars
- [ ] Voice synthesis
- [ ] Mobile app

---

## 📚 Resources

- **Ready Player Me API**: https://docs.readyplayer.me/
- **Three.js VRM**: https://github.com/pixiv/three-vrm
- **MediaPipe Hands**: https://google.github.io/mediapipe/solutions/hands.html
- **FastAPI WebSockets**: https://fastapi.tiangolo.com/advanced/websockets/

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy Coding! 🚀**
