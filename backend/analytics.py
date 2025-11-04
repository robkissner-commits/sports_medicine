from datetime import date, timedelta
from typing import List, Tuple, Optional, Dict
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models


def calculate_training_load_from_kinexon(
    distance_miles: float,
    accumulated_accel_load: float,
    average_speed_mph: Optional[float] = None,
    max_speed_mph: Optional[float] = None
) -> float:
    """
    Calculate training load from Kinexon metrics

    Formula balances:
    - Distance (primary workload indicator)
    - Acceleration load (intensity/explosive work)
    - Average speed (overall intensity)
    - Max speed (peak effort indicator)

    Args:
        distance_miles: Distance covered in miles
        accumulated_accel_load: Total acceleration load
        average_speed_mph: Average speed in mph (optional)
        max_speed_mph: Maximum speed in mph (optional)

    Returns:
        Calculated training load value
    """
    # Base load from distance (160 points per mile)
    # Example: 5 miles = 800 base load
    base_load = distance_miles * 160

    # Acceleration load component (1.5x multiplier)
    # Reflects high-intensity accelerations and decelerations
    accel_component = accumulated_accel_load * 1.5

    # Average speed component (5x multiplier)
    # Higher average speed = higher intensity
    speed_component = (average_speed_mph * 5) if average_speed_mph else 0

    # Max speed bonus (2x multiplier)
    # Peak speed efforts add to load
    max_speed_component = (max_speed_mph * 2) if max_speed_mph else 0

    # Total training load
    training_load = base_load + accel_component + speed_component + max_speed_component

    return round(training_load, 2)


