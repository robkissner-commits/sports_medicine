# Sports Medicine Injury Prevention System - AI Development Prompt

## System Overview

Build a comprehensive sports medicine injury prevention platform that uses evidence-based analytics to predict injury risk and recovery times for athletes. The system combines GPS training data from Kinexon wearables with lifestyle factors, injury history, and peer-reviewed research to provide actionable insights for sports medicine professionals.

**Core Philosophy**: Hybrid Evidence-Based System (not ML/AI) - Uses validated sports science research and proven algorithms rather than machine learning, ensuring transparency, explainability, and effectiveness with small datasets.

---

## Technical Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: SQLAlchemy ORM with SQLite (easily portable to PostgreSQL)
- **API Style**: RESTful with automatic OpenAPI documentation
- **Data Processing**: pandas for CSV uploads, numpy for calculations

### Frontend
- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **Charts**: Recharts for data visualization
- **Styling**: CSS modules with responsive design
- **API Client**: Axios

### Key Dependencies
```python
# Backend
fastapi==0.104.1
sqlalchemy==2.0.23
pandas==2.1.3
numpy==1.26.2
python-multipart==0.0.6
uvicorn==0.24.0

# Frontend
react==18.2.0
react-router-dom==6.20.0
recharts==2.10.3
axios==1.6.2
```

---

## Data Models & Database Schema

### 1. Athlete Model
Primary entity representing an athlete in the system.

**Fields:**
- `id`: Integer, Primary Key
- `name`: String, Required - Full name
- `age`: Integer, Required - Current age (affects recovery calculations)
- `position`: String, Optional - Playing position
- `team`: String, Optional - Team affiliation
- `email`: String, Optional - Contact email
- `created_at`: DateTime, Auto-generated
- `updated_at`: DateTime, Auto-updated

**Relationships:**
- One-to-Many: TrainingLoad, InjuryHistory, Treatment, LifestyleLog, RiskAssessment

### 2. TrainingLoad Model
Stores daily training data from Kinexon GPS wearables.

**Kinexon GPS Fields (User Input):**
- `id`: Integer, Primary Key
- `athlete_id`: Foreign Key to Athlete
- `date`: Date, Required - Training session date
- `distance_miles`: Float, Required - Distance covered in miles
- `accumulated_accel_load`: Float, Required - Cumulative acceleration load
- `average_speed_mph`: Float, Optional - Average speed in mph
- `max_speed_mph`: Float, Optional - Maximum speed reached in mph
- `session_type`: String, Optional - "Training", "Game", "Recovery"

**Calculated Fields:**
- `training_load`: Float, Auto-calculated - Composite training load metric
  - Formula: `(distance_miles × 160) + (accumulated_accel_load × 1.5) + (average_speed_mph × 5) + (max_speed_mph × 2)`
  - Rationale: Weighted combination emphasizing distance and acceleration

**Timestamps:**
- `created_at`: DateTime, Auto-generated

### 3. InjuryHistory Model
Tracks all injuries for athletes.

**Fields:**
- `id`: Integer, Primary Key
- `athlete_id`: Foreign Key to Athlete
- `injury_date`: Date, Required - When injury occurred
- `injury_type`: String, Required - Classification (e.g., "Muscle Strain Grade 2")
- `body_part`: String, Required - Anatomical location (e.g., "Hamstring", "Ankle")
- `severity`: String, Optional - "minor", "mild", "moderate", "severe", "catastrophic"
- `recovery_date`: Date, Optional - Actual return date
- `expected_recovery_date`: Date, Optional - Predicted return date
- `days_missed`: Integer, Optional - Actual days out
- `description`: Text, Optional - Detailed notes
- `treatment_plan`: Text, Optional - Prescribed treatment
- `created_at`: DateTime, Auto-generated

### 4. Treatment Model
Logs recovery modalities and interventions.

**Fields:**
- `id`: Integer, Primary Key
- `athlete_id`: Foreign Key to Athlete
- `date`: Date, Required
- `modality`: String, Required - Type (e.g., "Physiotherapy", "Ice Bath", "Massage")
- `duration`: Integer, Optional - Minutes
- `body_part`: String, Optional - Target area
- `severity`: String, Optional - Treatment intensity
- `notes`: Text, Optional
- `created_at`: DateTime, Auto-generated

### 5. LifestyleLog Model
Daily wellness and lifestyle factors.

**Fields:**
- `id`: Integer, Primary Key
- `athlete_id`: Foreign Key to Athlete
- `date`: Date, Required
- `sleep_hours`: Float, Optional - Hours of sleep (critical modifier)
- `sleep_quality`: Integer, Optional - 1-10 scale
- `nutrition_score`: Integer, Optional - 1-10 scale
- `hydration_liters`: Float, Optional - Daily water intake
- `stress_level`: Integer, Optional - 1-10 scale (critical modifier)
- `soreness_level`: Integer, Optional - 1-10 scale
- `fatigue_level`: Integer, Optional - 1-10 scale
- `notes`: Text, Optional
- `created_at`: DateTime, Auto-generated

### 6. RiskAssessment Model
Stores calculated risk scores with full breakdown.

**Traditional Metrics:**
- `id`: Integer, Primary Key
- `athlete_id`: Foreign Key to Athlete
- `date`: Date, Required - Assessment date
- `overall_risk_score`: Float - Composite score (0-100)
- `risk_level`: String - "low", "medium", "high"
- `acwr`: Float - Acute:Chronic Workload Ratio (Gabbett 2016)
- `acute_load`: Float - 7-day rolling average
- `chronic_load`: Float - 28-day rolling average

