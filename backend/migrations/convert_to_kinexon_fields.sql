-- Migration: Convert training_loads table to use Kinexon fields only
-- This migration removes old training load fields and adds Kinexon-specific fields

-- Step 1: Add new Kinexon columns
ALTER TABLE training_loads ADD COLUMN distance_miles FLOAT;
ALTER TABLE training_loads ADD COLUMN accumulated_accel_load FLOAT;
ALTER TABLE training_loads ADD COLUMN average_speed_mph FLOAT;
ALTER TABLE training_loads ADD COLUMN max_speed_mph FLOAT;

-- Step 2: Update session_type column (already exists, but ensure it's the right type)
-- No change needed - already exists as String

-- Step 3: For existing data, try to migrate what we can
-- If old total_distance exists (assumed in meters), convert to miles
UPDATE training_loads
SET distance_miles = total_distance * 0.000621371
WHERE total_distance IS NOT NULL AND distance_miles IS NULL;

-- If old max_speed exists (assumed in m/s), convert to mph
UPDATE training_loads
SET max_speed_mph = max_speed * 2.23694
WHERE max_speed IS NOT NULL AND max_speed_mph IS NULL;

-- Step 4: Drop old columns that are no longer used
ALTER TABLE training_loads DROP COLUMN IF EXISTS total_distance;
ALTER TABLE training_loads DROP COLUMN IF EXISTS high_speed_distance;
ALTER TABLE training_loads DROP COLUMN IF EXISTS sprint_distance;
ALTER TABLE training_loads DROP COLUMN IF EXISTS accelerations;
ALTER TABLE training_loads DROP COLUMN IF EXISTS decelerations;
ALTER TABLE training_loads DROP COLUMN IF EXISTS max_speed;
ALTER TABLE training_loads DROP COLUMN IF EXISTS duration;
ALTER TABLE training_loads DROP COLUMN IF EXISTS player_load;
ALTER TABLE training_loads DROP COLUMN IF EXISTS metabolic_power;

-- Step 5: Make required fields NOT NULL (after ensuring data is populated)
-- Note: You may need to delete records that don't have the required fields
-- or set default values before running these ALTER statements

-- DELETE FROM training_loads WHERE distance_miles IS NULL OR accumulated_accel_load IS NULL;

-- ALTER TABLE training_loads ALTER COLUMN distance_miles SET NOT NULL;
-- ALTER TABLE training_loads ALTER COLUMN accumulated_accel_load SET NOT NULL;

-- Note: Uncomment the above lines only after ensuring all records have required data
-- or after backing up and accepting data loss for incomplete records
