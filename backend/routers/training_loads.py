from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db
from ..analytics import calculate_training_load_from_kinexon

router = APIRouter(prefix="/training-loads", tags=["training-loads"])


@router.get("/{load_id}", response_model=schemas.TrainingLoad)
def get_training_load(load_id: int, db: Session = Depends(get_db)):
    """Get a specific training load record"""
    load = db.query(models.TrainingLoad).filter(models.TrainingLoad.id == load_id).first()
    if not load:
        raise HTTPException(status_code=404, detail="Training load not found")
    return load


@router.put("/{load_id}", response_model=schemas.TrainingLoad)
def update_training_load(
    load_id: int,
    load_update: schemas.TrainingLoadBase,
    db: Session = Depends(get_db)
):
    """Update a training load record - auto-calculates training_load from Kinexon data"""
    db_load = db.query(models.TrainingLoad).filter(models.TrainingLoad.id == load_id).first()
    if not db_load:
        raise HTTPException(status_code=404, detail="Training load not found")

    update_data = load_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_load, field, value)

    # Auto-calculate training load from Kinexon metrics
    db_load.training_load = calculate_training_load_from_kinexon(
        distance_miles=db_load.distance_miles,
        accumulated_accel_load=db_load.accumulated_accel_load,
        average_speed_mph=db_load.average_speed_mph,
        max_speed_mph=db_load.max_speed_mph
    )

    db.commit()
    db.refresh(db_load)
    return db_load


@router.delete("/{load_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_load(load_id: int, db: Session = Depends(get_db)):
    """Delete a training load record"""
    db_load = db.query(models.TrainingLoad).filter(models.TrainingLoad.id == load_id).first()
    if not db_load:
        raise HTTPException(status_code=404, detail="Training load not found")

    db.delete(db_load)
    db.commit()
    return None


@router.post("/", response_model=schemas.TrainingLoad, status_code=status.HTTP_201_CREATED)
def create_training_load(load: schemas.TrainingLoadCreate, db: Session = Depends(get_db)):
    """Create a new training load record - auto-calculates training_load from Kinexon data"""
    # Verify athlete exists
    athlete = db.query(models.Athlete).filter(models.Athlete.id == load.athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    # Calculate training load from Kinexon metrics
    training_load = calculate_training_load_from_kinexon(
        distance_miles=load.distance_miles,
        accumulated_accel_load=load.accumulated_accel_load,
        average_speed_mph=load.average_speed_mph,
        max_speed_mph=load.max_speed_mph
    )

    # Create training load record
    db_load = models.TrainingLoad(
        **load.model_dump(),
        training_load=training_load
    )
    db.add(db_load)
    db.commit()
    db.refresh(db_load)
    return db_load
