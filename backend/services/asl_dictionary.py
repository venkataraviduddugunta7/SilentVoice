"""
Comprehensive American Sign Language (ASL) Dictionary
Includes common conversational signs and emergency phrases
"""
from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from enum import Enum

class SignType(Enum):
    STATIC = "static"  # Single hand position
    DYNAMIC = "dynamic"  # Movement-based sign
    TWO_HANDED = "two_handed"  # Requires both hands
    FACIAL = "facial"  # Requires facial expression

@dataclass
class SignDefinition:
    """Definition of a sign language gesture"""
    name: str
    type: SignType
    description: str
    hand_shape: str
    movement: Optional[str] = None
    location: Optional[str] = None
    facial_expression: Optional[str] = None
    two_handed: bool = False
    
    # Landmark-based recognition patterns
    finger_states: Optional[Dict[str, bool]] = None  # Which fingers are extended
    hand_orientation: Optional[str] = None  # Palm direction
    relative_position: Optional[str] = None  # Position relative to body

# Comprehensive ASL Dictionary
ASL_DICTIONARY: Dict[str, SignDefinition] = {
    # Basic Greetings
    "HELLO": SignDefinition(
        name="HELLO",
        type=SignType.DYNAMIC,
        description="Wave hand side to side",
        hand_shape="Open hand",
        movement="Wave side to side",
        location="Shoulder height",
        finger_states={"all": True},
        hand_orientation="Palm forward"
    ),
    
    "GOODBYE": SignDefinition(
        name="GOODBYE",
        type=SignType.DYNAMIC,
        description="Wave fingers up and down",
        hand_shape="Open hand",
        movement="Bend fingers repeatedly",
        location="Shoulder height",
        finger_states={"all": True},
        hand_orientation="Palm forward"
    ),
    
    "GOOD_MORNING": SignDefinition(
        name="GOOD_MORNING",
        type=SignType.TWO_HANDED,
        description="Good + Morning signs",
        hand_shape="Flat hand to bent hand",
        movement="Touch chin then raise arm",
        two_handed=True
    ),
    
    "HOW_ARE_YOU": SignDefinition(
        name="HOW_ARE_YOU",
        type=SignType.DYNAMIC,
        description="Point forward with bent fingers, pull back",
        hand_shape="Bent fingers",
        movement="Forward and back",
        location="Chest height"
    ),
    
    # Essential Needs
    "HELP": SignDefinition(
        name="HELP",
        type=SignType.TWO_HANDED,
        description="Fist on flat palm, lift up",
        hand_shape="Fist on flat hand",
        movement="Lift up together",
        two_handed=True,
        relative_position="Center chest"
    ),
    
    "PLEASE": SignDefinition(
        name="PLEASE",
        type=SignType.DYNAMIC,
        description="Circular motion on chest",
        hand_shape="Flat hand",
        movement="Circular motion",
        location="Chest",
        hand_orientation="Palm on chest"
    ),
    
    "THANK_YOU": SignDefinition(
        name="THANK_YOU",
        type=SignType.DYNAMIC,
        description="Touch chin and move forward",
        hand_shape="Flat hand",
        movement="Chin to forward",
        location="Start at chin",
        hand_orientation="Palm in"
    ),
    
    "SORRY": SignDefinition(
        name="SORRY",
        type=SignType.DYNAMIC,
        description="Circular motion on chest with fist",
        hand_shape="Fist (A hand)",
        movement="Circular motion",
        location="Chest",
        hand_orientation="Palm on chest"
    ),
    
    "EXCUSE_ME": SignDefinition(
        name="EXCUSE_ME",
        type=SignType.DYNAMIC,
        description="Brush fingers across palm",
        hand_shape="Bent hand",
        movement="Brush across palm",
        two_handed=True
    ),
    
    # Basic Responses
    "YES": SignDefinition(
        name="YES",
        type=SignType.DYNAMIC,
        description="Fist nodding up and down",
        hand_shape="Fist (S hand)",
        movement="Nod up and down",
        location="Shoulder height",
        finger_states={"all": False}
    ),
    
    "NO": SignDefinition(
        name="NO",
        type=SignType.DYNAMIC,
        description="Index and middle finger close on thumb",
        hand_shape="Extended fingers to closed",
        movement="Fingers snap closed",
        finger_states={"index": True, "middle": True},
        location="Chest height"
    ),
    
    "MAYBE": SignDefinition(
        name="MAYBE",
        type=SignType.DYNAMIC,
        description="Flat hands alternating up and down",
        hand_shape="Flat hands",
        movement="Alternating up/down",
        two_handed=True
    ),
    
    "I_DONT_KNOW": SignDefinition(
        name="I_DONT_KNOW",
        type=SignType.DYNAMIC,
        description="Touch forehead, then palms up shrug",
        hand_shape="Flat hand to open palms",
        movement="Forehead touch to shrug",
        location="Forehead to shoulders"
    ),
    
    # Emergency & Health
    "EMERGENCY": SignDefinition(
        name="EMERGENCY",
        type=SignType.DYNAMIC,
        description="E hand shaking side to side",
        hand_shape="E hand (bent fingers)",
        movement="Shake side to side",
        location="Chest height",
        facial_expression="Urgent"
    ),
    
    "DANGER": SignDefinition(
        name="DANGER",
        type=SignType.TWO_HANDED,
        description="Fists alternating up across body",
        hand_shape="Fists",
        movement="Alternating diagonal motion",
        two_handed=True,
        facial_expression="Concerned"
    ),
    
    "SICK": SignDefinition(
        name="SICK",
        type=SignType.TWO_HANDED,
        description="Middle finger to forehead and stomach",
        hand_shape="Middle finger extended",
        movement="Touch forehead and stomach",
        two_handed=True
    ),
    
    "HURT": SignDefinition(
        name="HURT",
        type=SignType.DYNAMIC,
        description="Index fingers pointing at each other",
        hand_shape="Index fingers extended",
        movement="Jab toward each other",
        two_handed=True
    ),
    
    "DOCTOR": SignDefinition(
        name="DOCTOR",
        type=SignType.DYNAMIC,
        description="D hand taps wrist",
        hand_shape="D hand",
        movement="Tap wrist",
        two_handed=True
    ),
    
    # Basic Needs
    "HUNGRY": SignDefinition(
        name="HUNGRY",
        type=SignType.DYNAMIC,
        description="C hand moves down chest",
        hand_shape="C hand",
        movement="Down chest",
        location="Upper chest to stomach",
        hand_orientation="Palm in"
    ),
    
    "THIRSTY": SignDefinition(
        name="THIRSTY",
        type=SignType.DYNAMIC,
        description="Index finger traces down throat",
        hand_shape="Index finger extended",
        movement="Down throat",
        location="Throat",
        finger_states={"index": True}
    ),
    
    "WATER": SignDefinition(
        name="WATER",
        type=SignType.DYNAMIC,
        description="W hand taps chin",
        hand_shape="W hand (three fingers)",
        movement="Tap chin twice",
        location="Chin",
        finger_states={"index": True, "middle": True, "ring": True}
    ),
    
    "FOOD": SignDefinition(
        name="FOOD",
        type=SignType.DYNAMIC,
        description="Fingers to mouth repeatedly",
        hand_shape="Flat O hand",
        movement="To mouth repeatedly",
        location="Mouth"
    ),
    
    "BATHROOM": SignDefinition(
        name="BATHROOM",
        type=SignType.DYNAMIC,
        description="T hand shakes",
        hand_shape="T hand (thumb between fingers)",
        movement="Shake side to side",
        location="Chest height"
    ),
    
    "SLEEP": SignDefinition(
        name="SLEEP",
        type=SignType.DYNAMIC,
        description="Open hand closes over face",
        hand_shape="Open to closed hand",
        movement="Draw down over face",
        location="Face",
        facial_expression="Eyes closed"
    ),
    
    # Emotions
    "HAPPY": SignDefinition(
        name="HAPPY",
        type=SignType.DYNAMIC,
        description="Flat hand brushes up chest",
        hand_shape="Flat hand",
        movement="Brush up repeatedly",
        location="Chest",
        facial_expression="Smile"
    ),
    
    "SAD": SignDefinition(
        name="SAD",
        type=SignType.DYNAMIC,
        description="Hands trace tears down face",
        hand_shape="Open hands",
        movement="Down face",
        location="Face",
        two_handed=True,
        facial_expression="Sad"
    ),
    
    "ANGRY": SignDefinition(
        name="ANGRY",
        type=SignType.DYNAMIC,
        description="Claw hand at face",
        hand_shape="Claw hand",
        movement="Pull away from face",
        location="Face",
        facial_expression="Angry"
    ),
    
    "LOVE": SignDefinition(
        name="LOVE",
        type=SignType.TWO_HANDED,
        description="Cross arms over chest",
        hand_shape="Fists",
        movement="Hug motion",
        two_handed=True,
        relative_position="Cross chest"
    ),
    
    "SCARED": SignDefinition(
        name="SCARED",
        type=SignType.DYNAMIC,
        description="Hands shake in front of chest",
        hand_shape="Open hands",
        movement="Shake/tremble",
        location="Chest",
        two_handed=True,
        facial_expression="Fearful"
    ),
    
    # Questions
    "WHAT": SignDefinition(
        name="WHAT",
        type=SignType.DYNAMIC,
        description="Index finger across open palm",
        hand_shape="Index on palm",
        movement="Brush across",
        two_handed=True,
        facial_expression="Questioning"
    ),
    
    "WHERE": SignDefinition(
        name="WHERE",
        type=SignType.DYNAMIC,
        description="Index finger waves side to side",
        hand_shape="Index finger",
        movement="Wave side to side",
        location="Shoulder height",
        facial_expression="Questioning"
    ),
    
    "WHEN": SignDefinition(
        name="WHEN",
        type=SignType.DYNAMIC,
        description="Index circles around other index",
        hand_shape="Index fingers",
        movement="Circle and touch",
        two_handed=True,
        facial_expression="Questioning"
    ),
    
    "WHY": SignDefinition(
        name="WHY",
        type=SignType.DYNAMIC,
        description="Touch forehead, bring down to Y hand",
        hand_shape="Flat to Y hand",
        movement="Forehead down",
        location="Forehead to chest",
        facial_expression="Questioning"
    ),
    
    "WHO": SignDefinition(
        name="WHO",
        type=SignType.DYNAMIC,
        description="Index finger circles at mouth",
        hand_shape="L hand at chin",
        movement="Circle at mouth",
        location="Mouth",
        facial_expression="Questioning"
    ),
    
    # Common Phrases
    "MY_NAME": SignDefinition(
        name="MY_NAME",
        type=SignType.TWO_HANDED,
        description="H hands tap together",
        hand_shape="H hands",
        movement="Tap together",
        two_handed=True
    ),
    
    "NICE_TO_MEET_YOU": SignDefinition(
        name="NICE_TO_MEET_YOU",
        type=SignType.DYNAMIC,
        description="Index fingers come together",
        hand_shape="Index fingers",
        movement="Come together",
        two_handed=True
    ),
    
    "I_UNDERSTAND": SignDefinition(
        name="I_UNDERSTAND",
        type=SignType.DYNAMIC,
        description="Fist flicks up at forehead",
        hand_shape="Fist to flick",
        movement="Flick index up",
        location="Forehead"
    ),
    
    "I_DONT_UNDERSTAND": SignDefinition(
        name="I_DONT_UNDERSTAND",
        type=SignType.DYNAMIC,
        description="Index flicks at forehead with head shake",
        hand_shape="Index finger",
        movement="Flick with shake",
        location="Forehead",
        facial_expression="Confused"
    ),
}

