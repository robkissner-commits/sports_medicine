"""
Test Data Generator for Sports Medicine Injury Prevention System

Creates realistic test scenarios demonstrating:
1. Different risk levels (low, medium, high)
2. Training monotony and strain patterns
3. Recovery predictions for various injury types
4. Compound risk factors (sleep, stress, age, injury recency)

Usage:
    python -m backend.generate_test_data
"""

import sys
import os
from datetime import date, timedelta
import random
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import SessionLocal
from backend import models
from backend.analytics import AnalyticsEngine, calculate_training_load_from_kinexon


def clear_existing_data(db):
    """Clear all existing data from database"""
    print("Clearing existing data...")
    db.query(models.RiskAssessment).delete()
    db.query(models.LifestyleLog).delete()
    db.query(models.Treatment).delete()
    db.query(models.TrainingLoad).delete()
    db.query(models.InjuryHistory).delete()
    db.query(models.Athlete).delete()
    db.commit()
    print("✓ Data cleared")


def create_test_athletes(db):
    """Create diverse test athletes with different profiles"""
    athletes_data = [
        {
            "name": "Alex Thompson",
            "age": 23,
            "position": "Forward",
            "team": "Test Team A",
            "email": "alex.thompson@test.com",
            "scenario": "low_risk_optimal"
        },
        {
            "name": "Jordan Martinez",
            "age": 28,
            "position": "Midfielder",
            "team": "Test Team A",
            "email": "jordan.martinez@test.com",
            "scenario": "medium_risk_monotony"
        },
        {
            "name": "Sam Chen",
            "age": 32,
            "position": "Defender",
            "team": "Test Team B",
            "email": "sam.chen@test.com",
            "scenario": "high_risk_compound"
        },
        {
            "name": "Morgan Davis",
            "age": 35,
            "position": "Goalkeeper",
            "team": "Test Team B",
            "email": "morgan.davis@test.com",
            "scenario": "recent_injury"
        },
        {
            "name": "Casey Rodriguez",
            "age": 26,
            "position": "Forward",
            "team": "Test Team C",
            "email": "casey.rodriguez@test.com",
            "scenario": "load_spike"
        }
    ]

    athletes = []
    print("\nCreating test athletes...")
    for data in athletes_data:
        athlete = models.Athlete(
            name=data["name"],
            age=data["age"],
            position=data["position"],
            team=data["team"],
            email=data["email"]
        )
        db.add(athlete)
        db.flush()
        athletes.append((athlete, data["scenario"]))
        print(f"✓ Created: {athlete.name} ({data['scenario']})")

    db.commit()
    return athletes