**Enhanced Metrics (Evidence-Based):**
- `training_monotony`: Float - Average Load / Std Dev (Foster et al. 1998)
- `training_strain`: Float - Total Load × Monotony
- `load_z_score_7d`: Float - Statistical spike detection (7-day)
- `load_z_score_14d`: Float - Statistical spike detection (14-day)
- `load_z_score_28d`: Float - Statistical spike detection (28-day)

**Risk Modifiers:**
- `sleep_modifier`: Float - Multiplier based on sleep quality (<6hrs = 1.3×)
- `stress_modifier`: Float - Multiplier based on stress (high = 1.2×)
- `injury_recency_modifier`: Float - Based on days since last injury
- `age_modifier`: Float - Based on athlete age
- `compound_multiplier`: Float - Combined effect of all modifiers

**Additional Fields:**
- `recommendations`: Text - Generated recommendations
- `created_at`: DateTime, Auto-generated

---

## Core Analytics Engine

### Location: `backend/analytics.py`

### 1. Training Load Calculation
**Function:** `calculate_training_load_from_kinexon()`

```python
def calculate_training_load_from_kinexon(
    distance_miles: float,
    accumulated_accel_load: float,
    average_speed_mph: Optional[float] = None,
    max_speed_mph: Optional[float] = None
) -> float:
    """
    Calculate composite training load from Kinexon GPS metrics.

    Weighting rationale:
    - Distance (160 pts/mile): Primary workload indicator
    - Acceleration (1.5×): High metabolic cost, injury risk
    - Average speed (5×): Intensity indicator
    - Max speed (2×): Peak output, neuromuscular load
    """
    base_load = distance_miles * 160
    accel_component = accumulated_accel_load * 1.5
    speed_component = (average_speed_mph * 5) if average_speed_mph else 0
    max_speed_component = (max_speed_mph * 2) if max_speed_mph else 0

    return round(base_load + accel_component + speed_component + max_speed_component, 2)
```

### 2. ACWR (Acute:Chronic Workload Ratio)
**Function:** `calculate_acwr()`

Based on Gabbett (2016) research:
- **Acute Load**: 7-day rolling average
- **Chronic Load**: 28-day rolling average
- **Ratio**: Acute / Chronic

**Risk Zones:**
- `< 0.8`: Undertraining (deconditioning risk)
- `0.8 - 1.3`: Sweet spot (optimal adaptation)
- `1.3 - 1.5`: Caution zone (moderate risk)
- `> 1.5`: Danger zone (high injury risk)

```python
def calculate_acwr(db: Session, athlete_id: int, target_date: date) -> Dict:
    # Get 28 days of training loads
    loads = get_loads_before_date(db, athlete_id, target_date, days=28)

    if len(loads) < 7:
        return {"acwr": None, "risk": "insufficient_data"}

    acute_loads = loads[-7:]  # Last 7 days
    chronic_loads = loads  # All 28 days

    acute_avg = sum(load.training_load for load in acute_loads) / len(acute_loads)
    chronic_avg = sum(load.training_load for load in chronic_loads) / len(chronic_loads)

    acwr = acute_avg / chronic_avg if chronic_avg > 0 else 0

    return {
        "acwr": round(acwr, 2),
        "acute_load": round(acute_avg, 2),
        "chronic_load": round(chronic_avg, 2),
        "risk_category": categorize_acwr_risk(acwr)
    }
```

### 3. Training Monotony & Strain
**Functions:** `calculate_training_monotony()`, `calculate_training_strain()`

Based on Foster et al. (1998):
- **Monotony**: Average Daily Load / Standard Deviation
  - Low variation = High monotony = Higher injury risk
  - Monotony > 2.0 = Concerning
- **Strain**: Total Load × Monotony
  - Combined metric of volume and variation

```python
def calculate_training_monotony(loads: List[float]) -> float:
    """
    High monotony indicates lack of variation, which increases injury risk.
    Athletes need variability in training stimulus.
    """
    if len(loads) < 2:
        return 0.0

    mean_load = sum(loads) / len(loads)
    std_dev = (sum((x - mean_load) ** 2 for x in loads) / len(loads)) ** 0.5

    if std_dev == 0:
        return 0.0

    return mean_load / std_dev

def calculate_training_strain(total_load: float, monotony: float) -> float:
    """Strain = Total Load × Monotony"""
    return total_load * monotony
```

### 4. Z-Score Spike Detection
**Function:** `calculate_z_score_spike()`

Statistical method to detect unusual training loads:
- Calculate mean and standard deviation over rolling window
- Z-score = (Current Load - Mean) / Std Dev
- Z-score > 2.0 = Unusual spike (97.5th percentile)

```python
def calculate_z_score_spike(
    current_load: float,
    historical_loads: List[float],
    window_days: int = 28
) -> float:
    """
    Detect statistical anomalies in training load.
    Z-score > 2.0 indicates load is 2+ standard deviations above normal.
    """
    if len(historical_loads) < 7:
        return 0.0

    mean = sum(historical_loads) / len(historical_loads)
    variance = sum((x - mean) ** 2 for x in historical_loads) / len(historical_loads)
    std_dev = variance ** 0.5

    if std_dev == 0:
        return 0.0

    z_score = (current_load - mean) / std_dev
    return round(z_score, 2)
```

### 5. Risk Modifiers (Compound Risk System)

**Sleep Modifier:**
```python
def calculate_sleep_modifier(sleep_hours: float) -> float:
    """
    Research shows sleep < 6 hours significantly increases injury risk.
    Based on Fullagar et al. (2015) sleep and recovery research.
    """
    if sleep_hours < 6.0:
        return 1.3  # 30% increase
    elif sleep_hours < 7.0:
        return 1.1  # 10% increase
    else:
        return 1.0  # No modification
```

