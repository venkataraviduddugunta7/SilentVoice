from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from websocket_manager import websocket_manager  # Keep for compatibility
from websocket_handler import sign_handler  # Enhanced handler
from services.inference import get_inference_service
from services.asl_dictionary import get_asl_recognizer
from services.text2sign import text_to_signs
import json
import logging
import os
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

# Training data storage
TRAINING_DATA_DIR = "training_data"
os.makedirs(TRAINING_DATA_DIR, exist_ok=True)

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
    
    # Count extended fingers
    fingers_up = sum([index_extended, middle_extended, ring_extended, pinky_extended])
    
    # Calculate hand center
    hand_center_x = sum(l['x'] for l in landmarks) / len(landmarks)
    hand_center_y = sum(l['y'] for l in landmarks) / len(landmarks)
    
    # Hand height (0 = top, 1 = bottom)
    hand_height = hand_center_y
    
    # Hand openness (distance between fingertips and palm)
    palm_center = landmarks[MIDDLE_MCP]
    openness = sum([
        ((index_tip['x'] - palm_center['x'])**2 + (index_tip['y'] - palm_center['y'])**2)**0.5,
        ((middle_tip['x'] - palm_center['x'])**2 + (middle_tip['y'] - palm_center['y'])**2)**0.5,
        ((ring_tip['x'] - palm_center['x'])**2 + (ring_tip['y'] - palm_center['y'])**2)**0.5,
        ((pinky_tip['x'] - palm_center['x'])**2 + (pinky_tip['y'] - palm_center['y'])**2)**0.5
    ]) / 4
    
    # Detect specific hand shapes
    is_fist = fingers_up == 0 and not thumb_up
    is_open = fingers_up == 4 and openness > 0.15
    is_pointing = index_extended and fingers_up == 1
    is_peace = index_extended and middle_extended and fingers_up == 2
    is_ok = thumb_up and index_extended and middle_extended and fingers_up == 3
    
    return {
        "valid": True,
        "fingers_up": fingers_up,
        "thumb_up": thumb_up,
        "thumb_down": thumb_down,
        "index_up": index_extended,
        "middle_up": middle_extended,
        "ring_up": ring_extended,
        "pinky_up": pinky_extended,
        "is_fist": is_fist,
        "is_open": is_open,
        "is_pointing": is_pointing,
        "is_peace": is_peace,
        "is_ok": is_ok,
        "hand_height": hand_height,
        "hand_center_x": hand_center_x,
        "hand_center_y": hand_center_y,
        "openness": openness
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
        # Single hand gestures
        hand = hand_features[0]
        
        # Wave detection (HELLO) - open hand at shoulder height
        if hand["is_open"] and hand["hand_height"] < 0.5:
            return "HELLO", 0.92
        
        # Thumbs up (GOOD/YES)
        elif hand["thumb_up"] and hand["fingers_up"] == 0:
            return "GOOD", 0.95
        
        # Pointing (YOU/THERE)
        elif hand["is_pointing"]:
            return "YOU", 0.88
        
        # Peace sign
        elif hand["is_peace"]:
            return "PEACE", 0.90
        
        # OK sign
        elif hand["is_ok"]:
            return "OK", 0.87
        
        # Fist (NO/STOP)
        elif hand["is_fist"]:
            if hand["hand_height"] < 0.4:
                return "STOP", 0.85
            else:
                return "NO", 0.80
        
        # Open hand low (HELP)
        elif hand["is_open"] and hand["hand_height"] > 0.6:
            return "HELP", 0.75
        
        # Number gestures
        elif hand["fingers_up"] == 1:
            return "ONE", 0.93
        elif hand["fingers_up"] == 2:
            return "TWO", 0.93
        elif hand["fingers_up"] == 3:
            return "THREE", 0.93
        elif hand["fingers_up"] == 4:
            return "FOUR", 0.93
        elif hand["fingers_up"] == 5 or (hand["fingers_up"] == 4 and hand["thumb_up"]):
            return "FIVE", 0.93
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
            return "THANK_YOU", 0.60
    
    # Default case
    return "Unknown", 0.45

@router.post("/training/upload")
async def upload_training_data(data: Dict[str, Any]):
    """
    Upload training data for a gesture
    
    Expected format:
    {
        "gesture": "HELLO",
        "frames": [...],  # List of tracking data frames
        "duration": 3.5,
        "timestamp": 1234567890
    }
    """
    try:
        gesture = data.get("gesture")
        frames = data.get("frames")
        duration = data.get("duration")
        timestamp = data.get("timestamp", datetime.now().timestamp())
        
        if not gesture or not frames:
            raise HTTPException(status_code=400, detail="Missing gesture or frames data")
        
        # Create gesture directory
        gesture_dir = os.path.join(TRAINING_DATA_DIR, gesture)
        os.makedirs(gesture_dir, exist_ok=True)
        
        # Save training data
        filename = f"{gesture}_{int(timestamp)}.json"
        filepath = os.path.join(gesture_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump({
                "gesture": gesture,
                "frames": frames,
                "duration": duration,
                "timestamp": timestamp
            }, f)
        
        logger.info(f"Saved training data for {gesture}: {filename}")
        
        return JSONResponse({
            "status": "success",
            "message": f"Training data saved for {gesture}",
            "filename": filename
        })
        
    except Exception as e:
        logger.error(f"Error uploading training data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training/stats")
async def get_training_stats():
    """
    Get statistics about collected training data
    """
    try:
        stats = {}
        total_samples = 0
        
        if os.path.exists(TRAINING_DATA_DIR):
            for gesture_name in os.listdir(TRAINING_DATA_DIR):
                gesture_path = os.path.join(TRAINING_DATA_DIR, gesture_name)
                if os.path.isdir(gesture_path):
                    samples = len([f for f in os.listdir(gesture_path) if f.endswith('.json')])
                    stats[gesture_name] = samples
                    total_samples += samples
        
        return JSONResponse({
            "status": "success",
            "total_samples": total_samples,
            "gestures": stats,
            "data_directory": TRAINING_DATA_DIR
        })
        
    except Exception as e:
        logger.error(f"Error getting training stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/model")
async def trigger_model_training():
    """
    Trigger model training with collected data
    """
    try:
        # Import training module
        from train_model import train_sign_language_model
        
        # Run training in background (in production, use Celery or similar)
        import threading
        training_thread = threading.Thread(
            target=train_sign_language_model,
            kwargs={
                "data_dir": TRAINING_DATA_DIR,
                "model_save_path": "models/sign_language_model.h5",
                "epochs": 50,
                "batch_size": 32
            }
        )
        training_thread.start()
        
        return JSONResponse({
            "status": "success",
            "message": "Model training started in background"
        })
        
    except Exception as e:
        logger.error(f"Error starting model training: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
                if json_data.get("type") == "landmarks" or json_data.get("type") == "holistic":
                    # Handle both simple landmarks and holistic data
                    if json_data.get("type") == "holistic":
                        # Extract hand landmarks from holistic data
                        holistic_data = json_data.get("data", {})
                        pose_data = []
                        
                        if holistic_data.get("leftHandLandmarks"):
                            pose_data.append(holistic_data["leftHandLandmarks"])
                        if holistic_data.get("rightHandLandmarks"):
                            pose_data.append(holistic_data["rightHandLandmarks"])
                            
                        # Also extract pose and face for advanced recognition
                        pose_landmarks = holistic_data.get("poseLandmarks")
                        face_landmarks = holistic_data.get("faceLandmarks")
                    else:
                        # Simple landmarks format
                        pose_data = json_data.get("data", [])
                        pose_landmarks = None
                        face_landmarks = None
                    
                    if not pose_data or len(pose_data) == 0:
                        logger.warning("Received empty pose data")
                        continue
                    
                    logger.info(f"Received pose data: {len(pose_data)} hands")
                    
                    # Try ASL dictionary recognition first
                    asl_recognizer = get_asl_recognizer()
                    
                    # Store in gesture history for dynamic recognition
                    if not hasattr(websocket, 'gesture_history'):
                        websocket.gesture_history = []
                    
                    websocket.gesture_history.append(pose_data)
                    if len(websocket.gesture_history) > 30:  # Keep last 30 frames
                        websocket.gesture_history.pop(0)
                    
                    # Try dynamic recognition if we have enough frames
                    if len(websocket.gesture_history) >= 5:
                        predicted_word, confidence = asl_recognizer.recognize_dynamic_sign(
                            websocket.gesture_history,
                            pose_sequence=[pose_landmarks] if pose_landmarks else None,
                            face_sequence=[face_landmarks] if face_landmarks else None
                        )
                    else:
                        # Try static recognition
                        if pose_data and len(pose_data) > 0:
                            predicted_word, confidence = asl_recognizer.recognize_static_sign(
                                pose_data[0] if pose_data else [],
                                pose_landmarks,
                                face_landmarks
                            )
                        else:
                            predicted_word, confidence = "UNKNOWN", 0.0
                    
                    # If ASL recognition fails, try ML model
                    if confidence < 0.5:
                        inference_service = get_inference_service()
                        if inference_service.is_loaded:
                            try:
                                ml_word, ml_confidence = inference_service.predict(pose_data)
                                if ml_confidence > confidence:
                                    predicted_word, confidence = ml_word, ml_confidence
                                    logger.info(f"ML Model prediction: {predicted_word} ({confidence:.2f})")
                            except Exception as e:
                                logger.warning(f"ML model prediction failed: {e}")
                    
                    # Final fallback to rule-based
                    if confidence < 0.3:
                        rule_word, rule_confidence = process_sign_language(pose_data)
                        if rule_confidence > confidence:
                            predicted_word, confidence = rule_word, rule_confidence
                    
                    # Send prediction back to client
                    await websocket.send_text(json.dumps({
                        "type": "prediction",
                        "sign": predicted_word,
                        "confidence": confidence,
                        "timestamp": datetime.now().isoformat()
                    }))
                    
                elif json_data.get("type") == "speech":
                    # Handle speech to sign conversion
                    text = json_data.get("text", "")
                    
                    if text:
                        # Convert text to sign sequence
                        signs = text_to_signs(text)
                        
                        if signs:
                            await websocket.send_text(json.dumps({
                                "type": "signs",
                                "signs": signs,
                                "original_text": text,
                                "timestamp": datetime.now().isoformat()
                            }))
                        else:
                            await websocket.send_text(json.dumps({
                                "type": "error",
                                "message": "No signs found for text",
                                "text": text
                            }))
                    
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
        logger.info("WebSocket disconnected")
        await sign_handler.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await sign_handler.disconnect(websocket)

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SilentVoice Backend",
        "timestamp": datetime.now().isoformat()
    }

# Get active connections
@router.get("/connections")
async def get_connections():
    """Get active WebSocket connections"""
    return {
        "active_connections": len(sign_handler.active_connections),
        "status": "ok"
    }