def generate_training_loads(db, athlete, scenario, days=56):
    """Generate training load data based on scenario"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)

    print(f"\n  Generating training loads for {athlete.name}...")

    if scenario == "low_risk_optimal":
        # Optimal training: gradual progression, good variation
        base_load = 300
        loads = []
        for i in range(days):
            day_date = start_date + timedelta(days=i)
            # Gradual increase with variation
            week_num = i // 7
            progression = 1 + (week_num * 0.05)  # 5% per week
            variation = random.uniform(0.85, 1.15)  # ±15% daily variation
            load = base_load * progression * variation
            loads.append((day_date, load))

    elif scenario == "medium_risk_monotony":
        # High monotony: same load every day (dangerous)
        base_load = 350
        loads = []
        for i in range(days):
            day_date = start_date + timedelta(days=i)
            # Very little variation = high monotony
            load = base_load + random.uniform(-10, 10)
            loads.append((day_date, load))

    elif scenario == "high_risk_compound":
        # High ACWR: sudden spike in recent week
        loads = []
        for i in range(days):
            day_date = start_date + timedelta(days=i)
            if i < 49:  # First 7 weeks: low chronic load
                load = 250 + random.uniform(-30, 30)
            else:  # Last week: massive spike
                load = 550 + random.uniform(-50, 50)
            loads.append((day_date, load))

    elif scenario == "recent_injury":
        # Ramping back up after injury
        loads = []
        for i in range(days):
            day_date = start_date + timedelta(days=i)
            if i < 28:  # First 4 weeks: minimal load (recovering)
                load = 100 + random.uniform(-20, 20)
            else:  # Last 4 weeks: gradual return
                weeks_back = (i - 28) // 7
                load = 150 + (weeks_back * 50) + random.uniform(-25, 25)
            loads.append((day_date, load))

    elif scenario == "load_spike":
        # Z-score spike: unusual pattern
        base_load = 320
        loads = []
        for i in range(days):
            day_date = start_date + timedelta(days=i)
            if i == days - 3:  # Huge spike 3 days ago
                load = 700
            elif i >= days - 7:  # Recent high loads
                load = base_load * 1.4 + random.uniform(-40, 40)
            else:
                load = base_load + random.uniform(-50, 50)
            loads.append((day_date, load))

    # Create training load records with Kinexon metrics
    for day_date, target_load in loads:
        # Work backwards from desired load to generate realistic Kinexon metrics
        # Typical training session: 3-6 miles, significant acceleration load

        # Distance: typically 3-6 miles for field sports
        distance_miles = random.uniform(2.5, 6.5)

        # Accumulated Acceleration Load: typically 50-200 for training
        # Higher for intense sessions, lower for recovery
        intensity_factor = target_load / 350  # Normalize around 350 baseline
        accumulated_accel_load = max(30, min(250, 100 * intensity_factor + random.uniform(-20, 20)))

        # Average speed: typically 3-5 mph for field sports training
        average_speed_mph = random.uniform(3.0, 5.5)

        # Max speed: typically 12-18 mph for sprints
        max_speed_mph = random.uniform(12.0, 18.5)

        # Calculate actual training load from Kinexon metrics
        calculated_load = calculate_training_load_from_kinexon(
            distance_miles=distance_miles,
            accumulated_accel_load=accumulated_accel_load,
            average_speed_mph=average_speed_mph,
            max_speed_mph=max_speed_mph
        )

        training_load = models.TrainingLoad(
            athlete_id=athlete.id,
            date=day_date,
            distance_miles=distance_miles,
            accumulated_accel_load=accumulated_accel_load,
            average_speed_mph=average_speed_mph,
            max_speed_mph=max_speed_mph,
            training_load=calculated_load,
            session_type="Training"
        )
        db.add(training_load)

    print(f"  ✓ Generated {len(loads)} training sessions with Kinexon metrics")


def generate_lifestyle_data(db, athlete, scenario, days=14):
    """Generate lifestyle logs based on scenario"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)

    print(f"  Generating lifestyle data for {athlete.name}...")

    scenarios_config = {
        "low_risk_optimal": {
            "sleep_hours": (7.5, 8.5),
            "sleep_quality": (7, 9),
            "stress_level": (2, 4),
            "nutrition_score": (7, 9),
            "hydration_liters": (2.5, 3.5)
        },
        "medium_risk_monotony": {
            "sleep_hours": (6.5, 7.5),
            "sleep_quality": (6, 8),
            "stress_level": (4, 6),
            "nutrition_score": (6, 8),
            "hydration_liters": (2.0, 3.0)
        },
        "high_risk_compound": {
            "sleep_hours": (5.0, 6.0),  # Critical: <6 hrs
            "sleep_quality": (3, 5),
            "stress_level": (7, 9),  # High stress
            "nutrition_score": (4, 6),
            "hydration_liters": (1.5, 2.0)
        },
        "recent_injury": {
            "sleep_hours": (7.0, 8.0),
            "sleep_quality": (6, 8),
            "stress_level": (5, 7),  # Moderate stress
            "nutrition_score": (7, 9),
            "hydration_liters": (2.5, 3.0)
        },
        "load_spike": {
            "sleep_hours": (6.0, 7.0),
            "sleep_quality": (5, 7),
            "stress_level": (5, 7),
            "nutrition_score": (6, 8),
            "hydration_liters": (2.0, 2.5)
        }
    }

    config = scenarios_config.get(scenario, scenarios_config["low_risk_optimal"])

    for i in range(days):
        day_date = start_date + timedelta(days=i)
        lifestyle = models.LifestyleLog(
            athlete_id=athlete.id,
            date=day_date,
            sleep_hours=random.uniform(*config["sleep_hours"]),
            sleep_quality=random.randint(*config["sleep_quality"]),
            nutrition_score=random.randint(*config["nutrition_score"]),
            hydration_liters=random.uniform(*config["hydration_liters"]),
            stress_level=random.randint(*config["stress_level"]),
            soreness_level=random.randint(3, 7),
            fatigue_level=random.randint(3, 7)
        )
        db.add(lifestyle)

    print(f"  ✓ Generated {days} lifestyle logs")


