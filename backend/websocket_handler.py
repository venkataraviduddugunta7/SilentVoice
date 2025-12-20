"""
Enhanced WebSocket Handler with ML Model Integration
Handles real-time sign language detection and translation
"""

from typing import List, Dict, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect
import json
import logging
import asyncio
import time
import numpy as np
import os
from collections import deque

# Import model and database
from model import SignLanguageModel
from database_setup import SignDatabase

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SignLanguageWebSocketHandler:
    """
    Enhanced WebSocket handler with ML model integration for sign language translation
    """
    
    def __init__(self):
        # Store active connections
        self.active_connections: List[WebSocket] = []
        self.connection_data: Dict[WebSocket, Dict[str, Any]] = {}
        
        # ML Model
        self.model: Optional[SignLanguageModel] = None
        self.model_path = "models/sign_language_model.h5"
        self.confidence_threshold = 0.7
        
        # Database
        self.database: Optional[SignDatabase] = None
        
        # Frame buffering for sequence prediction
        self.frame_buffers: Dict[WebSocket, deque] = {}
        self.buffer_size = 30  # 30 frames for sequence
        self.min_frames_for_prediction = 15  # Minimum frames needed
        
        # Prediction management
        self.last_predictions: Dict[WebSocket, Dict] = {}
        self.prediction_cooldown = 0.5  # seconds between predictions
        
        # Initialize components
        self.initialize_model()
        self.initialize_database()
    
    def initialize_model(self):
        """Load the trained sign language model."""
        try:
            if os.path.exists(self.model_path):
                self.model = SignLanguageModel()
                self.model.load_model(self.model_path)
                logger.info(f"✅ Model loaded from {self.model_path}")
                logger.info(f"   Classes: {self.model.class_names}")
            else:
                logger.warning(f"⚠️ Model not found at {self.model_path}")
                logger.info("   Creating default model (untrained)")
                self.model = SignLanguageModel()
                self.model.build_model()
                
                # Set default class names
                self.model.class_names = [
                    'HELLO', 'THANK_YOU', 'YES', 'NO', 'PLEASE',
                    'SORRY', 'GOOD', 'BAD', 'LOVE', 'PEACE'
                ]
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            self.model = None
    
    def initialize_database(self):
        """Initialize database connection."""
        try:
            self.database = SignDatabase()
            logger.info("✅ Database initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize database: {e}")
            self.database = None
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Initialize frame buffer for this connection
        self.frame_buffers[websocket] = deque(maxlen=self.buffer_size)
        self.last_predictions[websocket] = {'time': 0, 'gesture': None}
        
        # Store client metadata
        self.connection_data[websocket] = {
            "client_id": client_id or f"client_{len(self.active_connections)}",
            "connected_at": time.time(),
            "predictions_count": 0
        }
        
        logger.info(f"✅ Client {self.connection_data[websocket]['client_id']} connected")
        
        # Send initial connection message
        await self.send_json(websocket, {
            "type": "connection",
            "status": "connected",
            "model_loaded": self.model is not None,
            "available_gestures": self.model.class_names if self.model else []
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            client_id = self.connection_data.get(websocket, {}).get("client_id", "unknown")
            self.active_connections.remove(websocket)
            
            # Clean up buffers and data
            if websocket in self.frame_buffers:
                del self.frame_buffers[websocket]
            if websocket in self.last_predictions:
                del self.last_predictions[websocket]
            if websocket in self.connection_data:
                del self.connection_data[websocket]
            
            logger.info(f"❌ Client {client_id} disconnected")
    
    async def send_json(self, websocket: WebSocket, data: Dict[str, Any]):
        """Send JSON data to a specific WebSocket connection."""
        try:
            await websocket.send_text(json.dumps(data))
        except Exception as e:
            logger.error(f"Error sending data: {e}")
            self.disconnect(websocket)
    
    async def process_landmarks(self, websocket: WebSocket, landmarks_data: Dict):
        """Process hand landmarks for sign detection."""
        if not self.model:
            await self.send_json(websocket, {
                "type": "error",
                "message": "Model not loaded"
            })
            return
        
        try:
            # Extract landmarks from the data
            landmarks = landmarks_data.get('data', {})
            
            # Convert MediaPipe format to our format
            if 'multiHandLandmarks' in landmarks:
                hand_landmarks = []
                for hand in landmarks['multiHandLandmarks']:
                    hand_data = []
                    for lm in hand:
                        hand_data.append({
                            'x': lm.get('x', 0),
                            'y': lm.get('y', 0),
                            'z': lm.get('z', 0)
                        })
                    hand_landmarks.append(hand_data)
                
                if hand_landmarks:
                    # Add to frame buffer
                    self.frame_buffers[websocket].append(hand_landmarks)
                    
                    # Check if we can make a prediction
                    current_time = time.time()
                    last_pred_time = self.last_predictions[websocket]['time']
                    
                    if (len(self.frame_buffers[websocket]) >= self.min_frames_for_prediction and
                        current_time - last_pred_time >= self.prediction_cooldown):
                        
                        # Make prediction
                        start_time = time.time()
                        gesture, confidence = self.model.predict(hand_landmarks)
                        inference_time = (time.time() - start_time) * 1000  # ms
                        
                        # Update last prediction
                        self.last_predictions[websocket] = {
                            'time': current_time,
                            'gesture': gesture
                        }
                        
                        # Send prediction if confidence is above threshold
                        if confidence >= self.confidence_threshold:
                            response = {
                                "type": "prediction",
                                "sign": gesture,
                                "confidence": float(confidence),
                                "inference_time_ms": round(inference_time, 2),
                                "timestamp": current_time
                            }
                            
                            await self.send_json(websocket, response)
                            
                            # Update statistics
                            self.connection_data[websocket]['predictions_count'] += 1
                            
                            # Log to database if available
                            if self.database:
                                self.database.insert_inference_log(
                                    gesture_detected=gesture,
                                    confidence=confidence,
                                    processing_time_ms=inference_time
                                )
                        else:
                            # Send low confidence response
                            await self.send_json(websocket, {
                                "type": "low_confidence",
                                "confidence": float(confidence),
                                "message": "Gesture not clear, please try again"
                            })
                else:
                    # No hands detected
                    await self.send_json(websocket, {
                        "type": "no_hands",
                        "message": "No hands detected"
                    })
                    
        except Exception as e:
            logger.error(f"Error processing landmarks: {e}")
            await self.send_json(websocket, {
                "type": "error",
                "message": f"Processing error: {str(e)}"
            })
    
    async def process_speech(self, websocket: WebSocket, speech_data: Dict):
        """Process speech input for sign language rendering."""
        text = speech_data.get('text', '').upper()
        
        # Map text to gestures (simple word mapping for now)
        gesture_map = {
            'HELLO': 'HELLO',
            'HI': 'HELLO',
            'THANK': 'THANK_YOU',
            'THANKS': 'THANK_YOU',
            'YES': 'YES',
            'NO': 'NO',
            'PLEASE': 'PLEASE',
            'SORRY': 'SORRY',
            'GOOD': 'GOOD',
            'BAD': 'BAD',
            'LOVE': 'LOVE',
            'PEACE': 'PEACE',
            'HELP': 'HELP',
            'STOP': 'STOP',
            'WAIT': 'WAIT',
            'COME': 'COME',
            'GO': 'GO'
        }
        
        # Find matching gestures
        words = text.split()
        matched_gestures = []
        
        for word in words:
            word_upper = word.upper()
            if word_upper in gesture_map:
                matched_gestures.append(gesture_map[word_upper])
            else:
                # Check partial matches
                for key in gesture_map:
                    if key in word_upper or word_upper in key:
                        matched_gestures.append(gesture_map[key])
                        break
        
        if matched_gestures:
            await self.send_json(websocket, {
                "type": "sign_sequence",
                "signs": matched_gestures,
                "original_text": text,
                "timestamp": time.time()
            })
        else:
            # Use finger spelling for unknown words
            await self.send_json(websocket, {
                "type": "finger_spelling",
                "letters": list(text.replace(' ', '')),
                "original_text": text,
                "timestamp": time.time()
            })
    
    async def handle_feedback(self, websocket: WebSocket, feedback_data: Dict):
        """Handle user feedback for continuous improvement."""
        if self.database:
            try:
                self.database.insert_feedback(
                    gesture_predicted=feedback_data.get('predicted'),
                    gesture_actual=feedback_data.get('actual'),
                    confidence=feedback_data.get('confidence', 0),
                    correct=feedback_data.get('correct', False),
                    session_id=self.connection_data[websocket]['client_id']
                )
                
                await self.send_json(websocket, {
                    "type": "feedback_received",
                    "message": "Thank you for your feedback!"
                })
            except Exception as e:
                logger.error(f"Error saving feedback: {e}")
    
    async def handle_message(self, websocket: WebSocket, message: str):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'landmarks':
                await self.process_landmarks(websocket, data)
            elif message_type == 'speech':
                await self.process_speech(websocket, data)
            elif message_type == 'feedback':
                await self.handle_feedback(websocket, data)
            elif message_type == 'ping':
                await self.send_json(websocket, {"type": "pong"})
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            await self.send_json(websocket, {
                "type": "error",
                "message": "Invalid JSON format"
            })
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_json(websocket, {
                "type": "error",
                "message": f"Error: {str(e)}"
            })
    
    def get_statistics(self) -> Dict:
        """Get handler statistics."""
        stats = {
            "active_connections": len(self.active_connections),
            "model_loaded": self.model is not None,
            "database_connected": self.database is not None,
            "total_predictions": sum(
                conn.get('predictions_count', 0) 
                for conn in self.connection_data.values()
            )
        }
        
        if self.model:
            stats["model_classes"] = self.model.class_names
            stats["confidence_threshold"] = self.confidence_threshold
        
        return stats


# Global handler instance
sign_handler = SignLanguageWebSocketHandler()