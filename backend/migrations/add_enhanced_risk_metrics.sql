-- Migration: Add Enhanced Risk Metrics to Risk Assessments Table
-- Date: 2025-11-04
-- Description: Adds new columns for Hybrid Evidence-Based System metrics

-- Add traditional metrics
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS acute_load REAL;
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS chronic_load REAL;

-- Add enhanced metrics (training monotony and strain)
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS training_monotony REAL;
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS training_strain REAL;

-- Add z-score spike detection metrics
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS current_z_score REAL;
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS max_z_score_7d REAL;

-- Add risk modifiers for compound risk scoring
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS sleep_modifier REAL;
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS stress_modifier REAL;
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS injury_recency_modifier REAL;
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS age_modifier REAL;
ALTER TABLE risk_assessments ADD COLUMN IF NOT EXISTS compound_multiplier REAL;

-- Create index for faster queries on new metrics
CREATE INDEX IF NOT EXISTS idx_risk_monotony ON risk_assessments(training_monotony);
CREATE INDEX IF NOT EXISTS idx_risk_strain ON risk_assessments(training_strain);

-- Display confirmation
SELECT 'Migration completed successfully' AS status;
