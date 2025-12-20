"""
Database setup and management for SilentVoice
SQLite database for training data, gestures, and feedback
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignDatabase:
    """Database manager for sign language data."""
    
    def __init__(self, db_path: str = 'database/signs.db'):
        """Initialize database connection."""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to database."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        logger.info(f"Connected to database: {self.db_path}")
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        
        # Training sequences table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_sequences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gesture_name TEXT NOT NULL,
                sequence_data TEXT NOT NULL,
                frame_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Gestures table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gestures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                category TEXT,
                difficulty TEXT,
                sample_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Model metadata table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                model_path TEXT,
                accuracy REAL,
                val_accuracy REAL,
                training_samples INTEGER,
                epochs INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Feedback table for continuous improvement
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gesture_predicted TEXT,
                gesture_actual TEXT,
                confidence REAL,
                correct BOOLEAN,
                user_id TEXT,
                session_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Inference logs table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inference_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gesture_detected TEXT,
                confidence REAL,
                processing_time_ms REAL,
                model_version TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("Database tables created/verified")
    
    def insert_training_sequence(self, gesture_name: str, sequence_data: List, frame_count: int = None) -> int:
        """Insert a training sequence."""
        if frame_count is None:
            frame_count = len(sequence_data)
        
        sequence_json = json.dumps(sequence_data)
        
        self.cursor.execute('''
            INSERT INTO training_sequences (gesture_name, sequence_data, frame_count)
            VALUES (?, ?, ?)
        ''', (gesture_name, sequence_json, frame_count))
        
        self.conn.commit()
        
        # Update gesture sample count
        self.update_gesture_sample_count(gesture_name)
        
        return self.cursor.lastrowid
    
    def insert_gesture(self, name: str, description: str = None, 
                      category: str = None, difficulty: str = 'beginner') -> int:
        """Insert or update a gesture definition."""
        try:
            self.cursor.execute('''
                INSERT INTO gestures (name, description, category, difficulty)
                VALUES (?, ?, ?, ?)
            ''', (name, description, category, difficulty))
            self.conn.commit()
            logger.info(f"Added gesture: {name}")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Gesture already exists, update it
            self.cursor.execute('''
                UPDATE gestures 
                SET description = ?, category = ?, difficulty = ?
                WHERE name = ?
            ''', (description, category, difficulty, name))
            self.conn.commit()
            logger.info(f"Updated gesture: {name}")
            return self.cursor.lastrowid
    
    def get_training_sequences(self, gesture_name: str = None) -> List[Dict]:
        """Get training sequences, optionally filtered by gesture."""
        if gesture_name:
            self.cursor.execute('''
                SELECT * FROM training_sequences 
                WHERE gesture_name = ?
                ORDER BY created_at DESC
            ''', (gesture_name,))
        else:
            self.cursor.execute('''
                SELECT * FROM training_sequences 
                ORDER BY created_at DESC
            ''')
        
        rows = self.cursor.fetchall()
        sequences = []
        
        for row in rows:
            sequences.append({
                'id': row['id'],
                'gesture_name': row['gesture_name'],
                'sequence_data': json.loads(row['sequence_data']),
                'frame_count': row['frame_count'],
                'created_at': row['created_at']
            })
        
        return sequences
    
    def get_gestures(self) -> List[Dict]:
        """Get all gesture definitions."""
        self.cursor.execute('SELECT * FROM gestures ORDER BY name')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_gesture_statistics(self) -> Dict:
        """Get statistics about training data."""
        stats = {}
        
        # Total sequences
        self.cursor.execute('SELECT COUNT(*) as total FROM training_sequences')
        stats['total_sequences'] = self.cursor.fetchone()['total']
        
        # Sequences per gesture
        self.cursor.execute('''
            SELECT gesture_name, COUNT(*) as count 
            FROM training_sequences 
            GROUP BY gesture_name
        ''')
        stats['sequences_per_gesture'] = {row['gesture_name']: row['count'] 
                                         for row in self.cursor.fetchall()}
        
        # Total gestures
        self.cursor.execute('SELECT COUNT(*) as total FROM gestures')
        stats['total_gestures'] = self.cursor.fetchone()['total']
        
        return stats
    
    def insert_model_metadata(self, model_name: str, model_path: str,
                            accuracy: float, val_accuracy: float,
                            training_samples: int, epochs: int) -> int:
        """Record model training metadata."""
        self.cursor.execute('''
            INSERT INTO model_metadata 
            (model_name, model_path, accuracy, val_accuracy, training_samples, epochs)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (model_name, model_path, accuracy, val_accuracy, training_samples, epochs))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def insert_feedback(self, gesture_predicted: str, gesture_actual: str,
                       confidence: float, correct: bool,
                       user_id: str = None, session_id: str = None) -> int:
        """Record user feedback for continuous improvement."""
        self.cursor.execute('''
            INSERT INTO feedback 
            (gesture_predicted, gesture_actual, confidence, correct, user_id, session_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (gesture_predicted, gesture_actual, confidence, correct, user_id, session_id))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def insert_inference_log(self, gesture_detected: str, confidence: float,
                           processing_time_ms: float, model_version: str = 'v1') -> int:
        """Log inference results."""
        self.cursor.execute('''
            INSERT INTO inference_logs 
            (gesture_detected, confidence, processing_time_ms, model_version)
            VALUES (?, ?, ?, ?)
        ''', (gesture_detected, confidence, processing_time_ms, model_version))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_gesture_sample_count(self, gesture_name: str):
        """Update the sample count for a gesture."""
        self.cursor.execute('''
            UPDATE gestures 
            SET sample_count = (
                SELECT COUNT(*) FROM training_sequences 
                WHERE gesture_name = ?
            )
            WHERE name = ?
        ''', (gesture_name, gesture_name))
        self.conn.commit()
    
    def export_training_data(self, output_file: str):
        """Export all training data to JSON file."""
        sequences = self.get_training_sequences()
        gestures = self.get_gestures()
        
        export_data = {
            'gestures': gestures,
            'sequences': sequences,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Exported data to {output_file}")
    
    def import_training_data(self, input_file: str):
        """Import training data from JSON file."""
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Import gestures
        for gesture in data.get('gestures', []):
            self.insert_gesture(
                name=gesture['name'],
                description=gesture.get('description'),
                category=gesture.get('category'),
                difficulty=gesture.get('difficulty', 'beginner')
            )
        
        # Import sequences
        for sequence in data.get('sequences', []):
            self.insert_training_sequence(
                gesture_name=sequence['gesture_name'],
                sequence_data=sequence['sequence_data'],
                frame_count=sequence.get('frame_count')
            )
        
        logger.info(f"Imported data from {input_file}")
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


def initialize_default_gestures():
    """Initialize database with default gestures."""
    db = SignDatabase()
    
    default_gestures = [
        {'name': 'HELLO', 'description': 'Open hand wave', 'category': 'greetings', 'difficulty': 'beginner'},
        {'name': 'THANK_YOU', 'description': 'Hand from chin forward', 'category': 'greetings', 'difficulty': 'beginner'},
        {'name': 'YES', 'description': 'Closed fist nod', 'category': 'responses', 'difficulty': 'beginner'},
        {'name': 'NO', 'description': 'Index/middle finger tap thumb', 'category': 'responses', 'difficulty': 'beginner'},
        {'name': 'PLEASE', 'description': 'Flat hand circles chest', 'category': 'requests', 'difficulty': 'beginner'},
        {'name': 'SORRY', 'description': 'Closed fist circles chest', 'category': 'emotions', 'difficulty': 'beginner'},
        {'name': 'GOOD', 'description': 'Thumbs up', 'category': 'responses', 'difficulty': 'beginner'},
        {'name': 'BAD', 'description': 'Thumbs down', 'category': 'responses', 'difficulty': 'beginner'},
        {'name': 'LOVE', 'description': 'ILY sign - thumb, index, pinky extended', 'category': 'emotions', 'difficulty': 'intermediate'},
        {'name': 'PEACE', 'description': 'Peace sign - index and middle finger', 'category': 'emotions', 'difficulty': 'beginner'},
        {'name': 'HELP', 'description': 'Flat hand on fist, both lift up', 'category': 'requests', 'difficulty': 'beginner'},
        {'name': 'STOP', 'description': 'Flat hand chops down', 'category': 'commands', 'difficulty': 'beginner'},
        {'name': 'WAIT', 'description': 'Wiggle fingers facing up', 'category': 'commands', 'difficulty': 'beginner'},
        {'name': 'COME', 'description': 'Index finger beckons', 'category': 'commands', 'difficulty': 'beginner'},
        {'name': 'GO', 'description': 'Both hands point forward', 'category': 'commands', 'difficulty': 'beginner'},
    ]
    
    for gesture in default_gestures:
        db.insert_gesture(**gesture)
    
    stats = db.get_gesture_statistics()
    logger.info(f"Database initialized with {stats['total_gestures']} gestures")
    
    db.close()


if __name__ == '__main__':
    # Initialize database with default gestures
    initialize_default_gestures()
    
    # Test database operations
    db = SignDatabase()
    
    # Show statistics
    stats = db.get_gesture_statistics()
    print("\nDatabase Statistics:")
    print(f"Total gestures: {stats['total_gestures']}")
    print(f"Total sequences: {stats['total_sequences']}")
    print(f"Sequences per gesture: {stats['sequences_per_gesture']}")
    
    # Show gestures
    gestures = db.get_gestures()
    print("\nAvailable Gestures:")
    for gesture in gestures:
        print(f"  - {gesture['name']}: {gesture['description']} ({gesture['difficulty']})")
    
    db.close()