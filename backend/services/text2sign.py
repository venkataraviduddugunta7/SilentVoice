"""
Text to Sign Mapping Service - Speech → Sign mapping
"""
from typing import Dict, List, Optional

# Text to sign language gesture mapping
TEXT_TO_SIGN_MAPPING: Dict[str, str] = {
    # Greetings
    'hello': 'HELLO',
    'hi': 'HELLO',
    'hey': 'HELLO',
    'goodbye': 'GOODBYE',
    'bye': 'GOODBYE',
    'welcome': 'WELCOME',
    
    # Responses
    'yes': 'YES',
    'yeah': 'YES',
    'yep': 'YES',
    'no': 'NO',
    'nope': 'NO',
    
    # Politeness
    'thank you': 'THANK_YOU',
    'thanks': 'THANK_YOU',
    'please': 'PLEASE',
    'sorry': 'SORRY',
    
    # Emotions/States
    'good': 'GOOD',
    'bad': 'BAD',
    'love': 'LOVE',
    'peace': 'PEACE',
    
    # Actions
    'help': 'HELP',
    'stop': 'STOP',
    'go': 'GO',
    'come': 'COME',
    'eat': 'EAT',
    'drink': 'DRINK',
    'sleep': 'SLEEP',
    'wake up': 'WAKE_UP',
}

def text_to_sign(text: str) -> Optional[str]:
    """
    Convert text to sign language gesture.
    
    Args:
        text: Input text string
        
    Returns:
        Sign gesture name or None if not found
    """
    # Normalize text
    normalized = text.lower().strip()
    
    # Direct mapping
    if normalized in TEXT_TO_SIGN_MAPPING:
        return TEXT_TO_SIGN_MAPPING[normalized]
    
    # Check for partial matches (word-by-word)
    words = normalized.split()
    for word in words:
        if word in TEXT_TO_SIGN_MAPPING:
            return TEXT_TO_SIGN_MAPPING[word]
    
    # Check for phrases
    for phrase, gesture in TEXT_TO_SIGN_MAPPING.items():
        if phrase in normalized:
            return gesture
    
    return None

def text_to_signs(text: str) -> List[str]:
    """
    Convert text to multiple sign language gestures (word-by-word).
    
    Args:
        text: Input text string
        
    Returns:
        List of sign gesture names
    """
    words = text.lower().strip().split()
    signs = []
    
    for word in words:
        gesture = text_to_sign(word)
        if gesture:
            signs.append(gesture)
    
    return signs

def get_available_signs() -> List[str]:
    """
    Get list of available sign language gestures.
    
    Returns:
        List of gesture names
    """
    return list(set(TEXT_TO_SIGN_MAPPING.values()))

def add_custom_mapping(text: str, gesture: str):
    """
    Add a custom text-to-sign mapping.
    
    Args:
        text: Text to map
        gesture: Gesture name
    """
    TEXT_TO_SIGN_MAPPING[text.lower().strip()] = gesture.upper()

