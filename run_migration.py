#!/usr/bin/env python3
"""
Run migration script to add sync columns to Cloud PostgreSQL
Date: 2026-01-12
"""

import psycopg2
import sys

# Cloud PostgreSQL connection
DB_CONFIG = {
    "host": "top2.nearest.of.nexus-cerebro-postgres-v2.internal",
    "port": 5432,
    "database": "nexus_memory",
    "user": "nexus_superuser",
    "password": "RpKeuQhnwqMOA4iQPILQshWtwFj0P2hm"
}

SQL_MIGRATION = """
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
"""

def run_migration():
    """Execute migration SQL"""
    try:
        print("🔄 Conectando a Cloud PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("🔄 Ejecutando migración SQL...")
        cursor.execute(SQL_MIGRATION)

        conn.commit()
        print("✅ Migración completada exitosamente")

        # Verificar columnas agregadas
        cursor.execute("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_schema = 'nexus_memory'
              AND table_name = 'zep_episodic_memory'
              AND column_name IN ('device_id', 'sync_status', 'last_modified_at')
            ORDER BY column_name;
        """)

        columns = cursor.fetchall()
        print(f"\n📊 Columnas agregadas ({len(columns)}):")
        for col_name, col_type, col_default in columns:
            print(f"  - {col_name}: {col_type} (default: {col_default})")

        # Verificar indexes
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'nexus_memory'
              AND tablename = 'zep_episodic_memory'
              AND indexname LIKE 'idx_%'
            ORDER BY indexname;
        """)

        indexes = cursor.fetchall()
        print(f"\n📊 Indexes creados ({len(indexes)}):")
        for (idx_name,) in indexes:
            print(f"  - {idx_name}")

        # Estadísticas de device_id
        cursor.execute("""
            SELECT device_id, COUNT(*) as count
            FROM nexus_memory.zep_episodic_memory
            GROUP BY device_id
            ORDER BY count DESC;
        """)

        stats = cursor.fetchall()
        print(f"\n📊 Episodios por dispositivo:")
        for device, count in stats:
            print(f"  - {device}: {count:,}")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ Error en migración: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
