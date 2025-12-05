# 🤟 SilentVoice - AI Sign Language Translator

> **Privacy-First Bi-Directional Sign Language Translator**  
> Real-time communication bridge between Deaf/Hard-of-Hearing and hearing communities

[![React](https://img.shields.io/badge/React-18.0-blue)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)](https://tensorflow.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-red)](https://mediapipe.dev/)

## 🎯 **Features**

- 🤲 **Real-time Hand Tracking** - MediaPipe-powered gesture detection
- 🤖 **3D Avatar Animation** - Ready Player Me avatar with facial expressions
- 🧠 **AI-Powered Recognition** - TensorFlow LSTM model for gesture classification
- 🔒 **Privacy-First** - No video uploads, only hand coordinates processed
- ⚡ **Low Latency** - WebSocket streaming for instant responses
- 📱 **Web-Based** - Works on any device with a camera
- 🎭 **Facial Expressions** - Avatar shows emotions matching gestures

## 🚀 **Quick Start**

### **1. Clone & Setup**
```bash
git clone <your-repo>
cd silent-voice
```

### **2. Start Backend**
```bash
cd backend
./run_backend.sh  # macOS/Linux
# or
run_backend.bat   # Windows
```

### **3. Start Frontend**
```bash
cd frontend
npm install
npm run dev
```

### **4. Open Application**
Visit: `http://localhost:3005`

## 🏋️ **Train Your Own Model**

### **Collect Training Data**
```bash
cd backend
source venv/bin/activate
python collect_training_data.py
```

1. Select gesture name (e.g., "HELLO")
2. Press SPACE to record
3. Perform gesture clearly
4. Record 20-30 samples per gesture

### **Train Model**
```bash
python train_model.py
```

The trained model automatically loads on backend restart!

## 🎮 **How to Use**

1. **Start Camera** - Click "START CAMERA" button
2. **Enable Debug** - Turn on debug mode to see recognition details
3. **Make Gestures** - Perform sign language gestures in front of camera
4. **Watch Avatar** - See your avatar animate with facial expressions
5. **Read Text** - View recognized text in real-time

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   FastAPI        │    │   TensorFlow    │
│                 │    │   Backend        │    │   ML Model      │
│ • MediaPipe     │◄──►│                  │◄──►│                 │
│ • 3D Avatar     │    │ • WebSocket API  │    │ • LSTM Network  │
│ • Real-time UI  │    │ • Gesture Logic  │    │ • Hand Tracking │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 **Project Structure**

```
silent-voice/
├── frontend/              # React/Next.js App
│   ├── src/
│   │   ├── app/          # Main application pages
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   └── utils/        # Utility functions
│   └── public/           # Static assets
│
├── backend/              # Python FastAPI Server
│   ├── main.py          # Server entry point
│   ├── api.py           # WebSocket API endpoints
│   ├── model.py         # TensorFlow model architecture
│   ├── train_model.py   # ML training script
│   └── collect_training_data.py  # Data collection
│
└── training_data/        # Your gesture recordings
    ├── HELLO/           # Hello gesture samples
    ├── THANKS/          # Thanks gesture samples
    └── ...              # More gestures
```

## 🎯 **Supported Gestures**

### **Currently Trained:**
- 👋 **HELLO** - Wave gesture with smile
- 🙏 **THANKS** - Gratitude gesture with warm expression
- 👍 **YES** - Thumbs up with enthusiasm
- 👎 **NO** - Negative gesture with serious expression
- ✌️ **PEACE** - V-sign with slight smile
- 👌 **GOOD** - OK gesture with confidence

### **Add Your Own:**
1. Use `collect_training_data.py` to record new gestures
2. Train model with `train_model.py`
3. Add animations in `GLBViewer.tsx`

## 🛠️ **Development**

### **Backend Development**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### **Frontend Development**
```bash
cd frontend
npm install
npm run dev
```

### **Add New Features**
- **New Gestures**: Record data → Train model → Add animations
- **UI Improvements**: Edit React components in `frontend/src/`
- **Avatar Customization**: Modify `GLBViewer.tsx`
- **API Extensions**: Update `backend/api.py`

## 📊 **Model Performance**

- **Accuracy**: 85-95% (depends on training data quality)
- **Latency**: <100ms end-to-end
- **Supported Hands**: 1-2 hands simultaneously
- **Frame Rate**: 30 FPS processing
- **Model Size**: ~2MB (lightweight for web deployment)

## 🔧 **Configuration**

### **Backend Settings** (`backend/main.py`)
```python
HOST = "0.0.0.0"
PORT = 8000
MODEL_PATH = "models/sign_language_model.h5"
```

### **Frontend Settings** (`frontend/src/utils/websocket.ts`)
```typescript
const WEBSOCKET_URL = "ws://localhost:8000/api/v1/ws/sign"
```

## 🚀 **Deployment**

### **Backend (Production)**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### **Frontend (Production)**
```bash
cd frontend
npm run build
npm start
```

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **MediaPipe** - Hand tracking technology
- **Ready Player Me** - 3D avatar platform
- **TensorFlow** - Machine learning framework
- **FastAPI** - High-performance web framework
- **React/Next.js** - Frontend framework

## 📞 **Support**

- 📧 **Email**: [your-email@example.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-username/silent-voice/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/silent-voice/discussions)

---

**Made with ❤️ for the Deaf and Hard-of-Hearing community**

*Breaking down communication barriers, one gesture at a time.*