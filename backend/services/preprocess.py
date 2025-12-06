"""
Preprocessing Service - Landmark normalization and feature extraction
"""
import numpy as np
from typing import List, Dict, Tuple

def normalize_landmarks(landmarks: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """
    Normalize hand landmarks to a consistent format.
    
    Args:
        landmarks: List of landmarks with x, y, z coordinates
        
    Returns:
        Normalized landmarks
    """
    if not landmarks or len(landmarks) == 0:
        return []
    
    # Ensure we have exactly 21 landmarks (MediaPipe hand model)
    if len(landmarks) != 21:
        landmarks = landmarks[:21]
    
    # Clamp values to valid ranges [0, 1] for x, y
    normalized = []
    for landmark in landmarks:
        normalized.append({
            'x': max(0, min(1, landmark.get('x', 0))),
            'y': max(0, min(1, landmark.get('y', 0))),
            'z': landmark.get('z', 0)
        })
    
    return normalized

def normalize_hands(hands: List[List[Dict[str, float]]]) -> List[List[Dict[str, float]]]:
    """
    Normalize multiple hands.
    
    Args:
        hands: List of hand landmark lists
        
    Returns:
        Normalized hands
    """
    return [normalize_landmarks(hand) for hand in hands if hand and len(hand) > 0]

def flatten_landmarks(landmarks: List[Dict[str, float]]) -> np.ndarray:
    """
    Flatten landmarks to feature vector.
    
    Args:
        landmarks: List of landmarks
        
    Returns:
        Flattened array of shape (63,) for one hand
    """
    features = []
    for landmark in landmarks:
        features.extend([landmark['x'], landmark['y'], landmark['z']])
    
    # Pad to 21 landmarks * 3 coords = 63 features
    while len(features) < 63:
        features.append(0.0)
    
    return np.array(features[:63], dtype=np.float32)

def flatten_hands(hands: List[List[Dict[str, float]]]) -> np.ndarray:
    """
    Flatten multiple hands for model input.
    
    Args:
        hands: List of hand landmark lists (max 2 hands)
        
    Returns:
        Flattened array of shape (126,) for 2 hands
    """
    max_hands = 2
    features_per_hand = 63
    total_size = max_hands * features_per_hand
    
    flattened = np.zeros(total_size, dtype=np.float32)
    
    for hand_idx in range(min(max_hands, len(hands))):
        normalized_hand = normalize_landmarks(hands[hand_idx])
        hand_features = flatten_landmarks(normalized_hand)
        start_idx = hand_idx * features_per_hand
        flattened[start_idx:start_idx + features_per_hand] = hand_features
    
    return flattened

def get_center_of_mass(landmarks: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Calculate center of mass for landmarks.
    
    Args:
        landmarks: List of landmarks
        
    Returns:
        Center of mass coordinates
    """
    if len(landmarks) == 0:
        return {'x': 0, 'y': 0, 'z': 0}
    
    sum_x = sum(l['x'] for l in landmarks)
    sum_y = sum(l['y'] for l in landmarks)
    sum_z = sum(l['z'] for l in landmarks)
    
    n = len(landmarks)
    return {
        'x': sum_x / n,
        'y': sum_y / n,
        'z': sum_z / n
    }

def center_landmarks(landmarks: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """
    Center landmarks around origin.
    
    Args:
        landmarks: List of landmarks
        
    Returns:
        Centered landmarks
    """
    center = get_center_of_mass(landmarks)
    return [
        {
            'x': l['x'] - center['x'],
            'y': l['y'] - center['y'],
            'z': l['z'] - center['z']
        }
        for l in landmarks
    ]

def scale_landmarks(landmarks: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """
    Scale landmarks to unit size.
    
    Args:
        landmarks: List of landmarks
        
    Returns:
        Scaled landmarks
    """
    if len(landmarks) == 0:
        return landmarks
    
    xs = [l['x'] for l in landmarks]
    ys = [l['y'] for l in landmarks]
    zs = [l['z'] for l in landmarks]
    
    scale_x = max(xs) - min(xs) or 1
    scale_y = max(ys) - min(ys) or 1
    scale_z = max(zs) - min(zs) or 1
    max_scale = max(scale_x, scale_y, scale_z)
    
    if max_scale == 0:
        return landmarks
    
    return [
        {
            'x': l['x'] / max_scale,
            'y': l['y'] / max_scale,
            'z': l['z'] / max_scale
        }
        for l in landmarks
    ]

