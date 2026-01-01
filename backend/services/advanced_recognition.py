"""
Advanced ASL Recognition Service with proper gesture patterns and filtering
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Optional
from collections import deque
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class GestureState(Enum):
    """States for gesture recognition"""
    IDLE = "idle"
    DETECTING = "detecting"
    HOLDING = "holding"
    TRANSITIONING = "transitioning"

@dataclass
class GestureFrame:
    """Single frame of gesture data"""
    timestamp: float
    left_hand: Optional[List[Dict]]
    right_hand: Optional[List[Dict]]
    pose: Optional[List[Dict]]
    face: Optional[List[Dict]]
    
@dataclass
class RecognizedGesture:
    """Recognized gesture with metadata"""
    sign: str
    confidence: float
    hand: str  # "left", "right", "both"
    duration: float
    frames: int
    is_motion: bool

class AdvancedASLRecognizer:
    """Advanced ASL recognition with proper filtering and validation"""
    
    def __init__(self):
        self.gesture_buffer = deque(maxlen=60)  # 2 seconds at 30fps
        self.current_state = GestureState.IDLE
        self.last_recognized = None
        self.last_recognition_time = 0
        self.recognition_cooldown = 1.0  # 1 second cooldown
        
        # Load ASL patterns
        self.load_asl_patterns()
        
        # Recognition thresholds
        self.min_confidence = 0.6
        self.min_frames_for_static = 5
        self.min_frames_for_dynamic = 10
        self.max_motion_threshold = 0.15
        
        # Gesture history for sentence building
        self.gesture_history = deque(maxlen=20)
        
    def load_asl_patterns(self):
        """Load ASL sign patterns from data files"""
        data_dir = Path("asl_data")
        
        # Load sign definitions
        signs_file = data_dir / "asl_signs.json"
        if signs_file.exists():
            with open(signs_file, "r") as f:
                self.asl_signs = json.load(f)
        else:
            # Fallback to basic patterns
            self.asl_signs = self._get_default_patterns()
            
        # Load landmark patterns
        patterns_file = data_dir / "landmark_patterns.json"
        if patterns_file.exists():
            with open(patterns_file, "r") as f:
                self.landmark_patterns = json.load(f)
        else:
            self.landmark_patterns = self._get_default_landmark_patterns()
            
    def _get_default_patterns(self) -> Dict:
        """Get default ASL patterns"""
        return {
            "HELLO": {
                "type": "dynamic",
                "hand": "right",
                "motion": "wave",
                "fingers": "open",
                "palm": "forward"
            },
            "YES": {
                "type": "dynamic",
                "hand": "right",
                "motion": "nod",
                "shape": "fist"
            },
            "NO": {
                "type": "static",
                "hand": "right",
                "fingers": [1, 1, 0, 0, 0],
                "motion": "snap"
            },
            "THANK_YOU": {
                "type": "dynamic",
                "hand": "right",
                "start": "chin",
                "motion": "forward",
                "palm": "up"
            },
            "PLEASE": {
                "type": "dynamic",
                "hand": "right",
                "location": "chest",
                "motion": "circular"
            },
            "HELP": {
                "type": "static",
                "hand": "both",
                "right": "fist",
                "left": "flat",
                "position": "support"
            },
            "I_LOVE_YOU": {
                "type": "static",
                "hand": "right",
                "fingers": [1, 0, 0, 1, 1],  # Index, pinky, thumb
            },
            "WATER": {
                "type": "dynamic",
                "hand": "right",
                "shape": "w",
                "location": "chin",
                "motion": "tap"
            },
            "FOOD": {
                "type": "dynamic",
                "hand": "right",
                "motion": "to_mouth",
                "repeat": 2
            },
            "HUNGRY": {
                "type": "dynamic",
                "hand": "right",
                "shape": "c",
                "location": "chest",
                "motion": "down"
            }
        }
    
    def _get_default_landmark_patterns(self) -> Dict:
        """Get default landmark patterns"""
        return {
            "hand_landmarks": {
                "num_points": 21,
                "fingers": {
                    "thumb": [1, 2, 3, 4],
                    "index": [5, 6, 7, 8],
                    "middle": [9, 10, 11, 12],
                    "ring": [13, 14, 15, 16],
                    "pinky": [17, 18, 19, 20]
                },
                "palm": [0, 5, 9, 13, 17]
            }
        }
    
    def process_frame(self, frame_data: Dict) -> Optional[RecognizedGesture]:
        """Process a single frame and return recognized gesture if any"""
        
        # Create frame object
        frame = GestureFrame(
            timestamp=frame_data.get("timestamp", 0),
            left_hand=frame_data.get("leftHandLandmarks"),
            right_hand=frame_data.get("rightHandLandmarks"),
            pose=frame_data.get("poseLandmarks"),
            face=frame_data.get("faceLandmarks")
        )
        
        # Add to buffer
        self.gesture_buffer.append(frame)
        
        # Check if enough frames
        if len(self.gesture_buffer) < self.min_frames_for_static:
            return None
            
        # Analyze gesture
        gesture = self._analyze_gesture()
        
        # Apply temporal filtering
        if gesture:
            gesture = self._apply_temporal_filter(gesture)
            
        return gesture
    
    def _analyze_gesture(self) -> Optional[RecognizedGesture]:
        """Analyze current buffer for gestures"""
        
        # Check for motion
        motion_level = self._calculate_motion()
        
        if motion_level < self.max_motion_threshold:
            # Static gesture
            return self._recognize_static_gesture()
        else:
            # Dynamic gesture
            return self._recognize_dynamic_gesture()
    
    def _calculate_motion(self) -> float:
        """Calculate motion level in buffer"""
        if len(self.gesture_buffer) < 2:
            return 0.0
            
        total_motion = 0.0
        prev_frame = self.gesture_buffer[0]
        
        for frame in list(self.gesture_buffer)[1:]:
            if prev_frame.right_hand and frame.right_hand:
                motion = self._calculate_hand_motion(
                    prev_frame.right_hand,
                    frame.right_hand
                )
                total_motion += motion
            prev_frame = frame
            
        return total_motion / len(self.gesture_buffer)
    
    def _calculate_hand_motion(self, hand1: List[Dict], hand2: List[Dict]) -> float:
        """Calculate motion between two hand frames"""
        if len(hand1) != len(hand2):
            return 0.0
            
        total_distance = 0.0
        for p1, p2 in zip(hand1, hand2):
            dx = p1.get("x", 0) - p2.get("x", 0)
            dy = p1.get("y", 0) - p2.get("y", 0)
            total_distance += np.sqrt(dx*dx + dy*dy)
            
        return total_distance / len(hand1)
    
    def _recognize_static_gesture(self) -> Optional[RecognizedGesture]:
        """Recognize static gestures"""
        
        # Get average hand position
        avg_hand = self._get_average_hand_position()
        if not avg_hand:
            return None
            
        # Extract features
        features = self._extract_hand_features(avg_hand)
        
        # Match against patterns
        best_match = None
        best_confidence = 0.0
        
        for sign_name, pattern in self.asl_signs.items():
            if pattern.get("type") != "static":
                continue
                
            confidence = self._match_static_pattern(features, pattern)
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = sign_name
        
        if best_confidence > self.min_confidence:
            return RecognizedGesture(
                sign=best_match,
                confidence=best_confidence,
                hand="right",
                duration=len(self.gesture_buffer) / 30.0,
                frames=len(self.gesture_buffer),
                is_motion=False
            )
        
        return None
    
    def _recognize_dynamic_gesture(self) -> Optional[RecognizedGesture]:
        """Recognize dynamic gestures"""
        
        # Extract motion features
        motion_features = self._extract_motion_features()
        if not motion_features:
            return None
            
        # Match against patterns
        best_match = None
        best_confidence = 0.0
        
        for sign_name, pattern in self.asl_signs.items():
            if pattern.get("type") != "dynamic":
                continue
                
            confidence = self._match_dynamic_pattern(motion_features, pattern)
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = sign_name
        
        if best_confidence > self.min_confidence:
            return RecognizedGesture(
                sign=best_match,
                confidence=best_confidence,
                hand="right",
                duration=len(self.gesture_buffer) / 30.0,
                frames=len(self.gesture_buffer),
                is_motion=True
            )
        
        return None
    
    def _get_average_hand_position(self) -> Optional[List[Dict]]:
        """Get average hand position from buffer"""
        valid_frames = [f for f in self.gesture_buffer if f.right_hand]
        if not valid_frames:
            return None
            
        # Average all landmarks
        avg_landmarks = []
        num_points = len(valid_frames[0].right_hand)
        
        for i in range(num_points):
            avg_x = np.mean([f.right_hand[i].get("x", 0) for f in valid_frames])
            avg_y = np.mean([f.right_hand[i].get("y", 0) for f in valid_frames])
            avg_z = np.mean([f.right_hand[i].get("z", 0) for f in valid_frames])
            avg_landmarks.append({"x": avg_x, "y": avg_y, "z": avg_z})
            
        return avg_landmarks
    
    def _extract_hand_features(self, hand_landmarks: List[Dict]) -> Dict:
        """Extract features from hand landmarks"""
        if not hand_landmarks or len(hand_landmarks) < 21:
            return {}
            
        features = {
            "finger_states": self._get_finger_states(hand_landmarks),
            "palm_orientation": self._get_palm_orientation(hand_landmarks),
            "hand_shape": self._get_hand_shape(hand_landmarks),
            "thumb_position": self._get_thumb_position(hand_landmarks)
        }
        
        return features
    
    def _get_finger_states(self, landmarks: List[Dict]) -> List[float]:
        """Get finger extension states (0=closed, 1=open)"""
        states = []
        
        # For each finger
        fingers = ["thumb", "index", "middle", "ring", "pinky"]
        finger_tips = [4, 8, 12, 16, 20]
        finger_bases = [2, 5, 9, 13, 17]
        
        for tip, base in zip(finger_tips, finger_bases):
            if tip < len(landmarks) and base < len(landmarks):
                # Calculate if finger is extended
                tip_y = landmarks[tip].get("y", 0)
                base_y = landmarks[base].get("y", 0)
                extended = 1.0 if tip_y < base_y else 0.0
                states.append(extended)
            else:
                states.append(0.0)
                
        return states
    
    def _get_palm_orientation(self, landmarks: List[Dict]) -> str:
        """Get palm orientation"""
        if len(landmarks) < 21:
            return "unknown"
            
        # Use wrist and middle finger base
        wrist = landmarks[0]
        middle_base = landmarks[9]
        
        dx = middle_base.get("x", 0) - wrist.get("x", 0)
        dy = middle_base.get("y", 0) - wrist.get("y", 0)
        
        if abs(dx) > abs(dy):
            return "horizontal"
        else:
            return "vertical"
    
    def _get_hand_shape(self, landmarks: List[Dict]) -> str:
        """Determine hand shape"""
        finger_states = self._get_finger_states(landmarks)
        
        open_fingers = sum(1 for f in finger_states if f > 0.5)
        
        if open_fingers == 0:
            return "fist"
        elif open_fingers == 5:
            return "open"
        elif open_fingers == 1:
            return "pointing"
        elif open_fingers == 2:
            return "peace"
        else:
            return "partial"
    
    def _get_thumb_position(self, landmarks: List[Dict]) -> str:
        """Get thumb position relative to hand"""
        if len(landmarks) < 21:
            return "unknown"
            
        thumb_tip = landmarks[4]
        index_base = landmarks[5]
        
        if thumb_tip.get("x", 0) < index_base.get("x", 0):
            return "in"
        else:
            return "out"
    
    def _extract_motion_features(self) -> Optional[Dict]:
        """Extract motion features from buffer"""
        if len(self.gesture_buffer) < self.min_frames_for_dynamic:
            return None
            
        features = {
            "motion_type": self._get_motion_type(),
            "direction": self._get_motion_direction(),
            "repetitions": self._count_repetitions(),
            "speed": self._get_motion_speed()
        }
        
        return features
    
    def _get_motion_type(self) -> str:
        """Determine type of motion"""
        positions = []
        
        for frame in self.gesture_buffer:
            if frame.right_hand and len(frame.right_hand) > 0:
                # Use wrist position
                wrist = frame.right_hand[0]
                positions.append([wrist.get("x", 0), wrist.get("y", 0)])
        
        if not positions:
            return "none"
            
        positions = np.array(positions)
        
        # Check for circular motion
        if self._is_circular_motion(positions):
            return "circular"
        
        # Check for wave motion
        if self._is_wave_motion(positions):
            return "wave"
            
        # Check for linear motion
        if self._is_linear_motion(positions):
            return "linear"
            
        return "complex"
    
    def _is_circular_motion(self, positions: np.ndarray) -> bool:
        """Check if positions form a circular pattern"""
        if len(positions) < 10:
            return False
            
        # Calculate center
        center = positions.mean(axis=0)
        
        # Calculate distances from center
        distances = np.sqrt(((positions - center) ** 2).sum(axis=1))
        
        # Check if distances are relatively constant
        std_dev = distances.std()
        mean_dist = distances.mean()
        
        return std_dev / mean_dist < 0.3 if mean_dist > 0 else False
    
    def _is_wave_motion(self, positions: np.ndarray) -> bool:
        """Check if positions form a wave pattern"""
        if len(positions) < 10:
            return False
            
        # Check horizontal variation
        x_variation = positions[:, 0].std()
        y_variation = positions[:, 1].std()
        
        # Wave has high x variation, low y variation
        return x_variation > 0.1 and y_variation < 0.05
    
    def _is_linear_motion(self, positions: np.ndarray) -> bool:
        """Check if positions form a linear pattern"""
        if len(positions) < 5:
            return False
            
        try:
            # Fit a line and check residuals
            from scipy import stats
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                positions[:, 0], positions[:, 1]
            )
            return abs(r_value) > 0.9
        except ImportError:
            # Fallback if scipy not available
            # Simple check: if points mostly move in one direction
            x_range = positions[:, 0].max() - positions[:, 0].min()
            y_range = positions[:, 1].max() - positions[:, 1].min()
            
            # Linear if one dimension dominates
            return max(x_range, y_range) > 3 * min(x_range, y_range)
    
    def _get_motion_direction(self) -> str:
        """Get primary direction of motion"""
        if len(self.gesture_buffer) < 2:
            return "none"
            
        start_frame = self.gesture_buffer[0]
        end_frame = self.gesture_buffer[-1]
        
        if not (start_frame.right_hand and end_frame.right_hand):
            return "none"
            
        start_wrist = start_frame.right_hand[0]
        end_wrist = end_frame.right_hand[0]
        
        dx = end_wrist.get("x", 0) - start_wrist.get("x", 0)
        dy = end_wrist.get("y", 0) - start_wrist.get("y", 0)
        
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        else:
            return "down" if dy > 0 else "up"
    
    def _count_repetitions(self) -> int:
        """Count motion repetitions"""
        # Simple peak counting
        positions = []
        
        for frame in self.gesture_buffer:
            if frame.right_hand and len(frame.right_hand) > 0:
                wrist = frame.right_hand[0]
                positions.append(wrist.get("y", 0))
        
        if len(positions) < 10:
            return 1
            
        # Count peaks
        peaks = 0
        for i in range(1, len(positions) - 1):
            if positions[i] > positions[i-1] and positions[i] > positions[i+1]:
                peaks += 1
                
        return max(1, peaks)
    
    def _get_motion_speed(self) -> float:
        """Calculate average motion speed"""
        if len(self.gesture_buffer) < 2:
            return 0.0
            
        total_distance = 0.0
        prev_frame = self.gesture_buffer[0]
        
        for frame in list(self.gesture_buffer)[1:]:
            if prev_frame.right_hand and frame.right_hand:
                distance = self._calculate_hand_motion(
                    prev_frame.right_hand,
                    frame.right_hand
                )
                total_distance += distance
            prev_frame = frame
            
        duration = len(self.gesture_buffer) / 30.0  # Assuming 30fps
        return total_distance / duration if duration > 0 else 0.0
    
    def _match_static_pattern(self, features: Dict, pattern: Dict) -> float:
        """Match features against static pattern"""
        confidence = 0.0
        matches = 0
        total = 0
        
        # Check finger states
        if "fingers" in pattern and "finger_states" in features:
            pattern_fingers = pattern["fingers"]
            actual_fingers = features["finger_states"]
            
            if isinstance(pattern_fingers, list):
                for i, expected in enumerate(pattern_fingers):
                    if i < len(actual_fingers):
                        if abs(actual_fingers[i] - expected) < 0.3:
                            matches += 1
                        total += 1
        
        # Check hand shape
        if "shape" in pattern and "hand_shape" in features:
            if pattern["shape"] == features["hand_shape"]:
                matches += 2
            total += 2
        
        # Check palm orientation
        if "palm" in pattern and "palm_orientation" in features:
            if pattern["palm"] in features["palm_orientation"]:
                matches += 1
            total += 1
        
        if total > 0:
            confidence = matches / total
            
        return confidence
    
    def _match_dynamic_pattern(self, features: Dict, pattern: Dict) -> float:
        """Match features against dynamic pattern"""
        confidence = 0.0
        matches = 0
        total = 0
        
        # Check motion type
        if "motion" in pattern and "motion_type" in features:
            motion_map = {
                "wave": "wave",
                "circular": "circular",
                "forward": "linear",
                "tap": "linear",
                "nod": "linear"
            }
            
            expected = motion_map.get(pattern["motion"], pattern["motion"])
            if expected == features["motion_type"]:
                matches += 2
            total += 2
        
        # Check direction
        if "motion" in pattern and "direction" in features:
            direction_map = {
                "forward": "right",
                "down": "down",
                "up": "up"
            }
            
            if pattern["motion"] in direction_map:
                if direction_map[pattern["motion"]] == features["direction"]:
                    matches += 1
                total += 1
        
        # Check repetitions
        if "repeat" in pattern and "repetitions" in features:
            if abs(pattern["repeat"] - features["repetitions"]) <= 1:
                matches += 1
            total += 1
        
        if total > 0:
            confidence = matches / total
            
        return confidence
    
    def _apply_temporal_filter(self, gesture: RecognizedGesture) -> Optional[RecognizedGesture]:
        """Apply temporal filtering to reduce false positives"""
        
        import time
        current_time = time.time()
        
        # Check cooldown
        if (self.last_recognized and 
            gesture.sign == self.last_recognized.sign and
            current_time - self.last_recognition_time < self.recognition_cooldown):
            return None
        
        # Update last recognition
        self.last_recognized = gesture
        self.last_recognition_time = current_time
        
        # Add to history
        self.gesture_history.append(gesture)
        
        return gesture
    
    def get_sentence_from_history(self) -> str:
        """Build sentence from gesture history"""
        if not self.gesture_history:
            return ""
            
        words = [g.sign for g in self.gesture_history]
        
        # Simple grammar rules
        sentence = " ".join(words)
        
        # Add basic grammar
        sentence = sentence.replace("I NEED HELP", "I need help")
        sentence = sentence.replace("THANK YOU", "Thank you")
        sentence = sentence.replace("HOW ARE YOU", "How are you?")
        
        return sentence
    
    def reset(self):
        """Reset recognizer state"""
        self.gesture_buffer.clear()
        self.gesture_history.clear()
        self.current_state = GestureState.IDLE
        self.last_recognized = None
        self.last_recognition_time = 0
