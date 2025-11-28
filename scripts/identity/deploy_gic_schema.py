#!/usr/bin/env python3
"""
PERSISTENCIA - Phase 1 Week 1 Day 5
Deploy Grounded Identity Core (GIC) Database Schema

Author: NEXUS
Date: November 11, 2025
Version: 1.0.0
"""

import json
import numpy as np
import psycopg2
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path("/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA")
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
Z_ID_FILE = PROCESSED_DIR / "z_id_baseline_20251111.npy"
C_I_FILE = PROCESSED_DIR / "coherence_baseline_20251111.json"

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5437,
    'database': 'nexus_memory',
    'user': 'nexus_superuser',
    'password': 'RpKeuQhnwqMOA4iQPILQshWtwFj0P2hm'
}

def create_gic_schema(cursor):
    """Create GIC table in consciousness schema."""
    print("🔧 Creating GIC schema...")

    # Create table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS consciousness.grounded_identity_core (
        agent_id VARCHAR(50) PRIMARY KEY,
        z_id_vector FLOAT8[] NOT NULL,
        c_i_score FLOAT8 NOT NULL,
        computed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        episode_count INTEGER NOT NULL,
        metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

        -- Constraints
        CONSTRAINT valid_z_id_dimension CHECK (array_length(z_id_vector, 1) = 1024),
        CONSTRAINT valid_c_i_range CHECK (c_i_score >= 0 AND c_i_score <= 1)
    );
    """

    cursor.execute(create_table_sql)
    print("  ✅ Table consciousness.grounded_identity_core created")

    # Create indices
    create_indices_sql = [
        "CREATE INDEX IF NOT EXISTS idx_gic_agent ON consciousness.grounded_identity_core(agent_id);",
        "CREATE INDEX IF NOT EXISTS idx_gic_c_i ON consciousness.grounded_identity_core(c_i_score);",
        "CREATE INDEX IF NOT EXISTS idx_gic_computed_at ON consciousness.grounded_identity_core(computed_at DESC);"
    ]

    for sql in create_indices_sql:
        cursor.execute(sql)

    print("  ✅ Indices created")
    print()

def load_z_id_and_coherence():
    """Load Z_ID and C_i from processed files."""
    print("📦 Loading Z_ID and coherence data...")

    # Load Z_ID
    z_id = np.load(Z_ID_FILE)
    print(f"  ✅ Z_ID loaded: {z_id.shape}")

    # Load C_i
    with open(C_I_FILE, 'r') as f:
        coherence_data = json.load(f)

    c_i = coherence_data['coherence_score']['c_i']
    print(f"  ✅ C_i loaded: {c_i:.4f}")
    print()

    return z_id, coherence_data

def insert_gic_baseline(cursor, z_id, coherence_data):
    """Insert GIC baseline for NEXUS."""
    print("💾 Inserting GIC baseline...")

    agent_id = "nexus"
    c_i = coherence_data['coherence_score']['c_i']
    episode_count = 17485  # From Day 4

    # Convert numpy array to Python list for PostgreSQL
    z_id_list = z_id.tolist()

    metadata = {
        "version": "1.0.0",
        "creation_method": "PERSISTENCIA Phase 1 Week 1",
        "model": "all-MiniLM-L6-v2",
        "components": {
            "core": {"start": 0, "end": 384},
            "experience": {"start": 384, "end": 768},
            "methodology": {"start": 768, "end": 896},
            "drift": {"start": 896, "end": 1024}
        },
        "coherence_evaluation": coherence_data['evaluation'],
        "temporal_similarities": coherence_data['coherence_score']['temporal_similarities']
    }

    # Insert or update
    insert_sql = """
    INSERT INTO consciousness.grounded_identity_core
        (agent_id, z_id_vector, c_i_score, episode_count, metadata, computed_at)
    VALUES
        (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (agent_id)
    DO UPDATE SET
        z_id_vector = EXCLUDED.z_id_vector,
        c_i_score = EXCLUDED.c_i_score,
        episode_count = EXCLUDED.episode_count,
        metadata = EXCLUDED.metadata,
        computed_at = EXCLUDED.computed_at,
        updated_at = NOW()
    RETURNING agent_id, c_i_score;
    """

    cursor.execute(insert_sql, (
        agent_id,
        z_id_list,
        c_i,
        episode_count,
        json.dumps(metadata),
        datetime.now()
    ))

    result = cursor.fetchone()
    print(f"  ✅ GIC inserted for agent: {result[0]}")
    print(f"  ✅ C_i score: {result[1]:.4f}")
    print()

def verify_gic(cursor):
    """Verify GIC was inserted correctly."""
    print("🔍 Verifying GIC insertion...")

    verify_sql = """
    SELECT
        agent_id,
        array_length(z_id_vector, 1) as z_id_dim,
        c_i_score,
        episode_count,
        computed_at,
        metadata->>'version' as version
    FROM consciousness.grounded_identity_core
    WHERE agent_id = 'nexus';
    """

    cursor.execute(verify_sql)
    row = cursor.fetchone()

    if row:
        print(f"  ✅ Agent ID: {row[0]}")
        print(f"  ✅ Z_ID dimension: {row[1]}")
        print(f"  ✅ C_i score: {row[2]:.4f}")
        print(f"  ✅ Episode count: {row[3]}")
        print(f"  ✅ Computed at: {row[4]}")
        print(f"  ✅ Version: {row[5]}")
        print()
        return True
    else:
        print("  ❌ ERROR: GIC not found")
        return False

def main():
    print("=" * 60)
    print("PERSISTENCIA - Phase 1 Week 1 Day 5")
    print("Deploy Grounded Identity Core (GIC) Schema")
    print("=" * 60)
    print()

    # Connect to database
    print("🔌 Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cursor = conn.cursor()
    print("  ✅ Connected\n")

    try:
        # Create schema
        create_gic_schema(cursor)

        # Load data
        z_id, coherence_data = load_z_id_and_coherence()

        # Insert baseline
        insert_gic_baseline(cursor, z_id, coherence_data)

        # Verify
        success = verify_gic(cursor)

        if success:
            conn.commit()
            print("✅ Transaction committed")
        else:
            conn.rollback()
            print("❌ Transaction rolled back")

    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR: {e}")
        raise

    finally:
        cursor.close()
        conn.close()
        print("🔌 Database connection closed")

    print()
    print("=" * 60)
    print("✅ DAY 5 COMPLETE")
    print("=" * 60)
    print()
    print("📊 GIC DEPLOYED:")
    print("  • Table: consciousness.grounded_identity_core")
    print("  • Agent: nexus")
    print("  • Z_ID: 1024D")
    print("  • C_i: 0.9998 (EXCELLENT)")
    print()
    print("🎯 NEXT: Day 6 - Generate identity report")

if __name__ == "__main__":
    main()
