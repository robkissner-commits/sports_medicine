from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List


# Athlete Schemas
class AthleteBase(BaseModel):
    name: str
    position: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    team: Optional[str] = None


class AthleteCreate(AthleteBase):
    pass


class AthleteUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    team: Optional[str] = None


class Athlete(AthleteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Training Load Schemas (Kinexon Data)
class TrainingLoadBase(BaseModel):
    date: date
    distance_miles: float  # Distance (mi) - REQUIRED
    accumulated_accel_load: float  # Accumulated Acceleration Load - REQUIRED
    average_speed_mph: Optional[float] = None  # Speed (Ø) (mph)
    max_speed_mph: Optional[float] = None  # Speed (max.) (mph)
    session_type: Optional[str] = None  # Optional: practice, game, recovery


class TrainingLoadCreate(TrainingLoadBase):
    athlete_id: int


class TrainingLoad(TrainingLoadBase):
    id: int
    athlete_id: int
    training_load: float  # Auto-calculated from Kinexon data
    created_at: datetime

    class Config:
        from_attributes = True


# Treatment Schemas
class TreatmentBase(BaseModel):
    date: date
    modality: str
    duration: Optional[int] = None
    body_part: Optional[str] = None
    severity: Optional[str] = None
    notes: Optional[str] = None


class TreatmentCreate(TreatmentBase):
    athlete_id: int


class Treatment(TreatmentBase):
    id: int
    athlete_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Lifestyle Log Schemas
class LifestyleLogBase(BaseModel):
    date: date
    sleep_hours: Optional[float] = None
    sleep_quality: Optional[int] = None
    nutrition_score: Optional[int] = None
    hydration_liters: Optional[float] = None
    stress_level: Optional[int] = None
    soreness_level: Optional[int] = None
    fatigue_level: Optional[int] = None
    notes: Optional[str] = None


class LifestyleLogCreate(LifestyleLogBase):
    athlete_id: int


class LifestyleLog(LifestyleLogBase):
    id: int
    athlete_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Risk Assessment Schemas
class RiskAssessmentBase(BaseModel):
    date: date
    overall_risk_score: float
    risk_level: str

    # Traditional metrics
    acwr: Optional[float] = None
    acute_load: Optional[float] = None
    chronic_load: Optional[float] = None
    load_spike_score: Optional[float] = None
    recovery_score: Optional[float] = None
    lifestyle_score: Optional[float] = None
    injury_history_score: Optional[float] = None

    # NEW: Enhanced metrics (Hybrid Evidence-Based System)
    training_monotony: Optional[float] = None
    training_strain: Optional[float] = None
    current_z_score: Optional[float] = None
    max_z_score_7d: Optional[float] = None

    # NEW: Risk modifiers (for transparency)
    sleep_modifier: Optional[float] = None
    stress_modifier: Optional[float] = None
    injury_recency_modifier: Optional[float] = None
    age_modifier: Optional[float] = None
    compound_multiplier: Optional[float] = None

    recommendations: Optional[str] = None


class RiskAssessmentCreate(RiskAssessmentBase):
    athlete_id: int


class RiskAssessment(RiskAssessmentBase):
    id: int
    athlete_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Injury History Schemas
class InjuryHistoryBase(BaseModel):
    injury_date: date
    injury_type: str
    body_part: str
    severity: Optional[str] = None
    recovery_date: Optional[date] = None
    days_missed: Optional[int] = None
    description: Optional[str] = None


class InjuryHistoryCreate(InjuryHistoryBase):
    athlete_id: int


class InjuryHistory(InjuryHistoryBase):
    id: int
    athlete_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Schemas
class AthleteRiskSummary(BaseModel):
    id: int
    name: str
    position: Optional[str]
    risk_level: str
    risk_score: float
    acwr: Optional[float]
    last_assessment_date: Optional[date]


class TeamOverview(BaseModel):
    total_athletes: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    athletes: List[AthleteRiskSummary]


# Analytics Schemas
class ACWRCalculation(BaseModel):
    athlete_id: int
    date: date
    acute_load: float
    chronic_load: float
    acwr: float
    risk_category: str


class AthleteDetail(Athlete):
    current_risk_level: Optional[str] = None
    current_risk_score: Optional[float] = None
    latest_acwr: Optional[float] = None
    recent_injuries_count: int = 0
    days_since_last_injury: Optional[int] = None

    class Config:
        from_attributes = True
