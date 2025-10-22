from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db
from ..analytics import AnalyticsEngine

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.post("/", response_model=schemas.Athlete, status_code=status.HTTP_201_CREATED)
def create_athlete(athlete: schemas.AthleteCreate, db: Session = Depends(get_db)):
    """Create a new athlete profile"""
    # Check if email already exists
    if athlete.email:
        existing = db.query(models.Athlete).filter(
            models.Athlete.email == athlete.email
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Athlete with this email already exists"
            )

    db_athlete = models.Athlete(**athlete.model_dump())
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)
    return db_athlete


@router.get("/", response_model=List[schemas.Athlete])
def list_athletes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all athletes"""
    athletes = db.query(models.Athlete).offset(skip).limit(limit).all()
    return athletes


@router.get("/{athlete_id}", response_model=schemas.AthleteDetail)
def get_athlete(athlete_id: int, db: Session = Depends(get_db)):
    """Get detailed athlete information including current risk status"""
    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    # Get latest risk assessment
    latest_assessment = db.query(models.RiskAssessment).filter(
        models.RiskAssessment.athlete_id == athlete_id
    ).order_by(models.RiskAssessment.date.desc()).first()

    # Count recent injuries (last 6 months)
    from datetime import timedelta
    six_months_ago = date.today() - timedelta(days=180)
    recent_injuries = db.query(models.InjuryHistory).filter(
        models.InjuryHistory.athlete_id == athlete_id,
        models.InjuryHistory.injury_date >= six_months_ago
    ).count()

    # Get days since last injury
    last_injury = db.query(models.InjuryHistory).filter(
        models.InjuryHistory.athlete_id == athlete_id
    ).order_by(models.InjuryHistory.injury_date.desc()).first()

    days_since_injury = None
    if last_injury:
        days_since_injury = (date.today() - last_injury.injury_date).days

    # Build response
    athlete_dict = {
        "id": athlete.id,
        "name": athlete.name,
        "position": athlete.position,
        "age": athlete.age,
        "email": athlete.email,
        "team": athlete.team,
        "created_at": athlete.created_at,
        "updated_at": athlete.updated_at,
        "current_risk_level": latest_assessment.risk_level if latest_assessment else None,
        "current_risk_score": latest_assessment.overall_risk_score if latest_assessment else None,
        "latest_acwr": latest_assessment.acwr if latest_assessment else None,
        "recent_injuries_count": recent_injuries,
        "days_since_last_injury": days_since_injury
    }

    return athlete_dict


@router.put("/{athlete_id}", response_model=schemas.Athlete)
def update_athlete(
    athlete_id: int,
    athlete_update: schemas.AthleteUpdate,
    db: Session = Depends(get_db)
):
    """Update athlete information"""
    db_athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not db_athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    update_data = athlete_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_athlete, field, value)

    db.commit()
    db.refresh(db_athlete)
    return db_athlete


@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_athlete(athlete_id: int, db: Session = Depends(get_db)):
    """Delete an athlete and all associated data"""
    db_athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not db_athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    db.delete(db_athlete)
    db.commit()
    return None


@router.get("/{athlete_id}/training-loads", response_model=List[schemas.TrainingLoad])
def get_athlete_training_loads(
    athlete_id: int,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """Get training loads for an athlete"""
    query = db.query(models.TrainingLoad).filter(
        models.TrainingLoad.athlete_id == athlete_id
    )

    if start_date:
        query = query.filter(models.TrainingLoad.date >= start_date)
    if end_date:
        query = query.filter(models.TrainingLoad.date <= end_date)

    loads = query.order_by(models.TrainingLoad.date).all()
    return loads


@router.get("/{athlete_id}/risk-history", response_model=List[schemas.RiskAssessment])
def get_athlete_risk_history(
    athlete_id: int,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """Get risk assessment history for an athlete"""
    query = db.query(models.RiskAssessment).filter(
        models.RiskAssessment.athlete_id == athlete_id
    )

    if start_date:
        query = query.filter(models.RiskAssessment.date >= start_date)
    if end_date:
        query = query.filter(models.RiskAssessment.date <= end_date)

    assessments = query.order_by(models.RiskAssessment.date).all()
    return assessments


@router.post("/{athlete_id}/calculate-risk", response_model=schemas.RiskAssessment)
def calculate_athlete_risk(
    athlete_id: int,
    target_date: date = None,
    db: Session = Depends(get_db)
):
    """Calculate and store current risk assessment for an athlete"""
    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    if not target_date:
        target_date = date.today()

    # Calculate risk using analytics engine
    risk_data = AnalyticsEngine.calculate_overall_risk(db, athlete_id, target_date)

    # Create risk assessment record
    assessment = models.RiskAssessment(
        athlete_id=athlete_id,
        date=target_date,
        **risk_data
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment
