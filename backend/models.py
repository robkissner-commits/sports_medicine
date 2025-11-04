from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    team = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    training_loads = relationship("TrainingLoad", back_populates="athlete", cascade="all, delete-orphan")
    treatments = relationship("Treatment", back_populates="athlete", cascade="all, delete-orphan")
    lifestyle_logs = relationship("LifestyleLog", back_populates="athlete", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="athlete", cascade="all, delete-orphan")
    injuries = relationship("InjuryHistory", back_populates="athlete", cascade="all, delete-orphan")


class TrainingLoad(Base):
    __tablename__ = "training_loads"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("athletes.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Kinexon metrics
    total_distance = Column(Float)  # meters
    high_speed_distance = Column(Float)  # meters
    sprint_distance = Column(Float)  # meters
    accelerations = Column(Integer)
    decelerations = Column(Integer)
    max_speed = Column(Float)  # km/h

    # Training load metrics
    training_load = Column(Float, nullable=False)  # RPE * duration or calculated load
    duration = Column(Integer)  # minutes
    session_type = Column(String)  # practice, game, recovery, etc.

    # Additional metrics
    player_load = Column(Float)  # Overall player load
    metabolic_power = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    athlete = relationship("Athlete", back_populates="training_loads")


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("athletes.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    modality = Column(String, nullable=False)  # ice bath, massage, PT, etc.
    duration = Column(Integer)  # minutes
    body_part = Column(String)  # affected area
    severity = Column(String)  # minor, moderate, severe
    notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    athlete = relationship("Athlete", back_populates="treatments")


class LifestyleLog(Base):
    __tablename__ = "lifestyle_logs"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("athletes.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    sleep_hours = Column(Float)
    sleep_quality = Column(Integer)  # 1-10 scale
    nutrition_score = Column(Integer)  # 1-10 scale
    hydration_liters = Column(Float)
    stress_level = Column(Integer)  # 1-10 scale
    soreness_level = Column(Integer)  # 1-10 scale
    fatigue_level = Column(Integer)  # 1-10 scale

    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    athlete = relationship("Athlete", back_populates="lifestyle_logs")


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("athletes.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    # Risk scores
    overall_risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)  # low, medium, high

    # Traditional contributing factors
    acwr = Column(Float)
    acute_load = Column(Float)
    chronic_load = Column(Float)
    load_spike_score = Column(Float)
    recovery_score = Column(Float)
    lifestyle_score = Column(Float)
    injury_history_score = Column(Float)

    # NEW: Enhanced metrics (Hybrid Evidence-Based System)
    training_monotony = Column(Float)
    training_strain = Column(Float)
    current_z_score = Column(Float)
    max_z_score_7d = Column(Float)

    # NEW: Risk modifiers (for transparency)
    sleep_modifier = Column(Float)
    stress_modifier = Column(Float)
    injury_recency_modifier = Column(Float)
    age_modifier = Column(Float)
    compound_multiplier = Column(Float)

    # Recommendations
    recommendations = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    athlete = relationship("Athlete", back_populates="risk_assessments")


class InjuryHistory(Base):
    __tablename__ = "injury_history"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("athletes.id"), nullable=False)

    injury_date = Column(Date, nullable=False)
    injury_type = Column(String, nullable=False)
    body_part = Column(String, nullable=False)
    severity = Column(String)  # minor, moderate, severe, catastrophic

    recovery_date = Column(Date)
    days_missed = Column(Integer)

    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    athlete = relationship("Athlete", back_populates="injuries")
