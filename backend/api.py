from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_manager import websocket_manager
import json
import logging
import random
from typing import Dict, Any, List, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

def analyze_hand_gesture(landmarks: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Analyze hand landmarks to extract gesture features.
    
    Args:
        landmarks: List of 21 hand landmarks with x, y, z coordinates
        
    Returns:
        Dictionary with gesture features
    """
    if len(landmarks) < 21:
        return {"valid": False}
    
    # Key landmark indices (MediaPipe hand model)
    WRIST = 0
    THUMB_TIP = 4
    INDEX_TIP = 8
    MIDDLE_TIP = 12
    RING_TIP = 16
    PINKY_TIP = 20
    INDEX_PIP = 6
    MIDDLE_PIP = 10
    
    wrist = landmarks[WRIST]
    thumb_tip = landmarks[THUMB_TIP]
    index_tip = landmarks[INDEX_TIP]
    middle_tip = landmarks[MIDDLE_TIP]
    ring_tip = landmarks[RING_TIP]
    pinky_tip = landmarks[PINKY_TIP]
    index_pip = landmarks[INDEX_PIP]
    middle_pip = landmarks[MIDDLE_PIP]
    
    # Calculate relative positions
    thumb_up = thumb_tip['y'] < wrist['y'] - 0.1
    index_up = index_tip['y'] < index_pip['y']
    middle_up = middle_tip['y'] < middle_pip['y']
    
    # Calculate distances
    thumb_index_dist = ((thumb_tip['x'] - index_tip['x'])**2 + (thumb_tip['y'] - index_tip['y'])**2)**0.5
    
    return {
        "valid": True,
        "thumb_up": thumb_up,
        "index_up": index_up,
        "middle_up": middle_up,
        "thumb_index_close": thumb_index_dist < 0.05,
        "hand_height": wrist['y'],
        "hand_center_x": wrist['x']
    }

def process_sign_language(pose_data: List[List[Dict[str, float]]]) -> Tuple[str, float]:
    """
    Process hand pose data and return predicted sign language word with confidence.
    
    Args:
        pose_data: List of hands, each containing list of landmarks with x, y, z coordinates
        
    Returns:
        Tuple of (predicted_word, confidence_score)
    """
    if not pose_data or len(pose_data) == 0:
        return "Unknown", 0.0
    
    num_hands = len(pose_data)
    
    # Analyze each hand
    hand_features = []
    for hand_landmarks in pose_data:
        features = analyze_hand_gesture(hand_landmarks)
        if features["valid"]:
            hand_features.append(features)
    
    if not hand_features:
        return "Unknown", 0.0
    
    # Basic gesture recognition based on hand features
    if num_hands == 1:
        hand = hand_features[0]
        
        # Thumbs up gesture
        if hand["thumb_up"] and not hand["index_up"]:
            return "YES", 0.85
        
        # Index finger pointing up
        elif hand["index_up"] and not hand["middle_up"]:
            return "HELLO", 0.80
        
        # OK sign (thumb and index close)
        elif hand["thumb_index_close"]:
            return "GOOD", 0.82
        
        # Hand wave (high position)
        elif hand["hand_height"] < 0.3:
            return "HELLO", 0.75
        
        else:
            return "PLEASE", 0.70
            
    elif num_hands == 2:
        # Two hand gestures
        left_hand = hand_features[0]
        right_hand = hand_features[1] if len(hand_features) > 1 else hand_features[0]
        
        # Both hands up
        if left_hand["hand_height"] < 0.4 and right_hand["hand_height"] < 0.4:
            return "THANK_YOU", 0.88
        
        # Hands together (prayer position)
        elif abs(left_hand["hand_center_x"] - right_hand["hand_center_x"]) < 0.2:
            return "PLEASE", 0.85
        
        else:
            return "HELLO", 0.75
    
    # Default case - unknown gesture
    return "Unknown", 0.50

@router.websocket("/ws/sign")
async def websocket_sign_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time sign language data processing
    Accepts hand coordinate data and processes it for translation
    """
    
    # Accept the connection
    await websocket_manager.connect(websocket)
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            
            try:
                # Parse JSON data
                json_data = json.loads(data)
                
                # Handle different message types
                if json_data.get("type") == "pose":
                    # New SilentVoice format
                    pose_data = json_data.get("data", [])
                    logger.info(f"Received pose data: {len(pose_data)} hands")
                    
                    # Process pose data for sign recognition
                    # TODO: Replace with actual ML model prediction
                    predicted_word, confidence = process_sign_language(pose_data)
                    
                    # Send prediction back to client
                    response = {
                        "type": "prediction",
                        "word": predicted_word,
                        "confidence": confidence
                    }
                    
                elif "landmarks" in json_data:
                    # Legacy format support
                    landmarks = json_data["landmarks"]
                    logger.info(f"Received hand landmarks: {len(landmarks)} points")
                    
                    # Convert to new format and process
                    pose_data = [landmarks] if landmarks else []
                    predicted_word, confidence = process_sign_language(pose_data)
                    
                    response = {
                        "type": "prediction",
                        "word": predicted_word,
                        "confidence": confidence
                    }
                else:
                    logger.info(f"Received unknown data format: {json_data}")
                    response = {
                        "type": "error",
                        "message": "Unknown data format"
                    }
                
                # Send response back to client
                await websocket_manager.send_json(websocket, response)
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON received: {e}")
                error_response = {
                    "status": "error",
                    "message": "Invalid JSON format",
                    "error": str(e)
                }
                await websocket_manager.send_json(websocket, error_response)
                
            except Exception as e:
                logger.error(f"Error processing data: {e}")
                error_response = {
                    "status": "error",
                    "message": "Error processing hand coordinates",
                    "error": str(e)
                }
                await websocket_manager.send_json(websocket, error_response)
                
    except WebSocketDisconnect:
        logger.info("Client disconnected from sign language endpoint")
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Unexpected error in WebSocket endpoint: {e}")
        websocket_manager.disconnect(websocket)

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "SilentVoice Backend",
        "active_connections": websocket_manager.get_connection_count()
    }

@router.get("/connections")
async def get_connections():
    """
    Get information about active WebSocket connections
    """
    return {
        "active_connections": websocket_manager.get_connection_count(),
        "status": "ok"
    }
