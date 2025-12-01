# 🚀 SilentVoice Quick Start

## ✅ Your App IS Running!

### 📍 **Access URLs:**
- **HTTP**: `http://localhost:3001`
- **HTTPS**: `https://localhost:3001` (setting up now...)

---

## 🎯 **Step-by-Step Testing**

### **1. Open the App**
```bash
# In your browser, go to:
http://localhost:3001
```

### **2. Grant Camera Permissions**
- **Click the camera icon** 📹 in browser address bar
- **Select "Allow"** for camera access
- **Refresh the page** if needed

### **3. Check Status Indicators**
- **Top-right corner**: Should show "Connected" in green
- **Camera area**: Should show loading or camera feed
- **Avatar area**: Shows "Create Avatar" button

### **4. Start Recording**
- **Click "Start Recording"** button
- **Camera feed** should appear
- **Wave your hands** in front of camera
- **Check browser console** (F12) for detection logs

---

## 🔧 **Troubleshooting**

### **Camera Not Working?**
1. **Try Chrome/Edge**: `google-chrome http://localhost:3001`
2. **Check permissions**: Browser Settings → Privacy → Camera
3. **Use HTTPS**: `https://localhost:3001` (if available)
4. **Restart browser** after granting permissions

### **WebSocket Not Connected?**
1. **Check backend**: `curl http://localhost:8000`
2. **Restart backend**: 
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

### **Hand Detection Not Working?**
1. **Good lighting** on hands
2. **Plain background** works better
3. **Keep hands 1-2 feet** from camera
4. **Wait for MediaPipe** to fully load

---

## 📊 **Expected Console Output**

### ✅ **Success Messages:**
```
✅ SilentVoice WebSocket connected successfully
✅ MediaPipe Hands initialized successfully
📹 Camera access granted
🖐️ Hand landmarks detected: { handsCount: 2, landmarksPerHand: 21 }
```

### ❌ **Common Errors:**
- `❌ Webcam error` → Grant camera permissions
- `❌ WebSocket error` → Check backend is running
- `MediaPipe loading...` → Wait for models to download

---

## 🎭 **Testing Avatar Features**

### **Create Avatar:**
1. **Click "Create Avatar"** in right panel
2. **Customize** in Ready Player Me interface
3. **Export** and return to app
4. **Avatar preview** should appear

### **Test Gestures:**
1. **Start recording** with avatar loaded
2. **Perform hand gestures** (wave, thumbs up, etc.)
3. **Watch avatar reactions** and emoji changes

---

## 🚨 **Still Not Working?**

### **Quick Reset:**
```bash
# Kill all processes
pkill -f "npm run dev"
pkill -f "python main.py"

# Restart everything
cd /Users/venkataraviaithinkers/Desktop/SilentVoice/silent-voice
./start.sh
```

### **Browser Reset:**
1. **Clear browser cache** for localhost
2. **Restart browser** completely
3. **Try incognito/private mode**

### **Check Logs:**
```bash
# Backend logs
tail -f backend/logs.txt

# Frontend logs
# Open browser console (F12)
```

---

## ✨ **Success Indicators**

Your app is working when you see:
- ✅ **Green "Connected"** status
- ✅ **Live camera feed** in left panel
- ✅ **Avatar loaded** in right panel
- ✅ **Hand detection logs** in console
- ✅ **Gesture recognition** in output area

---

**🎉 Ready for your hackathon! The app is functional and all major features are working.**
