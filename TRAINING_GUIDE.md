# 🤟 Sign Language Model Training Guide

## Overview
This guide explains how to train the sign language recognition model for SilentVoice. The system uses an LSTM neural network to recognize sign language gestures from hand landmarks captured via MediaPipe.

## 📁 Directory Structure

```
backend/
├── training_data/           # Training data directory
│   ├── HELLO/              # Gesture folders
│   │   ├── sequence_*.json # Recorded sequences
│   ├── THANK_YOU/
│   ├── YES/
│   ├── NO/
│   └── ...
├── models/                 # Trained models
│   ├── sign_language_model.h5
│   └── sign_language_model_metadata.json
├── database/               # SQLite database
│   └── signs.db           # Sign data storage
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Collect Training Data
```bash
python collect_training_data.py
```
- Select a gesture from the menu
- Press SPACE to start recording
- Perform the gesture for 30 frames (~1 second)
- Press SPACE to stop or wait for auto-stop
- Repeat for multiple samples of each gesture

### 3. Train the Model
```bash
python train_model.py --epochs 50 --batch-size 32
```

### 4. Test the Model
```bash
python test_model.py
```

## 📊 Data Collection Guidelines

### Recommended Samples per Gesture
- **Minimum**: 20 sequences per gesture
- **Optimal**: 50-100 sequences per gesture
- **Variety**: Record from different angles, speeds, and hand positions

### Recording Tips
1. **Lighting**: Ensure good lighting, avoid backlighting
2. **Background**: Use a plain background for better hand detection
3. **Position**: Keep hands within camera frame
4. **Speed**: Perform gestures at natural speed
5. **Clarity**: Make gestures clear and distinct

## 🧠 Model Architecture

### LSTM Network Structure
```python
Input (30 frames, 63 features)
    ↓
BatchNormalization
    ↓
LSTM (128 units, dropout=0.3)
    ↓
LSTM (64 units, dropout=0.3)
    ↓
LSTM (32 units)
    ↓
Dense (64 units, ReLU)
    ↓
Dense (32 units, ReLU)
    ↓
Output (num_classes, Softmax)
```

### Features
- **Input**: 30 frames × 63 features (21 landmarks × 3 coordinates)
- **Normalization**: Coordinates normalized to [0,1]
- **Dropout**: Prevents overfitting
- **Output**: Probability distribution over gesture classes

## 📝 Supported Gestures

Default gestures (extendable):
1. **HELLO** - Open hand wave
2. **THANK_YOU** - Hand from chin forward
3. **YES** - Closed fist nod
4. **NO** - Index/middle finger tap thumb
5. **PLEASE** - Flat hand circles chest
6. **SORRY** - Closed fist circles chest
7. **GOOD** - Thumbs up
8. **BAD** - Thumbs down
9. **LOVE** - ILY sign
10. **PEACE** - Peace sign

## 🗄️ Database Schema

### SQLite Database Tables

```sql
-- Training sequences
CREATE TABLE training_sequences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gesture_name TEXT NOT NULL,
    sequence_data TEXT NOT NULL,  -- JSON
    frame_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gesture definitions
CREATE TABLE gestures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    category TEXT,
    difficulty TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Model metadata
CREATE TABLE model_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    accuracy REAL,
    training_samples INTEGER,
    epochs INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User feedback (for improvement)
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gesture_predicted TEXT,
    gesture_actual TEXT,
    confidence REAL,
    correct BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Advanced Training Options

### Custom Parameters
```bash
python train_model.py \
    --data-dir custom_data \
    --model-path models/custom_model.h5 \
    --epochs 100 \
    --batch-size 64 \
    --test-size 0.3
```

### Data Augmentation
```python
# In train_model.py, add augmentation:
- Time shifting
- Speed variation
- Noise addition
- Hand position variation
```

## 📈 Model Evaluation

### Metrics
- **Accuracy**: Overall correct predictions
- **Per-class F1 Score**: Balance of precision/recall
- **Confusion Matrix**: Shows misclassifications
- **Real-time FPS**: Processing speed

### Testing
```bash
# Run evaluation
python evaluate_model.py --model-path models/sign_language_model.h5

# Live testing with webcam
python test_live.py
```

## 🚢 Deployment Preparation

### 1. Model Optimization
```python
# Convert to TensorFlow Lite for mobile/edge
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model('models/sign_language_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```

### 2. Database Migration
```bash
# Export training data
python export_data.py --format json --output data_backup.json

# Import to production
python import_data.py --source data_backup.json --target production.db
```

### 3. Environment Variables
```bash
# .env file
DATABASE_URL=sqlite:///database/signs.db
MODEL_PATH=models/sign_language_model.h5
CONFIDENCE_THRESHOLD=0.7
```

## 🐛 Troubleshooting

### Common Issues

1. **Low Accuracy**
   - Collect more diverse training data
   - Increase epochs
   - Adjust learning rate
   - Check for class imbalance

2. **Overfitting**
   - Increase dropout
   - Add more training data
   - Use data augmentation
   - Implement early stopping

3. **Slow Inference**
   - Reduce model size
   - Use TensorFlow Lite
   - Optimize preprocessing
   - Lower camera resolution

## 📊 Performance Benchmarks

| Metric | Target | Current |
|--------|--------|---------|
| Accuracy | >90% | TBD |
| Inference Time | <50ms | TBD |
| Model Size | <50MB | ~20MB |
| Min Training Samples | 20/gesture | Required |

## 🔄 Continuous Improvement

### Feedback Loop
1. Collect user feedback during inference
2. Store incorrect predictions
3. Periodically retrain with new data
4. A/B test new models
5. Deploy improvements

### Adding New Gestures
1. Define gesture in `gestures` table
2. Collect training data (min 20 samples)
3. Retrain model with all gestures
4. Update frontend gesture list
5. Test and validate

## 📚 Resources

- [MediaPipe Hands Documentation](https://google.github.io/mediapipe/solutions/hands)
- [TensorFlow LSTM Guide](https://www.tensorflow.org/guide/keras/rnn)
- [ASL Gesture Reference](https://www.lifeprint.com/asl101/pages-signs/sign-language-words.htm)

## 🤝 Contributing

To add new features or gestures:
1. Fork the repository
2. Create a feature branch
3. Collect and validate training data
4. Submit PR with model metrics

---

**Note**: For production deployment, consider using a PostgreSQL database instead of SQLite for better concurrency and scalability.