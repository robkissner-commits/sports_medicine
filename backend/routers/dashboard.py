from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import date, timedelta

from .. import models, schemas
from ..database import get_db
from ..analytics import AnalyticsEngine

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/team-overview", response_model=schemas.TeamOverview)
def get_team_overview(
    team: Optional[str] = None,
    risk_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get team overview with all athletes and their current risk levels
    """
    # Get all athletes
    query = db.query(models.Athlete)
    if team:
        query = query.filter(models.Athlete.team == team)

    athletes = query.all()

    athlete_summaries = []
    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0

    for athlete in athletes:
        # Get latest risk assessment
        latest_assessment = db.query(models.RiskAssessment).filter(
            models.RiskAssessment.athlete_id == athlete.id
        ).order_by(desc(models.RiskAssessment.date)).first()

        if latest_assessment:
            current_risk_level = latest_assessment.risk_level
            current_risk_score = latest_assessment.overall_risk_score
            acwr = latest_assessment.acwr
            assessment_date = latest_assessment.date
        else:
            # Calculate risk if no assessment exists
            risk_data = AnalyticsEngine.calculate_overall_risk(
                db, athlete.id, date.today()
            )
            current_risk_level = risk_data["risk_level"]
            current_risk_score = risk_data["overall_risk_score"]
            acwr = risk_data["acwr"]
            assessment_date = None

        # Count by risk level
        if current_risk_level == "high":
            high_risk_count += 1
        elif current_risk_level == "medium":
            medium_risk_count += 1
        else:
            low_risk_count += 1

        # Filter by risk level if specified
        if risk_level and current_risk_level != risk_level:
            continue

        athlete_summaries.append(
            schemas.AthleteRiskSummary(
                id=athlete.id,
                name=athlete.name,
                position=athlete.position,
                risk_level=current_risk_level,
                risk_score=current_risk_score,
                acwr=acwr,
                last_assessment_date=assessment_date
            )
        )

    # Sort by risk score (highest first)
    athlete_summaries.sort(key=lambda x: x.risk_score, reverse=True)

    return schemas.TeamOverview(
        total_athletes=len(athletes),
        high_risk_count=high_risk_count,
        medium_risk_count=medium_risk_count,
        low_risk_count=low_risk_count,
        athletes=athlete_summaries
    )


@router.post("/calculate-all-risks")
def calculate_all_athlete_risks(
    target_date: date = None,
    db: Session = Depends(get_db)
):
    """Calculate and store risk assessments for all athletes"""
    if not target_date:
        target_date = date.today()

    athletes = db.query(models.Athlete).all()
    calculated_count = 0
    errors = []

    for athlete in athletes:
        try:
            # Check if assessment already exists for this date
            existing = db.query(models.RiskAssessment).filter(
                models.RiskAssessment.athlete_id == athlete.id,
                models.RiskAssessment.date == target_date
            ).first()

            if existing:
                continue

            # Calculate risk
            risk_data = AnalyticsEngine.calculate_overall_risk(
                db, athlete.id, target_date
            )

            # Create assessment
            assessment = models.RiskAssessment(
                athlete_id=athlete.id,
                date=target_date,
                **risk_data
            )

            db.add(assessment)
            calculated_count += 1

        except Exception as e:
            errors.append(f"Athlete {athlete.name}: {str(e)}")

    db.commit()

    return {
        "message": f"Calculated risk for {calculated_count} athletes",
        "calculated_count": calculated_count,
        "errors": errors
    }


@router.get("/athlete/{athlete_id}/acwr-trend")
def get_athlete_acwr_trend(
    athlete_id: int,
    days: int = 56,
    db: Session = Depends(get_db)
):
    """Get ACWR trend for an athlete over specified days"""
    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    acwr_data = []
    current_date = start_date

    while current_date <= end_date:
        result = AnalyticsEngine.calculate_acwr(db, athlete_id, current_date)

        if result:
            acute_load, chronic_load, acwr = result

            # Determine risk category
            if acwr > 1.5 or acwr < 0.8:
                risk_category = "high"
            elif acwr > 1.3 or acwr < 0.9:
                risk_category = "medium"
            else:
                risk_category = "low"

            acwr_data.append({
                "date": current_date.isoformat(),
                "acute_load": round(acute_load, 2),
                "chronic_load": round(chronic_load, 2),
                "acwr": round(acwr, 2),
                "risk_category": risk_category
            })

        current_date += timedelta(days=1)

    return {
        "athlete_id": athlete_id,
        "athlete_name": athlete.name,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "data": acwr_data
    }


@router.get("/athlete/{athlete_id}/training-summary")
def get_athlete_training_summary(
    athlete_id: int,
    days: int = 28,
    db: Session = Depends(get_db)
):
    """Get training summary statistics for an athlete"""
    athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # Get training loads
    loads = db.query(models.TrainingLoad).filter(
        models.TrainingLoad.athlete_id == athlete_id,
        models.TrainingLoad.date >= start_date,
        models.TrainingLoad.date <= end_date
    ).order_by(models.TrainingLoad.date).all()

    if not loads:
        return {
            "athlete_id": athlete_id,
            "athlete_name": athlete.name,
            "period_days": days,
            "session_count": 0,
            "message": "No training data available"
        }

    # Calculate statistics
    total_load = sum(l.training_load for l in loads)
    avg_load = total_load / len(loads)
    max_load = max(l.training_load for l in loads)
    min_load = min(l.training_load for l in loads)

    total_distance = sum(l.total_distance or 0 for l in loads)
    total_high_speed = sum(l.high_speed_distance or 0 for l in loads)

    return {
        "athlete_id": athlete_id,
        "athlete_name": athlete.name,
        "period_days": days,
        "session_count": len(loads),
        "total_load": round(total_load, 2),
        "average_load": round(avg_load, 2),
        "max_load": round(max_load, 2),
        "min_load": round(min_load, 2),
        "total_distance_meters": round(total_distance, 2),
        "total_high_speed_distance_meters": round(total_high_speed, 2),
        "loads_by_date": [
            {
                "date": l.date.isoformat(),
                "training_load": l.training_load,
                "session_type": l.session_type
            } for l in loads
        ]
    }