class AnalyticsEngine:
    """
    Enhanced analytics engine with Hybrid Evidence-Based System

    Implements:
    - Traditional ACWR (Acute:Chronic Workload Ratio)
    - Training Monotony (Foster et al., 1998)
    - Training Strain (cumulative load × monotony)
    - Rolling Z-scores for spike detection
    - Compound risk scoring with evidence-based modifiers
    - Cox-based recovery time prediction
    """

    # Risk thresholds (evidence-based)
    ACWR_HIGH_RISK_UPPER = 1.5  # Gabbett, 2016
    ACWR_HIGH_RISK_LOWER = 0.8  # Gabbett, 2016
    ACWR_OPTIMAL = 1.0
    MONOTONY_HIGH_RISK = 2.0  # Foster, 1998
    HIGH_RISK_THRESHOLD = 70
    MEDIUM_RISK_THRESHOLD = 40

    @staticmethod
    def calculate_acwr(
        db: Session,
        athlete_id: int,
        target_date: date,
        acute_window: int = 7,
        chronic_window: int = 28
    ) -> Optional[Tuple[float, float, float]]:
        """
        Calculate Acute:Chronic Workload Ratio
        Returns: (acute_load, chronic_load, acwr) or None
        """
        # Get training loads for the chronic window
        start_date = target_date - timedelta(days=chronic_window - 1)

        loads = db.query(models.TrainingLoad).filter(
            and_(
                models.TrainingLoad.athlete_id == athlete_id,
                models.TrainingLoad.date >= start_date,
                models.TrainingLoad.date <= target_date
            )
        ).order_by(models.TrainingLoad.date).all()

        if len(loads) < acute_window:
            return None

        # Extract training load values
        load_values = [load.training_load for load in loads]

        # Calculate acute load (last 7 days average)
        acute_loads = load_values[-acute_window:]
        acute_load = np.mean(acute_loads) if acute_loads else 0

        # Calculate chronic load (28 days rolling average)
        chronic_load = np.mean(load_values) if load_values else 0

        # Calculate ACWR
        if chronic_load > 0:
            acwr = acute_load / chronic_load
        else:
            acwr = 0

        return acute_load, chronic_load, acwr

    @staticmethod
    def calculate_load_spike_score(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 14
    ) -> float:
        """
        Calculate score based on sudden spikes in training load
        Returns: Score from 0-100 (higher = more risk)
        """
        start_date = target_date - timedelta(days=lookback_days)

        loads = db.query(models.TrainingLoad).filter(
            and_(
                models.TrainingLoad.athlete_id == athlete_id,
                models.TrainingLoad.date >= start_date,
                models.TrainingLoad.date <= target_date
            )
        ).order_by(models.TrainingLoad.date).all()

        if len(loads) < 3:
            return 0

        load_values = [load.training_load for load in loads]

        # Calculate day-to-day percentage changes
        changes = []
        for i in range(1, len(load_values)):
            if load_values[i - 1] > 0:
                change = ((load_values[i] - load_values[i - 1]) / load_values[i - 1]) * 100
                changes.append(abs(change))

        if not changes:
            return 0

        # Score based on magnitude and frequency of large spikes
        avg_change = np.mean(changes)
        max_change = max(changes)
        spike_count = sum(1 for c in changes if c > 30)  # Count spikes > 30%

        score = min(100, (avg_change * 2) + (max_change * 0.5) + (spike_count * 10))
        return score

    @staticmethod
    def calculate_recovery_score(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 14
    ) -> float:
        """
        Calculate recovery score based on treatment frequency
        Returns: Score from 0-100 (higher = better recovery)
        """
        start_date = target_date - timedelta(days=lookback_days)

        treatments = db.query(models.Treatment).filter(
            and_(
                models.Treatment.athlete_id == athlete_id,
                models.Treatment.date >= start_date,
                models.Treatment.date <= target_date
            )
        ).all()

        # Ideal treatment frequency: 2-4 times per week
        treatment_count = len(treatments)
        weeks = lookback_days / 7
        treatments_per_week = treatment_count / weeks

        # Score based on optimal frequency
        if 2 <= treatments_per_week <= 4:
            frequency_score = 100
        elif treatments_per_week < 2:
            frequency_score = min(100, treatments_per_week * 50)
        else:
            frequency_score = max(0, 100 - ((treatments_per_week - 4) * 10))

        # Penalize for severe treatments (indicates injury)
        severe_count = sum(1 for t in treatments if t.severity in ["severe", "moderate"])
        severity_penalty = min(40, severe_count * 10)

        final_score = max(0, frequency_score - severity_penalty)
        return final_score

    @staticmethod
    def calculate_lifestyle_score(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 7
    ) -> float:
        """
        Calculate lifestyle score based on sleep, nutrition, stress
        Returns: Score from 0-100 (higher = better lifestyle habits)
        """
        start_date = target_date - timedelta(days=lookback_days)

        logs = db.query(models.LifestyleLog).filter(
            and_(
                models.LifestyleLog.athlete_id == athlete_id,
                models.LifestyleLog.date >= start_date,
                models.LifestyleLog.date <= target_date
            )
        ).all()

        if not logs:
            return 50  # Neutral score if no data

        scores = []

        for log in logs:
            log_score = 0
            factors = 0

            # Sleep (7-9 hours optimal)
            if log.sleep_hours:
                if 7 <= log.sleep_hours <= 9:
                    log_score += 25
                elif 6 <= log.sleep_hours <= 10:
                    log_score += 15
                else:
                    log_score += 5
                factors += 1

            # Sleep quality (1-10 scale)
            if log.sleep_quality:
                log_score += (log.sleep_quality * 2.5)
                factors += 1

            # Nutrition (1-10 scale)
            if log.nutrition_score:
                log_score += (log.nutrition_score * 2.5)
                factors += 1

            # Stress (inverted - lower is better, 1-10 scale)
            if log.stress_level:
                log_score += ((10 - log.stress_level + 1) * 2.5)
                factors += 1

            if factors > 0:
                scores.append(log_score)

        return np.mean(scores) if scores else 50

    @staticmethod
    def calculate_injury_history_score(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 180
    ) -> float:
        """
        Calculate risk score based on injury history
        Returns: Score from 0-100 (higher = more injury risk)
        """
        start_date = target_date - timedelta(days=lookback_days)

        injuries = db.query(models.InjuryHistory).filter(
            and_(
                models.InjuryHistory.athlete_id == athlete_id,
                models.InjuryHistory.injury_date >= start_date,
                models.InjuryHistory.injury_date <= target_date
            )
        ).all()

        if not injuries:
            return 0

        # Weight recent injuries more heavily
        score = 0
        for injury in injuries:
            days_ago = (target_date - injury.injury_date).days
            recency_factor = max(0.3, 1 - (days_ago / lookback_days))

            # Severity multiplier
            severity_multiplier = {
                "minor": 1,
                "moderate": 2,
                "severe": 3,
                "catastrophic": 4
            }.get(injury.severity, 1)

            injury_score = 20 * recency_factor * severity_multiplier
            score += injury_score

        return min(100, score)

    @staticmethod
    def calculate_training_monotony(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 7
    ) -> Optional[float]:
        """
        Calculate Training Monotony (Foster et al., 1998)
        Monotony = Average Load / Standard Deviation of Load

        High monotony (>2.0) indicates repetitive training without variation,
        which increases injury risk.

        Returns: Monotony score or None if insufficient data
        """
        start_date = target_date - timedelta(days=lookback_days - 1)

        loads = db.query(models.TrainingLoad).filter(
            and_(
                models.TrainingLoad.athlete_id == athlete_id,
                models.TrainingLoad.date >= start_date,
                models.TrainingLoad.date <= target_date
            )
        ).order_by(models.TrainingLoad.date).all()

        if len(loads) < 3:
            return None

        load_values = [load.training_load for load in loads]
        mean_load = np.mean(load_values)
        std_load = np.std(load_values)

        if std_load == 0:
            # No variation = very high monotony
            return 10.0

        monotony = mean_load / std_load
        return round(monotony, 2)

    @staticmethod
    def calculate_training_strain(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 7
    ) -> Optional[float]:
        """
        Calculate Training Strain (Foster et al., 1998)
        Strain = Total Weekly Load × Monotony

        Combines volume and monotony to detect dangerous training patterns.
        High strain indicates both high load AND lack of variation.

        Returns: Strain score or None if insufficient data
        """
        start_date = target_date - timedelta(days=lookback_days - 1)

        loads = db.query(models.TrainingLoad).filter(
            and_(
                models.TrainingLoad.athlete_id == athlete_id,
                models.TrainingLoad.date >= start_date,
                models.TrainingLoad.date <= target_date
            )
        ).all()

        if len(loads) < 3:
            return None

        load_values = [load.training_load for load in loads]
        total_load = sum(load_values)

        # Get monotony
        mean_load = np.mean(load_values)
        std_load = np.std(load_values)

        if std_load == 0:
            monotony = 10.0
        else:
            monotony = mean_load / std_load

        strain = total_load * monotony
        return round(strain, 2)

    @staticmethod
    def calculate_z_score_spike(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 28
    ) -> Dict[str, float]:
        """
        Calculate Z-score for recent loads compared to athlete's baseline

        Detects unusual spikes relative to the athlete's normal training pattern.
        Z-score > 2.0 indicates load is 2+ standard deviations above normal.

        Returns: dict with current_z_score and max_z_score_7d
        """
        start_date = target_date - timedelta(days=lookback_days - 1)

        loads = db.query(models.TrainingLoad).filter(
            and_(
                models.TrainingLoad.athlete_id == athlete_id,
                models.TrainingLoad.date >= start_date,
                models.TrainingLoad.date <= target_date
            )
        ).order_by(models.TrainingLoad.date).all()

        if len(loads) < 7:
            return {"current_z_score": 0, "max_z_score_7d": 0}

        load_values = [load.training_load for load in loads]

        # Calculate baseline (first 21 days)
        baseline_loads = load_values[:-7] if len(load_values) > 21 else load_values[:int(len(load_values) * 0.75)]
        if len(baseline_loads) < 3:
            baseline_loads = load_values

        baseline_mean = np.mean(baseline_loads)
        baseline_std = np.std(baseline_loads)

        if baseline_std == 0:
            return {"current_z_score": 0, "max_z_score_7d": 0}

        # Calculate z-scores for last 7 days
        recent_loads = load_values[-7:]
        z_scores = [(load - baseline_mean) / baseline_std for load in recent_loads]

        current_z_score = z_scores[-1] if z_scores else 0
        max_z_score_7d = max(z_scores) if z_scores else 0

        return {
            "current_z_score": round(current_z_score, 2),
            "max_z_score_7d": round(max_z_score_7d, 2)
        }

    @staticmethod
    def calculate_sleep_modifier(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 7
    ) -> float:
        """
        Calculate sleep risk modifier (evidence-based)

        Research shows sleep <6hrs increases injury risk by 30-50%
        Returns: Multiplier (1.0 = no change, >1.0 = increased risk)
        """
        start_date = target_date - timedelta(days=lookback_days - 1)

        logs = db.query(models.LifestyleLog).filter(
            and_(
                models.LifestyleLog.athlete_id == athlete_id,
                models.LifestyleLog.date >= start_date,
                models.LifestyleLog.date <= target_date
            )
        ).all()

        if not logs:
            return 1.0  # No data = no modifier

        sleep_hours = [log.sleep_hours for log in logs if log.sleep_hours]
        if not sleep_hours:
            return 1.0

        avg_sleep = np.mean(sleep_hours)

        # Evidence-based sleep thresholds
        if avg_sleep < 6:
            return 1.4  # 40% increased risk
        elif avg_sleep < 7:
            return 1.2  # 20% increased risk
        elif 7 <= avg_sleep <= 9:
            return 1.0  # Optimal
        else:
            return 1.1  # Slight increase (oversleeping can indicate illness)

    @staticmethod
    def calculate_stress_modifier(
        db: Session,
        athlete_id: int,
        target_date: date,
        lookback_days: int = 7
    ) -> float:
        """
        Calculate stress risk modifier

        High stress increases injury risk by reducing recovery capacity
        Returns: Multiplier (1.0 = no change, >1.0 = increased risk)
        """
        start_date = target_date - timedelta(days=lookback_days - 1)

        logs = db.query(models.LifestyleLog).filter(
            and_(
                models.LifestyleLog.athlete_id == athlete_id,
                models.LifestyleLog.date >= start_date,
                models.LifestyleLog.date <= target_date
            )
        ).all()

        if not logs:
            return 1.0

        stress_levels = [log.stress_level for log in logs if log.stress_level]
        if not stress_levels:
            return 1.0

        avg_stress = np.mean(stress_levels)

        # Stress scale: 1-10 (higher = worse)
        if avg_stress >= 8:
            return 1.3  # Very high stress
        elif avg_stress >= 6:
            return 1.15  # Moderate stress
        else:
            return 1.0  # Low stress

    @staticmethod
    def calculate_injury_recency_modifier(
        db: Session,
        athlete_id: int,
        target_date: date
    ) -> float:
        """
        Calculate injury recency modifier

        Recent injuries (<30 days) dramatically increase re-injury risk
        Returns: Multiplier (1.0 = no recent injury, >1.0 = increased risk)
        """
        # Check for injuries in last 90 days
        start_date = target_date - timedelta(days=90)

        injuries = db.query(models.InjuryHistory).filter(
            and_(
                models.InjuryHistory.athlete_id == athlete_id,
                models.InjuryHistory.injury_date >= start_date,
                models.InjuryHistory.injury_date <= target_date
            )
        ).order_by(models.InjuryHistory.injury_date.desc()).all()

        if not injuries:
            return 1.0

        most_recent = injuries[0]
        days_since = (target_date - most_recent.injury_date).days

        # Time-based modifiers
        if days_since < 14:
            return 1.8  # Very recent injury
        elif days_since < 30:
            return 1.5  # Recent injury
        elif days_since < 60:
            return 1.25  # Moderately recent
        else:
            return 1.1  # Past injury

    @staticmethod
    def calculate_age_modifier(athlete_age: Optional[int]) -> float:
        """
        Calculate age risk modifier

        Older athletes have slower recovery and higher injury risk
        Returns: Multiplier (1.0 = young, >1.0 = increased risk)
        """
        if not athlete_age:
            return 1.0

        if athlete_age < 25:
            return 1.0  # Peak recovery
        elif athlete_age < 30:
            return 1.1  # Slight increase
        elif athlete_age < 35:
            return 1.2  # Moderate increase
        else:
            return 1.3  # Higher risk

    @classmethod
    def calculate_overall_risk(
        cls,
        db: Session,
        athlete_id: int,
        target_date: date
    ) -> dict:
        """
        ENHANCED: Calculate overall risk using Hybrid Evidence-Based System

        Implements:
        1. Traditional risk scoring (ACWR, spikes, recovery, lifestyle, injury history)
        2. Training monotony and strain (Foster, 1998)
        3. Z-score spike detection
        4. Compound risk modifiers (sleep, stress, injury recency, age)

        Returns: dict with comprehensive risk metrics and recommendations
        """
        # Get athlete info for age modifier
        athlete = db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()
        athlete_age = athlete.age if athlete else None

        # ========== PART 1: Traditional Metrics ==========

        # Calculate ACWR
        acwr_result = cls.calculate_acwr(db, athlete_id, target_date)
        if acwr_result:
            acute_load, chronic_load, acwr = acwr_result
        else:
            acute_load = chronic_load = acwr = None

        # Calculate component scores
        load_spike_score = cls.calculate_load_spike_score(db, athlete_id, target_date)
        recovery_score = cls.calculate_recovery_score(db, athlete_id, target_date)
        lifestyle_score = cls.calculate_lifestyle_score(db, athlete_id, target_date)
        injury_history_score = cls.calculate_injury_history_score(db, athlete_id, target_date)

        # ========== PART 2: NEW Enhanced Metrics ==========

        # Training monotony and strain
        monotony = cls.calculate_training_monotony(db, athlete_id, target_date, lookback_days=7)
        strain = cls.calculate_training_strain(db, athlete_id, target_date, lookback_days=7)

        # Z-score spike detection
        z_scores = cls.calculate_z_score_spike(db, athlete_id, target_date)
        current_z = z_scores["current_z_score"]
        max_z_7d = z_scores["max_z_score_7d"]

        # ========== PART 3: Base Risk Scoring ==========

        # ACWR risk component
        acwr_risk = 0
        if acwr:
            if acwr > cls.ACWR_HIGH_RISK_UPPER or acwr < cls.ACWR_HIGH_RISK_LOWER:
                acwr_risk = 80
            elif acwr > 1.3 or acwr < 0.9:
                acwr_risk = 50
            else:
                acwr_risk = 20

        # Monotony risk component (NEW)
        monotony_risk = 0
        if monotony:
            if monotony > cls.MONOTONY_HIGH_RISK:
                monotony_risk = 60  # High risk from repetitive training
            elif monotony > 1.5:
                monotony_risk = 30
            else:
                monotony_risk = 10

        # Z-score risk component (NEW)
        z_score_risk = 0
        if max_z_7d > 2.5:
            z_score_risk = 70  # Extreme spike
        elif max_z_7d > 2.0:
            z_score_risk = 50  # Significant spike
        elif max_z_7d > 1.5:
            z_score_risk = 25  # Moderate spike
        else:
            z_score_risk = 10

        # Base risk score (before modifiers)
        base_risk = (
            acwr_risk * 0.25 +
            monotony_risk * 0.15 +
            z_score_risk * 0.15 +
            load_spike_score * 0.15 +
            (100 - recovery_score) * 0.15 +
            (100 - lifestyle_score) * 0.10 +
            injury_history_score * 0.05
        )

        # ========== PART 4: Compound Risk Modifiers ==========

        sleep_mod = cls.calculate_sleep_modifier(db, athlete_id, target_date)
        stress_mod = cls.calculate_stress_modifier(db, athlete_id, target_date)
        injury_recency_mod = cls.calculate_injury_recency_modifier(db, athlete_id, target_date)
        age_mod = cls.calculate_age_modifier(athlete_age)

        # Compound risk = base risk × all modifiers
        # This is the KEY innovation: modifiers multiply when risk factors combine
        overall_risk = base_risk * sleep_mod * stress_mod * injury_recency_mod * age_mod

        # Cap at 100
        overall_risk = min(100, overall_risk)

        # ========== PART 5: Risk Level Classification ==========

        if overall_risk >= cls.HIGH_RISK_THRESHOLD:
            risk_level = "high"
        elif overall_risk >= cls.MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
        else:
            risk_level = "low"

        # ========== PART 6: Generate Enhanced Recommendations ==========

        recommendations = cls.generate_enhanced_recommendations(
            acwr, monotony, strain, current_z, max_z_7d,
            load_spike_score, recovery_score, lifestyle_score,
            injury_history_score, sleep_mod, stress_mod,
            injury_recency_mod, age_mod, risk_level
        )

        # ========== PART 7: Return Comprehensive Metrics ==========

        return {
            # Overall
            "overall_risk_score": round(overall_risk, 2),
            "risk_level": risk_level,

            # Traditional metrics
            "acwr": round(acwr, 2) if acwr else None,
            "acute_load": round(acute_load, 2) if acute_load else None,
            "chronic_load": round(chronic_load, 2) if chronic_load else None,
            "load_spike_score": round(load_spike_score, 2),
            "recovery_score": round(recovery_score, 2),
            "lifestyle_score": round(lifestyle_score, 2),
            "injury_history_score": round(injury_history_score, 2),

            # NEW: Enhanced metrics
            "training_monotony": round(monotony, 2) if monotony else None,
            "training_strain": round(strain, 2) if strain else None,
            "current_z_score": round(current_z, 2),
            "max_z_score_7d": round(max_z_7d, 2),

            # NEW: Risk modifiers (for transparency)
            "sleep_modifier": round(sleep_mod, 2),
            "stress_modifier": round(stress_mod, 2),
            "injury_recency_modifier": round(injury_recency_mod, 2),
            "age_modifier": round(age_mod, 2),
            "compound_multiplier": round(sleep_mod * stress_mod * injury_recency_mod * age_mod, 2),

            # Recommendations
            "recommendations": recommendations
        }

    @staticmethod
    def generate_enhanced_recommendations(
        acwr: Optional[float],
        monotony: Optional[float],
        strain: Optional[float],
        current_z: float,
        max_z_7d: float,
        load_spike_score: float,
        recovery_score: float,
        lifestyle_score: float,
        injury_history_score: float,
        sleep_mod: float,
        stress_mod: float,
        injury_recency_mod: float,
        age_mod: float,
        risk_level: str
    ) -> str:
        """Generate enhanced evidence-based intervention recommendations"""
        recommendations = []

        # ========== COMPOUND RISK ALERTS (NEW) ==========
        compound_multiplier = sleep_mod * stress_mod * injury_recency_mod * age_mod

        if compound_multiplier > 2.0:
            recommendations.append(
                "🚨 COMPOUND RISK ALERT: Multiple risk factors are combining (multiplier: {:.2f}×). "
                "This athlete requires immediate attention and likely needs reduced training volume.".format(compound_multiplier)
            )

        # ========== TRAINING MONOTONY & STRAIN (NEW) ==========
        if monotony and monotony > 2.0:
            recommendations.append(
                "⚠️ HIGH TRAINING MONOTONY ({:.2f}): Training is too repetitive. "
                "Add variety: alternate high/low intensity days, change session types, include cross-training.".format(monotony)
            )
        elif monotony and monotony > 1.5:
            recommendations.append(
                "📊 ELEVATED MONOTONY ({:.2f}): Consider adding more training variation to prevent overuse injuries.".format(monotony)
            )

        if strain and strain > 3000:
            recommendations.append(
                "🔴 EXTREME TRAINING STRAIN ({:.0f}): Combination of high volume and monotony is dangerous. "
                "Immediate load reduction and variation required.".format(strain)
            )

        # ========== Z-SCORE SPIKES (NEW) ==========
        if max_z_7d > 2.5:
            recommendations.append(
                "📈 EXTREME LOAD SPIKE (Z-score: {:.2f}): Recent training >2.5 std deviations above baseline. "
                "This is a major injury risk factor. Reduce to normal levels immediately.".format(max_z_7d)
            )
        elif max_z_7d > 2.0:
            recommendations.append(
                "📊 SIGNIFICANT LOAD SPIKE (Z-score: {:.2f}): Training spike detected. "
                "Return to more typical training loads this week.".format(max_z_7d)
            )

        # ========== ACWR RECOMMENDATIONS ==========
        if acwr:
            if acwr > 1.5:
                recommendations.append(
                    "⚠️ ACWR VERY HIGH ({:.2f}): Acute load significantly exceeds chronic load. "
                    "Reduce volume by 20-30% this week (Gabbett, 2016).".format(acwr)
                )
            elif acwr < 0.8:
                recommendations.append(
                    "⚠️ ACWR VERY LOW ({:.2f}): Risk of detraining and sudden spike vulnerability. "
                    "Gradually increase load by 10% per week.".format(acwr)
                )
            elif acwr > 1.3:
                recommendations.append(
                    "⚡ ACWR ELEVATED ({:.2f}): Monitor closely. Consider 10-15% volume reduction.".format(acwr)
                )
            elif 0.8 <= acwr <= 1.3:
                recommendations.append(
                    "✅ ACWR OPTIMAL ({:.2f}): Training load ratio is in safe zone.".format(acwr)
                )

        # ========== SLEEP MODIFIER ALERTS (NEW) ==========
        if sleep_mod >= 1.4:
            recommendations.append(
                "😴 CRITICAL SLEEP DEFICIT: Sleep <6 hrs increases injury risk by 40%. "
                "Prioritize 8+ hours sleep. Consider adjusting training schedule."
            )
        elif sleep_mod >= 1.2:
            recommendations.append(
                "💤 POOR SLEEP: Sleep <7 hrs detected. Target 7-9 hours for optimal recovery."
            )

        # ========== STRESS MODIFIER ALERTS (NEW) ==========
        if stress_mod >= 1.3:
            recommendations.append(
                "🧠 HIGH STRESS LOAD: Elevated stress impairs recovery and increases injury risk. "
                "Consider stress management techniques, reduced training volume, or mental skills coaching."
            )
        elif stress_mod >= 1.15:
            recommendations.append(
                "😓 MODERATE STRESS: Monitor stress levels and recovery. May need volume adjustments."
            )

        # ========== INJURY RECENCY ALERTS (NEW) ==========
        if injury_recency_mod >= 1.8:
            recommendations.append(
                "🏥 VERY RECENT INJURY (<14 days): Re-injury risk is EXTREMELY HIGH. "
                "Ensure full clearance from medical staff. Gradual return-to-play protocol essential."
            )
        elif injury_recency_mod >= 1.5:
            recommendations.append(
                "⚕️ RECENT INJURY (<30 days): Elevated re-injury risk. "
                "Maintain modified training and preventive strengthening program."
            )

        # ========== AGE MODIFIER ALERTS (NEW) ==========
        if age_mod >= 1.3:
            recommendations.append(
                "👴 AGE CONSIDERATION (35+ years): Older athletes need more recovery time. "
                "Ensure adequate rest days and recovery modalities."
            )

        # ========== RECOVERY RECOMMENDATIONS ==========
        if recovery_score < 40:
            recommendations.append(
                "🔧 LOW RECOVERY SCORE: Increase recovery modalities: massage, ice baths, compression, sleep optimization."
            )
        elif recovery_score < 60:
            recommendations.append(
                "💆 MODERATE RECOVERY NEEDED: Add 1-2 recovery sessions this week."
            )

        # ========== LIFESTYLE RECOMMENDATIONS ==========
        if lifestyle_score < 50:
            recommendations.append(
                "🌟 POOR LIFESTYLE METRICS: Focus on: 8+ hrs sleep, balanced nutrition, hydration (2-3L/day), stress management."
            )

        # ========== OVERALL RISK SUMMARY ==========
        if risk_level == "high":
            recommendations.insert(0,
                "🚨 HIGH RISK ALERT: Multiple risk factors detected. "
                "IMMEDIATE INTERVENTION REQUIRED: Rest day, active recovery only, or significant load reduction."
            )
        elif risk_level == "medium":
            recommendations.insert(0,
                "⚠️ MODERATE RISK: Athlete showing concerning patterns. "
                "Monitor closely and modify training intensity/volume as needed."
            )

        if not recommendations:
            recommendations.append(
                "✅ EXCELLENT: Athlete showing good balance across all metrics. "
                "Continue current training plan with regular monitoring."
            )

        return "\n\n".join(recommendations)

    @staticmethod
    def generate_recommendations(
        acwr: Optional[float],
        load_spike_score: float,
        recovery_score: float,
        lifestyle_score: float,
        injury_history_score: float,
        risk_level: str
    ) -> str:
        """Generate specific intervention recommendations"""
        recommendations = []

        # ACWR recommendations
        if acwr:
            if acwr > 1.5:
                recommendations.append(
                    "⚠️ ACWR is very high (>1.5). Reduce training volume by 20-30% this week."
                )
            elif acwr < 0.8:
                recommendations.append(
                    "⚠️ ACWR is very low (<0.8). Athlete may be detraining. Gradually increase load."
                )
            elif acwr > 1.3:
                recommendations.append(
                    "⚡ ACWR elevated (>1.3). Monitor closely and consider 10-15% volume reduction."
                )

        # Load spike recommendations
        if load_spike_score > 60:
            recommendations.append(
                "📊 Large training load fluctuations detected. Implement more gradual load progression."
            )

        # Recovery recommendations
        if recovery_score < 40:
            recommendations.append(
                "🔧 Low recovery score. Increase recovery modalities: massage, ice baths, sleep optimization."
            )
        elif recovery_score < 60:
            recommendations.append(
                "💆 Moderate recovery needed. Add 1-2 additional recovery sessions this week."
            )

        # Lifestyle recommendations
        if lifestyle_score < 50:
            recommendations.append(
                "😴 Poor lifestyle metrics. Focus on: 8+ hours sleep, proper nutrition, stress management."
            )
        elif lifestyle_score < 70:
            recommendations.append(
                "🌟 Lifestyle factors need attention. Review sleep quality and nutrition habits."
            )

        # Injury history recommendations
        if injury_history_score > 40:
            recommendations.append(
                "🏥 Recent injury history concerning. Consider preventive strengthening and mobility work."
            )

        # Overall risk recommendations
        if risk_level == "high":
            recommendations.insert(0,
                "🚨 HIGH RISK ALERT: Immediate intervention required. Consider rest day or active recovery only."
            )
        elif risk_level == "medium":
            recommendations.insert(0,
                "⚠️ MODERATE RISK: Monitor closely. Modify training intensity/volume as needed."
            )

        if not recommendations:
            recommendations.append("✅ Athlete showing good balance. Continue current training plan.")

        return "\n".join(recommendations)


