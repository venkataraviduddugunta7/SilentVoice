# 🧪 SilentVoice Testing Instructions

## 🚀 Quick Test Setup

### 1. **Start the Application**
```bash
# Backend should already be running on port 8000
# Frontend is running on port 3001

# Open in browser:
http://localhost:3001
```

### 2. **Test WebSocket Connection**
✅ **Expected**: Green "Connected" status in top-right navbar
❌ **If Red**: Check that backend is running on port 8000

### 3. **Test Camera Access**
1. **Allow camera permissions** when prompted
2. **Check camera feed** appears in left panel
✅ **Expected**: Live camera feed visible
❌ **If Error**: Click "Reload Page" or check camera permissions

### 4. **Test Hand Detection**
1. **Click "Start Recording"** button
2. **Show your hands** to the camera
3. **Check browser console** (F12 → Console)
✅ **Expected**: See logs like "🖐️ Hand landmarks detected"
❌ **If No Detection**: 
   - Ensure good lighting
   - Hold hands clearly in camera view
   - Wait for MediaPipe to load (green status)

### 5. **Test Avatar System**
1. **Click "Create Avatar"** in right panel
2. **Customize your avatar** in Ready Player Me
3. **Export avatar** and return to app
✅ **Expected**: Avatar appears with preview image
❌ **If Issues**: Check browser console for errors

### 6. **Test Gesture Recognition**
1. **Start recording** with hands visible
2. **Perform clear hand gestures**
3. **Watch for recognition** in output panel
✅ **Expected**: Text appears with confidence scores
❌ **If No Recognition**: Backend ML model needs training data

---

## 🔧 Fixed Issues

### ✅ **WebSocket Connection Loop** - FIXED
- **Problem**: Constant reconnections causing backend spam
- **Solution**: Removed callback dependencies from useEffect
- **Result**: Stable single connection

### ✅ **Hand Detection Not Working** - FIXED  
- **Problem**: MediaPipe re-initializing constantly
- **Solution**: Fixed dependency arrays in camera components
- **Result**: Stable hand tracking initialization

### ✅ **UI Theme Issues** - FIXED
- **Problem**: Dark theme not matching modern design
- **Solution**: Updated to light theme with gradients
- **Result**: Professional, modern appearance

---

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running, start it:
cd backend
source venv/bin/activate
python main.py
```

### Frontend Issues
```bash
# If frontend not accessible:
cd frontend
npm run dev

# Check for port conflicts:
lsof -i :3000
lsof -i :3001
```

### Camera Issues
1. **Check browser permissions**: Settings → Privacy → Camera
2. **Try different browser**: Chrome works best with MediaPipe
3. **Check HTTPS**: Some browsers require HTTPS for camera access

### Hand Detection Issues
1. **Lighting**: Ensure good lighting on hands
2. **Background**: Plain background works better
3. **Distance**: Keep hands 1-2 feet from camera
4. **Patience**: MediaPipe models take time to load initially

---

## 📊 Expected Console Output

### ✅ **Successful Startup**
```
🚀 Initializing SilentVoice WebSocket connection...
✅ SilentVoice WebSocket connected successfully
🤖 Initializing MediaPipe Hands for SilentVoice...
📦 Loading MediaPipe file: hands_solution_packed_assets.data
✅ MediaPipe Hands initialized successfully
📹 Camera access granted: MediaStream
```

### ✅ **Hand Detection Working**
```
🖐️ Hand landmarks detected: {
  handsCount: 2,
  landmarksPerHand: 21,
  timestamp: "2024-12-01T19:30:45.123Z"
}
```

### ✅ **Avatar System Working**
```
New Avatar URL: https://models.readyplayer.me/...
```

---

## 🎯 Next Steps

1. **Train ML Model**: Follow DEVELOPMENT_GUIDE.md for gesture training
2. **Add More Gestures**: Extend the gesture recognition system  
3. **Deploy**: Use deployment guide for production hosting
4. **Customize**: Add your own features and improvements

---

**🎉 If all tests pass, your SilentVoice app is ready for the hackathon!**
