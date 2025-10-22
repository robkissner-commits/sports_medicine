from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/lifestyle", tags=["lifestyle"])


@router.post("/", response_model=schemas.LifestyleLog, status_code=status.HTTP_201_CREATED)
def create_lifestyle_log(log: schemas.LifestyleLogCreate, db: Session = Depends(get_db)):
    """Create a new lifestyle log entry"""
    # Verify athlete exists
    athlete = db.query(models.Athlete).filter(models.Athlete.id == log.athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    db_log = models.LifestyleLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/athlete/{athlete_id}", response_model=List[schemas.LifestyleLog])
def get_athlete_lifestyle_logs(
    athlete_id: int,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """Get lifestyle logs for an athlete"""
    query = db.query(models.LifestyleLog).filter(
        models.LifestyleLog.athlete_id == athlete_id
    )

    if start_date:
        query = query.filter(models.LifestyleLog.date >= start_date)
    if end_date:
        query = query.filter(models.LifestyleLog.date <= end_date)

    logs = query.order_by(models.LifestyleLog.date.desc()).all()
    return logs


@router.put("/{log_id}", response_model=schemas.LifestyleLog)
def update_lifestyle_log(
    log_id: int,
    log_update: schemas.LifestyleLogBase,
    db: Session = Depends(get_db)
):
    """Update a lifestyle log entry"""
    db_log = db.query(models.LifestyleLog).filter(models.LifestyleLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Lifestyle log not found")

    for field, value in log_update.model_dump(exclude_unset=True).items():
        setattr(db_log, field, value)

    db.commit()
    db.refresh(db_log)
    return db_log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lifestyle_log(log_id: int, db: Session = Depends(get_db)):
    """Delete a lifestyle log entry"""
    db_log = db.query(models.LifestyleLog).filter(models.LifestyleLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Lifestyle log not found")

    db.delete(db_log)
    db.commit()
    return None
