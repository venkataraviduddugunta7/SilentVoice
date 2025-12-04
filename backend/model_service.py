"""
Model Service for Loading and Using the Trained Sign Language Model
This service loads the model once and provides prediction functions.
"""

import os
import logging
from typing import List, Dict, Tuple, Optional
from model import SignLanguageModel

logger = logging.getLogger(__name__)

class ModelService:
    """Service for managing the sign language recognition model."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one model instance."""
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the model service."""
        if self._model is None:
            self._model = SignLanguageModel()
            self._is_loaded = False
    
    def load_model(self, model_path: str = 'models/sign_language_model.h5') -> bool:
        """
        Load the trained model.
        
        Args:
            model_path: Path to the saved model file
            
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(model_path):
                logger.warning(f"Model file not found: {model_path}")
                logger.info("Using rule-based fallback. Train a model first with: python train_model.py")
                return False
            
            self._model.load_model(model_path)
            self._is_loaded = True
            logger.info(f"✅ Model loaded successfully from {model_path}")
            logger.info(f"   Classes: {self._model.class_names}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            self._is_loaded = False
            return False
    
    def predict(self, landmarks: List[List[Dict[str, float]]]) -> Tuple[str, float]:
        """
        Predict gesture from hand landmarks.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Tuple of (predicted_class, confidence)
        """
        if not self._is_loaded:
            raise ValueError("Model not loaded. Call load_model() first or use fallback.")
        
        try:
            return self._model.predict(landmarks)
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return "Unknown", 0.0
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._is_loaded
    
    def get_class_names(self) -> List[str]:
        """Get list of class names the model recognizes."""
        if self._is_loaded and self._model.class_names:
            return self._model.class_names
        return []


# Global model service instance
model_service = ModelService()

def get_model_service() -> ModelService:
    """Get the global model service instance."""
    return model_service