class RecoveryPredictor:
    """
    Evidence-Based Recovery Time Prediction Module

    Uses Cox Proportional Hazards-inspired approach with published research data
    to estimate recovery times for injuries.

    Based on research from:
    - Mueller-Wohlfahrt et al. (2013) - Muscle injury classification
    - Waldén et al. (2016) - Hamstring injury recovery times
    - Silvers-Granelli et al. (2015) - ACL injury prevention
    """

    # Evidence-based baseline recovery times (days)
    RECOVERY_BASELINES = {
        # Muscle Strains
        "muscle_strain_grade1": {"min": 7, "typical": 10, "max": 14},
        "muscle_strain_grade2": {"min": 14, "typical": 21, "max": 28},
        "muscle_strain_grade3": {"min": 28, "typical": 42, "max": 90},

        # Ligament Sprains
        "ligament_sprain_grade1": {"min": 7, "typical": 14, "max": 21},
        "ligament_sprain_grade2": {"min": 21, "typical": 35, "max": 56},
        "ligament_sprain_grade3": {"min": 90, "typical": 180, "max": 365},

        # Tendon Injuries
        "tendinopathy": {"min": 21, "typical": 60, "max": 90},
        "tendon_rupture": {"min": 90, "typical": 180, "max": 365},

        # Bone Injuries
        "stress_reaction": {"min": 14, "typical": 28, "max": 42},
        "stress_fracture": {"min": 42, "typical": 84, "max": 120},
        "bone_fracture": {"min": 42, "typical": 90, "max": 180},

        # Joint Injuries
        "cartilage_damage": {"min": 28, "typical": 90, "max": 180},
        "meniscus_tear": {"min": 21, "typical": 42, "max": 90},

        # Soft Tissue
        "contusion": {"min": 3, "typical": 7, "max": 14},
        "laceration": {"min": 7, "typical": 14, "max": 21},

        # Default
        "other": {"min": 7, "typical": 21, "max": 42}
    }

    # Severity multipliers
    SEVERITY_MULTIPLIERS = {
        "minor": 0.8,
        "mild": 0.9,
        "moderate": 1.0,
        "severe": 1.5,
        "catastrophic": 2.0
    }

    @classmethod
    def predict_recovery_time(
        cls,
        injury_type: str,
        severity: Optional[str] = None,
        athlete_age: Optional[int] = None,
        previous_injury_same_area: bool = False,
        days_since_previous_injury: Optional[int] = None
    ) -> Dict[str, float]:
        """
        Predict recovery time range for an injury

        Args:
            injury_type: Type of injury (e.g., "muscle_strain_grade2")
            severity: Severity level if not in injury type
            athlete_age: Athlete's age
            previous_injury_same_area: Whether previous injury in same area
            days_since_previous_injury: Days since last injury in same area

        Returns:
            dict with min_days, typical_days, max_days, and modifiers applied
        """
        # Get baseline recovery times
        injury_key = cls._normalize_injury_type(injury_type)
        if injury_key not in cls.RECOVERY_BASELINES:
            injury_key = "other"

        baseline = cls.RECOVERY_BASELINES[injury_key]

        # Start with baseline
        min_days = baseline["min"]
        typical_days = baseline["typical"]
        max_days = baseline["max"]

        # Apply modifiers (multiplicative)
        total_modifier = 1.0

        # 1. Age modifier (research shows 20-30% increase for older athletes)
        if athlete_age:
            if athlete_age < 25:
                age_mod = 1.0  # Baseline recovery
            elif athlete_age < 30:
                age_mod = 1.1  # 10% longer
            elif athlete_age < 35:
                age_mod = 1.2  # 20% longer
            else:
                age_mod = 1.3  # 30% longer
            total_modifier *= age_mod

        # 2. Severity modifier
        if severity:
            severity_lower = severity.lower()
            if severity_lower in cls.SEVERITY_MULTIPLIERS:
                total_modifier *= cls.SEVERITY_MULTIPLIERS[severity_lower]

        # 3. Previous injury modifier (30-50% increase for re-injury)
        if previous_injury_same_area:
            if days_since_previous_injury and days_since_previous_injury < 180:
                # Recent previous injury = much higher risk of prolonged recovery
                total_modifier *= 1.5  # 50% longer
            else:
                total_modifier *= 1.3  # 30% longer

        # Apply modifiers
        min_days = int(min_days * total_modifier)
        typical_days = int(typical_days * total_modifier)
        max_days = int(max_days * total_modifier)

        return {
            "min_recovery_days": min_days,
            "typical_recovery_days": typical_days,
            "max_recovery_days": max_days,
            "expected_return_date_min": date.today() + timedelta(days=min_days),
            "expected_return_date_typical": date.today() + timedelta(days=typical_days),
            "expected_return_date_max": date.today() + timedelta(days=max_days),
            "modifiers_applied": {
                "total_multiplier": round(total_modifier, 2),
                "age_factor": age_mod if athlete_age else 1.0,
                "severity_factor": cls.SEVERITY_MULTIPLIERS.get(severity.lower(), 1.0) if severity else 1.0,
                "previous_injury_factor": 1.5 if previous_injury_same_area and days_since_previous_injury and days_since_previous_injury < 180 else (1.3 if previous_injury_same_area else 1.0)
            }
        }

    @classmethod
    def predict_recovery_for_athlete_injury(
        cls,
        db: Session,
        injury_id: int
    ) -> Dict[str, any]:
        """
        Predict recovery time for a specific injury record in database

        Args:
            db: Database session
            injury_id: ID of injury record

        Returns:
            Recovery prediction dict with estimated return dates
        """
        # Get the injury
        injury = db.query(models.InjuryHistory).filter(
            models.InjuryHistory.id == injury_id
        ).first()

        if not injury:
            return {"error": "Injury not found"}

        # Get athlete info
        athlete = db.query(models.Athlete).filter(
            models.Athlete.id == injury.athlete_id
        ).first()

        athlete_age = athlete.age if athlete else None

        # Check for previous injuries in same body part
        previous_injuries = db.query(models.InjuryHistory).filter(
            and_(
                models.InjuryHistory.athlete_id == injury.athlete_id,
                models.InjuryHistory.body_part == injury.body_part,
                models.InjuryHistory.injury_date < injury.injury_date,
                models.InjuryHistory.id != injury.id
            )
        ).order_by(models.InjuryHistory.injury_date.desc()).first()

        previous_injury_same_area = previous_injuries is not None

        days_since_previous = None
        if previous_injury_same_area:
            days_since_previous = (injury.injury_date - previous_injuries.injury_date).days

        # Make prediction
        prediction = cls.predict_recovery_time(
            injury_type=injury.injury_type,
            severity=injury.severity,
            athlete_age=athlete_age,
            previous_injury_same_area=previous_injury_same_area,
            days_since_previous_injury=days_since_previous
        )

        # Add context
        prediction["injury_id"] = injury.id
        prediction["athlete_id"] = injury.athlete_id
        prediction["injury_date"] = injury.injury_date
        prediction["body_part"] = injury.body_part
        prediction["injury_type"] = injury.injury_type

        return prediction

    @staticmethod
    def _normalize_injury_type(injury_type: str) -> str:
        """Normalize injury type string to match baseline keys"""
        injury_lower = injury_type.lower().replace(" ", "_")

        # Direct matches
        if injury_lower in RecoveryPredictor.RECOVERY_BASELINES:
            return injury_lower

        # Pattern matching
        if "strain" in injury_lower:
            if "grade_3" in injury_lower or "severe" in injury_lower:
                return "muscle_strain_grade3"
            elif "grade_2" in injury_lower or "moderate" in injury_lower:
                return "muscle_strain_grade2"
            else:
                return "muscle_strain_grade1"

        if "sprain" in injury_lower:
            if "grade_3" in injury_lower or "severe" in injury_lower:
                return "ligament_sprain_grade3"
            elif "grade_2" in injury_lower or "moderate" in injury_lower:
                return "ligament_sprain_grade2"
            else:
                return "ligament_sprain_grade1"

        if "tendon" in injury_lower:
            if "rupture" in injury_lower or "tear" in injury_lower:
                return "tendon_rupture"
            else:
                return "tendinopathy"

        if "fracture" in injury_lower:
            if "stress" in injury_lower:
                return "stress_fracture"
            else:
                return "bone_fracture"

        if "contusion" in injury_lower or "bruise" in injury_lower:
            return "contusion"

        # Default
        return "other"
