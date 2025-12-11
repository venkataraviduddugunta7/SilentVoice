# SilentVoice - Folder Structure

## Project Overview
Real-time bidirectional sign language translator using MediaPipe, LSTM neural networks, and 3D avatar visualization.

## Current Folder Structure

```
silent-voice/
│
├── backend/                    # Python FastAPI Backend
│   ├── api.py                  # API routes
│   ├── main.py                 # WebSocket + REST endpoints
│   ├── model.py                # Model definitions
│   ├── model_service.py        # Model service
│   ├── train_model.py          # Training script
│   ├── collect_training_data.py # Data collection
│   ├── websocket_manager.py    # WebSocket handling
│   ├── requirements.txt        # Python dependencies
│   ├── run_backend.sh          # Backend startup script
│   ├── run_backend.bat         # Windows startup script
│   ├── setup_venv.sh           # Virtual environment setup
│   │
│   ├── model/                  # Model architecture
│   │   ├── __init__.py
│   │   └── lstm_model.py       # LSTM model implementation
│   │
│   └── services/               # Backend services
│       ├── __init__.py
│       ├── preprocess.py       # Landmark normalization
│       ├── inference.py        # Prediction logic
│       └── text2sign.py        # Speech → Sign mapping
│
├── frontend/                   # Next.js Frontend
│   ├── package.json            # Node.js dependencies
│   ├── package-lock.json       # Lock file
│   ├── next-env.d.ts          # Next.js TypeScript config
│   ├── start.sh                # Frontend startup script
│   ├── README.md               # Frontend documentation
│   ├── QUICK_START.md          # Quick start guide
│   ├── REFINEMENT_SUMMARY.md   # Refinement notes
│   │
│   ├── shared/                 # Shared types and protocols
│   │   ├── protocol.md         # Message format documentation
│   │   └── types/
│   │       └── index.ts        # TypeScript type definitions
│   │
│   └── docs/
│       └── STRUCTURE.md        # Structure documentation
│
├── shared/                     # Root-level shared resources
│   ├── protocol.md             # Coordinate message format
│   └── types/
│       └── index.ts            # Shared TypeScript types
│
├── docs/                       # Project documentation
│   └── STRUCTURE.md            # Project structure docs
│
├── package.json                # Root package.json
├── package-lock.json           # Root lock file
├── start.sh                    # Root startup script
├── README.md                   # Main project README
├── QUICK_START.md              # Quick start guide
├── REFINEMENT_SUMMARY.md       # Refinement notes
├── .gitignore                  # Git ignore rules
└── next-env.d.ts              # Next.js config
```

## Key Components

### Backend (`/backend/`)
- **Language**: Python
- **Framework**: FastAPI
- **Purpose**: Handles AI model inference, WebSocket connections, and API endpoints
- **Main Files**:
  - `main.py` - Entry point, WebSocket server
  - `api.py` - REST API routes
  - `model_service.py` - Model loading and management
  - `train_model.py` - Model training script

### Frontend (`/frontend/`)
- **Language**: TypeScript/JavaScript
- **Framework**: Next.js
- **Purpose**: Web interface for sign language translation
- **Main Files**:
  - Next.js app structure
  - Shared types and protocols

### Shared (`/shared/`)
- **Purpose**: Shared TypeScript types and protocol definitions
- **Files**:
  - `protocol.md` - Message format documentation
  - `types/index.ts` - TypeScript type definitions

## Technology Stack

- **Backend**: Python, FastAPI, MediaPipe, TensorFlow/Keras (LSTM)
- **Frontend**: Next.js, TypeScript, React
- **Communication**: WebSocket, REST API
- **AI/ML**: MediaPipe Hands, LSTM Neural Networks

## Quick Start

1. **Backend**: `cd backend && python main.py`
2. **Frontend**: `cd frontend && npm install && npm run dev`
