# SilentVoice

Real-time bidirectional sign language translator using MediaPipe, LSTM neural networks, and 3D avatar visualization.

## Features

### Sign → Speech
- Real-time hand tracking using MediaPipe
- LSTM-based gesture recognition
- Text and speech output
- Confidence scoring

### Speech → Sign
- Web Speech API integration
- Text-to-sign mapping
- 3D avatar animation
- Real-time visualization

## Project Structure

```
silentvoice/
│
├─ frontend/                 # Next.js (Web + Extension UI)
│  ├─ app/
│  │   ├─ (landing)/         # Marketing/Info pages
│  │   ├─ live/              # Live Translate Screen
│  │   ├─ train/             # Gesture Data Collection
│  │   └─ avatar/            # 3D Avatar View
│  │
│  ├─ components/
│  │   ├─ WebcamFeed.tsx
│  │   ├─ GestureVisualizer.tsx
│  │   ├─ PredictionOverlay.tsx
│  │   ├─ SpeechToTextPanel.tsx
│  │   └─ AvatarRenderer.tsx
│  │
│  ├─ hooks/
│  │   ├─ useHandTracking.ts # MediaPipe + Frames extraction
│  │   ├─ useWebSocket.ts    # Connect to backend inference
│  │   └─ useSpeech.ts       # Web Speech API integration
│  │
│  ├─ utils/
│  │   ├─ normalize.ts       # Data cleaning + prep
│  │   ├─ fileExport.ts      # Export training data
│  │   └─ gestureConfig.ts   # Sign vocabulary + mapping
│  │
│  └─ extension/             # Chrome Extension build target
│      ├─ manifest.json
│      ├─ contentScript.js
│      └─ overlay.css
│
├─ backend/                  # FastAPI + AI Model
│  ├─ main.py                # WebSocket + REST endpoints
│  ├─ api.py                 # API routes
│  ├─ model/
│  │   ├─ lstm_model.py      # Model architecture
│  │   └─ silentvoice.h5     # Trained model file
│  │
│  ├─ services/
│  │   ├─ preprocess.py      # Landmark normalization
│  │   ├─ inference.py       # Predict sign + confidence
│  │   └─ text2sign.py       # Speech → Sign mapping
│  │
│  └─ storage/
│      ├─ dataset/           # Raw/processed training data
│      └─ logs/
│
├─ shared/
│  ├─ types/                 # Shared TypeScript types
│  └─ protocol.md            # Coordinate message format
│
└─ docs/
    ├─ Architecture.png
    ├─ Roadmap.md
    └─ AI-Usage.md
```

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## Feature Flow

### Sign → Speech
1. Webcam Feed → MediaPipe Hands
2. Hand Landmarks → normalize.ts
3. WebSocket → backend inference
4. PredictionOverlay → speak()

### Speech → Sign
1. Microphone Input → Speech Recognition
2. Vocabulary Mapping → gestureConfig.ts
3. 3D Avatar → Sign Animation

## Development

### Training Model
```bash
cd backend
python train_model.py
```

### Collecting Training Data
```bash
cd backend
python collect_training_data.py
```

Or use the web interface at `/train`

## Documentation

- [Protocol Documentation](shared/protocol.md)
- [Architecture](docs/Architecture.png)
- [Roadmap](docs/Roadmap.md)

## License

MIT