def generate_injuries(db, athlete, scenario):
    """Generate injury history based on scenario"""
    print(f"  Generating injuries for {athlete.name}...")

    if scenario == "recent_injury":
        # Recent hamstring strain
        injury = models.InjuryHistory(
            athlete_id=athlete.id,
            injury_date=date.today() - timedelta(days=35),
            injury_type="Muscle Strain Grade 2",
            body_part="Hamstring",
            severity="moderate",
            recovery_date=date.today() - timedelta(days=14),
            days_missed=21,
            description="Grade 2 hamstring strain during sprint training"
        )
        db.add(injury)
        print("  ✓ Added recent hamstring injury")

    elif scenario == "high_risk_compound":
        # Old injury + recent minor injury
        old_injury = models.InjuryHistory(
            athlete_id=athlete.id,
            injury_date=date.today() - timedelta(days=180),
            injury_type="Ligament Sprain Grade 2",
            body_part="Ankle",
            severity="moderate",
            recovery_date=date.today() - timedelta(days=145),
            days_missed=35,
            description="Ankle sprain from contact"
        )
        db.add(old_injury)

        recent_injury = models.InjuryHistory(
            athlete_id=athlete.id,
            injury_date=date.today() - timedelta(days=12),
            injury_type="Muscle Strain Grade 1",
            body_part="Calf",
            severity="mild",
            description="Minor calf strain, still training with modifications"
        )
        db.add(recent_injury)
        print("  ✓ Added multiple injuries")

    elif scenario == "load_spike":
        # Previous similar injury
        injury = models.InjuryHistory(
            athlete_id=athlete.id,
            injury_date=date.today() - timedelta(days=90),
            injury_type="Tendinopathy",
            body_part="Achilles",
            severity="moderate",
            recovery_date=date.today() - timedelta(days=30),
            days_missed=60,
            description="Achilles tendinopathy from overuse"
        )
        db.add(injury)
        print("  ✓ Added previous tendinopathy")

    else:
        # Low risk: old minor injury
        if random.random() > 0.5:
            injury = models.InjuryHistory(
                athlete_id=athlete.id,
                injury_date=date.today() - timedelta(days=200),
                injury_type="Contusion",
                body_part="Thigh",
                severity="minor",
                recovery_date=date.today() - timedelta(days=193),
                days_missed=7,
                description="Minor contusion from contact"
            )
            db.add(injury)
            print("  ✓ Added minor old injury")


def generate_treatments(db, athlete, scenario, days=21):
    """Generate treatment records based on scenario"""
    print(f"  Generating treatments for {athlete.name}...")

    treatment_count = 0

    if scenario in ["recent_injury", "high_risk_compound"]:
        # More frequent treatments
        treatment_frequency = 0.4  # 40% of days
        modalities = ["Physiotherapy", "Massage", "Ice Bath", "Compression", "Stretching"]
    else:
        # Normal recovery treatments
        treatment_frequency = 0.2  # 20% of days
        modalities = ["Massage", "Ice Bath", "Foam Rolling"]

    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)

    for i in range(days):
        if random.random() < treatment_frequency:
            day_date = start_date + timedelta(days=i)
            treatment = models.Treatment(
                athlete_id=athlete.id,
                date=day_date,
                modality=random.choice(modalities),
                duration=random.randint(20, 60),
                body_part=random.choice(["Legs", "Back", "General"]),
                notes="Regular recovery session"
            )
            db.add(treatment)
            treatment_count += 1

    print(f"  ✓ Generated {treatment_count} treatments")


