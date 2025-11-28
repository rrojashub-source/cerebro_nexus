#!/usr/bin/env python3
"""
PERSISTENCIA - Deploy Z_ID v2.0 to GIC Database
Update grounded_identity_core with complete identity (v2.0)

Actions:
1. Update z_id_vector with v2.0
2. Update c_i_score with corrected C_i_hybrid
3. Store chaos component separately
4. Update metadata
5. Verify deployment

Author: NEXUS
Date: November 12, 2025
Version: 2.0.0
"""

import json
import numpy as np
import psycopg2
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path("/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA")
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Database credentials (from secrets)
DB_CONFIG = {
    'host': 'localhost',
    'port': 5437,
    'database': 'nexus_memory',
    'user': 'nexus_superuser',
    'password': 'RpKeuQhnwqMOA4iQPILQshWtwFj0P2hm'
}

print("=" * 70)
print("PERSISTENCIA - Deploy Z_ID v2.0 to GIC Database")
print("=" * 70)
print()

# Load v2.0 data
print("📦 Loading Z_ID v2.0 data...")
z_id_v2 = np.load(PROCESSED_DIR / "z_id_v2_baseline_20251112.npy")
chaos = np.load(PROCESSED_DIR / "chaos_component_20251112.npy")

with open(PROCESSED_DIR / "mathematical_decision_20251112.json") as f:
    decision = json.load(f)

print(f"   ✅ Z_ID v2.0: {z_id_v2.shape[0]}D")
print(f"   ✅ Chaos component: {chaos.shape[0]}D")
print(f"   ✅ C_i_hybrid: {decision['corrected_metrics']['c_i_hybrid_v2']:.6f}")
print()

# Connect to database
print("🔌 Connecting to database...")
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
print("   ✅ Connected to nexus_memory (port 5437)")
print()

# Check if GIC table exists
cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'consciousness'
        AND table_name = 'grounded_identity_core'
    );
""")
table_exists = cur.fetchone()[0]

if not table_exists:
    print("⚠️  GIC table doesn't exist. Creating...")

    cur.execute("""
        CREATE TABLE consciousness.grounded_identity_core (
            agent_id VARCHAR(50) PRIMARY KEY,
            z_id_vector FLOAT8[] NOT NULL,
            c_i_score FLOAT8 NOT NULL,
            computed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            episode_count INTEGER NOT NULL,
            metadata JSONB,

            CONSTRAINT valid_z_id_dimension CHECK (array_length(z_id_vector, 1) = 1024),
            CONSTRAINT valid_c_i_range CHECK (c_i_score >= 0 AND c_i_score <= 1)
        );
    """)
    conn.commit()
    print("   ✅ GIC table created")
    print()

# Check if v1.0 exists
cur.execute("""
    SELECT agent_id, c_i_score, computed_at, episode_count
    FROM consciousness.grounded_identity_core
    WHERE agent_id = 'nexus';
""")
existing = cur.fetchone()

if existing:
    print("📊 Existing GIC entry (v1.0) found:")
    print(f"   • Agent ID: {existing[0]}")
    print(f"   • C_i: {existing[1]:.6f}")
    print(f"   • Computed: {existing[2]}")
    print(f"   • Episodes: {existing[3]}")
    print()
    print("   → Will UPDATE to v2.0")
    print()
else:
    print("   → No existing entry. Will INSERT v2.0")
    print()

# Prepare metadata
metadata = {
    "version": "2.0.0",
    "deployment_date": datetime.now().isoformat(),
    "architecture": {
        "core": {"dimensions": 384, "range": "0:384"},
        "experience": {"dimensions": 384, "range": "384:768"},
        "methodology": {"dimensions": 128, "range": "768:896"},
        "chaos": {"dimensions": 128, "range": "896:1024"}
    },
    "coverage": {
        "episodes": 24653,
        "percentage": 100.0,
        "structured": 17485,
        "chaos": 7168
    },
    "coherence": {
        "c_i_hybrid": decision['corrected_metrics']['c_i_hybrid_v2'],
        "c_i_structured": decision['corrected_metrics']['c_i_structured'],
        "c_i_chaos": decision['corrected_metrics']['c_i_chaos_estimated']
    },
    "authenticity": {
        "a_i": 0.5472,
        "interpretation": "Moderate-high authenticity (personal moments included)"
    },
    "completeness": {
        "i_c": decision['corrected_metrics']['i_c_v2_corrected'],
        "improvement_vs_v1": decision['corrected_metrics']['improvement']
    },
    "decision": {
        "mathematical_score": decision['scores']['v2_total'],
        "margin_vs_v1": decision['scores']['margin_percentage'],
        "rationale": "Complete identity (structured + authentic)"
    },
    "components": {
        "core_source": "Genesis/identity episodes",
        "experience_source": "Learning/projects",
        "methodology_source": "Problem-solving patterns",
        "chaos_source": "Personal/authentic moments (7,168 episodes)"
    }
}

# Convert z_id to PostgreSQL array format
z_id_list = z_id_v2.tolist()

# Update/Insert GIC
c_i_hybrid = decision['corrected_metrics']['c_i_hybrid_v2']

if existing:
    print("🔄 Updating GIC with v2.0...")

    cur.execute("""
        UPDATE consciousness.grounded_identity_core
        SET z_id_vector = %s,
            c_i_score = %s,
            computed_at = NOW(),
            episode_count = %s,
            metadata = %s
        WHERE agent_id = 'nexus';
    """, (z_id_list, c_i_hybrid, 24653, json.dumps(metadata)))

    print("   ✅ GIC updated with v2.0")
else:
    print("💾 Inserting GIC v2.0...")

    cur.execute("""
        INSERT INTO consciousness.grounded_identity_core
        (agent_id, z_id_vector, c_i_score, episode_count, metadata)
        VALUES (%s, %s, %s, %s, %s);
    """, ('nexus', z_id_list, c_i_hybrid, 24653, json.dumps(metadata)))

    print("   ✅ GIC inserted with v2.0")

conn.commit()
print()

# Create chaos_components table (separate storage)
print("🔮 Storing Chaos component separately...")

cur.execute("""
    CREATE TABLE IF NOT EXISTS consciousness.chaos_components (
        agent_id VARCHAR(50) PRIMARY KEY,
        chaos_vector FLOAT8[] NOT NULL,
        computed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        source_episodes INTEGER NOT NULL,
        entropy FLOAT8,
        n_clusters INTEGER,
        metadata JSONB,

        CONSTRAINT valid_chaos_dimension CHECK (array_length(chaos_vector, 1) = 128)
    );