**Stress Modifier:**
```python
def calculate_stress_modifier(stress_level: int) -> float:
    """
    High stress (> 7/10) impairs recovery and increases injury risk.
    """
    if stress_level >= 8:
        return 1.2  # 20% increase
    elif stress_level >= 7:
        return 1.1  # 10% increase
    else:
        return 1.0
```

**Injury Recency Modifier:**
```python
def calculate_injury_recency_modifier(days_since_injury: int) -> float:
    """
    Recent injuries dramatically increase re-injury risk.
    Risk decreases over time but remains elevated for 6 months.
    """
    if days_since_injury < 14:
        return 1.5  # 50% increase - very recent
    elif days_since_injury < 30:
        return 1.3  # 30% increase - recent
    elif days_since_injury < 90:
        return 1.2  # 20% increase - recovering
    elif days_since_injury < 180:
        return 1.1  # 10% increase - mostly recovered
    else:
        return 1.0  # No modification after 6 months
```

**Age Modifier:**
```python
def calculate_age_modifier(age: int) -> float:
    """
    Older athletes require longer recovery times.
    Based on Dogramaci et al. (2011) age and recovery research.
    """
    if age < 25:
        return 1.0  # Baseline
    elif age < 30:
        return 1.05  # 5% increase
    elif age < 35:
        return 1.1  # 10% increase
    else:
        return 1.15  # 15% increase
```

### 6. Overall Risk Calculation
**Function:** `calculate_overall_risk()`

```python
def calculate_overall_risk(db: Session, athlete_id: int, target_date: date) -> Dict:
    """
    Calculate comprehensive risk assessment combining:
    1. Traditional ACWR
    2. Training monotony and strain
    3. Statistical spike detection
    4. Lifestyle modifiers (compound effect)
    5. Injury history
    """

    # Step 1: Get all data
    acwr_data = calculate_acwr(db, athlete_id, target_date)
    loads_7d = get_recent_loads(db, athlete_id, target_date, 7)
    loads_28d = get_recent_loads(db, athlete_id, target_date, 28)
    lifestyle = get_recent_lifestyle(db, athlete_id, target_date, 7)
    injuries = get_recent_injuries(db, athlete_id, target_date, 180)

    # Step 2: Calculate base metrics
    monotony = calculate_training_monotony([l.training_load for l in loads_7d])
    strain = calculate_training_strain(sum(l.training_load for l in loads_7d), monotony)
    z_score_7d = calculate_z_score_spike(loads_7d[-1].training_load, [l.training_load for l in loads_7d[:-1]], 7)

    # Step 3: Base risk score (0-100)
    base_risk = 0

    # ACWR contribution (40% weight)
    if acwr_data["acwr"]:
        if acwr_data["acwr"] > 1.5:
            base_risk += 40
        elif acwr_data["acwr"] > 1.3:
            base_risk += 25
        elif acwr_data["acwr"] < 0.8:
            base_risk += 20
        else:
            base_risk += 5

    # Monotony contribution (20% weight)
    if monotony > 2.5:
        base_risk += 20
    elif monotony > 2.0:
        base_risk += 12

    # Z-score spike contribution (20% weight)
    if z_score_7d > 2.5:
        base_risk += 20
    elif z_score_7d > 2.0:
        base_risk += 12

    # Recent injury (20% weight)
    if injuries:
        days_since = (target_date - injuries[0].injury_date).days
        if days_since < 30:
            base_risk += 20
        elif days_since < 90:
            base_risk += 12

    # Step 4: Calculate compound modifiers
    sleep_mod = calculate_sleep_modifier(avg_sleep(lifestyle))
    stress_mod = calculate_stress_modifier(avg_stress(lifestyle))
    injury_mod = calculate_injury_recency_modifier(days_since) if injuries else 1.0
    age_mod = calculate_age_modifier(athlete.age)

    compound_multiplier = sleep_mod * stress_mod * injury_mod * age_mod

    # Step 5: Apply multiplier to base risk
    final_risk = min(100, base_risk * compound_multiplier)

    # Step 6: Categorize risk
    if final_risk < 30:
        risk_level = "low"
    elif final_risk < 60:
        risk_level = "medium"
    else:
        risk_level = "high"

    # Step 7: Generate recommendations
    recommendations = generate_enhanced_recommendations(
        risk_level=risk_level,
        acwr=acwr_data["acwr"],
        monotony=monotony,
        sleep_hours=avg_sleep(lifestyle),
        stress_level=avg_stress(lifestyle),
        recent_injury=injuries[0] if injuries else None
    )

    return {
        "overall_risk_score": round(final_risk, 1),
        "risk_level": risk_level,
        "acwr": acwr_data["acwr"],
        "acute_load": acwr_data["acute_load"],
        "chronic_load": acwr_data["chronic_load"],
        "training_monotony": round(monotony, 2),
        "training_strain": round(strain, 2),
        "load_z_score_7d": round(z_score_7d, 2),
        "sleep_modifier": round(sleep_mod, 2),
        "stress_modifier": round(stress_mod, 2),
        "injury_recency_modifier": round(injury_mod, 2),
        "age_modifier": round(age_mod, 2),
        "compound_multiplier": round(compound_multiplier, 2),
        "recommendations": recommendations
    }
```

### 7. Recovery Time Prediction
**Class:** `RecoveryPredictor`

Evidence-based recovery prediction using Cox Proportional Hazards-inspired approach.

