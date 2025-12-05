# 🚀 SilentVoice ML Training Guide

## 📋 **Project Overview**

SilentVoice is a real-time sign language translator with:
- **Frontend**: React/Next.js web app with 3D avatar
- **Backend**: FastAPI server with TensorFlow ML model
- **ML Pipeline**: Hand tracking → LSTM model → Gesture recognition

---

## 🗂️ **Project Structure**

```
silent-voice/
├── frontend/                    # React/Next.js Web App
│   ├── src/
│   │   ├── app/page.tsx        # Main UI (camera, avatar, controls)
│   │   ├── components/
│   │   │   ├── CameraView.tsx  # MediaPipe hand tracking
│   │   │   ├── GLBViewer.tsx   # 3D avatar with animations
│   │   │   └── OutputText.tsx  # Text display
│   │   ├── hooks/
│   │   │   └── useRecognizer.ts # WebSocket connection
│   │   └── utils/
│   │       └── websocket.ts    # Real-time communication
│   └── public/models/          # 3D avatar files
│
├── backend/                     # Python FastAPI Server
│   ├── main.py                 # Server startup
│   ├── api.py                  # WebSocket API & gesture processing
│   ├── model.py                # TensorFlow LSTM model architecture
│   ├── train_model.py          # Training script
│   ├── collect_training_data.py # Data collection tool
│   ├── model_service.py        # Model loading service
│   └── requirements.txt        # Python dependencies
│
└── Training Files (You'll create)
    ├── training_data/          # Gesture recordings
    │   ├── HELLO/             # Hello gesture samples
    │   ├── THANKS/            # Thanks gesture samples
    │   └── YES/               # Yes gesture samples
    └── models/                # Trained models
        └── sign_language_model.h5
```

---

## 🎯 **How Machine Learning Works in SilentVoice**

### **1. Data Flow:**
```
Camera → MediaPipe → Hand Landmarks → LSTM Model → Gesture Prediction → Avatar Animation
```

### **2. Current Status:**
- ✅ **Frontend**: Captures hand landmarks using MediaPipe
- ✅ **Backend**: Rule-based gesture detection (basic fallback)
- ⚠️ **ML Model**: Architecture ready, needs training data
- ✅ **Avatar**: Responds to gesture predictions with animations

---

## 🏋️ **Training Your ML Model**

### **Step 1: Collect Training Data**

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python collect_training_data.py
```

**What this does:**
- Opens your webcam
- Records hand landmarks for each gesture
- Saves sequences as JSON files
- Organizes by gesture name

**Instructions:**
1. Select gesture name (e.g., "HELLO")
2. Press SPACE to start recording
3. Perform the gesture slowly and clearly
4. Press SPACE to stop recording
5. Repeat 20-30 times per gesture
6. Record multiple gestures (HELLO, THANKS, YES, NO, PEACE, etc.)

### **Step 2: Train the Model**

```bash
python train_model.py
```

**What this does:**
- Loads all your recorded gesture data
- Trains an LSTM neural network
- Saves the trained model as `models/sign_language_model.h5`
- Shows training progress and accuracy

### **Step 3: Test Your Model**

Restart your backend server - it will automatically load your trained model:

```bash
python main.py
```

---

## 🎮 **Frontend Development Guide**

### **Key React Components:**

#### **1. Main App (`frontend/src/app/page.tsx`)**
- Controls UI state (recording, debug mode, language)
- Manages WebSocket connection
- Handles gesture predictions

#### **2. Camera Component (`frontend/src/components/CameraView.tsx`)**
- Uses MediaPipe for hand tracking
- Sends hand landmarks to backend
- Shows real-time hand detection

#### **3. Avatar Component (`frontend/src/components/GLBViewer.tsx`)**
- Renders 3D Ready Player Me avatar
- Animates gestures based on predictions
- Handles facial expressions

#### **4. WebSocket Hook (`frontend/src/hooks/useRecognizer.ts`)**
- Manages real-time communication
- Handles gesture predictions
- Manages connection status

### **Adding New Features:**

#### **Add New Gestures:**
1. **Collect Data**: Use `collect_training_data.py`
2. **Update Backend**: Add gesture to `backend/api.py`
3. **Add Animation**: Update `GLBViewer.tsx` gesture animations
4. **Retrain Model**: Run `train_model.py`

#### **Improve UI:**
- Edit `frontend/src/app/page.tsx` for layout
- Modify `frontend/src/app/globals.css` for styling
- Add new components in `frontend/src/components/`

---

## 🔧 **Development Commands**

### **Backend:**
```bash
cd backend
source venv/bin/activate
python main.py                    # Start server
python collect_training_data.py   # Collect gesture data
python train_model.py            # Train ML model
```

### **Frontend:**
```bash
cd frontend
npm run dev                      # Start development server
npm run build                    # Build for production
```

---

## 📊 **Training Tips**

### **For Better Accuracy:**
1. **Record 30+ samples** per gesture
2. **Vary hand positions** (left/right, different angles)
3. **Record in different lighting** conditions
4. **Include negative samples** (random hand movements)
5. **Keep gestures consistent** but natural

### **Model Parameters** (in `model.py`):
- `sequence_length = 30`: Frames per gesture (adjust for longer/shorter gestures)
- `lstm_units = 128`: Model complexity (increase for more gestures)
- `dropout = 0.3`: Prevents overfitting (adjust if model memorizes training data)

---

## 🎯 **Next Development Steps**

### **Immediate (This Week):**
1. ✅ Collect training data for 5-10 basic gestures
2. ✅ Train your first ML model
3. ✅ Test gesture recognition accuracy
4. ✅ Add more gesture animations to avatar

### **Short Term (Next 2 Weeks):**
1. 📈 Expand to 20+ gestures
2. 🎨 Improve avatar animations
3. 📱 Add mobile support
4. 🔊 Add text-to-speech output

### **Long Term (Next Month):**
1. 🌐 Deploy to web hosting
2. 📚 Add gesture learning mode
3. 👥 Multi-user support
4. 🏆 Competition-ready features

---

## 🆘 **Troubleshooting**

### **Model Not Loading:**
- Check `models/sign_language_model.h5` exists
- Verify training completed successfully
- Check backend logs for errors

### **Poor Accuracy:**
- Collect more training data
- Ensure consistent gesture performance
- Adjust model parameters
- Add data augmentation

### **WebSocket Issues:**
- Ensure backend is running on port 8000
- Check firewall settings
- Verify frontend connects to correct URL

---

## 📞 **Need Help?**

Your SilentVoice project is ready for ML training! Start with collecting data for basic gestures like HELLO, THANKS, YES, NO, and PEACE. The system will automatically use your trained model once it's ready.

**Ready to train your first model? Run:**
```bash
cd backend && python collect_training_data.py
```
