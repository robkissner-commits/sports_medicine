from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from datetime import datetime, date

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/upload", tags=["data-upload"])


@router.post("/training-loads")
async def upload_training_loads(
    file: UploadFile = File(...),
    athlete_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload Kinexon training load data from CSV

    Expected columns:
    - date or Date (YYYY-MM-DD)
    - athlete_id or athlete_name (if not provided in form)
    - training_load or load
    - total_distance
    - high_speed_distance
    - sprint_distance
    - accelerations
    - decelerations
    - max_speed
    - duration
    - session_type
    - player_load
    - metabolic_power
    """
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(
            status_code=400,
            detail="File must be CSV or Excel format"
        )

    try:
        # Read file
        contents = await file.read()

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()

        # Parse dates
        date_col = 'date' if 'date' in df.columns else df.columns[0]
        df[date_col] = pd.to_datetime(df[date_col])

        created_count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                # Determine athlete_id
                current_athlete_id = athlete_id
                if not current_athlete_id:
                    if 'athlete_id' in row:
                        current_athlete_id = int(row['athlete_id'])
                    elif 'athlete_name' in row:
                        # Find athlete by name
                        athlete = db.query(models.Athlete).filter(
                            models.Athlete.name == row['athlete_name']
                        ).first()
                        if athlete:
                            current_athlete_id = athlete.id

                if not current_athlete_id:
                    errors.append(f"Row {idx + 1}: No athlete_id specified")
                    continue

                # Verify athlete exists
                athlete = db.query(models.Athlete).filter(
                    models.Athlete.id == current_athlete_id
                ).first()
                if not athlete:
                    errors.append(f"Row {idx + 1}: Athlete ID {current_athlete_id} not found")
                    continue

                # Extract training load value
                training_load = None
                if 'training_load' in row and pd.notna(row['training_load']):
                    training_load = float(row['training_load'])
                elif 'load' in row and pd.notna(row['load']):
                    training_load = float(row['load'])
                elif 'player_load' in row and pd.notna(row['player_load']):
                    training_load = float(row['player_load'])

                if training_load is None:
                    errors.append(f"Row {idx + 1}: No training_load value found")
                    continue

                # Create training load record
                load_data = {
                    'athlete_id': current_athlete_id,
                    'date': row[date_col].date(),
                    'training_load': training_load,
                }

                # Add optional fields
                optional_fields = [
                    'total_distance', 'high_speed_distance', 'sprint_distance',
                    'accelerations', 'decelerations', 'max_speed', 'duration',
                    'session_type', 'player_load', 'metabolic_power'
                ]

                for field in optional_fields:
                    if field in row and pd.notna(row[field]):
                        load_data[field] = row[field]

                db_load = models.TrainingLoad(**load_data)
                db.add(db_load)
                created_count += 1

            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        db.commit()

        return {
            "message": f"Successfully imported {created_count} training load records",
            "created_count": created_count,
            "errors": errors[:10] if errors else []  # Limit error list
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/treatments")
async def upload_treatments(
    file: UploadFile = File(...),
    athlete_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload ATS treatment data from CSV

    Expected columns:
    - date or treatment_date
    - athlete_id or athlete_name (if not provided in form)
    - modality or treatment_type
    - duration
    - body_part
    - severity
    - notes
    """
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(
            status_code=400,
            detail="File must be CSV or Excel format"
        )

    try:
        contents = await file.read()

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        df.columns = df.columns.str.lower().str.strip()

        # Parse dates
        date_col = 'date' if 'date' in df.columns else 'treatment_date' if 'treatment_date' in df.columns else df.columns[0]
        df[date_col] = pd.to_datetime(df[date_col])

        created_count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                current_athlete_id = athlete_id
                if not current_athlete_id:
                    if 'athlete_id' in row:
                        current_athlete_id = int(row['athlete_id'])
                    elif 'athlete_name' in row:
                        athlete = db.query(models.Athlete).filter(
                            models.Athlete.name == row['athlete_name']
                        ).first()
                        if athlete:
                            current_athlete_id = athlete.id

                if not current_athlete_id:
                    errors.append(f"Row {idx + 1}: No athlete_id specified")
                    continue

                # Get modality
                modality = row.get('modality') or row.get('treatment_type')
                if pd.isna(modality):
                    errors.append(f"Row {idx + 1}: No modality specified")
                    continue

                treatment_data = {
                    'athlete_id': current_athlete_id,
                    'date': row[date_col].date(),
                    'modality': str(modality),
                }

                # Add optional fields
                if 'duration' in row and pd.notna(row['duration']):
                    treatment_data['duration'] = int(row['duration'])
                if 'body_part' in row and pd.notna(row['body_part']):
                    treatment_data['body_part'] = str(row['body_part'])
                if 'severity' in row and pd.notna(row['severity']):
                    treatment_data['severity'] = str(row['severity'])
                if 'notes' in row and pd.notna(row['notes']):
                    treatment_data['notes'] = str(row['notes'])

                db_treatment = models.Treatment(**treatment_data)
                db.add(db_treatment)
                created_count += 1

            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        db.commit()

        return {
            "message": f"Successfully imported {created_count} treatment records",
            "created_count": created_count,
            "errors": errors[:10] if errors else []
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/injuries")
async def upload_injury_history(
    file: UploadFile = File(...),
    athlete_id: int = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload injury history from CSV

    Expected columns:
    - injury_date
    - athlete_id or athlete_name
    - injury_type
    - body_part
    - severity
    - recovery_date
    - days_missed
    - description
    """
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="File must be CSV or Excel format")

    try:
        contents = await file.read()

        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))

        df.columns = df.columns.str.lower().str.strip()
        df['injury_date'] = pd.to_datetime(df['injury_date'])

        if 'recovery_date' in df.columns:
            df['recovery_date'] = pd.to_datetime(df['recovery_date'])

        created_count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                current_athlete_id = athlete_id
                if not current_athlete_id:
                    if 'athlete_id' in row:
                        current_athlete_id = int(row['athlete_id'])
                    elif 'athlete_name' in row:
                        athlete = db.query(models.Athlete).filter(
                            models.Athlete.name == row['athlete_name']
                        ).first()
                        if athlete:
                            current_athlete_id = athlete.id

                if not current_athlete_id:
                    errors.append(f"Row {idx + 1}: No athlete_id specified")
                    continue

                injury_data = {
                    'athlete_id': current_athlete_id,
                    'injury_date': row['injury_date'].date(),
                    'injury_type': row['injury_type'],
                    'body_part': row['body_part'],
                }

                # Optional fields
                if 'severity' in row and pd.notna(row['severity']):
                    injury_data['severity'] = str(row['severity'])
                if 'recovery_date' in row and pd.notna(row['recovery_date']):
                    injury_data['recovery_date'] = row['recovery_date'].date()
                if 'days_missed' in row and pd.notna(row['days_missed']):
                    injury_data['days_missed'] = int(row['days_missed'])
                if 'description' in row and pd.notna(row['description']):
                    injury_data['description'] = str(row['description'])

                db_injury = models.InjuryHistory(**injury_data)
                db.add(db_injury)
                created_count += 1

            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        db.commit()

        return {
            "message": f"Successfully imported {created_count} injury records",
            "created_count": created_count,
            "errors": errors[:10] if errors else []
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
