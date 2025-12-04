"""
Data Collection Script for Sign Language Training
Captures hand landmarks from webcam and saves them as training sequences.
"""

import cv2
import mediapipe as mp
import json
import os
import time
from datetime import datetime
from typing import List, Dict
import argparse

class TrainingDataCollector:
    """Collect hand landmark sequences for training."""
    
    def __init__(self, output_dir: str = 'training_data'):
        self.output_dir = output_dir
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = None
        self.current_gesture = None
        self.sequence = []
        self.frame_count = 0
        self.sequence_length = 30  # Frames per sequence
        
    def start_camera(self):
        """Initialize camera."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        print("✅ Camera initialized")
    
    def stop_camera(self):
        """Release camera."""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Camera released")
    
    def process_frame(self, frame) -> List[List[Dict]]:
        """Process a frame and extract hand landmarks."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        hands_data = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    })
                hands_data.append(landmarks)
        
        return hands_data
    
    def save_sequence(self, gesture_name: str, sequence: List[List[List[Dict]]]):
        """Save a collected sequence to JSON file."""
        gesture_dir = os.path.join(self.output_dir, gesture_name)
        os.makedirs(gesture_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sequence_{timestamp}_{len(sequence)}frames.json"
        filepath = os.path.join(gesture_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(sequence, f, indent=2)
        
        print(f"✅ Saved sequence: {filepath}")
        return filepath
    
    def collect_sequence(self, gesture_name: str):
        """Collect a sequence of frames for a gesture."""
        print(f"\n📹 Collecting sequence for: {gesture_name}")
        print("Press SPACE to start recording, SPACE again to stop")
        print("Press 'q' to cancel")
        
        sequence = []
        recording = False
        frame_count = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process frame
            hands_data = self.process_frame(frame)
            
            # Draw landmarks
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
            
            # Display status
            status_text = f"Gesture: {gesture_name}"
            if recording:
                status_text += f" | Recording... ({len(sequence)}/{self.sequence_length} frames)"
                cv2.putText(frame, status_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Add to sequence
                sequence.append(hands_data)
                frame_count += 1
                
                if frame_count >= self.sequence_length:
                    recording = False
                    break
            else:
                status_text += " | Press SPACE to start"
                cv2.putText(frame, status_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            cv2.imshow('Training Data Collection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space to start/stop
                if not recording:
                    recording = True
                    sequence = []
                    frame_count = 0
                    print("🔴 Recording started...")
                else:
                    recording = False
                    break
            elif key == ord('q'):  # Quit
                return None
        
        if len(sequence) > 0:
            filepath = self.save_sequence(gesture_name, sequence)
            return filepath
        return None
    
    def run_interactive_collection(self, gestures: List[str]):
        """Run interactive data collection session."""
        print("=" * 60)
        print("Sign Language Training Data Collection")
        print("=" * 60)
        print("\nInstructions:")
        print("1. Select a gesture to record")
        print("2. Press SPACE to start/stop recording")
        print("3. Perform the gesture while recording")
        print("4. Press 'q' to quit")
        print("=" * 60)
        
        self.start_camera()
        
        try:
            while True:
                print("\nAvailable gestures:")
                for i, gesture in enumerate(gestures, 1):
                    print(f"  {i}. {gesture}")
                print(f"  {len(gestures) + 1}. Quit")
                
                choice = input("\nSelect gesture (number): ").strip()
                
                if choice == str(len(gestures) + 1) or choice.lower() == 'q':
                    break
                
                try:
                    gesture_idx = int(choice) - 1
                    if 0 <= gesture_idx < len(gestures):
                        gesture_name = gestures[gesture_idx]
                        self.collect_sequence(gesture_name)
                    else:
                        print("❌ Invalid choice")
                except ValueError:
                    print("❌ Invalid input")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
        finally:
            self.stop_camera()
            print("\n✅ Data collection session ended")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Collect training data for sign language recognition')
    parser.add_argument('--output-dir', type=str, default='training_data',
                        help='Output directory for training data')
    parser.add_argument('--gestures', type=str, nargs='+',
                        default=['HELLO', 'THANK_YOU', 'YES', 'NO', 'PLEASE', 'SORRY', 'GOOD', 'BAD', 'LOVE', 'PEACE'],
                        help='List of gestures to collect')
    
    args = parser.parse_args()
    
    collector = TrainingDataCollector(output_dir=args.output_dir)
    collector.run_interactive_collection(args.gestures)

if __name__ == '__main__':
    main()

