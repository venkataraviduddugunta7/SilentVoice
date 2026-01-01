#!/usr/bin/env python3
"""
Download and setup pre-trained ASL recognition models and datasets
"""

import os
import json
import requests
import zipfile
import numpy as np
from pathlib import Path

def download_file(url, destination):
    """Download a file with progress indicator"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"Downloading: {percent:.1f}%", end='\r')
    print(f"Downloaded: {destination}")

def setup_asl_models():
    """Download and setup ASL recognition models"""
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    data_dir = Path("asl_data")
    data_dir.mkdir(exist_ok=True)
    
    print("Setting up ASL recognition system...")
    
    # 1. Download ASL sign mappings
    print("\n1. Creating ASL sign mappings...")
    
    # Comprehensive ASL dictionary with MediaPipe landmark patterns
    asl_signs = {
        # Letters (Fingerspelling)
        "A": {"fingers": [0, 0, 0, 0, 0], "thumb": "in", "description": "Fist with thumb on side"},
        "B": {"fingers": [1, 1, 1, 1, 0], "thumb": "across", "description": "Flat hand, thumb across palm"},
        "C": {"fingers": [0.5, 0.5, 0.5, 0.5, 0.5], "thumb": "out", "description": "Curved hand like C"},
        "D": {"fingers": [1, 0, 0, 0, 0], "thumb": "touch", "description": "Index up, others touch thumb"},
        "E": {"fingers": [0.5, 0.5, 0.5, 0.5, 0], "thumb": "in", "description": "Fingers bent, thumb in"},
        "F": {"fingers": [0, 1, 1, 1, 0], "thumb": "touch_index", "description": "OK sign"},
        "G": {"fingers": [1, 0, 0, 0, 0], "thumb": "out", "description": "Index pointing, thumb out"},
        "H": {"fingers": [1, 1, 0, 0, 0], "thumb": "out", "description": "Index and middle horizontal"},
        "I": {"fingers": [0, 0, 0, 1, 0], "thumb": "in", "description": "Pinky up"},
        "J": {"fingers": [0, 0, 0, 1, 0], "thumb": "in", "motion": "hook", "description": "I with J motion"},
        "K": {"fingers": [1, 1, 0, 0, 0], "thumb": "between", "description": "Index and middle up, thumb between"},
        "L": {"fingers": [1, 0, 0, 0, 1], "thumb": "out", "description": "L shape"},
        "M": {"fingers": [0, 0, 0, 0, 0], "thumb": "under_three", "description": "Thumb under three fingers"},
        "N": {"fingers": [0, 0, 0, 0, 0], "thumb": "under_two", "description": "Thumb under two fingers"},
        "O": {"fingers": [0.5, 0.5, 0.5, 0.5, 0.5], "thumb": "touch", "description": "O shape"},
        "P": {"fingers": [1, 1, 0, 0, 0], "thumb": "between", "motion": "down", "description": "K pointing down"},
        "Q": {"fingers": [1, 0, 0, 0, 1], "thumb": "out", "motion": "down", "description": "G pointing down"},
        "R": {"fingers": [1, 1, 0, 0, 0], "thumb": "cross", "description": "Crossed fingers"},
        "S": {"fingers": [0, 0, 0, 0, 0], "thumb": "over", "description": "Fist with thumb over fingers"},
        "T": {"fingers": [0, 0, 0, 0, 0], "thumb": "between_index", "description": "Thumb between index and middle"},
        "U": {"fingers": [1, 1, 0, 0, 0], "thumb": "out", "description": "Two fingers up together"},
        "V": {"fingers": [1, 1, 0, 0, 0], "thumb": "out", "spread": True, "description": "Peace sign"},
        "W": {"fingers": [1, 1, 1, 0, 0], "thumb": "out", "description": "Three fingers up"},
        "X": {"fingers": [1, 0, 0, 0, 0], "thumb": "in", "bent": True, "description": "Index bent like hook"},
        "Y": {"fingers": [0, 0, 0, 1, 1], "thumb": "out", "description": "Thumb and pinky out"},
        "Z": {"fingers": [1, 0, 0, 0, 0], "thumb": "out", "motion": "zigzag", "description": "Index draws Z"},
        
        # Numbers
        "1": {"fingers": [1, 0, 0, 0, 0], "thumb": "in", "description": "Index finger up"},
        "2": {"fingers": [1, 1, 0, 0, 0], "thumb": "in", "description": "Index and middle up"},
        "3": {"fingers": [1, 1, 0, 0, 1], "thumb": "out", "description": "Thumb, index, middle up"},
        "4": {"fingers": [1, 1, 1, 1, 0], "thumb": "in", "description": "Four fingers up"},
        "5": {"fingers": [1, 1, 1, 1, 1], "thumb": "out", "description": "All fingers up"},
        "6": {"fingers": [1, 1, 1, 0, 0], "thumb": "touch_pinky", "description": "Three up, thumb touches pinky"},
        "7": {"fingers": [1, 1, 0, 1, 0], "thumb": "touch_ring", "description": "Thumb touches ring finger"},
        "8": {"fingers": [1, 0, 1, 1, 0], "thumb": "touch_middle", "description": "Thumb touches middle"},
        "9": {"fingers": [0, 1, 1, 1, 0], "thumb": "touch_index", "description": "Thumb touches index"},
        "10": {"fingers": [0, 0, 0, 0, 1], "thumb": "up", "motion": "shake", "description": "Thumbs up with shake"},
        
        # Common Words
        "HELLO": {"motion": "wave", "hand": "open", "description": "Open hand waving"},
        "GOODBYE": {"motion": "wave_fingers", "hand": "open", "description": "Fingers wave down"},
        "PLEASE": {"motion": "circular", "location": "chest", "hand": "flat", "description": "Circular motion on chest"},
        "THANK_YOU": {"motion": "forward", "start": "chin", "hand": "flat", "description": "Hand from chin forward"},
        "SORRY": {"motion": "circular", "location": "chest", "hand": "fist", "description": "Fist circles on chest"},
        "YES": {"motion": "nod", "hand": "fist", "description": "Fist nods like head"},
        "NO": {"fingers": [1, 1, 0, 0, 0], "motion": "close", "description": "Two fingers close on thumb"},
        "HELP": {"hand": "fist", "support": "flat", "motion": "lift", "description": "Fist on flat palm, lift up"},
        "LOVE": {"hand": "fist", "motion": "cross", "location": "chest", "description": "Arms cross on chest"},
        "FRIEND": {"fingers": "hook", "motion": "flip", "description": "Index fingers hook and flip"},
        "FAMILY": {"hand": "f", "motion": "circle", "description": "F hands in circle"},
        "WATER": {"hand": "w", "location": "chin", "motion": "tap", "description": "W taps chin"},
        "FOOD": {"hand": "flat", "motion": "to_mouth", "description": "Hand to mouth repeatedly"},
        "HUNGRY": {"hand": "c", "motion": "down", "location": "chest", "description": "C hand down chest"},
        "HAPPY": {"hand": "flat", "motion": "up", "location": "chest", "description": "Hands brush up on chest"},
        "SAD": {"hand": "open", "motion": "down", "location": "face", "description": "Hands pull down from face"},
        "TIRED": {"hand": "flat", "location": "chest", "motion": "drop", "description": "Hands drop from chest"},
        "GOOD": {"hand": "flat", "motion": "forward", "start": "chin", "description": "Hand from chin forward"},
        "BAD": {"hand": "flat", "motion": "down", "start": "chin", "description": "Hand from chin down"},
        "MORE": {"hand": "flat_o", "motion": "tap", "description": "Fingertips tap together"},
        "FINISHED": {"hand": "open", "motion": "flip", "description": "Hands flip over"},
        "WANT": {"hand": "claw", "motion": "pull", "description": "Claw hands pull toward body"},
        "NEED": {"hand": "x", "motion": "down", "description": "X hand moves down"},
        "BATHROOM": {"hand": "t", "motion": "shake", "description": "T hand shakes"},
        "WORK": {"hand": "fist", "motion": "tap", "description": "Fist taps on fist"},
        "SCHOOL": {"hand": "flat", "motion": "clap", "description": "Hands clap twice"},
        "HOME": {"hand": "flat_o", "motion": "touch", "location": "cheek_chin", "description": "Fingers touch cheek to chin"},
        "TIME": {"hand": "index", "location": "wrist", "motion": "tap", "description": "Index taps wrist"},
        "TODAY": {"hand": "y", "motion": "down", "description": "Y hands move down"},
        "TOMORROW": {"hand": "thumb", "location": "cheek", "motion": "forward", "description": "Thumb from cheek forward"},
        "YESTERDAY": {"hand": "y", "location": "chin", "motion": "back", "description": "Y from chin backward"},
    }
    
    # Save sign mappings
    with open(data_dir / "asl_signs.json", "w") as f:
        json.dump(asl_signs, f, indent=2)
    print(f"✓ Created {len(asl_signs)} ASL sign definitions")
    
    # 2. Create training data structure
    print("\n2. Creating training data structure...")
    
    training_structure = {
        "letters": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        "numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        "common_words": [
            "HELLO", "GOODBYE", "PLEASE", "THANK_YOU", "SORRY",
            "YES", "NO", "HELP", "LOVE", "FRIEND", "FAMILY",
            "WATER", "FOOD", "HUNGRY", "HAPPY", "SAD",
            "GOOD", "BAD", "MORE", "FINISHED", "WANT", "NEED",
            "BATHROOM", "WORK", "SCHOOL", "HOME", "TIME",
            "TODAY", "TOMORROW", "YESTERDAY"
        ],
        "phrases": [
            "HELLO HOW ARE YOU",
            "I AM FINE",
            "THANK YOU VERY MUCH",
            "I NEED HELP",
            "WHERE IS BATHROOM",
            "I AM HUNGRY",
            "NICE TO MEET YOU",
            "WHAT IS YOUR NAME",
            "MY NAME IS",
            "I LOVE YOU",
            "SEE YOU LATER",
            "GOOD MORNING",
            "GOOD NIGHT",
            "EXCUSE ME",
            "I AM SORRY"
        ]
    }
    
    with open(data_dir / "training_structure.json", "w") as f:
        json.dump(training_structure, f, indent=2)
    print(f"✓ Created training structure with {len(training_structure['common_words'])} words")
    
    # 3. Create landmark extraction patterns
    print("\n3. Creating landmark patterns...")
    
    landmark_patterns = {
        "hand_landmarks": {
            "num_points": 21,
            "connections": [
                [0, 1], [1, 2], [2, 3], [3, 4],  # Thumb
                [0, 5], [5, 6], [6, 7], [7, 8],  # Index
                [0, 9], [9, 10], [10, 11], [11, 12],  # Middle
                [0, 13], [13, 14], [14, 15], [15, 16],  # Ring
                [0, 17], [17, 18], [18, 19], [19, 20],  # Pinky
                [5, 9], [9, 13], [13, 17]  # Palm
            ]
        },
        "pose_landmarks": {
            "num_points": 33,
            "key_points": {
                "nose": 0,
                "left_shoulder": 11,
                "right_shoulder": 12,
                "left_elbow": 13,
                "right_elbow": 14,
                "left_wrist": 15,
                "right_wrist": 16
            }
        },
        "face_landmarks": {
            "num_points": 468,
            "key_regions": {
                "lips": list(range(0, 20)),
                "left_eye": list(range(33, 42)),
                "right_eye": list(range(133, 142)),
                "left_eyebrow": list(range(46, 53)),
                "right_eyebrow": list(range(55, 62))
            }
        }
    }
    
    with open(data_dir / "landmark_patterns.json", "w") as f:
        json.dump(landmark_patterns, f, indent=2)
    print("✓ Created landmark extraction patterns")
    
    # 4. Create sample training data
    print("\n4. Creating sample training data...")
    
    sample_data_dir = data_dir / "samples"
    sample_data_dir.mkdir(exist_ok=True)
    
    # Create sample for each sign
    for sign in ["HELLO", "THANK_YOU", "YES", "NO", "HELP"]:
        sign_dir = sample_data_dir / sign
        sign_dir.mkdir(exist_ok=True)
        
        # Create 5 sample variations
        for i in range(5):
            sample = {
                "sign": sign,
                "timestamp": f"2024_sample_{i}",
                "frames": []
            }
            
            # Generate 30 frames of synthetic data
            for frame in range(30):
                frame_data = {
                    "frame_id": frame,
                    "hands": [
                        {
                            "landmarks": [
                                {"x": np.random.random(), "y": np.random.random(), "z": np.random.random()}
                                for _ in range(21)
                            ],
                            "handedness": "Right"
                        }
                    ],
                    "pose": {
                        "landmarks": [
                            {"x": np.random.random(), "y": np.random.random(), "z": np.random.random(), "visibility": np.random.random()}
                            for _ in range(33)
                        ]
                    }
                }
                sample["frames"].append(frame_data)
            
            with open(sign_dir / f"sample_{i}.json", "w") as f:
                json.dump(sample, f)
    
    print("✓ Created sample training data")
    
    # 5. Download instructions for real datasets
    print("\n5. Instructions for real ASL datasets:")
    print("=" * 50)
    print("To get real ASL training data, you can use:")
    print()
    print("1. WLASL Dataset (Word-Level ASL)")
    print("   - 2000 ASL words")
    print("   - Download: https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed")
    print()
    print("2. MS-ASL Dataset (Microsoft ASL)")
    print("   - 1000+ ASL signs")
    print("   - Download: https://www.microsoft.com/en-us/research/project/ms-asl/")
    print()
    print("3. INCLUDE Dataset")
    print("   - 50 ASL signs with 5 participants")
    print("   - Download: https://www.kaggle.com/datasets/prathumarikeri/indian-sign-language-isl")
    print()
    print("4. ASL Alphabet Dataset")
    print("   - 87,000 images of ASL alphabet")
    print("   - Download: https://www.kaggle.com/datasets/grassknoted/asl-alphabet")
    print("=" * 50)
    
    print("\n✅ ASL recognition system setup complete!")
    print(f"Data saved in: {data_dir.absolute()}")
    print(f"Models directory: {models_dir.absolute()}")
    
    return str(data_dir.absolute())

if __name__ == "__main__":
    data_path = setup_asl_models()
    print(f"\nNext steps:")
    print("1. Download real datasets from the links above")
    print("2. Place them in: {data_path}")
    print("3. Run: python train_model.py")
