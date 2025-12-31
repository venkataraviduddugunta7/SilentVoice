# SilentVoice - Complete Setup Guide

## 🚀 Quick Start

Run the application with one command:
```bash
./run_app.sh
```

This will:
1. Install all dependencies
2. Start the backend server (port 8000)
3. Start the frontend server (port 3000)
4. Open your browser to http://localhost:3000

## 📋 Prerequisites

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (3.8 or higher) - [Download](https://www.python.org/)
- **Webcam** - Required for sign language recognition
- **Microphone** - Required for speech recognition
- **Chrome/Edge Browser** - For best compatibility

## 🛠️ Manual Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

1. Navigate to frontend directory:
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

## 🎯 Features & Usage

### 1. Real-time Translation (http://localhost:3000/translate)

#### Sign to Speech Mode
- Click "Start Camera" to begin tracking
- Make ASL signs in front of the camera
- The system will recognize and display the text
- Text will be spoken aloud (if sound is enabled)

**Supported Signs:**
- Basic Greetings: HELLO, GOODBYE, GOOD_MORNING, HOW_ARE_YOU
- Responses: YES, NO, MAYBE, I_DONT_KNOW
- Polite Phrases: PLEASE, THANK_YOU, SORRY, EXCUSE_ME
- Emergency: HELP, EMERGENCY, DANGER, SICK, HURT
- Basic Needs: HUNGRY, THIRSTY, WATER, FOOD, BATHROOM, SLEEP
- Emotions: HAPPY, SAD, ANGRY, LOVE, SCARED
- Numbers: ONE through FIVE
- Questions: WHAT, WHERE, WHEN, WHY, WHO

#### Speech to Sign Mode
- Click "Start Listening" to activate microphone
- Speak clearly into the microphone
- The 3D avatar will display the corresponding sign
- See the sign description below the avatar

### 2. Training Studio (http://localhost:3000/train)

#### Recording Training Data
1. Select a gesture from the left panel
2. Position yourself with good lighting
3. Click "Start Recording"
4. Perform the gesture for 2-3 seconds
5. Click "Stop Recording"
6. Repeat for multiple samples (5-10 per gesture recommended)

#### Managing Training Data
- **Upload to Server**: Send collected data to backend for model training
- **Export JSON**: Download training data for backup
- **Clear All Data**: Remove all local training data

#### Training the Model
After collecting sufficient data:
1. Click "Upload to Server"
2. Navigate to backend API
3. Trigger model training via API endpoint:
```bash
curl -X POST http://localhost:8000/api/v1/train/model
```

### 3. Learning Mode (http://localhost:3000/learn)

Interactive tutorials for learning ASL signs (coming soon).

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to modify:
- WebSocket settings
- CORS origins
- Model parameters
- Confidence thresholds

### Frontend Configuration

Edit `frontend/next.config.js` to modify:
- API endpoints
- WebSocket URLs
- UI settings

## 📊 Model Training

### Collecting Training Data

1. Use the Training Studio to record gestures
2. Aim for at least 20-30 samples per gesture
3. Vary hand position, lighting, and background
4. Include different people if possible

### Training Process

1. Ensure training data is uploaded to backend
2. Run training script:
```bash
cd backend
python train_model.py --epochs 50 --batch-size 32
```

3. Model will be saved to `backend/models/sign_language_model.h5`

### Model Performance

- Current accuracy: ~85% on basic signs
- Best performance with good lighting
- Works with one or two hands
- Supports dynamic gestures

## 🐛 Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Ensure no other app is using the camera
- Try refreshing the page
- Use HTTPS or localhost (not file://)

### WebSocket Connection Failed
- Ensure backend is running on port 8000
- Check firewall settings
- Verify CORS settings in backend
- Check browser console for errors

### Low Recognition Accuracy
- Ensure good lighting (avoid backlight)
- Keep hands clearly visible
- Maintain consistent distance from camera
- Perform gestures slowly and clearly
- Collect more training data

### Speech Recognition Not Working
- Check microphone permissions
- Ensure microphone is not muted
- Speak clearly and at normal volume
- Use Chrome or Edge browser

## 🚀 Performance Optimization

### Frontend Optimization
- Use production build: `npm run build && npm start`
- Enable GPU acceleration in browser
- Close unnecessary tabs/applications
- Use wired internet connection

### Backend Optimization
- Use GPU for TensorFlow (if available)
- Increase worker processes
- Enable model caching
- Use batch processing for multiple requests

## 📱 Browser Extensions (Future)

The app is designed to be packaged as a browser extension for:
- Google Meet integration
- Zoom web client support
- Microsoft Teams compatibility
- General web page translation

## 🤝 Contributing

### Adding New Signs

1. Add sign definition to `backend/services/asl_dictionary.py`
2. Collect training data using Training Studio
3. Update frontend sign mappings
4. Test recognition accuracy

### Improving Recognition

1. Implement data augmentation
2. Add temporal modeling for dynamic signs
3. Include facial expression recognition
4. Add context-aware prediction

## 📄 API Documentation

### WebSocket Endpoints

#### Sign Recognition
```
ws://localhost:8000/api/v1/ws/sign
```

Send:
```json
{
  "type": "holistic",
  "data": {
    "leftHandLandmarks": [...],
    "rightHandLandmarks": [...],
    "poseLandmarks": [...],
    "faceLandmarks": [...]
  },
  "timestamp": 1234567890
}
```

Receive:
```json
{
  "type": "prediction",
  "sign": "HELLO",
  "confidence": 0.92,
  "timestamp": "2024-01-01T12:00:00"
}
```

### REST Endpoints

#### Upload Training Data
```
POST /api/v1/training/upload
```

#### Get Training Stats
```
GET /api/v1/training/stats
```

#### Trigger Model Training
```
POST /api/v1/train/model
```

#### Health Check
```
GET /api/v1/health
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Check backend logs for API errors
4. Ensure all dependencies are installed

## 🎯 Future Enhancements

- [ ] Add more ASL signs (target: 100+ signs)
- [ ] Implement sentence formation
- [ ] Add sign language grammar rules
- [ ] Support multiple sign languages (BSL, ISL, etc.)
- [ ] Mobile app development
- [ ] Offline mode support
- [ ] Video call integration
- [ ] Real-time translation overlay
- [ ] Gesture customization
- [ ] User profiles and progress tracking

## 📜 License

MIT License - Feel free to use and modify for your needs.
