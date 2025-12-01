from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketManager:
    """
    Manages WebSocket connections for real-time sign language translation
    """
    
    def __init__(self):
        # Store active connections
        self.active_connections: List[WebSocket] = []
        # Store connection metadata (optional)
        self.connection_data: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """
        Accept a new WebSocket connection
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Store client metadata
        self.connection_data[websocket] = {
            "client_id": client_id or f"client_{len(self.active_connections)}",
            "connected_at": None  # You can add timestamp here
        }
        
        logger.info(f"Client {self.connection_data[websocket]['client_id']} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection
        """
        if websocket in self.active_connections:
            client_id = self.connection_data.get(websocket, {}).get("client_id", "unknown")
            self.active_connections.remove(websocket)
            
            # Clean up connection data
            if websocket in self.connection_data:
                del self.connection_data[websocket]
            
            logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_json(self, websocket: WebSocket, data: Dict[str, Any]):
        """
        Send JSON data to a specific WebSocket connection
        """
        try:
            await websocket.send_text(json.dumps(data))
        except Exception as e:
            logger.error(f"Error sending data to client: {e}")
            # Remove the connection if it's broken
            self.disconnect(websocket)
    
    async def broadcast_json(self, data: Dict[str, Any]):
        """
        Broadcast JSON data to all active connections
        """
        if not self.active_connections:
            logger.warning("No active connections to broadcast to")
            return
        
        # Create a copy of connections to iterate over
        connections_copy = self.active_connections.copy()
        
        for connection in connections_copy:
            try:
                await connection.send_text(json.dumps(data))
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                # Remove broken connections
                self.disconnect(connection)
    
    def get_connection_count(self) -> int:
        """
        Get the number of active connections
        """
        return len(self.active_connections)
    
    def get_client_info(self, websocket: WebSocket) -> Dict[str, Any]:
        """
        Get client information for a specific connection
        """
        return self.connection_data.get(websocket, {})

# Global WebSocket manager instance
websocket_manager = WebSocketManager()