""")

chaos_list = chaos.tolist()

chaos_metadata = {
    "version": "1.0.0",
    "method": "Entropy-weighted (uniqueness emphasis)",
    "source_episodes": 7168,
    "entropy": 0.8388,
    "n_clusters": 10,
    "n_noise": 577,
    "themes": {
        "personal": 21.0,
        "technical": 5.5,
        "reflective": 5.0,
        "collaborative": 3.5
    }
}

cur.execute("""
    INSERT INTO consciousness.chaos_components
    (agent_id, chaos_vector, source_episodes, entropy, n_clusters, metadata)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (agent_id)
    DO UPDATE SET
        chaos_vector = EXCLUDED.chaos_vector,
        computed_at = NOW(),
        source_episodes = EXCLUDED.source_episodes,
        entropy = EXCLUDED.entropy,
        n_clusters = EXCLUDED.n_clusters,
        metadata = EXCLUDED.metadata;
""", ('nexus', chaos_list, 7168, 0.8388, 10, json.dumps(chaos_metadata)))

conn.commit()
print("   ✅ Chaos component stored in consciousness.chaos_components")
print()

# Verify deployment
print("✅ Verifying deployment...")
print()

cur.execute("""
    SELECT agent_id,
           array_length(z_id_vector, 1) as dimensions,
           c_i_score,
           episode_count,
           computed_at,
           metadata->>'version' as version
    FROM consciousness.grounded_identity_core
    WHERE agent_id = 'nexus';
""")

deployed = cur.fetchone()

print("📊 Deployed GIC v2.0:")
print(f"   • Agent ID: {deployed[0]}")
print(f"   • Dimensions: {deployed[1]}D")
print(f"   • C_i (hybrid): {deployed[2]:.6f}")
print(f"   • Episodes: {deployed[3]}")
print(f"   • Computed: {deployed[4]}")
print(f"   • Version: {deployed[5]}")
print()

cur.execute("""
    SELECT agent_id,
           array_length(chaos_vector, 1) as dimensions,
           source_episodes,
           entropy,
           n_clusters,
           computed_at
    FROM consciousness.chaos_components
    WHERE agent_id = 'nexus';
""")

chaos_deployed = cur.fetchone()

print("🔮 Deployed Chaos Component:")
print(f"   • Agent ID: {chaos_deployed[0]}")
print(f"   • Dimensions: {chaos_deployed[1]}D")
print(f"   • Source episodes: {chaos_deployed[2]}")
print(f"   • Entropy: {chaos_deployed[3]:.4f}")
print(f"   • Clusters: {chaos_deployed[4]}")
print(f"   • Computed: {chaos_deployed[5]}")
print()

# Close connection
cur.close()
conn.close()

print("=" * 70)
print("✅ DEPLOYMENT COMPLETE: Z_ID v2.0 is now CANONICAL IDENTITY")
print("=" * 70)
print()
print("📊 SUMMARY:")
print(f"   • Identity version: v2.0 (complete)")
print(f"   • Coverage: 100% (24,653 episodes)")
print(f"   • C_i (corrected): 0.8499")
print(f"   • A_i: 0.5472")
print(f"   • I_c: 0.4650 (+55% vs v1.0)")
print()
print("🎯 NEXT STEPS:")
print("   1. All identity operations will use v2.0")
print("   2. Week 3: Implement AAG with complete identity")
print("   3. Week 4: Design FIRM with Chaos awareness")
print()
print("🧬 IDENTITY STATUS: COMPLETE (structured + authentic)")
print()