def calculate_risks(db, athletes):
    """Calculate risk assessments for all athletes"""
    print("\n=== Calculating Risk Assessments ===")

    for athlete, scenario in athletes:
        print(f"\nCalculating risk for {athlete.name}...")
        try:
            risk_data = AnalyticsEngine.calculate_overall_risk(
                db=db,
                athlete_id=athlete.id,
                target_date=date.today()
            )

            # Create risk assessment record
            risk_assessment = models.RiskAssessment(
                athlete_id=athlete.id,
                date=date.today(),
                **risk_data
            )
            db.add(risk_assessment)
            db.commit()

            print(f"  ✓ Risk Level: {risk_data['risk_level'].upper()}")
            print(f"  ✓ Risk Score: {risk_data['overall_risk_score']:.1f}")
            if risk_data.get("training_monotony"):
                print(f"  ✓ Monotony: {risk_data['training_monotony']:.2f}")
            if risk_data.get("compound_multiplier"):
                print(f"  ✓ Compound Multiplier: {risk_data['compound_multiplier']:.2f}×")

        except Exception as e:
            print(f"  ✗ Error calculating risk: {e}")

    db.commit()


def print_summary(db, athletes):
    """Print summary of generated data"""
    print("\n" + "="*60)
    print("TEST DATA GENERATION COMPLETE")
    print("="*60)

    print(f"\nTotal Athletes: {len(athletes)}")

    for athlete, scenario in athletes:
        # Get latest risk assessment
        latest_risk = db.query(models.RiskAssessment).filter(
            models.RiskAssessment.athlete_id == athlete.id
        ).order_by(models.RiskAssessment.date.desc()).first()

        print(f"\n{athlete.name} ({scenario}):")
        print(f"  Age: {athlete.age}")
        print(f"  Risk Level: {latest_risk.risk_level.upper() if latest_risk else 'Not Calculated'}")
        print(f"  Risk Score: {latest_risk.overall_risk_score:.1f if latest_risk else 'N/A'}")
        print(f"  ACWR: {latest_risk.acwr:.2f if latest_risk and latest_risk.acwr else 'N/A'}")

        training_count = db.query(models.TrainingLoad).filter(
            models.TrainingLoad.athlete_id == athlete.id
        ).count()
        injury_count = db.query(models.InjuryHistory).filter(
            models.InjuryHistory.athlete_id == athlete.id
        ).count()
        treatment_count = db.query(models.Treatment).filter(
            models.Treatment.athlete_id == athlete.id
        ).count()

        print(f"  Training Sessions: {training_count}")
        print(f"  Injuries: {injury_count}")
        print(f"  Treatments: {treatment_count}")

    print("\n" + "="*60)
    print("Access the system at: http://localhost:5173")
    print("="*60)


def main():
    """Main function to generate all test data"""
    print("\n" + "="*60)
    print("SPORTS MEDICINE TEST DATA GENERATOR")
    print("="*60)

    db = SessionLocal()

    try:
        # Step 1: Clear existing data
        clear_existing_data(db)

        # Step 2: Create test athletes
        athletes = create_test_athletes(db)

        # Step 3: Generate data for each athlete
        for athlete, scenario in athletes:
            print(f"\n--- Generating data for {athlete.name} ({scenario}) ---")
            generate_training_loads(db, athlete, scenario, days=56)
            generate_lifestyle_data(db, athlete, scenario, days=14)
            generate_injuries(db, athlete, scenario)
            generate_treatments(db, athlete, scenario, days=21)

        db.commit()

        # Step 4: Calculate risks
        calculate_risks(db, athletes)

        # Step 5: Print summary
        print_summary(db, athletes)

        print("\n✅ Test data generation successful!")

    except Exception as e:
        print(f"\n❌ Error during data generation: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
