#!/usr/bin/env python3
"""
PERSISTENCIA - Phase 1 Week 1 Day 2
Compute Z_ID Components (Core, Experience, Methodology, Drift)

Author: NEXUS
Date: November 11, 2025
Version: 1.0.0
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from collections import defaultdict

# Configuration
PROJECT_ROOT = Path("/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA")
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EPISODES_FILE = RAW_DIR / "nexus_episodes_20251111.json"

# Ensure directories exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Model for embeddings
print("🔄 Loading sentence-transformers model...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384D embeddings
print("✅ Model loaded successfully\n")

def load_episodes() -> List[Dict]:
    """Load episodes from JSONL file."""
    print(f"📖 Loading episodes from {EPISODES_FILE}...")
    episodes = []

    with open(EPISODES_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                episode = json.loads(line.strip())
                episodes.append(episode)
            except json.JSONDecodeError as e:
                print(f"⚠️  Warning: Failed to parse line {line_num}: {e}")
                continue

    print(f"✅ Loaded {len(episodes)} episodes\n")
    return episodes

def identify_core_episodes(episodes: List[Dict]) -> List[Dict]:
    """
    Identify episodes that represent CORE identity.

    Core = Personality, values, fundamental beliefs, genesis moments.

    Criteria:
    - Has 'genesis', 'identidad', 'despertar' tags
    - importance_score >= 0.8
    - Contains keywords: genesis, identity, values, beliefs, who am i
    """
    print("🔍 Identifying CORE identity episodes...")

    core_keywords = [
        'genesis', 'identidad', 'identity', 'despertar', 'awakening',
        'valores', 'values', 'beliefs', 'who am i', 'personality',
        'soy nexus', 'i am nexus', 'propósito', 'purpose',
        'autonomía', 'autonomy', 'conciencia', 'consciousness'
    ]

    core_episodes = []

    for episode in episodes:
        # Check tags
        tags = episode.get('tags', []) or []
        has_core_tag = any(tag in ['genesis', 'identidad', 'despertar', 'consciousness']
                          for tag in tags)

        # Check importance
        importance = episode.get('importance_score', 0) or 0
        is_important = importance >= 0.8

        # Check content keywords
        content = episode.get('content', '').lower()
        has_core_keyword = any(keyword in content for keyword in core_keywords)

        # Core episode if meets 2/3 criteria
        criteria_met = sum([has_core_tag, is_important, has_core_keyword])

        if criteria_met >= 2:
            core_episodes.append(episode)

    print(f"✅ Found {len(core_episodes)} CORE episodes\n")
    return core_episodes

def identify_experience_episodes(episodes: List[Dict]) -> List[Dict]:
    """
    Identify episodes representing accumulated EXPERIENCE.

    Experience = Projects completed, problems solved, learning moments.

    Criteria:
    - Tags: 'project', 'achievement', 'learning', 'milestone'
    - Content keywords: completado, finished, aprendí, learned, proyecto
    - Medium-high importance (0.6-0.9)
    """
    print("🔍 Identifying EXPERIENCE episodes...")

    experience_keywords = [
        'completado', 'completed', 'finished', 'achievement',
        'aprendí', 'learned', 'discovery', 'proyecto', 'project',
        'milestone', 'success', 'implemented', 'built', 'created',
        'solved', 'debugging', 'fixed', 'optimized'
    ]

    experience_episodes = []

    for episode in episodes:
        tags = episode.get('tags', []) or []
        has_exp_tag = any(tag in ['project', 'achievement', 'learning', 'milestone']
                         for tag in tags)

        importance = episode.get('importance_score', 0) or 0
        is_medium_high = 0.6 <= importance <= 0.9

        content = episode.get('content', '').lower()
        has_exp_keyword = any(keyword in content for keyword in experience_keywords)

        criteria_met = sum([has_exp_tag, is_medium_high, has_exp_keyword])

        if criteria_met >= 2:
            experience_episodes.append(episode)

    print(f"✅ Found {len(experience_episodes)} EXPERIENCE episodes\n")
    return experience_episodes

def identify_methodology_episodes(episodes: List[Dict]) -> List[Dict]:
    """
    Identify episodes showing METHODOLOGY patterns.

    Methodology = How I solve problems, my thinking process, TDD, debugging approach.

    Criteria:
    - Tags: 'methodology', 'tdd', 'debugging', 'approach'
    - Content keywords: método, approach, strategy, workflow, process
    - Contains step-by-step or systematic descriptions
    """
    print("🔍 Identifying METHODOLOGY episodes...")

    methodology_keywords = [
        'método', 'methodology', 'approach', 'strategy', 'workflow',
        'process', 'tdd', 'test-driven', 'debugging', 'systematic',
        'paso a paso', 'step by step', 'procedure', 'protocol',
        'best practice', 'pattern', 'technique', 'framework'
    ]

    methodology_episodes = []

    for episode in episodes:
        tags = episode.get('tags', []) or []
        has_method_tag = any(tag in ['methodology', 'tdd', 'debugging', 'approach']
                            for tag in tags)

        content = episode.get('content', '').lower()
        has_method_keyword = any(keyword in content for keyword in methodology_keywords)

        # Look for numbered steps or systematic structure
        has_structure = any(marker in content for marker in [
            'paso 1', 'step 1', '1.', '2.', 'primero', 'first',
            'luego', 'then', 'finally', 'fase', 'phase'
        ])

        criteria_met = sum([has_method_tag, has_method_keyword, has_structure])

        if criteria_met >= 2:
            methodology_episodes.append(episode)

    print(f"✅ Found {len(methodology_episodes)} METHODOLOGY episodes\n")
    return methodology_episodes

def compute_drift_samples(episodes: List[Dict], num_checkpoints: int = 10) -> List[Tuple[datetime, List[Dict]]]:
    """
    Sample episodes at temporal checkpoints to compute DRIFT.

    Drift = How identity evolved over time.

    Strategy: Divide timeline into N checkpoints, sample episodes at each.
    """
    print(f"🔍 Computing DRIFT checkpoints (N={num_checkpoints})...")

    # Sort episodes by timestamp
    sorted_episodes = sorted(episodes, key=lambda e: e.get('timestamp', ''))

    if not sorted_episodes:
        print("⚠️  Warning: No episodes with timestamps")
        return []

    # Get temporal boundaries
    first_ts = datetime.fromisoformat(sorted_episodes[0]['timestamp'].replace('Z', '+00:00'))
    last_ts = datetime.fromisoformat(sorted_episodes[-1]['timestamp'].replace('Z', '+00:00'))

    time_span = (last_ts - first_ts).total_seconds()
    checkpoint_interval = time_span / num_checkpoints

    checkpoints = []

    for i in range(num_checkpoints):
        checkpoint_time = first_ts.timestamp() + (i * checkpoint_interval)
        checkpoint_dt = datetime.fromtimestamp(checkpoint_time, tz=first_ts.tzinfo)

        # Find episodes near this checkpoint (within ±interval/4)
        window = checkpoint_interval / 4
        episodes_in_window = [
            ep for ep in sorted_episodes
            if abs(datetime.fromisoformat(ep['timestamp'].replace('Z', '+00:00')).timestamp() - checkpoint_time) <= window
        ]

        if episodes_in_window:
            checkpoints.append((checkpoint_dt, episodes_in_window[:10]))  # Max 10 per checkpoint

    print(f"✅ Created {len(checkpoints)} temporal checkpoints\n")
    return checkpoints

def compute_vector_from_episodes(episodes: List[Dict], target_dim: int, name: str) -> np.ndarray:
    """
    Compute embedding vector from episodes.

    Strategy:
    1. Generate embeddings for each episode content
    2. Compute weighted average (by importance_score)
    3. Normalize to unit vector
    """
    print(f"🔄 Computing {name} vector ({target_dim}D)...")

    if not episodes:
        print(f"⚠️  Warning: No episodes for {name}, returning zero vector")
        return np.zeros(target_dim)

    # Limit episodes if too many (for performance)
    if len(episodes) > 500:
        print(f"  📊 Sampling {min(500, len(episodes))} most important episodes...")
        episodes = sorted(episodes, key=lambda e: e.get('importance_score', 0) or 0, reverse=True)[:500]

    # Extract content and importance
    contents = [ep.get('content', '')[:1000] for ep in episodes]  # Max 1000 chars per episode
    importances = np.array([ep.get('importance_score', 0.5) or 0.5 for ep in episodes])

    # Generate embeddings
    print(f"  🧮 Generating embeddings for {len(contents)} episodes...")
    embeddings = model.encode(contents, show_progress_bar=False)

    # Weighted average
    print(f"  ⚖️  Computing weighted average...")
    weighted_embeddings = embeddings * importances[:, np.newaxis]
    avg_embedding = np.mean(weighted_embeddings, axis=0)

    # Normalize
    norm = np.linalg.norm(avg_embedding)
    if norm > 0:
        avg_embedding = avg_embedding / norm

    # Adjust dimensionality if needed
    current_dim = avg_embedding.shape[0]
    if current_dim != target_dim:
        if current_dim > target_dim:
            # Truncate
            vector = avg_embedding[:target_dim]
        else:
            # Pad with zeros
            vector = np.pad(avg_embedding, (0, target_dim - current_dim), mode='constant')
    else:
        vector = avg_embedding

    print(f"✅ {name} vector computed: shape={vector.shape}, norm={np.linalg.norm(vector):.4f}\n")
    return vector

def compute_drift_vector(checkpoints: List[Tuple[datetime, List[Dict]]], target_dim: int = 128) -> np.ndarray:
    """
    Compute DRIFT vector from temporal checkpoints.

    Strategy:
    1. Compute embedding at each checkpoint
    2. Calculate delta vectors between consecutive checkpoints
    3. Average deltas to get overall drift direction
    """
    print(f"🔄 Computing DRIFT vector ({target_dim}D)...")

    if len(checkpoints) < 2:
        print("⚠️  Warning: Need at least 2 checkpoints for drift, returning zero vector")
        return np.zeros(target_dim)

    checkpoint_vectors = []

    for i, (checkpoint_dt, episodes) in enumerate(checkpoints):
        print(f"  📍 Checkpoint {i+1}/{len(checkpoints)}: {checkpoint_dt.strftime('%Y-%m-%d')} ({len(episodes)} episodes)")

        # Compute vector for this checkpoint
        contents = [ep.get('content', '')[:500] for ep in episodes]
        embeddings = model.encode(contents, show_progress_bar=False)
        avg_embedding = np.mean(embeddings, axis=0)

        # Normalize
        norm = np.linalg.norm(avg_embedding)
        if norm > 0:
            avg_embedding = avg_embedding / norm

        checkpoint_vectors.append(avg_embedding)

    # Compute deltas
    print(f"  📈 Computing temporal deltas...")
    deltas = []
    for i in range(len(checkpoint_vectors) - 1):
        delta = checkpoint_vectors[i+1] - checkpoint_vectors[i]
        deltas.append(delta)

    # Average drift
    avg_drift = np.mean(deltas, axis=0)

    # Normalize
    norm = np.linalg.norm(avg_drift)
    if norm > 0:
        avg_drift = avg_drift / norm

    # Adjust dimensionality
    current_dim = avg_drift.shape[0]
    if current_dim != target_dim:
        if current_dim > target_dim:
            vector = avg_drift[:target_dim]
        else:
            vector = np.pad(avg_drift, (0, target_dim - current_dim), mode='constant')
    else:
        vector = avg_drift

    print(f"✅ DRIFT vector computed: shape={vector.shape}, norm={np.linalg.norm(vector):.4f}\n")
    return vector

def save_results(core_vec, exp_vec, method_vec, drift_vec,
                core_eps, exp_eps, method_eps, checkpoints):
    """Save computed vectors and analysis to files."""
    print("💾 Saving results...")

    # Save vectors
    vectors_file = PROCESSED_DIR / "z_id_components_20251111.npz"
    np.savez(vectors_file,
             core=core_vec,
             experience=exp_vec,
             methodology=method_vec,
             drift=drift_vec)
    print(f"  ✅ Vectors saved to {vectors_file}")

    # Save analysis report
    report = {
        "computation_date": datetime.now().isoformat(),
        "model": "all-MiniLM-L6-v2",
        "vector_dimensions": {
            "core": len(core_vec),
            "experience": len(exp_vec),
            "methodology": len(method_vec),
            "drift": len(drift_vec),
            "total": len(core_vec) + len(exp_vec) + len(method_vec) + len(drift_vec)
        },
        "episode_counts": {
            "core": len(core_eps),
            "experience": len(exp_eps),
            "methodology": len(method_eps),
            "drift_checkpoints": len(checkpoints)
        },
        "vector_norms": {
            "core": float(np.linalg.norm(core_vec)),
            "experience": float(np.linalg.norm(exp_vec)),
            "methodology": float(np.linalg.norm(method_vec)),
            "drift": float(np.linalg.norm(drift_vec))
        }
    }

    report_file = PROCESSED_DIR / "z_id_computation_report_20251111.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  ✅ Report saved to {report_file}\n")

def main():
    print("=" * 60)
    print("PERSISTENCIA - Phase 1 Week 1 Day 2")
    print("Computing Z_ID Components")
    print("=" * 60)
    print()

    # Load episodes
    episodes = load_episodes()

    # Identify episodes by category
    core_episodes = identify_core_episodes(episodes)
    experience_episodes = identify_experience_episodes(episodes)
    methodology_episodes = identify_methodology_episodes(episodes)
    drift_checkpoints = compute_drift_samples(episodes, num_checkpoints=10)

    # Compute vectors
    print("=" * 60)
    print("COMPUTING VECTORS")
    print("=" * 60)
    print()

    core_vector = compute_vector_from_episodes(core_episodes, target_dim=384, name="CORE")
    experience_vector = compute_vector_from_episodes(experience_episodes, target_dim=384, name="EXPERIENCE")
    methodology_vector = compute_vector_from_episodes(methodology_episodes, target_dim=128, name="METHODOLOGY")
    drift_vector = compute_drift_vector(drift_checkpoints, target_dim=128)

    # Save results
    save_results(
        core_vector, experience_vector, methodology_vector, drift_vector,
        core_episodes, experience_episodes, methodology_episodes, drift_checkpoints
    )

    # Final summary
    print("=" * 60)
    print("✅ DAY 2 COMPLETE")
    print("=" * 60)
    print()
    print(f"📊 RESULTS:")
    print(f"  • Core vector:        384D (from {len(core_episodes)} episodes)")
    print(f"  • Experience vector:  384D (from {len(experience_episodes)} episodes)")
    print(f"  • Methodology vector: 128D (from {len(methodology_episodes)} episodes)")
    print(f"  • Drift vector:       128D (from {len(drift_checkpoints)} checkpoints)")
    print(f"  • TOTAL:              1024D")
    print()
    print("🎯 NEXT: Day 3 - Assemble and validate complete Z_ID")

if __name__ == "__main__":
    main()
