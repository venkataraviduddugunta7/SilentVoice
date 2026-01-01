#!/usr/bin/env python3
"""
Demo script to showcase sign language recognition with realistic patterns
"""

import asyncio
import websockets
import json
import time
import numpy as np
from typing import List, Dict

class SignLanguageDemo:
    """Generate realistic sign language patterns for demonstration"""
    
    def __init__(self):
        self.signs = {
            "HELLO": self.generate_hello_pattern,
            "THANK_YOU": self.generate_thank_you_pattern,
            "YES": self.generate_yes_pattern,
            "NO": self.generate_no_pattern,
            "HELP": self.generate_help_pattern,
            "I_LOVE_YOU": self.generate_i_love_you_pattern,
            "PLEASE": self.generate_please_pattern,
            "SORRY": self.generate_sorry_pattern,
            "HUNGRY": self.generate_hungry_pattern,
            "WATER": self.generate_water_pattern,
        }
        
    def generate_hand_landmarks(self, shape="open", position=(0.5, 0.5)):
        """Generate 21 hand landmarks based on shape"""
        landmarks = []
        base_x, base_y = position
        
        if shape == "open":
            # Open hand - all fingers extended
            finger_positions = [
                [(0, 0), (0, -0.05), (0, -0.1), (0, -0.15), (0, -0.2)],  # Thumb
                [(-0.05, -0.05), (-0.05, -0.1), (-0.05, -0.15), (-0.05, -0.2), (-0.05, -0.25)],  # Index
                [(0, -0.05), (0, -0.1), (0, -0.15), (0, -0.2), (0, -0.25)],  # Middle
                [(0.05, -0.05), (0.05, -0.1), (0.05, -0.15), (0.05, -0.2), (0.05, -0.25)],  # Ring
                [(0.1, -0.05), (0.1, -0.1), (0.1, -0.15), (0.1, -0.2), (0.1, -0.25)]  # Pinky
            ]
        elif shape == "fist":
            # Closed fist
            finger_positions = [
                [(0, 0), (0, -0.02), (0, -0.03), (0, -0.04), (0, -0.05)],  # Thumb
                [(-0.05, 0), (-0.05, -0.02), (-0.05, -0.03), (-0.05, -0.04), (-0.05, -0.05)],  # Index
                [(0, 0), (0, -0.02), (0, -0.03), (0, -0.04), (0, -0.05)],  # Middle
                [(0.05, 0), (0.05, -0.02), (0.05, -0.03), (0.05, -0.04), (0.05, -0.05)],  # Ring
                [(0.1, 0), (0.1, -0.02), (0.1, -0.03), (0.1, -0.04), (0.1, -0.05)]  # Pinky
            ]
        elif shape == "pointing":
            # Index finger pointing
            finger_positions = [
                [(0, 0), (0, -0.02), (0, -0.03), (0, -0.04), (0, -0.05)],  # Thumb
                [(-0.05, -0.05), (-0.05, -0.1), (-0.05, -0.15), (-0.05, -0.2), (-0.05, -0.25)],  # Index extended
                [(0, 0), (0, -0.02), (0, -0.03), (0, -0.04), (0, -0.05)],  # Middle
                [(0.05, 0), (0.05, -0.02), (0.05, -0.03), (0.05, -0.04), (0.05, -0.05)],  # Ring
                [(0.1, 0), (0.1, -0.02), (0.1, -0.03), (0.1, -0.04), (0.1, -0.05)]  # Pinky
            ]
        elif shape == "i_love_you":
            # I love you sign - thumb, index, pinky extended
            finger_positions = [
                [(0, 0), (0, -0.05), (0, -0.1), (0, -0.15), (0, -0.2)],  # Thumb extended
                [(-0.05, -0.05), (-0.05, -0.1), (-0.05, -0.15), (-0.05, -0.2), (-0.05, -0.25)],  # Index extended
                [(0, 0), (0, -0.02), (0, -0.03), (0, -0.04), (0, -0.05)],  # Middle closed
                [(0.05, 0), (0.05, -0.02), (0.05, -0.03), (0.05, -0.04), (0.05, -0.05)],  # Ring closed
                [(0.1, -0.05), (0.1, -0.1), (0.1, -0.15), (0.1, -0.2), (0.1, -0.25)]  # Pinky extended
            ]
        else:
            # Default open hand
            finger_positions = [
                [(0, 0), (0, -0.05), (0, -0.1), (0, -0.15), (0, -0.2)],  # Thumb
                [(-0.05, -0.05), (-0.05, -0.1), (-0.05, -0.15), (-0.05, -0.2), (-0.05, -0.25)],  # Index
                [(0, -0.05), (0, -0.1), (0, -0.15), (0, -0.2), (0, -0.25)],  # Middle
                [(0.05, -0.05), (0.05, -0.1), (0.05, -0.15), (0.05, -0.2), (0.05, -0.25)],  # Ring
                [(0.1, -0.05), (0.1, -0.1), (0.1, -0.15), (0.1, -0.2), (0.1, -0.25)]  # Pinky
            ]
        
        # Wrist position
        landmarks.append({"x": base_x, "y": base_y, "z": 0})
        
        # Add finger landmarks
        for finger in finger_positions:
            for dx, dy in finger[1:]:  # Skip base, it's included in wrist
                landmarks.append({
                    "x": base_x + dx,
                    "y": base_y + dy,
                    "z": 0
                })
        
        return landmarks[:21]  # Ensure exactly 21 landmarks
    
    def generate_hello_pattern(self, frames=30):
        """Generate HELLO sign - waving motion"""
        pattern = []
        for i in range(frames):
            # Wave motion - hand moves side to side
            t = i / frames
            x_offset = 0.5 + 0.2 * np.sin(t * 2 * np.pi)
            
            landmarks = self.generate_hand_landmarks("open", (x_offset, 0.4))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_thank_you_pattern(self, frames=20):
        """Generate THANK YOU sign - hand from chin forward"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Start at chin, move forward
            y_pos = 0.3 + t * 0.2  # Move forward
            
            landmarks = self.generate_hand_landmarks("open", (0.5, y_pos))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_yes_pattern(self, frames=20):
        """Generate YES sign - fist nodding"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Nodding motion
            y_offset = 0.4 + 0.1 * np.sin(t * 2 * np.pi)
            
            landmarks = self.generate_hand_landmarks("fist", (0.5, y_offset))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_no_pattern(self, frames=15):
        """Generate NO sign - two fingers closing on thumb"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Fingers close together
            shape = "open" if t < 0.5 else "fist"
            
            landmarks = self.generate_hand_landmarks(shape, (0.5, 0.4))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_help_pattern(self, frames=20):
        """Generate HELP sign - fist on flat palm, lifting"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Lift motion
            y_pos = 0.5 - t * 0.1  # Move up
            
            landmarks = self.generate_hand_landmarks("fist", (0.5, y_pos))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_i_love_you_pattern(self, frames=10):
        """Generate I LOVE YOU sign - static sign"""
        pattern = []
        for i in range(frames):
            landmarks = self.generate_hand_landmarks("i_love_you", (0.5, 0.4))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_please_pattern(self, frames=30):
        """Generate PLEASE sign - circular motion on chest"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Circular motion
            angle = t * 2 * np.pi
            x_pos = 0.5 + 0.1 * np.cos(angle)
            y_pos = 0.6 + 0.1 * np.sin(angle)
            
            landmarks = self.generate_hand_landmarks("open", (x_pos, y_pos))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_sorry_pattern(self, frames=30):
        """Generate SORRY sign - fist circles on chest"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Circular motion
            angle = t * 2 * np.pi
            x_pos = 0.5 + 0.08 * np.cos(angle)
            y_pos = 0.6 + 0.08 * np.sin(angle)
            
            landmarks = self.generate_hand_landmarks("fist", (x_pos, y_pos))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_hungry_pattern(self, frames=20):
        """Generate HUNGRY sign - C hand down chest"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Move down chest
            y_pos = 0.4 + t * 0.2
            
            landmarks = self.generate_hand_landmarks("open", (0.5, y_pos))
            pattern.append(landmarks)
        
        return pattern
    
    def generate_water_pattern(self, frames=15):
        """Generate WATER sign - W taps chin"""
        pattern = []
        for i in range(frames):
            t = i / frames
            # Tapping motion
            y_offset = 0.3 if (i % 5) < 3 else 0.28
            
            landmarks = self.generate_hand_landmarks("open", (0.5, y_offset))
            pattern.append(landmarks)
        
        return pattern
    
    async def send_sign(self, websocket, sign_name: str):
        """Send a complete sign to the WebSocket"""
        if sign_name not in self.signs:
            print(f"Sign {sign_name} not found")
            return
        
        print(f"\n🤟 Performing sign: {sign_name}")
        
        # Generate pattern
        pattern = self.signs[sign_name]()
        
        # Send each frame
        for i, landmarks in enumerate(pattern):
            message = {
                "type": "holistic",
                "data": {
                    "rightHandLandmarks": landmarks,
                    "leftHandLandmarks": None,
                    "poseLandmarks": None,
                    "faceLandmarks": None
                },
                "timestamp": time.time()
            }
            
            await websocket.send(json.dumps(message))
            await asyncio.sleep(0.033)  # ~30 FPS
        
        # Wait for recognition
        await asyncio.sleep(0.5)
    
    async def demo_conversation(self):
        """Run a demo conversation"""
        uri = "ws://localhost:8000/api/v1/ws/sign"
        
        print("=" * 50)
        print("🤖 SilentVoice Sign Language Demo")
        print("=" * 50)
        
        try:
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to SilentVoice backend")
                
                # Create task to receive messages
                async def receive_messages():
                    try:
                        while True:
                            message = await websocket.recv()
                            data = json.loads(message)
                            
                            if data.get("type") == "prediction":
                                sign = data.get("sign", "")
                                confidence = data.get("confidence", 0)
                                if sign != "UNKNOWN":
                                    print(f"  → Recognized: {sign} (confidence: {confidence:.2%})")
                            elif data.get("type") == "gesture_metadata":
                                print(f"  → Metadata: {data.get('hand')} hand, "
                                      f"{'dynamic' if data.get('is_motion') else 'static'} gesture, "
                                      f"{data.get('frames')} frames")
                    except websockets.exceptions.ConnectionClosed:
                        pass
                    except Exception as e:
                        print(f"Error receiving: {e}")
                
                # Start receiving task
                receive_task = asyncio.create_task(receive_messages())
                
                # Demo conversation
                conversations = [
                    ("Basic Greetings", ["HELLO", "THANK_YOU", "PLEASE"]),
                    ("Responses", ["YES", "NO", "SORRY"]),
                    ("Needs", ["HELP", "HUNGRY", "WATER"]),
                    ("Emotions", ["I_LOVE_YOU", "THANK_YOU"])
                ]
                
                for category, signs in conversations:
                    print(f"\n📚 Category: {category}")
                    print("-" * 30)
                    
                    for sign in signs:
                        await self.send_sign(websocket, sign)
                        await asyncio.sleep(1)  # Pause between signs
                
                print("\n" + "=" * 50)
                print("✨ Demo Complete!")
                print("=" * 50)
                
                # Cancel receive task
                receive_task.cancel()
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Make sure the backend is running on http://localhost:8000")

async def main():
    """Main demo function"""
    demo = SignLanguageDemo()
    await demo.demo_conversation()

if __name__ == "__main__":
    print("\n🚀 Starting Sign Language Demo...")
    print("This will demonstrate various ASL signs to the backend")
    print("-" * 50)
    
    asyncio.run(main())
