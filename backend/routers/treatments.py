from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/treatments", tags=["treatments"])


@router.get("/athlete/{athlete_id}", response_model=List[schemas.Treatment])
def get_athlete_treatments(athlete_id: int, db: Session = Depends(get_db)):
    """Get all treatment records for an athlete"""
    treatments = db.query(models.Treatment).filter(
        models.Treatment.athlete_id == athlete_id
    ).order_by(models.Treatment.date.desc()).all()
    return treatments


@router.get("/{treatment_id}", response_model=schemas.Treatment)
def get_treatment(treatment_id: int, db: Session = Depends(get_db)):
    """Get a specific treatment record"""
    treatment = db.query(models.Treatment).filter(models.Treatment.id == treatment_id).first()
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment


@router.put("/{treatment_id}", response_model=schemas.Treatment)
def update_treatment(
    treatment_id: int,
    treatment_update: schemas.TreatmentBase,
    db: Session = Depends(get_db)
):
    """Update a treatment record"""
    db_treatment = db.query(models.Treatment).filter(models.Treatment.id == treatment_id).first()
    if not db_treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    update_data = treatment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_treatment, field, value)

    db.commit()
    db.refresh(db_treatment)
    return db_treatment


@router.delete("/{treatment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    """Delete a treatment record"""
    db_treatment = db.query(models.Treatment).filter(models.Treatment.id == treatment_id).first()
    if not db_treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")

    db.delete(db_treatment)
    db.commit()
    return None


@router.post("/", response_model=schemas.Treatment, status_code=status.HTTP_201_CREATED)
def create_treatment(treatment: schemas.TreatmentCreate, db: Session = Depends(get_db)):
    """Create a new treatment record"""
    # Verify athlete exists
    athlete = db.query(models.Athlete).filter(models.Athlete.id == treatment.athlete_id).first()
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")

    db_treatment = models.Treatment(**treatment.model_dump())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    return db_treatment
