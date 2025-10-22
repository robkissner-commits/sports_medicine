from datetime import date, timedelta
from typing import List, Tuple, Optional
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import and_

from . import models


class AnalyticsEngine:
    """Core analytics engine for calculating risk metrics and ACWR"""

    # Risk thresholds
    ACWR_HIGH_RISK_UPPER = 1.5
    ACWR_HIGH_RISK_LOWER = 0.8
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

    @classmethod
    def calculate_overall_risk(
        cls,
        db: Session,
        athlete_id: int,
        target_date: date
    ) -> dict:
        """
        Calculate overall risk score and generate recommendations
        Returns: dict with risk metrics and recommendations
        """
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

        # Calculate weighted overall risk score
        # ACWR risk
        acwr_risk = 0
        if acwr:
            if acwr > cls.ACWR_HIGH_RISK_UPPER or acwr < cls.ACWR_HIGH_RISK_LOWER:
                acwr_risk = 80
            elif acwr > 1.3 or acwr < 0.9:
                acwr_risk = 50
            else:
                acwr_risk = 20

        # Weighted combination
        overall_risk = (
            acwr_risk * 0.30 +
            load_spike_score * 0.25 +
            (100 - recovery_score) * 0.20 +
            (100 - lifestyle_score) * 0.15 +
            injury_history_score * 0.10
        )

        # Determine risk level
        if overall_risk >= cls.HIGH_RISK_THRESHOLD:
            risk_level = "high"
        elif overall_risk >= cls.MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Generate recommendations
        recommendations = cls.generate_recommendations(
            acwr, load_spike_score, recovery_score,
            lifestyle_score, injury_history_score, risk_level
        )

        return {
            "overall_risk_score": round(overall_risk, 2),
            "risk_level": risk_level,
            "acwr": round(acwr, 2) if acwr else None,
            "load_spike_score": round(load_spike_score, 2),
            "recovery_score": round(recovery_score, 2),
            "lifestyle_score": round(lifestyle_score, 2),
            "injury_history_score": round(injury_history_score, 2),
            "recommendations": recommendations
        }

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
