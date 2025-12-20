# Quick Setup & Testing Guide

## 1. Initialize Database (One Time)
```bash
cd backend
python database.py
```

## 2. Collect Training Data
```bash
cd backend
python collect_training_data.py
```
- Choose option 1 to collect all signs
- Or option 2 for specific signs
- Follow on-screen instructions

## 3. Train the Model
```bash
cd backend
python train_model.py
```

## 4. Start the Application
```bash
# From root directory
./start.sh
```

## 5. Test Sign Detection

### Test Sign → Speech:
1. Open http://localhost:3000/translate
2. Make sure you're in "Sign → Speech" mode
3. Click "Start Camera"
4. Make these gestures:
   - **Hello**: Open palm, wave
   - **Yes**: Thumbs up
   - **No**: Thumbs down
   - **Peace**: Two fingers up (V sign)

### Test Speech → Sign:
1. Switch to "Speech → Sign" mode
2. Click microphone
3. Say: "Hello", "Thank you", "Yes", "No"
4. Watch the 3D avatar respond

## Troubleshooting

### Issue: No signs detected
**Solution:**
1. Check browser console for errors
2. Ensure good lighting
3. Make signs clearly in camera view
4. Check WebSocket connection in Network tab

### Issue: Avatar not loading
**Solution:**
1. The app will fall back to simple avatar if Ready Player Me fails
2. Check internet connection for avatar loading
3. Simple avatar will still show sign animations

### Issue: Model not found error
**Solution:**
```bash
cd backend
# Create dummy model for testing
python -c "
import numpy as np
import json
from pathlib import Path

# Create model directory
Path('models').mkdir(exist_ok=True)

# Create dummy model metadata
metadata = {
    'labels': ['hello', 'yes', 'no', 'thank_you', 'please'],
    'input_shape': [30, 126],
    'num_classes': 5
}

with open('models/model_metadata.json', 'w') as f:
    json.dump(metadata, f)

print('Created dummy model metadata')
"
```

## Quick Database Check
```bash
cd backend
python -c "
from database import SessionLocal, Sign
db = SessionLocal()
signs = db.query(Sign).all()
print(f'Database has {len(signs)} signs')
for sign in signs:
    print(f'  - {sign.word}: {sign.description}')
db.close()
"
```

## Verify WebSocket Connection
```bash
# Test WebSocket directly
curl -N -H "Connection: Upgrade" \
     -H "Upgrade: websocket" \
     -H "Sec-WebSocket-Version: 13" \
     -H "Sec-WebSocket-Key: $(openssl rand -base64 16)" \
     http://localhost:8000/api/v1/ws/sign
```

## Check Backend Health
```bash
curl http://localhost:8000/api/v1/health
```