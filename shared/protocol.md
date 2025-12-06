# SilentVoice Communication Protocol

## WebSocket Protocol

### Connection
- **Endpoint**: `ws://localhost:8000/api/v1/ws/sign`
- **Protocol**: WebSocket (text frames, JSON messages)

### Message Format

#### Client → Server: Pose Data

Send hand landmark data for gesture recognition.

```json
{
  "type": "pose",
  "data": [
    [
      {"x": 0.5, "y": 0.3, "z": 0.1},
      {"x": 0.52, "y": 0.32, "z": 0.12},
      ...
    ],
    [
      {"x": 0.7, "y": 0.4, "z": 0.2},
      ...
    ]
  ]
}
```

**Structure:**
- `type`: Always `"pose"` for pose data
- `data`: Array of hands (max 2)
  - Each hand: Array of 21 landmarks
  - Each landmark: `{x, y, z}` coordinates (normalized 0-1)

#### Server → Client: Prediction

Receive gesture prediction with confidence score.

```json
{
  "type": "prediction",
  "word": "HELLO",
  "confidence": 0.85
}
```

**Structure:**
- `type`: Always `"prediction"` for predictions
- `word`: Gesture name (e.g., "HELLO", "YES", "NO")
- `confidence`: Confidence score (0.0 - 1.0)

#### Server → Client: Error

Receive error messages.

```json
{
  "type": "error",
  "message": "Invalid data format",
  "error": "Details..."
}
```

## REST API

### Health Check
- **GET** `/api/v1/health`
- **Response**: `{"status": "healthy", "service": "SilentVoice Backend"}`

### Connections
- **GET** `/api/v1/connections`
- **Response**: `{"active_connections": 1, "status": "ok"}`

## Data Flow

### Sign → Speech Flow
1. Client captures webcam feed
2. MediaPipe extracts hand landmarks (21 points per hand)
3. Client sends landmarks via WebSocket
4. Server processes with LSTM model
5. Server returns prediction + confidence
6. Client displays text and speaks result

### Speech → Sign Flow
1. Client captures microphone input
2. Web Speech API transcribes speech
3. Client maps text to sign gesture
4. Client displays 3D avatar with gesture animation

## Coordinate System

- **X**: Horizontal position (0 = left, 1 = right)
- **Y**: Vertical position (0 = top, 1 = bottom)
- **Z**: Depth (relative, can be negative)

All coordinates are normalized to [0, 1] range for X and Y.

## Gesture Vocabulary

Supported gestures:
- HELLO, YES, NO, THANK_YOU, PLEASE, SORRY
- GOOD, BAD, LOVE, PEACE
- GOODBYE, WELCOME, HELP, STOP
- GO, COME, EAT, DRINK, SLEEP, WAKE_UP

