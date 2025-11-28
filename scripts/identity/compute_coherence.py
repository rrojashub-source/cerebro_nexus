#!/usr/bin/env python3
"""
PERSISTENCIA - Phase 1 Week 1 Day 4
Calculate Baseline C_i (Identity Coherence Score)

Formula: C_i = (1/(T-1)) * Σ_{t=1}^{T-1} cos(z_i^t, z_i^{t+1})

Author: NEXUS
Date: November 11, 2025
Version: 1.0.0
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

# Configuration
PROJECT_ROOT = Path("/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA")
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EPISODES_FILE = RAW_DIR / "nexus_episodes_20251111.json"

print("🔄 Loading sentence-transformers model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded\n")

def load_episodes():
    """Load and parse all episodes."""
    print("📖 Loading episodes...")
    episodes = []

    with open(EPISODES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                episode = json.loads(line.strip())
                episodes.append(episode)
            except json.JSONDecodeError:
                continue

    # Sort by timestamp
    episodes = sorted(episodes, key=lambda e: e.get('timestamp', ''))

    print(f"  ✅ Loaded {len(episodes)} episodes\n")
    return episodes

def create_temporal_checkpoints(episodes, num_checkpoints=10):
    """Divide episodes into temporal checkpoints."""
    print(f"📍 Creating {num_checkpoints} temporal checkpoints...")

    if not episodes:
        return []

    # Get temporal boundaries
    first_ts = datetime.fromisoformat(episodes[0]['timestamp'].replace('Z', '+00:00'))
    last_ts = datetime.fromisoformat(episodes[-1]['timestamp'].replace('Z', '+00:00'))

    print(f"  ℹ️  Timeline: {first_ts.date()} → {last_ts.date()}")

    time_span = (last_ts - first_ts).total_seconds()
    checkpoint_interval = time_span / num_checkpoints

    checkpoints = []

    for i in range(num_checkpoints):
        checkpoint_time = first_ts.timestamp() + ((i + 1) * checkpoint_interval)
        checkpoint_dt = datetime.fromtimestamp(checkpoint_time, tz=first_ts.tzinfo)

        # Get all episodes up to this checkpoint
        episodes_until_checkpoint = [
            ep for ep in episodes
            if datetime.fromisoformat(ep['timestamp'].replace('Z', '+00:00')).timestamp() <= checkpoint_time
        ]

        if len(episodes_until_checkpoint) > 100:  # Minimum episodes for meaningful Z_ID
            checkpoints.append({
                'date': checkpoint_dt,
                'episodes': episodes_until_checkpoint,
                'count': len(episodes_until_checkpoint)
            })

            print(f"  ✅ Checkpoint {i+1}: {checkpoint_dt.date()} ({len(episodes_until_checkpoint)} episodes)")

    print()
    return checkpoints

def compute_simple_z_id(episodes, target_dim=1024):
    """
    Compute simplified Z_ID from episodes.

    Strategy: Weighted average of all episode embeddings.
    Simpler than Day 2's categorization, but sufficient for coherence measurement.
    """
    if not episodes or len(episodes) < 10:
        return np.zeros(target_dim)

    # Sample if too many (for performance)
    if len(episodes) > 500:
        # Sample most important episodes
        episodes = sorted(episodes, key=lambda e: e.get('importance_score', 0) or 0, reverse=True)[:500]

    # Extract content and importance
    contents = [ep.get('content', '')[:1000] for ep in episodes]
    importances = np.array([ep.get('importance_score', 0.5) or 0.5 for ep in episodes])

    # Generate embeddings (384D from model)
    embeddings = model.encode(contents, show_progress_bar=False)

    # Weighted average
    weighted_embeddings = embeddings * importances[:, np.newaxis]
    avg_embedding = np.mean(weighted_embeddings, axis=0)

    # Normalize
    norm = np.linalg.norm(avg_embedding)
    if norm > 0:
        avg_embedding = avg_embedding / norm

    # Pad to target dimension (1024D)
    current_dim = avg_embedding.shape[0]
    if current_dim < target_dim:
        z_id = np.pad(avg_embedding, (0, target_dim - current_dim), mode='constant')
    elif current_dim > target_dim:
        z_id = avg_embedding[:target_dim]
    else:
        z_id = avg_embedding

    return z_id

def compute_coherence_score(checkpoints):
    """
    Calculate C_i from temporal Z_ID trajectory.

    C_i = (1/(T-1)) * Σ cos(z_i^t, z_i^{t+1})
    """
    print("🧮 Computing Identity Coherence Score (C_i)...")

    if len(checkpoints) < 2:
        print("  ⚠️  Warning: Need at least 2 checkpoints")
        return 0.0, []

    # Compute Z_ID at each checkpoint
    z_id_trajectory = []

    for i, checkpoint in enumerate(checkpoints, 1):
        print(f"  🔄 Computing Z_ID for checkpoint {i}/{len(checkpoints)}...")

        z_id = compute_simple_z_id(checkpoint['episodes'], target_dim=1024)
        z_id_trajectory.append({
            'date': checkpoint['date'].isoformat(),
            'episode_count': checkpoint['count'],
            'z_id': z_id
        })

    print()

    # Calculate cosine similarity between consecutive checkpoints
    print("  📊 Calculating temporal similarities...")

    similarities = []
    for i in range(len(z_id_trajectory) - 1):
        z1 = z_id_trajectory[i]['z_id']
        z2 = z_id_trajectory[i+1]['z_id']

        similarity = 1 - cosine(z1, z2)
        similarities.append(similarity)

        date1 = z_id_trajectory[i]['date'][:10]
        date2 = z_id_trajectory[i+1]['date'][:10]
        print(f"      {date1} → {date2}: {similarity:.4f}")

    # Coherence Score = Average similarity
    c_i = np.mean(similarities)

    print()
    print(f"  ✅ Identity Coherence Score (C_i): {c_i:.4f}")
    print()

    return c_i, similarities

def evaluate_coherence(c_i):
    """Evaluate coherence score against thresholds."""
    print("📈 Evaluating coherence...")

    if c_i >= 0.85:
        status = "EXCELLENT"
        emoji = "🟢"
        interpretation = "Robust, stable identity"
    elif c_i >= 0.70:
        status = "GOOD"
        emoji = "🟡"
        interpretation = "Coherent identity with some evolution"
    elif c_i >= 0.50:
        status = "MODERATE"
        emoji = "🟠"
        interpretation = "Significant identity drift detected"
    else:
        status = "LOW"
        emoji = "🔴"
        interpretation = "Identity instability - investigate"

    print(f"  {emoji} Status: {status}")
    print(f"  ℹ️  Interpretation: {interpretation}")
    print()

    thresholds = {
        'excellent': 0.85,
        'good': 0.70,
        'moderate': 0.50
    }

    return {
        'status': status,
        'interpretation': interpretation,
        'thresholds': thresholds
    }

def save_results(c_i, similarities, evaluation):
    """Save coherence analysis results."""
    print("💾 Saving coherence results...")

    report = {
        "computation_date": datetime.now().isoformat(),
        "agent_id": "nexus",
        "coherence_score": {
            "c_i": float(c_i),
            "formula": "C_i = (1/(T-1)) * Σ cos(z_i^t, z_i^{t+1})",
            "temporal_similarities": [float(s) for s in similarities],
            "num_checkpoints": len(similarities) + 1
        },
        "evaluation": evaluation,
        "interpretation": {
            "c_i >= 0.85": "Robust identity (target)",
            "c_i >= 0.70": "Good coherence",
            "c_i >= 0.50": "Moderate drift",
            "c_i < 0.50": "Identity instability"
        }
    }

    report_file = PROCESSED_DIR / "coherence_baseline_20251111.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"  ✅ Report saved: {report_file}")
    print()

def main():
    print("=" * 60)
    print("PERSISTENCIA - Phase 1 Week 1 Day 4")
    print("Calculate Baseline C_i (Identity Coherence Score)")
    print("=" * 60)
    print()

    # Load episodes
    episodes = load_episodes()

    # Create temporal checkpoints
    checkpoints = create_temporal_checkpoints(episodes, num_checkpoints=10)

    if len(checkpoints) < 2:
        print("❌ ERROR: Not enough checkpoints for coherence calculation")
        return

    # Compute coherence
    c_i, similarities = compute_coherence_score(checkpoints)

    # Evaluate
    evaluation = evaluate_coherence(c_i)

    # Save results
    save_results(c_i, similarities, evaluation)

    # Final summary
    print("=" * 60)
    print("✅ DAY 4 COMPLETE")
    print("=" * 60)
    print()
    print(f"📊 BASELINE C_i ESTABLISHED:")
    print(f"  • Coherence Score: {c_i:.4f}")
    print(f"  • Status: {evaluation['status']}")
    print(f"  • Checkpoints: {len(similarities) + 1}")
    print()
    print("🎯 NEXT: Day 5 - Extend database schema for GIC")

if __name__ == "__main__":
    main()
