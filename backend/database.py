"""
Database setup and models for SilentVoice
Supports both SQLite (development) and PostgreSQL (production)
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pathlib import Path

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/silentvoice.db")

# Create data directory if it doesn't exist
Path("data").mkdir(exist_ok=True)

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models

class Sign(Base):
    """Sign language dictionary entry"""
    __tablename__ = "signs"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50))  # greetings, common, alphabet, etc.
    difficulty = Column(String(20))  # beginner, intermediate, advanced
    description = Column(Text)  # How to perform the sign
    hand_landmarks = Column(JSON)  # Reference landmarks for this sign
    video_url = Column(String(500))  # Optional video demonstration
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    training_samples = relationship("TrainingSample", back_populates="sign")
    user_progress = relationship("UserProgress", back_populates="sign")


class TrainingSample(Base):
    """Training data samples for improving the model"""
    __tablename__ = "training_samples"
    
    id = Column(Integer, primary_key=True, index=True)
    sign_id = Column(Integer, ForeignKey("signs.id"))
    landmarks = Column(JSON, nullable=False)  # Hand landmark data
    user_id = Column(String(100))  # Who provided this sample
    quality_score = Column(Float)  # Quality of the sample (0-1)
    is_validated = Column(Integer, default=0)  # Has this been validated?
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sign = relationship("Sign", back_populates="training_samples")


class UserProgress(Base):
    """Track user learning progress"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True)
    sign_id = Column(Integer, ForeignKey("signs.id"))
    practice_count = Column(Integer, default=0)
    accuracy = Column(Float)  # Average accuracy (0-1)
    last_practiced = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sign = relationship("Sign", back_populates="user_progress")


class ModelVersion(Base):
    """Track trained model versions"""
    __tablename__ = "model_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(50), unique=True)
    model_path = Column(String(500))
    accuracy = Column(Float)
    training_samples = Column(Integer)  # Number of samples used
    labels = Column(JSON)  # List of signs this model can recognize
    model_metadata = Column(JSON)  # Additional model info (renamed from metadata)
    is_active = Column(Integer, default=0)  # Is this the current model?
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)


# Database helper functions

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_signs(db: Session):
    """Initialize the database with basic signs"""
    basic_signs = [
        {"word": "hello", "category": "greetings", "difficulty": "beginner", 
         "description": "Open hand, palm facing out, wave side to side"},
        {"word": "thank_you", "category": "greetings", "difficulty": "beginner",
         "description": "Flat hand starts at chin, moves forward"},
        {"word": "please", "category": "greetings", "difficulty": "beginner",
         "description": "Flat hand circles on chest"},
        {"word": "yes", "category": "responses", "difficulty": "beginner",
         "description": "Closed fist nods up and down"},
        {"word": "no", "category": "responses", "difficulty": "beginner",
         "description": "Index and middle finger tap thumb"},
        {"word": "help", "category": "common", "difficulty": "beginner",
         "description": "Flat hand on opposite fist, both lift up"},
        {"word": "sorry", "category": "emotions", "difficulty": "beginner",
         "description": "Closed fist circles on chest"},
        {"word": "love", "category": "emotions", "difficulty": "intermediate",
         "description": "Cross arms over chest"},
        {"word": "friend", "category": "people", "difficulty": "intermediate",
         "description": "Hook index fingers together, flip"},
        {"word": "family", "category": "people", "difficulty": "intermediate",
         "description": "F handshapes in circle"},
    ]
    
    for sign_data in basic_signs:
        # Check if sign already exists
        existing = db.query(Sign).filter(Sign.word == sign_data["word"]).first()
        if not existing:
            sign = Sign(**sign_data)
            db.add(sign)
    
    db.commit()
    print(f"Initialized {len(basic_signs)} basic signs in database")


def save_training_sample(db: Session, sign_word: str, landmarks: List, user_id: str = "anonymous"):
    """Save a training sample to the database"""
    sign = db.query(Sign).filter(Sign.word == sign_word).first()
    if not sign:
        # Create new sign if it doesn't exist
        sign = Sign(word=sign_word, category="custom")
        db.add(sign)
        db.commit()
        db.refresh(sign)
    
    sample = TrainingSample(
        sign_id=sign.id,
        landmarks=landmarks,
        user_id=user_id,
        quality_score=0.8  # Default quality score
    )
    db.add(sample)
    db.commit()
    return sample


def get_training_data(db: Session, min_quality: float = 0.7) -> Dict:
    """Get all training data for model training"""
    samples = db.query(TrainingSample).filter(
        TrainingSample.quality_score >= min_quality
    ).all()
    
    data = {}
    for sample in samples:
        sign_word = sample.sign.word
        if sign_word not in data:
            data[sign_word] = []
        data[sign_word].append(sample.landmarks)
    
    return data


def update_user_progress(db: Session, user_id: str, sign_word: str, accuracy: float):
    """Update user's learning progress"""
    sign = db.query(Sign).filter(Sign.word == sign_word).first()
    if not sign:
        return None
    
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.sign_id == sign.id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            sign_id=sign.id,
            practice_count=1,
            accuracy=accuracy,
            last_practiced=datetime.utcnow()
        )
        db.add(progress)
    else:
        progress.practice_count += 1
        # Update running average accuracy
        progress.accuracy = (progress.accuracy * (progress.practice_count - 1) + accuracy) / progress.practice_count
        progress.last_practiced = datetime.utcnow()
    
    db.commit()
    return progress


def get_model_version(db: Session) -> Optional[ModelVersion]:
    """Get the active model version"""
    return db.query(ModelVersion).filter(ModelVersion.is_active == 1).first()


def save_model_version(db: Session, version: str, model_path: str, accuracy: float, 
                      training_samples: int, labels: List[str], metadata: Dict = None):
    """Save a new model version"""
    # Deactivate previous models
    db.query(ModelVersion).update({ModelVersion.is_active: 0})
    
    # Create new model version
    model = ModelVersion(
        version=version,
        model_path=model_path,
        accuracy=accuracy,
        training_samples=training_samples,
        labels=labels,
        model_metadata=metadata or {},
        is_active=1
    )
    db.add(model)
    db.commit()
    return model


# Initialize database with basic data
if __name__ == "__main__":
    db = SessionLocal()
    try:
        initialize_signs(db)
        print("Database initialized successfully!")
    finally:
        db.close()