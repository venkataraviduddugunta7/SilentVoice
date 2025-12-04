# Sign Language Model Training Guide

This guide explains how to train your TensorFlow/LSTM model for sign language gesture recognition.

## Overview

SilentVoice uses a TensorFlow/Keras LSTM model to recognize sign language gestures from hand landmarks. The system works in two modes:

1. **ML Model Mode** (when trained): Uses TensorFlow LSTM for accurate gesture recognition
2. **Rule-Based Fallback** (default): Uses simple rule-based detection for basic gestures

## Quick Start

### 1. Collect Training Data

First, collect training data by recording hand gestures:

```bash
cd backend
python collect_training_data.py
```

This will:
- Open your webcam
- Let you select gestures to record
- Save sequences of hand landmarks as JSON files
- Organize data by gesture name in `training_data/` directory

**Instructions:**
- Press SPACE to start/stop recording
- Perform the gesture while recording
- Record multiple sequences for each gesture (recommended: 20-50 per gesture)
- Press 'q' to quit

### 2. Train the Model

Once you have collected training data:

```bash
python train_model.py
```

This will:
- Load all training sequences
- Split data into train/validation sets
- Build and train the LSTM model
- Save the trained model to `models/sign_language_model.h5`

**Training Options:**
```bash
python train_model.py \
  --data-dir training_data \
  --model-path models/sign_language_model.h5 \
  --epochs 50 \
  --batch-size 32
```

### 3. Use the Trained Model

The backend will automatically load the model on startup. If a model is found, it will be used for predictions. Otherwise, the system falls back to rule-based detection.

## Data Structure

Training data should be organized as follows:

```
training_data/
├── HELLO/
│   ├── sequence_20241202_143022_30frames.json
│   ├── sequence_20241202_143145_30frames.json
│   └── ...
├── THANK_YOU/
│   ├── sequence_20241202_143500_30frames.json
│   └── ...
└── ...
```

Each JSON file contains a sequence of frames:
```json
[
  [
    {"x": 0.5, "y": 0.3, "z": 0.1},  // Landmark 0
    {"x": 0.6, "y": 0.4, "z": 0.2},  // Landmark 1
    ...  // 21 landmarks per hand
  ],
  [
    ...  // Hand 2 (optional)
  ]
]
```

## Model Architecture

The LSTM model consists of:
- **Input**: Sequences of 30 frames, each with 63 features (21 landmarks × 3 coordinates × 2 hands)
- **LSTM Layers**: 3 stacked LSTM layers (128, 64, 32 units)
- **Dense Layers**: 2 fully connected layers (64, 32 units)
- **Output**: Softmax layer with N classes (one per gesture)

## Tips for Better Training

1. **Collect Diverse Data**:
   - Record gestures from different angles
   - Include variations in hand position
   - Record in different lighting conditions

2. **Balance Your Dataset**:
   - Collect similar number of sequences for each gesture
   - Aim for at least 20-30 sequences per gesture

3. **Data Quality**:
   - Ensure hands are clearly visible
   - Keep gestures consistent within each class
   - Remove bad sequences before training

4. **Training Parameters**:
   - Start with 30-50 epochs
   - Use batch size 16-32
   - Monitor validation accuracy to avoid overfitting

## Supported Gestures

Default gestures:
- HELLO
- THANK_YOU
- YES
- NO
- PLEASE
- SORRY
- GOOD
- BAD
- LOVE
- PEACE

You can add more gestures by:
1. Creating a new directory in `training_data/`
2. Collecting sequences for that gesture
3. Retraining the model

## Troubleshooting

**Model not loading:**
- Check that `models/sign_language_model.h5` exists
- Verify model file is not corrupted
- Check backend logs for error messages

**Low accuracy:**
- Collect more training data
- Ensure data quality is good
- Try adjusting model hyperparameters
- Check for class imbalance

**Training fails:**
- Verify training data structure is correct
- Check that JSON files are valid
- Ensure sufficient disk space
- Check TensorFlow installation

## Next Steps

After training:
1. Test the model with the web interface
2. Monitor prediction confidence scores
3. Collect more data for low-confidence gestures
4. Retrain periodically to improve accuracy

For more information, see the main README.md file.

