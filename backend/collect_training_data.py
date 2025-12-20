#!/usr/bin/env python3
"""
Interactive training data collection for sign language
This script helps you collect hand landmark data for training the model
"""

import cv2
import mediapipe as mp
import numpy as np
import os
import json
from pathlib import Path
from datetime import datetime
import time
from database import SessionLocal, save_training_sample, initialize_signs

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Signs to collect
SIGNS_TO_COLLECT = [
    'hello', 'thank_you', 'please', 'yes', 'no',
    'help', 'sorry', 'goodbye', 'love', 'friend',
    'eat', 'drink', 'sleep', 'work', 'home'
]

# Configuration
SAMPLES_PER_SIGN = 30  # Number of samples to collect per sign
FRAMES_PER_SAMPLE = 30  # Number of frames per sample
DATA_PATH = Path('training_data')


class TrainingDataCollector:
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.db = SessionLocal()
        
        # Create data directory
        DATA_PATH.mkdir(exist_ok=True)
        
    def extract_landmarks(self, results):
        """Extract hand landmarks from MediaPipe results"""
        if not results.multi_hand_landmarks:
            return None
            
        landmarks = []
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
                
        # Pad with zeros if only one hand detected (we expect 2 hands max)
        while len(landmarks) < 21 * 3 * 2:  # 21 landmarks * 3 coords * 2 hands
            landmarks.append(0.0)
            
        return landmarks[:21 * 3 * 2]  # Ensure consistent size
    
    def collect_samples(self, sign_name, num_samples=SAMPLES_PER_SIGN):
        """Collect training samples for a specific sign"""
        print(f"\n{'='*50}")
        print(f"Collecting data for sign: {sign_name.upper()}")
        print(f"{'='*50}")
        print(f"Please perform the sign for '{sign_name}'")
        print("Press SPACE to start recording each sample")
        print("Press Q to skip this sign\n")
        
        sign_path = DATA_PATH / sign_name
        sign_path.mkdir(exist_ok=True)
        
        samples_collected = 0
        
        while samples_collected < num_samples:
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(frame_rgb)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
            
            # Display instructions
            cv2.putText(frame, f"Sign: {sign_name.upper()}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Samples: {samples_collected}/{num_samples}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press SPACE to record, Q to skip", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            
            cv2.imshow('Collect Training Data', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space bar to start recording
                # Record a sequence of frames
                print(f"Recording sample {samples_collected + 1}...")
                sequence = []
                
                for frame_num in range(FRAMES_PER_SAMPLE):
                    ret, frame = self.cap.read()
                    if not ret:
                        continue
                        
                    frame = cv2.flip(frame, 1)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(frame_rgb)
                    
                    landmarks = self.extract_landmarks(results)
                    if landmarks:
                        sequence.append(landmarks)
                    
                    # Visual feedback during recording
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                frame,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style()
                            )
                    
                    # Show recording indicator
                    cv2.putText(frame, "RECORDING", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, f"Frame: {frame_num + 1}/{FRAMES_PER_SAMPLE}", (10, 70),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    cv2.imshow('Collect Training Data', frame)
                    cv2.waitKey(1)
                
                # Save the sequence
                if len(sequence) == FRAMES_PER_SAMPLE:
                    # Save to file
                    sample_path = sign_path / f"sample_{samples_collected}.json"
                    with open(sample_path, 'w') as f:
                        json.dump(sequence, f)
                    
                    # Save to database
                    save_training_sample(self.db, sign_name, sequence, user_id="collector")
                    
                    samples_collected += 1
                    print(f"Sample {samples_collected} saved!")
                else:
                    print("Failed to capture enough frames, try again")
                    
                # Short pause between samples
                time.sleep(1)
                
            elif key == ord('q'):  # Skip this sign
                print(f"Skipping {sign_name}")
                break
                
        print(f"Completed collecting {samples_collected} samples for {sign_name}")
        
    def collect_all_signs(self):
        """Collect training data for all signs"""
        print("\n" + "="*60)
        print("SIGN LANGUAGE TRAINING DATA COLLECTION")
        print("="*60)
        print(f"Signs to collect: {', '.join(SIGNS_TO_COLLECT)}")
        print(f"Samples per sign: {SAMPLES_PER_SIGN}")
        print(f"Frames per sample: {FRAMES_PER_SAMPLE}")
        print("="*60 + "\n")
        
        for sign in SIGNS_TO_COLLECT:
            self.collect_samples(sign)
            
            # Ask if user wants to continue
            print("\nPress ENTER to continue to next sign, or Q to quit...")
            if input().lower() == 'q':
                break
        
        print("\n" + "="*60)
        print("DATA COLLECTION COMPLETE!")
        print(f"Data saved to: {DATA_PATH}")
        print("="*60)
        
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        self.db.close()
        

def main():
    """Main entry point"""
    collector = TrainingDataCollector()
    
    try:
        # Initialize database with basic signs
        initialize_signs(collector.db)
        
        print("Welcome to Sign Language Training Data Collector!")
        print("\nOptions:")
        print("1. Collect all signs")
        print("2. Collect specific sign")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            collector.collect_all_signs()
        elif choice == '2':
            sign_name = input("Enter sign name: ").lower()
            num_samples = int(input(f"Number of samples (default {SAMPLES_PER_SIGN}): ") or SAMPLES_PER_SIGN)
            collector.collect_samples(sign_name, num_samples)
        else:
            print("Exiting...")
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        collector.cleanup()
        

if __name__ == "__main__":
    main()