class ASLRecognizer:
    """Advanced ASL gesture recognition using landmarks"""
    
    def __init__(self):
        self.dictionary = ASL_DICTIONARY
        self.gesture_history = []
        self.confidence_threshold = 0.7
        
    def recognize_static_sign(
        self, 
        hand_landmarks: List[Dict[str, float]], 
        pose_landmarks: Optional[List[Dict[str, float]]] = None,
        face_landmarks: Optional[List[Dict[str, float]]] = None
    ) -> Tuple[str, float]:
        """
        Recognize static ASL signs from landmarks
        
        Args:
            hand_landmarks: Hand landmark positions
            pose_landmarks: Optional body pose landmarks
            face_landmarks: Optional face landmarks
            
        Returns:
            Tuple of (sign_name, confidence)
        """
        if not hand_landmarks or len(hand_landmarks) < 21:
            return "UNKNOWN", 0.0
            
        # Extract hand features
        features = self._extract_hand_features(hand_landmarks)
        
        # Match against dictionary
        best_match = "UNKNOWN"
        best_confidence = 0.0
        
        for sign_name, sign_def in self.dictionary.items():
            if sign_def.type == SignType.STATIC:
                confidence = self._match_static_sign(features, sign_def)
                if confidence > best_confidence:
                    best_match = sign_name
                    best_confidence = confidence
                    
        return best_match, best_confidence
    
    def recognize_dynamic_sign(
        self,
        hand_sequence: List[List[Dict[str, float]]],
        pose_sequence: Optional[List[List[Dict[str, float]]]] = None,
        face_sequence: Optional[List[List[Dict[str, float]]]] = None
    ) -> Tuple[str, float]:
        """
        Recognize dynamic ASL signs from landmark sequences
        
        Args:
            hand_sequence: Sequence of hand landmarks over time
            pose_sequence: Optional sequence of pose landmarks
            face_sequence: Optional sequence of face landmarks
            
        Returns:
            Tuple of (sign_name, confidence)
        """
        if not hand_sequence or len(hand_sequence) < 5:
            return "UNKNOWN", 0.0
            
        # Extract motion features
        motion_features = self._extract_motion_features(hand_sequence)
        
        # Match against dictionary
        best_match = "UNKNOWN"
        best_confidence = 0.0
        
        for sign_name, sign_def in self.dictionary.items():
            if sign_def.type in [SignType.DYNAMIC, SignType.TWO_HANDED]:
                confidence = self._match_dynamic_sign(motion_features, sign_def)
                if confidence > best_confidence:
                    best_match = sign_name
                    best_confidence = confidence
                    
        return best_match, best_confidence
    
    def _extract_hand_features(self, landmarks: List[Dict[str, float]]) -> Dict:
        """Extract features from hand landmarks"""
        features = {
            "finger_states": self._get_finger_states(landmarks),
            "hand_orientation": self._get_hand_orientation(landmarks),
            "hand_shape": self._get_hand_shape(landmarks),
            "relative_position": self._get_relative_position(landmarks)
        }
        return features
    
    def _get_finger_states(self, landmarks: List[Dict[str, float]]) -> Dict[str, bool]:
        """Determine which fingers are extended"""
        # MediaPipe hand landmark indices
        THUMB_TIP = 4
        INDEX_TIP = 8
        MIDDLE_TIP = 12
        RING_TIP = 16
        PINKY_TIP = 20
        
        THUMB_IP = 3
        INDEX_PIP = 6
        MIDDLE_PIP = 10
        RING_PIP = 14
        PINKY_PIP = 18
        
        states = {}
        
        # Check each finger
        if len(landmarks) >= 21:
            # Thumb (different axis)
            states["thumb"] = landmarks[THUMB_TIP]["x"] > landmarks[THUMB_IP]["x"] + 0.02
            
            # Other fingers (y-axis)
            states["index"] = landmarks[INDEX_TIP]["y"] < landmarks[INDEX_PIP]["y"] - 0.02
            states["middle"] = landmarks[MIDDLE_TIP]["y"] < landmarks[MIDDLE_PIP]["y"] - 0.02
            states["ring"] = landmarks[RING_TIP]["y"] < landmarks[RING_PIP]["y"] - 0.02
            states["pinky"] = landmarks[PINKY_TIP]["y"] < landmarks[PINKY_PIP]["y"] - 0.02
            
            states["all"] = all([states["thumb"], states["index"], states["middle"], 
                                states["ring"], states["pinky"]])
            
        return states
    
    def _get_hand_orientation(self, landmarks: List[Dict[str, float]]) -> str:
        """Determine palm orientation"""
        if len(landmarks) < 21:
            return "unknown"
            
        # Use wrist and middle finger base to determine orientation
        WRIST = 0
        MIDDLE_MCP = 9
        
        wrist = landmarks[WRIST]
        middle_base = landmarks[MIDDLE_MCP]
        
        # Calculate palm normal (simplified)
        dx = middle_base["x"] - wrist["x"]
        dy = middle_base["y"] - wrist["y"]
        dz = middle_base.get("z", 0) - wrist.get("z", 0)
        
        # Determine primary orientation
        if abs(dz) > 0.3:
            return "palm_forward" if dz > 0 else "palm_back"
        elif abs(dy) > abs(dx):
            return "palm_up" if dy < 0 else "palm_down"
        else:
            return "palm_side"
    
    def _get_hand_shape(self, landmarks: List[Dict[str, float]]) -> str:
        """Classify hand shape"""
        states = self._get_finger_states(landmarks)
        
        # Common ASL handshapes
        if states.get("all", False):
            return "open_hand"
        elif not any(states.values()):
            return "fist"
        elif states.get("index") and not states.get("middle"):
            return "pointing"
        elif states.get("index") and states.get("middle") and not states.get("ring"):
            return "peace"
        elif states.get("thumb") and states.get("index") and states.get("pinky"):
            return "ily"  # I Love You
        else:
            return "other"
    
    def _get_relative_position(self, landmarks: List[Dict[str, float]]) -> str:
        """Get hand position relative to video frame"""
        if not landmarks:
            return "unknown"
            
        # Average position
        avg_x = sum(l["x"] for l in landmarks) / len(landmarks)
        avg_y = sum(l["y"] for l in landmarks) / len(landmarks)
        
        # Classify position
        if avg_y < 0.3:
            position = "high"
        elif avg_y > 0.7:
            position = "low"
        else:
            position = "middle"
            
        if avg_x < 0.3:
            position += "_left"
        elif avg_x > 0.7:
            position += "_right"
        else:
            position += "_center"
            
        return position
    
    def _extract_motion_features(self, sequence: List[List[Dict[str, float]]]) -> Dict:
        """Extract motion features from landmark sequence"""
        if len(sequence) < 2:
            return {}
            
        features = {
            "movement_type": self._classify_movement(sequence),
            "movement_direction": self._get_movement_direction(sequence),
            "movement_speed": self._calculate_movement_speed(sequence),
            "hand_shape_changes": self._detect_shape_changes(sequence)
        }
        
        return features
    
    def _classify_movement(self, sequence: List[List[Dict[str, float]]]) -> str:
        """Classify the type of movement"""
        if len(sequence) < 2:
            return "static"
            
        # Calculate total displacement
        first_frame = sequence[0]
        last_frame = sequence[-1]
        
        if not first_frame or not last_frame:
            return "unknown"
            
        # Average position change
        total_displacement = 0
        for i in range(min(len(first_frame), len(last_frame))):
            if i < len(first_frame) and i < len(last_frame):
                dx = last_frame[i]["x"] - first_frame[i]["x"]
                dy = last_frame[i]["y"] - first_frame[i]["y"]
                total_displacement += (dx**2 + dy**2) ** 0.5
                
        avg_displacement = total_displacement / min(len(first_frame), len(last_frame))
        
        if avg_displacement < 0.05:
            return "static"
        elif avg_displacement < 0.15:
            return "small_movement"
        else:
            return "large_movement"
    
    def _get_movement_direction(self, sequence: List[List[Dict[str, float]]]) -> str:
        """Determine primary movement direction"""
        if len(sequence) < 2:
            return "none"
            
        # Calculate average movement vector
        total_dx = 0
        total_dy = 0
        
        for i in range(1, len(sequence)):
            if sequence[i] and sequence[i-1]:
                for j in range(min(len(sequence[i]), len(sequence[i-1]))):
                    total_dx += sequence[i][j]["x"] - sequence[i-1][j]["x"]
                    total_dy += sequence[i][j]["y"] - sequence[i-1][j]["y"]
                    
        # Determine primary direction
        if abs(total_dx) > abs(total_dy):
            return "horizontal" if total_dx > 0 else "horizontal_left"
        else:
            return "vertical" if total_dy > 0 else "vertical_up"
    
    def _calculate_movement_speed(self, sequence: List[List[Dict[str, float]]]) -> float:
        """Calculate average movement speed"""
        if len(sequence) < 2:
            return 0.0
            
        total_speed = 0
        count = 0
        
        for i in range(1, len(sequence)):
            if sequence[i] and sequence[i-1]:
                frame_speed = 0
                for j in range(min(len(sequence[i]), len(sequence[i-1]))):
                    dx = sequence[i][j]["x"] - sequence[i-1][j]["x"]
                    dy = sequence[i][j]["y"] - sequence[i-1][j]["y"]
                    frame_speed += (dx**2 + dy**2) ** 0.5
                    
                total_speed += frame_speed
                count += 1
                
        return total_speed / count if count > 0 else 0.0
    
    def _detect_shape_changes(self, sequence: List[List[Dict[str, float]]]) -> List[str]:
        """Detect hand shape changes throughout sequence"""
        shapes = []
        
        for frame in sequence:
            if frame and len(frame) >= 21:
                shape = self._get_hand_shape(frame)
                if not shapes or shapes[-1] != shape:
                    shapes.append(shape)
                    
        return shapes
    
    def _match_static_sign(self, features: Dict, sign_def: SignDefinition) -> float:
        """Match extracted features against sign definition"""
        confidence = 0.0
        factors = 0
        
        # Match finger states
        if sign_def.finger_states and "finger_states" in features:
            match_score = 0
            for finger, state in sign_def.finger_states.items():
                if finger in features["finger_states"]:
                    if features["finger_states"][finger] == state:
                        match_score += 1
                        
            if sign_def.finger_states:
                confidence += match_score / len(sign_def.finger_states)
                factors += 1
                
        # Match hand orientation
        if sign_def.hand_orientation and "hand_orientation" in features:
            if features["hand_orientation"] == sign_def.hand_orientation:
                confidence += 1.0
            factors += 1
            
        # Match relative position
        if sign_def.relative_position and "relative_position" in features:
            if sign_def.relative_position in features["relative_position"]:
                confidence += 0.8
            factors += 1
            
        return confidence / factors if factors > 0 else 0.0
    
    def _match_dynamic_sign(self, features: Dict, sign_def: SignDefinition) -> float:
        """Match motion features against sign definition"""
        confidence = 0.0
        factors = 0
        
        # Match movement type
        if sign_def.movement and "movement_type" in features:
            if "circular" in sign_def.movement.lower() and "circular" in features.get("movement_type", ""):
                confidence += 1.0
            elif "wave" in sign_def.movement.lower() and features.get("movement_speed", 0) > 0.1:
                confidence += 0.8
            elif "tap" in sign_def.movement.lower() and "small_movement" in features.get("movement_type", ""):
                confidence += 0.7
            factors += 1
            
        # Additional matching logic can be added here
        
        return confidence / factors if factors > 0 else 0.0

# Singleton instance
_asl_recognizer: Optional[ASLRecognizer] = None

def get_asl_recognizer() -> ASLRecognizer:
    """Get the global ASL recognizer instance"""
    global _asl_recognizer
    if _asl_recognizer is None:
        _asl_recognizer = ASLRecognizer()
    return _asl_recognizer
