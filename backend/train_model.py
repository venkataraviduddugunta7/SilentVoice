"""
Training script for Sign Language Gesture Recognition Model
Collects data and trains the LSTM model on hand landmark sequences.
"""

import os
import json
import numpy as np
import tensorflow as tf
from model.lstm_model import SignLanguageModel
from typing import Tuple, List

# Default class names for training
DEFAULT_CLASS_NAMES = [
    "HELLO", "THANK_YOU", "YES", "NO", "PLEASE", 
    "SORRY", "HELP", "LOVE", "GOOD", "BAD",
    "STOP", "GO", "WATER", "FOOD", "BATHROOM",
    "HAPPY", "SAD", "ANGRY", "SCARED", "TIRED"
]
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_training_data(data_dir: str = 'training_data') -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Load training data from JSON files.
    
    Expected structure:
    training_data/
        HELLO/
            sequence_1.json
            sequence_2.json
            ...
        THANK_YOU/
            ...
    
    Each JSON file contains a list of frames, where each frame is:
    [
        [  # Hand 1
            {"x": 0.5, "y": 0.3, "z": 0.1},  # Landmark 0
            {"x": 0.6, "y": 0.4, "z": 0.2},  # Landmark 1
            ...  # 21 landmarks total
        ],
        [  # Hand 2 (optional)
            ...
        ]
    ]
    
    Args:
        data_dir: Directory containing training data
        
    Returns:
        Tuple of (X, y, class_names) where:
        - X: Feature sequences (n_samples, sequence_length, num_features)
        - y: Labels (n_samples,) - string labels
        - class_names: List of unique class names
    """
    X = []
    y = []
    class_names = []
    
    if not os.path.exists(data_dir):
        logger.warning(f"Training data directory not found: {data_dir}")
        logger.info("Creating sample training data structure...")
        create_sample_data_structure(data_dir)
        return None, None, None
    
    # Iterate through gesture directories
    for gesture_name in os.listdir(data_dir):
        gesture_path = os.path.join(data_dir, gesture_name)
        
        if not os.path.isdir(gesture_path):
            continue
        
        if gesture_name not in class_names:
            class_names.append(gesture_name)
        
        gesture_idx = class_names.index(gesture_name)
        
        # Load all sequences for this gesture
        sequence_files = [f for f in os.listdir(gesture_path) if f.endswith('.json')]
        
        logger.info(f"Loading {len(sequence_files)} sequences for gesture: {gesture_name}")
        
        for seq_file in sequence_files:
            seq_path = os.path.join(gesture_path, seq_file)
            
            try:
                with open(seq_path, 'r') as f:
                    sequence_data = json.load(f)
                
                # Process sequence
                model = SignLanguageModel()
                features = model.prepare_sequence(sequence_data)
                
                X.append(features)
                y.append(gesture_name)
                
            except Exception as e:
                logger.error(f"Error loading {seq_path}: {e}")
                continue
    
    if len(X) == 0:
        logger.error("No training data found!")
        return None, None, None
    
    X = np.array(X)
    y = np.array(y)
    
    logger.info(f"Loaded {len(X)} samples across {len(class_names)} classes")
    logger.info(f"Class names: {class_names}")
    logger.info(f"Feature shape: {X.shape}")
    
    return X, y, class_names

def create_sample_data_structure(data_dir: str):
    """Create sample directory structure for training data."""
    os.makedirs(data_dir, exist_ok=True)
    
    for gesture in DEFAULT_CLASS_NAMES:
        gesture_dir = os.path.join(data_dir, gesture)
        os.makedirs(gesture_dir, exist_ok=True)
        
        # Create a README in each directory
        readme_path = os.path.join(gesture_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write(f"# {gesture} Training Data\n\n")
            f.write(f"Place JSON sequence files for the '{gesture}' gesture here.\n\n")
            f.write("Each JSON file should contain a list of frames:\n")
            f.write("```json\n")
            f.write("[\n")
            f.write("  [  // Hand 1 - 21 landmarks\n")
            f.write("    {\"x\": 0.5, \"y\": 0.3, \"z\": 0.1},\n")
            f.write("    ...\n")
            f.write("  ],\n")
            f.write("  [  // Hand 2 (optional)\n")
            f.write("    ...\n")
            f.write("  ]\n")
            f.write("]\n")
            f.write("```\n")

def prepare_labels(y: np.ndarray, class_names: List[str]) -> np.ndarray:
    """
    Convert string labels to one-hot encoded vectors.
    
    Args:
        y: String labels (n_samples,)
        class_names: List of all class names
        
    Returns:
        One-hot encoded labels (n_samples, num_classes)
    """
    num_classes = len(class_names)
    y_encoded = np.zeros((len(y), num_classes))
    
    for i, label in enumerate(y):
        if label in class_names:
            class_idx = class_names.index(label)
            y_encoded[i, class_idx] = 1.0
    
    return y_encoded

def train_sign_language_model(
    data_dir: str = 'training_data',
    model_save_path: str = 'models/sign_language_model.h5',
    epochs: int = 50,
    batch_size: int = 32,
    test_size: float = 0.2
):
    """
    Main training function.
    
    Args:
        data_dir: Directory containing training data
        model_save_path: Path to save trained model
        epochs: Number of training epochs
        batch_size: Batch size for training
        test_size: Fraction of data to use for validation
    """
    logger.info("=" * 60)
    logger.info("Sign Language Gesture Recognition Model Training")
    logger.info("=" * 60)
    
    # Load training data
    logger.info("Loading training data...")
    X, y, class_names = load_training_data(data_dir)
    
    if X is None:
        logger.error("Failed to load training data. Please collect data first.")
        logger.info("Run: python collect_training_data.py")
        return
    
    # Prepare labels
    logger.info("Preparing labels...")
    y_encoded = prepare_labels(y, class_names)
    
    # Split data
    logger.info("Splitting data into train/validation sets...")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y_encoded, test_size=test_size, random_state=42, stratify=y
    )
    
    logger.info(f"Training samples: {len(X_train)}")
    logger.info(f"Validation samples: {len(X_val)}")
    
    # Create and train model
    logger.info("Building model...")
    model = SignLanguageModel(
        sequence_length=X.shape[1],
        num_features=X.shape[2],
        num_classes=len(class_names)
    )
    
    model.build_model()
    model.model.summary()
    
    logger.info("Starting training...")
    history = model.train(
        X_train, y_train,
        X_val, y_val,
        epochs=epochs,
        batch_size=batch_size,
        class_names=class_names
    )
    
    # Save model
    logger.info("Saving model...")
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    model.save_model(model_save_path)
    
    logger.info("=" * 60)
    logger.info("Training completed successfully!")
    logger.info(f"Model saved to: {model_save_path}")
    logger.info("=" * 60)
    
    # Print final metrics
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    logger.info(f"Final training accuracy: {final_train_acc:.4f}")
    logger.info(f"Final validation accuracy: {final_val_acc:.4f}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Train Sign Language Gesture Recognition Model')
    parser.add_argument('--data-dir', type=str, default='training_data',
                        help='Directory containing training data')
    parser.add_argument('--model-path', type=str, default='models/sign_language_model.h5',
                        help='Path to save trained model')
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32,
                        help='Batch size for training')
    parser.add_argument('--test-size', type=float, default=0.2,
                        help='Fraction of data for validation')
    
    args = parser.parse_args()
    
    train_sign_language_model(
        data_dir=args.data_dir,
        model_save_path=args.model_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        test_size=args.test_size
    )