**Research Base:**
- Mueller-Wohlfahrt et al. (2013) - Muscle injury classification
- Waldén et al. (2016) - Hamstring recovery times
- Doherty et al. (2017) - Ligament sprain recovery
- Cook & Purdam (2009) - Tendinopathy continuum
- Fredericson & Kent (2005) - Stress fracture healing
- Dogramaci et al. (2011) - Age effects on recovery
- Hägglund et al. (2006) - Re-injury risk factors

**Baseline Recovery Times (Days):**
```python
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
}
```

**Severity Multipliers:**
```python
SEVERITY_MULTIPLIERS = {
    "minor": 0.8,      # 20% faster
    "mild": 0.9,       # 10% faster
    "moderate": 1.0,   # Baseline
    "severe": 1.5,     # 50% longer
    "catastrophic": 2.0  # 100% longer
}
```

**Recovery Calculation:**
```python
def predict_recovery_time(
    injury_type: str,
    severity: str,
    athlete_age: int,
    previous_injury_same_area: bool,
    days_since_previous_injury: int
) -> Dict:
    """
    Predict recovery timeline with modifiers.

    Returns:
    - min_recovery_days: Best case scenario
    - typical_recovery_days: Expected timeline
    - max_recovery_days: Conservative estimate
    - expected_return_date_min/typical/max: Calendar dates
    - justification: Detailed explanation with research citations
    - research_links: Array of relevant studies with URLs
    """

    # Get baseline
    baseline = RECOVERY_BASELINES[normalize_injury_type(injury_type)]

    # Calculate modifiers
    age_modifier = get_age_modifier(athlete_age)
    severity_modifier = SEVERITY_MULTIPLIERS[severity]
    reinjury_modifier = 1.5 if (previous_injury_same_area and days_since_previous_injury < 180) else 1.3 if previous_injury_same_area else 1.0

    total_modifier = age_modifier * severity_modifier * reinjury_modifier

    # Apply modifiers
    min_days = int(baseline["min"] * total_modifier)
    typical_days = int(baseline["typical"] * total_modifier)
    max_days = int(baseline["max"] * total_modifier)

    # Generate justification
    justification = generate_justification(
        injury_type=injury_type,
        baseline=baseline,
        age=athlete_age,
        age_modifier=age_modifier,
        severity=severity,
        severity_modifier=severity_modifier,
        previous_injury=previous_injury_same_area,
        days_since=days_since_previous_injury,
        reinjury_modifier=reinjury_modifier
    )

    # Get research links
    research_links = get_research_links(
        injury_type=injury_type,
        age=athlete_age,
        previous_injury=previous_injury_same_area
    )

    return {
        "min_recovery_days": min_days,
        "typical_recovery_days": typical_days,
        "max_recovery_days": max_days,
        "expected_return_date_min": date.today() + timedelta(days=min_days),
        "expected_return_date_typical": date.today() + timedelta(days=typical_days),
        "expected_return_date_max": date.today() + timedelta(days=max_days),
        "modifiers_applied": {
            "total_multiplier": total_modifier,
            "age_factor": age_modifier,
            "severity_factor": severity_modifier,
            "previous_injury_factor": reinjury_modifier
        },
        "justification": justification,
        "research_links": research_links
    }
```

**Justification Generator:**
The system generates detailed explanations like:
```
**Injury Classification:** Muscle Strain Grade 2
**Baseline Recovery Range:** 14-28 days (typical: 21 days)

**Evidence Base:**
- Mueller-Wohlfahrt, H. W., et al. (2013). Terminology and classification of muscle injuries in sport: The Munich consensus statement.
- Finding: Grade 2 strains: 14-28 days with progressive loading

**Risk Modifiers Applied (Total: 1.56×):**
- **Age Factor (1.2×):** Athlete is 32 years old
  - Research shows athletes over 30 require 20% longer recovery
  - Citation: Dogramaci, Y., et al. (2011). The effect of age on recovery from muscle damage...

- **Re-injury Risk Factor (1.3×):** Previous injury in same body part
  - History of injury increases recovery time by 30%
  - Citation: Hägglund, M., et al. (2006). Injuries affect team performance negatively...

**Clinical Recommendation:**
- Best case: Early return with optimal recovery conditions
- Typical case: Expected return with standard rehabilitation protocol
- Worst case: Conservative estimate accounting for complications

*Monitor progress closely and adjust timeline based on functional testing and pain-free movement.*
```

**Research Links Include:**
- Full citation
- Direct URL to journal article
- DOI for academic lookup
- Clickable buttons in UI

---

## API Endpoints

### Base URL: `/api`

### Athletes
- `GET /athletes` - List all athletes
- `POST /athletes` - Create athlete
- `GET /athletes/{id}` - Get athlete details
- `PUT /athletes/{id}` - Update athlete
- `DELETE /athletes/{id}` - Delete athlete

### Training Loads
- `GET /training-loads/athlete/{athlete_id}` - Get athlete's training history
- `POST /training-loads` - Create training load (auto-calculates load from Kinexon data)
- `PUT /training-loads/{id}` - Update training load
- `DELETE /training-loads/{id}` - Delete training load

**Request Body Example:**
```json
{
  "athlete_id": 1,
  "date": "2024-12-04",
  "distance_miles": 4.5,
  "accumulated_accel_load": 125.3,
  "average_speed_mph": 4.2,
  "max_speed_mph": 16.8,
  "session_type": "Training"
}
```
Note: `training_load` is automatically calculated - do not include in request.

