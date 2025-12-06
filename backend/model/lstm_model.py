"""
LSTM Model Architecture for Sign Language Recognition
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import List, Dict, Tuple, Optional
import os
import json
import logging

logger = logging.getLogger(__name__)

class SignLanguageModel:
    """
    LSTM-based model for recognizing sign language gestures from hand landmarks.
    """
    
    def __init__(self, sequence_length: int = 30, num_features: int = 63, num_classes: int = 10):
        """
        Initialize the sign language recognition model.
        
        Args:
            sequence_length: Number of frames in a sequence (default: 30)
            num_features: Number of features per frame (21 landmarks * 3 coords = 63)
            num_classes: Number of gesture classes to recognize
        """
        self.sequence_length = sequence_length
        self.num_features = num_features
        self.num_classes = num_classes
        self.model = None
        self.class_names = []
        self.is_trained = False
        
    def build_model(self) -> keras.Model:
        """
        Build the LSTM model architecture.
        
        Returns:
            Compiled Keras model
        """
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=(self.sequence_length, self.num_features)),
            
            # Normalization layer
            layers.BatchNormalization(),
            
            # First LSTM layer with dropout
            layers.LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.3),
            layers.BatchNormalization(),
            
            # Second LSTM layer
            layers.LSTM(64, return_sequences=True, dropout=0.3, recurrent_dropout=0.3),
            layers.BatchNormalization(),
            
            # Third LSTM layer
            layers.LSTM(32, return_sequences=False, dropout=0.3),
            layers.BatchNormalization(),
            
            # Dense layers
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.4),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.3),
            
            # Output layer
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'top_k_categorical_accuracy']
        )
        
        self.model = model
        return model
    
    def prepare_sequence(self, landmarks: List[List[Dict[str, float]]]) -> np.ndarray:
        """
        Prepare hand landmark data for model input.
        
        Args:
            landmarks: List of hand landmarks (can be 1 or 2 hands)
            
        Returns:
            Normalized feature array of shape (sequence_length, num_features)
        """
        # Flatten landmarks to feature vector
        features = []
        
        if len(landmarks) == 0:
            return np.zeros((self.sequence_length, self.num_features))
        
        # Process up to 2 hands
        for hand_idx in range(min(2, len(landmarks))):
            hand = landmarks[hand_idx]
            if len(hand) >= 21:
                for landmark in hand[:21]:
                    features.extend([landmark.get('x', 0), landmark.get('y', 0), landmark.get('z', 0)])
            else:
                for _ in range(21):
                    features.extend([0, 0, 0])
        
        # If only one hand, pad second hand with zeros
        if len(landmarks) == 1:
            for _ in range(21):
                features.extend([0, 0, 0])
        
        # Ensure we have exactly num_features
        features = features[:self.num_features]
        while len(features) < self.num_features:
            features.append(0)
        
        features = np.array(features, dtype=np.float32)
        sequence = np.tile(features, (self.sequence_length, 1))
        
        return sequence
    
    def predict(self, landmarks: List[List[Dict[str, float]]]) -> Tuple[str, float]:
        """
        Predict gesture from hand landmarks.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Tuple of (predicted_class, confidence)
        """
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        sequence = self.prepare_sequence(landmarks)
        sequence = np.expand_dims(sequence, axis=0)
        
        predictions = self.model.predict(sequence, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])
        
        if self.class_names and predicted_idx < len(self.class_names):
            predicted_class = self.class_names[predicted_idx]
        else:
            predicted_class = f"Class_{predicted_idx}"
        
        return predicted_class, confidence
    
    def save_model(self, model_path: str, metadata_path: str = None):
        """Save the trained model and metadata."""
        if self.model is None:
            raise ValueError("No model to save. Train or load a model first.")
        
        os.makedirs(os.path.dirname(model_path) if os.path.dirname(model_path) else '.', exist_ok=True)
        self.model.save(model_path)
        logger.info(f"Model saved to {model_path}")
        
        if metadata_path is None:
            metadata_path = model_path.replace('.h5', '_metadata.json')
        
        metadata = {
            'sequence_length': self.sequence_length,
            'num_features': self.num_features,
            'num_classes': self.num_classes,
            'class_names': self.class_names,
            'is_trained': self.is_trained
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Metadata saved to {metadata_path}")
    
    def load_model(self, model_path: str, metadata_path: str = None):
        """Load a trained model and metadata."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        self.model = keras.models.load_model(model_path)
        logger.info(f"Model loaded from {model_path}")
        
        if metadata_path is None:
            metadata_path = model_path.replace('.h5', '_metadata.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.sequence_length = metadata.get('sequence_length', self.sequence_length)
            self.num_features = metadata.get('num_features', self.num_features)
            self.num_classes = metadata.get('num_classes', self.num_classes)
            self.class_names = metadata.get('class_names', [])
            self.is_trained = metadata.get('is_trained', False)
            
            logger.info(f"Metadata loaded from {metadata_path}")
            logger.info(f"Class names: {self.class_names}")

