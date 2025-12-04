# 🚀 Quick Start - Run Backend

## Option 1: Using the Startup Script (Recommended)

### macOS/Linux:
```bash
cd backend
./run_backend.sh
```

### Windows:
```bash
cd backend
run_backend.bat
```

## Option 2: Manual Start

### Step 1: Activate Virtual Environment

**macOS/Linux:**
```bash
cd backend
source venv/bin/activate
```

**Windows:**
```bash
cd backend
venv\Scripts\activate
```

### Step 2: Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### Step 3: Start the Server
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Verify Backend is Running

Once started, you should see:
```
🚀 SilentVoice backend starting up...
📡 WebSocket endpoint available at: ws://localhost:8000/api/v1/ws/sign
📚 API documentation available at: http://localhost:8000/docs
```

## 🌐 Access Points

- **API Root**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/api/v1/ws/sign
- **Health Check**: http://localhost:8000/api/v1/health

## 🔧 Troubleshooting

**Port already in use?**
- Change port in `main.py` or use: `uvicorn main:app --port 8001`

**Module not found?**
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Permission denied on script?**
- macOS/Linux: `chmod +x run_backend.sh`

## 📝 Notes

- Backend will use rule-based gesture detection by default
- ML model will be loaded automatically if `models/sign_language_model.h5` exists
- Server runs with auto-reload enabled (restarts on code changes)

