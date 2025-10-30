from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/injuries", tags=["injuries"])


@router.get("/athlete/{athlete_id}", response_model=List[schemas.InjuryHistory])
def get_athlete_injuries(athlete_id: int, db: Session = Depends(get_db)):
    """Get all injury records for an athlete"""
    injuries = db.query(models.InjuryHistory).filter(
        models.InjuryHistory.athlete_id == athlete_id
    ).order_by(models.InjuryHistory.injury_date.desc()).all()
    return injuries


@router.get("/{injury_id}", response_model=schemas.InjuryHistory)
def get_injury(injury_id: int, db: Session = Depends(get_db)):
    """Get a specific injury record"""
    injury = db.query(models.InjuryHistory).filter(models.InjuryHistory.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    return injury


@router.put("/{injury_id}", response_model=schemas.InjuryHistory)
def update_injury(
    injury_id: int,
    injury_update: schemas.InjuryHistoryBase,
    db: Session = Depends(get_db)
):
    """Update an injury record"""
    db_injury = db.query(models.InjuryHistory).filter(models.InjuryHistory.id == injury_id).first()
    if not db_injury:
        raise HTTPException(status_code=404, detail="Injury not found")

    update_data = injury_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_injury, field, value)

    db.commit()
    db.refresh(db_injury)
    return db_injury


@router.delete("/{injury_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_injury(injury_id: int, db: Session = Depends(get_db)):
    """Delete an injury record"""
    db_injury = db.query(models.InjuryHistory).filter(models.InjuryHistory.id == injury_id).first()
    if not db_injury:
        raise HTTPException(status_code=404, detail="Injury not found")

    db.delete(db_injury)
    db.commit()
    return None


@router.post("/", response_model=schemas.InjuryHistory, status_code=status.HTTP_201_CREATED)
def create_injury(injury: schemas.InjuryHistoryCreate, db: Session = Depends(get_db)):
    """Create a new injury record"""
    # Verify athlete exists
    athlete = db.query(models.Athlete).filter(models.Athlete.id == injury.athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    db_injury = models.InjuryHistory(**injury.model_dump())
    db.add(db_injury)
    db.commit()
    db.refresh(db_injury)
    return db_injury
