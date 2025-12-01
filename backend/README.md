# SilentVoice Backend

FastAPI backend for real-time sign language processing with WebSocket support.

## 🚀 Quick Start

1. **Setup virtual environment:**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

2. **Activate environment:**
```bash
source venv/bin/activate
```

3. **Start server:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### HTTP Endpoints
- `GET /` - API information
- `GET /api/v1/health` - Health check
- `GET /api/v1/connections` - Active WebSocket connections
- `GET /docs` - Interactive API documentation

### WebSocket Endpoints
- `WS /api/v1/ws/sign` - Real-time sign language data processing

## 🔌 WebSocket Protocol

### Client → Server
```json
{
  "landmarks": [
    {"x": 0.5, "y": 0.3, "z": 0.1},
    {"x": 0.6, "y": 0.4, "z": 0.2}
  ],
  "timestamp": "2023-12-01T10:30:00Z",
  "handsCount": 1,
  "landmarksPerHand": 21
}
```

### Server → Client
```json
{
  "status": "received",
  "message": "Hand coordinates processed successfully",
  "timestamp": "2023-12-01T10:30:00Z",
  "landmarks_count": 21
}
```

## 🛠️ Development

### Adding ML Models
1. Add model dependencies to `requirements.txt`
2. Load models in `api.py`
3. Process landmarks in WebSocket handler
4. Return predictions to client

### Environment Variables
Create `.env` file:
```
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📦 Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **WebSockets**: Real-time communication
- **NumPy**: Numerical computing
- **TensorFlow**: Machine learning
- **MediaPipe**: Computer vision
