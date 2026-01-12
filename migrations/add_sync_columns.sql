-- Migration: Add sync columns to episodic_memory
-- Date: 2026-01-12
-- Purpose: Enable bidirectional sync PC <-> Cloud

-- Add sync-related columns
ALTER TABLE nexus_memory.zep_episodic_memory
ADD COLUMN IF NOT EXISTS device_id VARCHAR(50) DEFAULT 'nexus-pc',
ADD COLUMN IF NOT EXISTS sync_status VARCHAR(20) DEFAULT 'synced',
ADD COLUMN IF NOT EXISTS last_modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Create indexes for efficient sync queries
CREATE INDEX IF NOT EXISTS idx_last_modified ON nexus_memory.zep_episodic_memory(last_modified_at);
CREATE INDEX IF NOT EXISTS idx_device_id ON nexus_memory.zep_episodic_memory(device_id);
CREATE INDEX IF NOT EXISTS idx_sync_status ON nexus_memory.zep_episodic_memory(sync_status);

-- Create trigger to auto-update last_modified_at
CREATE OR REPLACE FUNCTION update_modified_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_episodic_memory_modtime ON nexus_memory.zep_episodic_memory;
CREATE TRIGGER update_episodic_memory_modtime
BEFORE UPDATE ON nexus_memory.zep_episodic_memory
FOR EACH ROW
EXECUTE FUNCTION update_modified_timestamp();

-- Update existing rows to set device_id based on tags
UPDATE nexus_memory.zep_episodic_memory
SET device_id = CASE
    WHEN 'laptop' = ANY(tags) THEN 'nexus-laptop'
    WHEN 'mobile' = ANY(tags) THEN 'nexus-mobile'
    ELSE 'nexus-pc'
END
WHERE device_id = 'nexus-pc';

-- Set all existing episodes as 'synced' (already in Cloud)
UPDATE nexus_memory.zep_episodic_memory
SET sync_status = 'synced'
WHERE sync_status IS NULL;
