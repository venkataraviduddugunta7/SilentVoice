"""
Inference Service - Predict sign and confidence from landmarks
"""
import logging
import sys
import os
from typing import List, Dict, Tuple, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.lstm_model import SignLanguageModel
from services.preprocess import normalize_hands, flatten_hands

logger = logging.getLogger(__name__)

class InferenceService:
    """Service for running inference on hand landmarks."""
    
    def __init__(self, model: Optional[SignLanguageModel] = None):
        """
        Initialize inference service.
        
        Args:
            model: Optional pre-loaded model instance
        """
        self.model = model
        self.is_loaded = model is not None
    
    def load_model(self, model_path: str) -> bool:
        """
        Load a trained model.
        
        Args:
            model_path: Path to the model file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            self.model = SignLanguageModel()
            self.model.load_model(model_path)
            self.is_loaded = True
            logger.info(f"✅ Inference model loaded from {model_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error loading inference model: {e}")
            self.is_loaded = False
            return False
    
    def predict(self, landmarks: List[List[Dict[str, float]]]) -> Tuple[str, float]:
        """
        Predict gesture from hand landmarks.
        
        Args:
            landmarks: List of hand landmark lists
            
        Returns:
            Tuple of (predicted_word, confidence_score)
        """
        if not self.is_loaded or self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        try:
            # Normalize landmarks
            normalized_hands = normalize_hands(landmarks)
            
            if not normalized_hands:
                return "Unknown", 0.0
            
            # Predict using model
            predicted_word, confidence = self.model.predict(normalized_hands)
            
            return predicted_word, confidence
            
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            return "Unknown", 0.0
    
    def predict_batch(self, landmarks_batch: List[List[List[Dict[str, float]]]]) -> List[Tuple[str, float]]:
        """
        Predict gestures for a batch of landmark sequences.
        
        Args:
            landmarks_batch: List of landmark sequences
            
        Returns:
            List of (predicted_word, confidence) tuples
        """
        return [self.predict(landmarks) for landmarks in landmarks_batch]

# Global inference service instance
_inference_service: Optional[InferenceService] = None

def get_inference_service() -> InferenceService:
    """Get the global inference service instance."""
    global _inference_service
    if _inference_service is None:
        _inference_service = InferenceService()
    return _inference_service