### Injuries
- `GET /injuries/athlete/{athlete_id}` - Get injury history
- `POST /injuries` - Log new injury
- `PUT /injuries/{id}` - Update injury
- `DELETE /injuries/{id}` - Delete injury
- `GET /injuries/{injury_id}/recovery-prediction` - Get evidence-based recovery prediction

### Treatments
- `GET /treatments/athlete/{athlete_id}` - Get treatment history
- `POST /treatments` - Log treatment
- `PUT /treatments/{id}` - Update treatment
- `DELETE /treatments/{id}` - Delete treatment

### Lifestyle Logs
- `GET /lifestyle/athlete/{athlete_id}` - Get lifestyle logs
- `POST /lifestyle` - Create lifestyle log
- `PUT /lifestyle/{id}` - Update lifestyle log
- `DELETE /lifestyle/{id}` - Delete lifestyle log

### Analytics
- `GET /analytics/athlete/{athlete_id}/risk` - Calculate current risk assessment
- `POST /analytics/athlete/{athlete_id}/calculate-risk` - Recalculate and save risk
- `GET /analytics/athlete/{athlete_id}/risk-history` - Get historical risk assessments
- `GET /analytics/athlete/{athlete_id}/acwr-trend?days=56` - Get ACWR trend data
- `GET /analytics/athlete/{athlete_id}/training-summary?days=28` - Get training summary

### Data Upload
- `POST /upload/training-data` - Bulk upload CSV from Kinexon
  - Required columns: "Date", "Distance (mi)", "Accumulated Acceleration Load"
  - Optional columns: "Speed (Ø) (mph)", "Speed (max.) (mph)", "Session Type"
  - Accepts athlete_id as form parameter
  - Auto-calculates training_load for each row

---

## Frontend Components

### 1. Dashboard (`Dashboard.jsx`)
**Purpose:** Overview of all athletes with sortable risk indicators

**Features:**
- Table of all athletes with:
  - Name, Age, Position, Team
  - Risk Level badge (color-coded: green/yellow/red)
  - Risk Score (0-100)
  - ACWR value
  - Last assessment date
- Click athlete row to navigate to detailed profile
- Add new athlete button
- Responsive table with mobile view

