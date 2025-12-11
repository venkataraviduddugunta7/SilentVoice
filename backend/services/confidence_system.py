"""
Confidence Threshold System for accurate predictions
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ConfidenceSystem:
    """
    Advanced confidence scoring and threshold management
    """
    
    def __init__(self):
        # Confidence thresholds for different scenarios
        self.thresholds = {
            'high_confidence': 0.85,      # Very certain
            'medium_confidence': 0.70,    # Reasonably certain
            'low_confidence': 0.50,       # Uncertain
            'rejection_threshold': 0.40   # Too uncertain to predict
        }
        
        # Adaptive threshold based on context
        self.context_modifiers = {
            'single_hand': 1.0,           # Normal confidence
            'two_hands': 0.95,            # Slightly lower for complex signs
            'moving_sign': 0.90,          # Lower for motion-based signs
            'static_sign': 1.05           # Higher for static signs
        }
        
        # History for temporal smoothing
        self.prediction_history = []
        self.history_size = 5
        
        # Calibration parameters
        self.calibration_factor = 1.0
        self.noise_threshold = 0.1
        
    def calculate_confidence(self, 
                            predictions: np.ndarray,
                            landmarks: Optional[Dict] = None,
                            context: str = 'single_hand') -> Tuple[str, float, Dict]:
        """
        Calculate confidence score with advanced metrics
        
        Args:
            predictions: Model prediction probabilities
            landmarks: Hand landmark data for additional analysis
            context: Context of the sign (single_hand, two_hands, etc.)
            
        Returns:
            Tuple of (predicted_sign, confidence_score, metadata)
        """
        
        # Get base confidence from model
        max_prob_idx = np.argmax(predictions)
        base_confidence = float(predictions[max_prob_idx])
        
        # Apply context modifier
        context_modifier = self.context_modifiers.get(context, 1.0)
        adjusted_confidence = base_confidence * context_modifier
        
        # Calculate entropy for uncertainty measurement
        entropy = -np.sum(predictions * np.log(predictions + 1e-10))
        max_entropy = -np.log(1.0 / len(predictions))
        normalized_entropy = entropy / max_entropy
        
        # Entropy penalty (high entropy = low confidence)
        entropy_penalty = 1.0 - (normalized_entropy * 0.3)
        adjusted_confidence *= entropy_penalty
        
        # Landmark stability check
        if landmarks:
            stability_score = self._calculate_landmark_stability(landmarks)
            adjusted_confidence *= stability_score
        
        # Temporal smoothing
        if self.prediction_history:
            temporal_confidence = self._apply_temporal_smoothing(
                max_prob_idx, adjusted_confidence
            )
            adjusted_confidence = temporal_confidence
        
        # Apply calibration
        final_confidence = min(adjusted_confidence * self.calibration_factor, 1.0)
        
        # Update history
        self._update_history(max_prob_idx, final_confidence)
        
        # Determine confidence level
        confidence_level = self._get_confidence_level(final_confidence)
        
        # Prepare metadata
        metadata = {
            'base_confidence': base_confidence,
            'adjusted_confidence': adjusted_confidence,
            'final_confidence': final_confidence,
            'entropy': normalized_entropy,
            'confidence_level': confidence_level,
            'context': context,
            'should_predict': final_confidence >= self.thresholds['rejection_threshold']
        }
        
        # Get sign name (would come from vocabulary mapping)
        sign_name = self._idx_to_sign(max_prob_idx)
        
        # Log if confidence is low
        if confidence_level == 'low' or confidence_level == 'rejected':
            logger.warning(f"Low confidence prediction: {sign_name} ({final_confidence:.2%})")
        
        return sign_name, final_confidence, metadata
    
    def _calculate_landmark_stability(self, landmarks: Dict) -> float:
        """
        Calculate stability score based on landmark positions
        """
        # Simplified stability check - in production, compare with previous frames
        if not landmarks:
            return 1.0
        
        # Check for landmark completeness
        if 'multiHandLandmarks' in landmarks:
            hand_count = len(landmarks['multiHandLandmarks'])
            if hand_count == 0:
                return 0.5  # No hands detected
            
            # Check landmark quality (simplified)
            for hand in landmarks['multiHandLandmarks']:
                if len(hand) < 21:  # Should have 21 landmarks
                    return 0.7
        
        return 1.0  # Good stability
    
    def _apply_temporal_smoothing(self, 
                                 current_idx: int, 
                                 current_confidence: float) -> float:
        """
        Apply temporal smoothing based on prediction history
        """
        if not self.prediction_history:
            return current_confidence
        
        # Check consistency with recent predictions
        recent_predictions = [h['idx'] for h in self.prediction_history[-3:]]
        consistency_score = recent_predictions.count(current_idx) / len(recent_predictions)
        
        # Boost confidence if consistent, reduce if not
        if consistency_score >= 0.67:  # At least 2 out of 3 same
            return min(current_confidence * 1.1, 1.0)
        elif consistency_score <= 0.33:  # Different predictions
            return current_confidence * 0.9
        
        return current_confidence
    
    def _update_history(self, idx: int, confidence: float):
        """
        Update prediction history for temporal analysis
        """
        self.prediction_history.append({
            'idx': idx,
            'confidence': confidence
        })
        
        # Keep only recent history
        if len(self.prediction_history) > self.history_size:
            self.prediction_history.pop(0)
    
    def _get_confidence_level(self, confidence: float) -> str:
        """
        Categorize confidence into levels
        """
        if confidence >= self.thresholds['high_confidence']:
            return 'high'
        elif confidence >= self.thresholds['medium_confidence']:
            return 'medium'
        elif confidence >= self.thresholds['low_confidence']:
            return 'low'
        else:
            return 'rejected'
    
    def _idx_to_sign(self, idx: int) -> str:
        """
        Map prediction index to sign name
        """
        # This would be loaded from your vocabulary
        sign_mapping = {
            0: 'hello',
            1: 'thank_you',
            2: 'please',
            3: 'yes',
            4: 'no',
            5: 'help',
            6: 'stop',
            7: 'wait',
            8: 'sorry',
            9: 'goodbye'
        }
        
        return sign_mapping.get(idx, f'sign_{idx}')
    
    def calibrate(self, true_positives: List[float], false_positives: List[float]):
        """
        Calibrate confidence scores based on performance
        """
        if true_positives and false_positives:
            # Simple calibration - adjust based on precision
            tp_mean = np.mean(true_positives)
            fp_mean = np.mean(false_positives) if false_positives else 0
            
            if tp_mean > 0:
                self.calibration_factor = 1.0 + (tp_mean - fp_mean) * 0.1
                self.calibration_factor = np.clip(self.calibration_factor, 0.8, 1.2)
                
                logger.info(f"Calibrated confidence system: factor={self.calibration_factor:.2f}")
    
    def reset_history(self):
        """
        Reset prediction history
        """
        self.prediction_history = []
    
    def update_thresholds(self, thresholds: Dict[str, float]):
        """
        Update confidence thresholds
        """
        self.thresholds.update(thresholds)
        logger.info(f"Updated confidence thresholds: {self.thresholds}")
    
    def get_stats(self) -> Dict:
        """
        Get confidence system statistics
        """
        if not self.prediction_history:
            return {
                'average_confidence': 0,
                'prediction_count': 0,
                'high_confidence_ratio': 0
            }
        
        confidences = [h['confidence'] for h in self.prediction_history]
        high_conf_count = sum(1 for c in confidences if c >= self.thresholds['high_confidence'])
        
        return {
            'average_confidence': np.mean(confidences),
            'prediction_count': len(confidences),
            'high_confidence_ratio': high_conf_count / len(confidences),
            'calibration_factor': self.calibration_factor
        }