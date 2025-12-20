from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_manager import websocket_manager  # Keep for compatibility
from websocket_handler import sign_handler  # Enhanced handler
from services.inference import get_inference_service
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
    Enhanced hand gesture analysis for better basic sign recognition.
    
    Args:
        landmarks: List of 21 hand landmarks with x, y, z coordinates
        
    Returns:
        Dictionary with gesture features
    """
    if len(landmarks) < 21:
        return {"valid": False}
    
    # Key landmark indices (MediaPipe hand model)
    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8
    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12
    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20
    
    # Extract key landmarks
    wrist = landmarks[WRIST]
    thumb_tip = landmarks[THUMB_TIP]
    thumb_ip = landmarks[THUMB_IP]
    index_tip = landmarks[INDEX_TIP]
    index_pip = landmarks[INDEX_PIP]
    index_mcp = landmarks[INDEX_MCP]
    middle_tip = landmarks[MIDDLE_TIP]
    middle_pip = landmarks[MIDDLE_PIP]
    ring_tip = landmarks[RING_TIP]
    ring_pip = landmarks[RING_PIP]
    pinky_tip = landmarks[PINKY_TIP]
    pinky_pip = landmarks[PINKY_PIP]
    
    # Enhanced finger detection with better thresholds
    # Thumb detection (different orientation)
    thumb_up = thumb_tip['y'] < thumb_ip['y'] - 0.02
    thumb_down = thumb_tip['y'] > wrist['y'] + 0.05
    
    # Finger extension detection (more accurate)
    index_extended = index_tip['y'] < index_pip['y'] - 0.02
    middle_extended = middle_tip['y'] < middle_pip['y'] - 0.02
    ring_extended = ring_tip['y'] < ring_pip['y'] - 0.02
    pinky_extended = pinky_tip['y'] < pinky_pip['y'] - 0.02
    
    # Additional gesture features
    # Distance calculations for gesture recognition
    thumb_index_dist = ((thumb_tip['x'] - index_tip['x'])**2 + (thumb_tip['y'] - index_tip['y'])**2)**0.5
    
    # Hand orientation and position
    hand_height = wrist['y']
    hand_center_x = wrist['x']
    
    # Gesture-specific calculations
    # Open palm detection
    all_fingers_up = index_extended and middle_extended and ring_extended and pinky_extended
    
    # Pointing detection
    only_index_up = index_extended and not middle_extended and not ring_extended and not pinky_extended
    
    # Peace sign detection
    peace_sign = index_extended and middle_extended and not ring_extended and not pinky_extended
    
    # Fist detection
    all_fingers_down = not index_extended and not middle_extended and not ring_extended and not pinky_extended
    
    # Wave detection (hand movement would need temporal analysis)
    wave_position = hand_height < 0.4 and hand_center_x > 0.3 and hand_center_x < 0.7
    
    return {
        "valid": True,
        "thumb_up": thumb_up,
        "thumb_down": thumb_down,
        "index_extended": index_extended,
        "middle_extended": middle_extended,
        "ring_extended": ring_extended,
        "pinky_extended": pinky_extended,
        "all_fingers_up": all_fingers_up,
        "only_index_up": only_index_up,
        "peace_sign": peace_sign,
        "all_fingers_down": all_fingers_down,
        "thumb_index_close": thumb_index_dist < 0.08,
        "hand_height": hand_height,
        "hand_center_x": hand_center_x,
        "wave_position": wave_position,
        # Legacy compatibility
        "index_up": index_extended,
        "middle_up": middle_extended,
        "ring_up": ring_extended,
        "pinky_up": pinky_extended
    }

def process_sign_language(pose_data: List[List[Dict[str, float]]]) -> Tuple[str, float]:
    """
    Enhanced sign language processing with better gesture recognition.
    
    Args:
        pose_data: List of hands, each containing list of landmarks with x, y, z coordinates
        
    Returns:
        Tuple of (predicted_word, confidence_score)
    """
    if not pose_data or len(pose_data) == 0:
        return "Unknown", 0.0
    
    num_hands = len(pose_data)
    logger.debug(f"Processing {num_hands} hands for gesture recognition")
    
    # Analyze each hand
    hand_features = []
    for i, hand_landmarks in enumerate(pose_data):
        features = analyze_hand_gesture(hand_landmarks)
        if features["valid"]:
            hand_features.append(features)
            logger.debug(f"Hand {i+1} features: {features}")
    
    if not hand_features:
        logger.debug("No valid hand features found")
        return "Unknown", 0.0
    
    # Enhanced gesture recognition for basic signs
    if num_hands == 1:
        hand = hand_features[0]
        
        # HELLO - Open palm or wave position
        if hand["all_fingers_up"] and hand["wave_position"]:
            return "HELLO", 0.95
        elif hand["all_fingers_up"] and hand["hand_height"] < 0.4:
            return "HELLO", 0.90
        
        # YES - Clear thumbs up
        elif hand["thumb_up"] and hand["all_fingers_down"]:
            return "YES", 0.98
        elif hand["thumb_up"] and not hand["index_extended"]:
            return "YES", 0.92
        
        # NO - Thumbs down or closed fist
        elif hand["thumb_down"]:
            return "NO", 0.95
        elif hand["all_fingers_down"] and not hand["thumb_up"]:
            return "NO", 0.85
        
        # PEACE - V sign with index and middle fingers
        elif hand["peace_sign"]:
            return "PEACE", 0.96
        
        # GOOD - OK sign or pointing up
        elif hand["thumb_index_close"] and hand["middle_extended"]:
            return "GOOD", 0.93
        elif hand["only_index_up"] and hand["hand_height"] > 0.4:
            return "GOOD", 0.88
        
        # PLEASE - Open palm at medium height
        elif hand["all_fingers_up"] and hand["hand_height"] > 0.4:
            return "PLEASE", 0.87
        
        # Basic pointing or greeting
        elif hand["only_index_up"]:
            if hand["hand_height"] < 0.4:
                return "HELLO", 0.82
            else:
                return "GOOD", 0.80
        
        # Any raised hand as potential greeting
        elif hand["hand_height"] < 0.35:
            return "HELLO", 0.70
        
        # Default for any gesture
        else:
            return "HELLO", 0.55
            
    elif num_hands == 2:
        # Two hand gestures - enhanced detection
        left_hand = hand_features[0]
        right_hand = hand_features[1] if len(hand_features) > 1 else hand_features[0]
        
        # Both hands raised high (celebration/greeting)
        if left_hand["hand_height"] < 0.25 and right_hand["hand_height"] < 0.25:
            return "HELLO", 0.95
        
        # Prayer/thank you gesture - hands close together at center
        elif abs(left_hand["hand_center_x"] - right_hand["hand_center_x"]) < 0.12:
            if left_hand["hand_height"] < 0.6 and right_hand["hand_height"] < 0.6:
                return "THANK_YOU", 0.96
            else:
                return "PLEASE", 0.90
        
        # Both thumbs up - love/approval
        elif left_hand["thumb_up"] and right_hand["thumb_up"]:
            return "LOVE", 0.98
        
        # Both hands showing peace signs
        elif (left_hand["index_up"] and left_hand["middle_up"] and 
              right_hand["index_up"] and right_hand["middle_up"]):
            return "PEACE", 0.94
        
        # Hands spread wide apart - big/good gesture
        elif abs(left_hand["hand_center_x"] - right_hand["hand_center_x"]) > 0.5:
            return "GOOD", 0.85
        
        # Clapping motion (hands close, medium height)
        elif (abs(left_hand["hand_center_x"] - right_hand["hand_center_x"]) < 0.2 and
              left_hand["hand_height"] > 0.3 and right_hand["hand_height"] > 0.3):
            return "GOOD", 0.83
        
        else:
            return "THANK_YOU", 0.70
    
    # Default case
    return "Unknown", 0.45

@router.websocket("/ws/sign")
async def websocket_sign_endpoint(websocket: WebSocket):
    """
    Enhanced WebSocket endpoint with ML model integration
    Accepts hand landmark data for real-time sign language translation
    """
    
    # Use enhanced handler with ML support
    await sign_handler.connect(websocket)
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            
            try:
                # Parse the JSON data
                json_data = json.loads(data)
                
                # Check data type
                if json_data.get("type") == "landmarks":
                    # New SilentVoice format
                    pose_data = json_data.get("data", [])
                    
                    if not pose_data or len(pose_data) == 0:
                        logger.warning("Received empty pose data")
                        continue
                    
                    logger.info(f"Received pose data: {len(pose_data)} hands")
                    
                    # Try to use ML model, fallback to rule-based
                    inference_service = get_inference_service()
                    if inference_service.is_loaded:
                        try:
                            predicted_word, confidence = inference_service.predict(pose_data)
                            logger.info(f"ML Model prediction: {predicted_word} ({confidence:.2f})")
                        except Exception as e:
                            logger.warning(f"ML model prediction failed: {e}. Using fallback.")
                            predicted_word, confidence = process_sign_language(pose_data)
                    else:
                        # Use rule-based fallback
                        predicted_word, confidence = process_sign_language(pose_data)
                    
                    # Send prediction with lower threshold for basic gestures
                    if confidence > 0.4 and predicted_word != "Unknown":
                        response = {
                            "type": "prediction",
                            "word": predicted_word,
                            "confidence": confidence
                        }
                        await websocket_manager.send_json(websocket, response)
                        logger.info(f"✅ Sent prediction: {predicted_word} ({confidence:.2f})")
                    else:
                        logger.debug(f"Low confidence prediction ignored: {predicted_word} ({confidence:.2f})")
                    
                elif "landmarks" in json_data:
                    # Legacy format support
                    landmarks = json_data["landmarks"]
                    logger.info(f"Received hand landmarks: {len(landmarks)} points")
                    
                    # Convert to new format and process
                    pose_data = [landmarks] if landmarks else []
                    predicted_word, confidence = process_sign_language(pose_data)
                    
                    # Only send if confidence is high enough
                    if confidence > 0.5 and predicted_word != "Unknown":
                        response = {
                            "type": "prediction",
                            "word": predicted_word,
                            "confidence": confidence
                        }
                        await websocket_manager.send_json(websocket, response)
                else:
                    logger.info(f"Received unknown data format: {json_data}")
                    response = {
                        "type": "error",
                        "message": "Unknown data format"
                    }
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