**Risk Badge Colors:**
- Green (#28a745): Low risk (< 30)
- Yellow (#ffc107): Medium risk (30-60)
- Red (#dc3545): High risk (> 60)

### 2. Athlete Profile (`AthleteProfile.jsx`)
**Purpose:** Comprehensive athlete detail view with tabs

**Tabs:**

#### Overview Tab
- Athlete info card (name, age, position, team, email)
- Current risk assessment with RiskBreakdown component
- "Recalculate Risk" button
- ACWR trend chart (56 days)
- Training summary cards

#### Training Tab
- Table of all training loads with Kinexon metrics
- Columns: Date, Distance (mi), Accel Load, Avg Speed, Max Speed, Calculated Load, Session Type
- Inline editing for each row
- Delete functionality
- Calculated Load shown in bold (read-only)

#### Injuries Tab
- Table of injury history
- "Predict Recovery" button for each injury
- Recovery prediction cards (when clicked):
  - Timeline with best/typical/worst case dates
  - Risk modifier tags
  - **Clinical Justification section** (NEW)
    - Formatted explanation with markdown
    - Research citations inline
  - **Supporting Research section** (NEW)
    - Cards for each relevant study
    - "View Full Study" button → journal URL
    - "DOI" button → doi.org link
- Inline editing for injuries

#### Treatments Tab
- Table of treatment history
- Columns: Date, Modality, Body Part, Duration, Severity, Notes
- Inline editing and delete

#### Lifestyle Tab
- Table of lifestyle logs
- Columns: Date, Sleep hrs, Sleep Quality, Nutrition, Hydration, Stress, Soreness, Fatigue, Notes
- Inline editing and delete

### 3. Add Athlete (`AddAthlete.jsx`)
**Purpose:** Form to create new athlete

**Fields:**
- Name (required)
- Age (required, number)
- Position (optional)
- Team (optional)
- Email (optional)

**Validation:**
- All required fields must be filled
- Age must be positive integer
- Form clears on successful submission
- Redirects to dashboard after creation

### 4. Data Upload (`DataUpload.jsx`)
**Purpose:** Bulk CSV upload from Kinexon system

**Features:**
- File input (accepts .csv only)
- Athlete selector dropdown
- Upload button
- Progress indicator
- Success/error messages

**CSV Format Expected:**
```csv
Date,Distance (mi),Accumulated Acceleration Load,Speed (Ø) (mph),Speed (max.) (mph),Session Type
2024-12-01,4.5,125.3,4.2,16.8,Training
2024-12-02,3.8,98.7,3.9,15.2,Training
2024-12-03,5.2,145.6,4.5,17.9,Game
```

**Process:**
1. User selects athlete
2. User uploads CSV
3. Backend parses exact column names (case-sensitive on key parts)
4. Backend auto-calculates training_load for each row
5. Backend bulk inserts all records
6. Returns count of created records

### 5. RiskBreakdown (`RiskBreakdown.jsx`)
**Purpose:** Comprehensive risk visualization component

**Sections:**

#### Overall Risk Score
- Large number display (0-100)
- Color-coded based on level
- Risk level badge

#### Compound Multiplier Alert
- Shows when compound_multiplier > 1.0
- Highlights cumulative effect of risk factors
- Red alert box with multiplier value

#### Traditional Metrics Grid
- ACWR with color coding
- Acute Load (7-day avg)
- Chronic Load (28-day avg)
- Recent Recovery Days
- Lifestyle scores (sleep, stress)

#### Enhanced Metrics Section
- Training Monotony with interpretation
- Training Strain
- Z-Score spikes (7d, 14d, 28d) with warning indicators

#### Risk Modifiers
- Individual modifier cards:
  - Sleep modifier with icon
  - Stress modifier with icon
  - Injury recency modifier
  - Age modifier
- Shows multiplier value (e.g., 1.3×)

#### Enhanced Recommendations
- Bullet list of actionable recommendations
- Research citations included
- Color-coded by urgency

**Styling:**
- Card-based layout
- Gradient backgrounds
- Icons for visual appeal
- Responsive grid
- Hover effects

---

## Key Features & User Workflows

### Workflow 1: Adding a New Athlete
1. User clicks "Add Athlete" on dashboard
2. Fills form (name, age, position, team, email)
3. Submits form
4. System creates athlete record
5. Redirects to dashboard with new athlete visible

### Workflow 2: Uploading Training Data
1. User navigates to Data Upload page
2. Selects athlete from dropdown
3. Uploads Kinexon CSV file with columns:
   - Date (required)
   - Distance (mi) (required)
   - Accumulated Acceleration Load (required)
   - Speed (Ø) (mph) (optional)
   - Speed (max.) (mph) (optional)
4. System parses CSV, calculates training_load for each row
5. Bulk inserts all training sessions
6. Shows success message with count

### Workflow 3: Viewing Athlete Risk
1. User clicks athlete on dashboard
2. System loads athlete profile
3. Overview tab shows current risk assessment with:
   - Overall risk score
   - Detailed breakdown in RiskBreakdown component
   - ACWR trend chart
   - All metrics explained
4. User can click "Recalculate Risk" to update assessment

### Workflow 4: Predicting Injury Recovery
1. User navigates to athlete's Injuries tab
2. Clicks "Predict Recovery" on an injury
3. System analyzes:
   - Injury type and severity
   - Athlete age
   - Previous injuries in same body part
   - Days since previous injury
4. System displays:
   - Best/typical/worst case recovery timelines
   - Expected return dates
   - Risk modifier breakdown
   - **Clinical justification with research citations**
   - **Links to supporting research papers**
5. User can click research links to view studies

### Workflow 5: Editing Historical Data
1. User navigates to any data tab (Training, Injuries, etc.)
2. Clicks "Edit" button on a row
3. Input fields appear inline
4. User modifies values
5. Clicks "Save" to commit changes
6. System validates and updates record
7. Table refreshes with new data

### Workflow 6: Monitoring ACWR Trends
1. User views athlete profile Overview tab
2. ACWR trend chart displays 56 days of data
3. Chart shows:
   - Daily ACWR values as line
   - Sweet spot zone (0.8-1.3) highlighted in green
   - Caution zone (1.3-1.5) in yellow
   - Danger zone (>1.5) in red
4. Hover over points to see exact values
5. Identifies training load spikes visually

---

## Styling Guidelines

### Color Palette
```css
/* Risk Levels */
--risk-low: #28a745;      /* Green */
--risk-medium: #ffc107;   /* Yellow/Amber */
--risk-high: #dc3545;     /* Red */

/* UI Elements */
--primary: #2196f3;       /* Blue */
--secondary: #6c757d;     /* Gray */
--success: #28a745;       /* Green */
--warning: #ffc107;       /* Amber */
--danger: #dc3545;        /* Red */
--info: #17a2b8;          /* Cyan */

/* Backgrounds */
--bg-light: #f8f9fa;
--bg-white: #ffffff;
--bg-dark: #343a40;

/* Research Links */
--research-primary: #6366f1;  /* Indigo */
--research-doi: #10b981;      /* Emerald */
```

### Typography
- **Headings**: System font stack, bold, dark gray
- **Body**: 14-16px, line-height 1.5
- **Small text**: 12-13px for labels and citations
- **Monospace**: For data values (training load, dates)

### Component Patterns
- **Cards**: White background, border-radius 8px, box-shadow, left-border accent
- **Tables**: Striped rows, hover effect, responsive collapse on mobile
- **Buttons**: Rounded, color-coded by action, hover darkens
- **Badges**: Small, rounded-pill, colored by value
- **Charts**: Recharts with custom colors matching risk palette

### Responsive Breakpoints
```css
/* Mobile */
@media (max-width: 768px) {
  /* Stack grids vertically */
  /* Collapse tables to cards */
  /* Enlarge touch targets */
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  /* 2-column grids */
}

/* Desktop */
@media (min-width: 1025px) {
  /* Full multi-column layouts */
}
```

---

## Research Citations & Evidence Base

### Primary Research Sources

1. **Gabbett, T. J. (2016)**
   - Title: "The training-injury prevention paradox"
   - Journal: British Journal of Sports Medicine, 50(3), 169-176
   - DOI: 10.1136/bjsports-2015-095788
   - Key Finding: ACWR sweet spot of 0.8-1.3 minimizes injury risk
   - Application: Base ACWR calculation and risk zones

2. **Foster, C., et al. (1998)**
   - Title: "Effects of specific versus cross-training on running performance"
   - Journal: European Journal of Applied Physiology, 70, 367-372
   - Key Finding: Training monotony increases injury and illness risk
   - Application: Monotony and strain calculations

3. **Mueller-Wohlfahrt, H. W., et al. (2013)**
   - Title: "Terminology and classification of muscle injuries in sport: The Munich consensus statement"
   - Journal: British Journal of Sports Medicine, 47(6), 342-350
   - DOI: 10.1136/bjsports-2012-091448
   - URL: https://bjsm.bmj.com/content/47/6/342
   - Key Finding: Standardized muscle injury grading with recovery timelines
   - Application: Baseline recovery times for muscle strains

4. **Waldén, M., et al. (2016)**
   - Title: "Return to play after hamstring muscle injuries in professional football players"
   - Journal: British Journal of Sports Medicine, 50(7), 431-436
   - DOI: 10.1136/bjsports-2015-095506
   - URL: https://bjsm.bmj.com/content/50/7/431
   - Key Finding: Average RTP 21 days, MRI-detected injuries 28 days
   - Application: Hamstring injury predictions

5. **Doherty, C., et al. (2017)**
   - Title: "Treatment and prevention of acute and recurrent ankle sprain"
   - Journal: British Journal of Sports Medicine, 51(2), 113-125
   - DOI: 10.1136/bjsports-2016-096178
   - URL: https://bjsm.bmj.com/content/51/2/113
   - Key Finding: Grade-specific recovery timelines for ankle sprains
   - Application: Ligament sprain predictions

6. **Cook, J. L., & Purdam, C. R. (2009)**
   - Title: "Is tendon pathology a continuum?"
   - Journal: British Journal of Sports Medicine, 43(6), 409-416
   - DOI: 10.1136/bjsm.2008.051193
   - URL: https://bjsm.bmj.com/content/43/6/409
   - Key Finding: Tendinopathy continuum model with stage-specific timelines
   - Application: Tendon injury predictions

7. **Dogramaci, Y., et al. (2011)**
   - Title: "The effect of age on recovery from muscle damage after strenuous eccentric exercise"
   - Journal: Journal of Sports Science & Medicine, 10(1), 118-125
   - URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3737905/
   - Key Finding: Athletes >30 years require 10-30% longer recovery
   - Application: Age modifiers in risk and recovery calculations

8. **Hägglund, M., et al. (2013)**
   - Title: "Injuries affect team performance negatively in professional football"
   - Journal: British Journal of Sports Medicine, 47(12), 738-742
   - DOI: 10.1136/bjsports-2013-092215
   - URL: https://bjsm.bmj.com/content/47/12/738
   - Key Finding: Re-injury within 6 months shows 30-50% longer recovery
   - Application: Re-injury risk modifiers

---

## Implementation Notes

### Database Setup
```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./sports_medicine.db"
# For production: "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### CORS Configuration
```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sports Medicine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend API Client
```javascript
// frontend/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getAthletes = () => api.get('/athletes');
export const getAthlete = (id) => api.get(`/athletes/${id}`);
export const createAthlete = (data) => api.post('/athletes', data);
export const updateAthlete = (id, data) => api.put(`/athletes/${id}`, data);
export const deleteAthlete = (id) => api.delete(`/athletes/${id}`);

export const getAthleteTrainingLoads = (id) => api.get(`/training-loads/athlete/${id}`);
export const createTrainingLoad = (data) => api.post('/training-loads', data);
export const updateTrainingLoad = (id, data) => api.put(`/training-loads/${id}`, data);
export const deleteTrainingLoad = (id) => api.delete(`/training-loads/${id}`);

export const getAthleteInjuries = (id) => api.get(`/injuries/athlete/${id}`);
export const getInjuryRecoveryPrediction = (id) => api.get(`/injuries/${id}/recovery-prediction`);
export const createInjury = (data) => api.post('/injuries', data);
export const updateInjury = (id, data) => api.put(`/injuries/${id}`, data);
export const deleteInjury = (id) => api.delete(`/injuries/${id}`);

export const getAthleteTreatments = (id) => api.get(`/treatments/athlete/${id}`);
export const createTreatment = (data) => api.post('/treatments', data);
export const updateTreatment = (id, data) => api.put(`/treatments/${id}`, data);
export const deleteTreatment = (id) => api.delete(`/treatments/${id}`);

export const getAthleteLifestyleLogs = (id) => api.get(`/lifestyle/athlete/${id}`);
export const createLifestyleLog = (data) => api.post('/lifestyle', data);
export const updateLifestyleLog = (id, data) => api.put(`/lifestyle/${id}`, data);
export const deleteLifestyleLog = (id) => api.delete(`/lifestyle/${id}`);

export const getAthleteRisk = (id) => api.get(`/analytics/athlete/${id}/risk`);
export const calculateAthleteRisk = (id) => api.post(`/analytics/athlete/${id}/calculate-risk`);
export const getAthleteRiskHistory = (id) => api.get(`/analytics/athlete/${id}/risk-history`);
export const getAthleteACWRTrend = (id, days = 56) => api.get(`/analytics/athlete/${id}/acwr-trend?days=${days}`);
export const getAthleteTrainingSummary = (id, days = 28) => api.get(`/analytics/athlete/${id}/training-summary?days=${days}`);

export const uploadTrainingData = (formData) => api.post('/upload/training-data', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});

export default api;
```

### Running the Application

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs (auto-generated Swagger UI)

---

## Testing & Data Generation

### Test Data Generator
Location: `backend/generate_test_data.py`

**Purpose:** Creates realistic test data with 5 athlete scenarios:

1. **Alex Thompson (Low Risk)**
   - Optimal training progression
   - Good lifestyle factors
   - No recent injuries
   - Expected: Risk score < 30

2. **Jordan Martinez (Medium Risk - Monotony)**
   - High training monotony (same load daily)
   - Moderate lifestyle
   - Expected: Risk score 30-40, high monotony warning

3. **Sam Chen (High Risk - Compound)**
   - Poor sleep (<6 hours)
   - High stress (7-9/10)
   - Recent minor injury
   - Training load spike
   - Expected: Risk score > 60, compound multiplier > 1.5×

4. **Morgan Davis (Recent Injury)**
   - Hamstring strain 35 days ago
   - Gradual return to training
   - Expected: Elevated injury recency modifier

5. **Casey Rodriguez (Load Spike)**
   - Normal baseline
   - Sudden 700-point training load 3 days ago
   - Expected: High z-score spike

**Run generator:**
```bash
python -m backend.generate_test_data
```

### Manual Testing Checklist

**Risk Calculation:**
- [ ] Low ACWR (< 0.8) triggers undertraining warning
- [ ] High ACWR (> 1.5) triggers high risk
- [ ] High monotony (> 2.0) triggers warning
- [ ] Z-score > 2.0 triggers spike detection
- [ ] Sleep < 6 hours applies 1.3× modifier
- [ ] Stress > 7 applies 1.2× modifier
- [ ] Recent injury (<30 days) applies 1.5× modifier
- [ ] Multiple modifiers compound multiplicatively

**Recovery Prediction:**
- [ ] Muscle strain Grade 2 baseline: 14-28 days
- [ ] Age > 30 increases timeline
- [ ] Severity modifiers apply correctly
- [ ] Re-injury (<180 days) increases timeline
- [ ] Justification includes research citations
- [ ] Research links are clickable and valid

**CSV Upload:**
- [ ] Accepts Kinexon column names exactly
- [ ] Calculates training_load automatically
- [ ] Handles optional columns (speeds)
- [ ] Bulk inserts all rows
- [ ] Reports success count

**Frontend:**
- [ ] Dashboard shows all athletes
- [ ] Risk badges color-coded correctly
- [ ] Athlete profile loads all tabs
- [ ] Inline editing works for all data types
- [ ] Charts render ACWR trend
- [ ] Recovery prediction displays justification
- [ ] Research links open in new tabs

---

## Security & Deployment Considerations

### Security
- **Input Validation**: All API endpoints validate input types
- **SQL Injection**: Using SQLAlchemy ORM prevents SQL injection
- **CORS**: Configured for specific origins only
- **File Upload**: CSV parsing sanitized, limited file size
- **Authentication**: NOT IMPLEMENTED (add for production)
  - Recommend: JWT tokens with FastAPI security
  - User roles: Admin, Clinician, Coach (read-only)

### Production Deployment

**Backend:**
- Use PostgreSQL instead of SQLite
- Add environment variables for config
- Use proper secret management
- Add rate limiting
- Enable HTTPS
- Add logging and monitoring
- Use Gunicorn or similar ASGI server

**Frontend:**
- Build for production: `npm run build`
- Serve static files via Nginx or CDN
- Enable gzip compression
- Add error tracking (e.g., Sentry)

**Database:**
- Regular backups
- Migration system (Alembic recommended)
- Connection pooling
- Indexes on foreign keys and date columns

**Monitoring:**
- API response times
- Error rates
- Database query performance
- User activity logs

---

## Future Enhancements

### Phase 2 Features
1. **Team Dashboard**
   - Overview of entire team risk
   - Heatmap of player statuses
   - Training load distribution

2. **Automated Alerts**
   - Email/SMS notifications for high risk
   - Daily risk digests for coaches
   - Injury milestone reminders

3. **Advanced Analytics**
   - Trend analysis over seasons
   - Position-specific risk profiles
   - Return-to-play progression tracking

4. **Integration**
   - Direct Kinexon API integration (no CSV)
   - Electronic health records (EHR) sync
   - Calendar integration for return dates

5. **Reports**
   - PDF export of athlete profiles
   - Season summary reports
   - Injury incidence analysis

### Phase 3 Features
1. **Mobile App**
   - Athlete self-reporting
   - Push notifications
   - Offline mode

2. **Multi-tenancy**
   - Support multiple teams/organizations
   - Role-based access control
   - Separate data isolation

3. **Machine Learning (Optional)**
   - Personalized risk models per athlete
   - Predictive injury type likelihood
   - Optimal load recommendations
   - Requires: 100+ athletes, 1+ year data

---

## Development Guidelines

### Code Style
**Python:**
- Follow PEP 8
- Type hints for function parameters
- Docstrings for all functions
- Max line length: 120 characters

**JavaScript:**
- ES6+ syntax
- Functional components with hooks
- PropTypes for component validation
- 2-space indentation

### Git Workflow
- Feature branches: `feature/description`
- Commit messages: Clear, present tense
- Pull requests: Required for main branch
- Code review: Before merging

### Documentation
- API docs auto-generated by FastAPI
- Component props documented
- README with setup instructions
- Inline comments for complex logic

---

## Summary

This system provides a comprehensive, evidence-based platform for sports medicine injury prevention. It:

1. **Tracks Training**: Kinexon GPS data with auto-calculated training load
2. **Assesses Risk**: Multi-factor analysis combining ACWR, monotony, z-scores, and lifestyle modifiers
3. **Predicts Recovery**: Evidence-based timelines with research citations
4. **Visualizes Data**: Interactive charts and color-coded risk indicators
5. **Educates Users**: Research links and justifications for all predictions
6. **Scales Efficiently**: Works with small datasets (5+ athletes), no ML required

The hybrid evidence-based approach ensures:
- **Transparency**: Every calculation explained
- **Credibility**: Backed by peer-reviewed research
- **Practicality**: Works immediately without training data
- **Accuracy**: Based on validated sports science

All calculations are deterministic, explainable, and traceable to scientific literature, making the system ideal for clinical use in professional and collegiate sports settings.
