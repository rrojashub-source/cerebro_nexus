#!/usr/bin/env python3
"""
PERSISTENCIA - Phase 1 Week 1 Day 3
Assemble and Validate Z_ID Complete (1024D)

Author: NEXUS
Date: November 11, 2025
Version: 1.0.0
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from scipy.spatial.distance import cosine

# Configuration
PROJECT_ROOT = Path("/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA")
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
COMPONENTS_FILE = PROCESSED_DIR / "z_id_components_20251111.npz"

def load_components():
    """Load Z_ID components from Day 2."""
    print("📦 Loading Z_ID components from Day 2...")

    data = np.load(COMPONENTS_FILE)

    core = data['core']
    experience = data['experience']
    methodology = data['methodology']
    drift = data['drift']

    print(f"  ✅ Core:        {core.shape}")
    print(f"  ✅ Experience:  {experience.shape}")
    print(f"  ✅ Methodology: {methodology.shape}")
    print(f"  ✅ Drift:       {drift.shape}")
    print()

    return core, experience, methodology, drift

def assemble_z_id(core, experience, methodology, drift):
    """Assemble complete Z_ID by concatenating components."""
    print("🔧 Assembling complete Z_ID vector...")

    # Concatenate in order: Core + Experience + Methodology + Drift
    z_id = np.concatenate([core, experience, methodology, drift])

    print(f"  ✅ Z_ID assembled: {z_id.shape}")
    print(f"  ✅ Expected: (1024,), Actual: {z_id.shape}")

    if z_id.shape[0] != 1024:
        print(f"  ⚠️  WARNING: Expected 1024D, got {z_id.shape[0]}D")

    print()
    return z_id

def validate_z_id(z_id):
    """Validate Z_ID mathematical properties."""
    print("🔍 Validating Z_ID properties...")

    validations = {}

    # 1. Dimensionality
    is_1024d = z_id.shape[0] == 1024
    validations['dimensionality'] = is_1024d
    print(f"  {'✅' if is_1024d else '❌'} Dimensionality: {z_id.shape[0]} == 1024")

    # 2. No NaN
    has_no_nan = not np.isnan(z_id).any()
    validations['no_nan'] = has_no_nan
    print(f"  {'✅' if has_no_nan else '❌'} No NaN values: {has_no_nan}")

    # 3. No Inf
    has_no_inf = not np.isinf(z_id).any()
    validations['no_inf'] = has_no_inf
    print(f"  {'✅' if has_no_inf else '❌'} No Inf values: {has_no_inf}")

    # 4. Norm calculation
    norm = np.linalg.norm(z_id)
    validations['norm'] = float(norm)
    print(f"  ℹ️  Norm: {norm:.6f}")

    # 5. Value distribution
    mean = np.mean(z_id)
    std = np.std(z_id)
    min_val = np.min(z_id)
    max_val = np.max(z_id)
    validations['mean'] = float(mean)
    validations['std'] = float(std)
    validations['min'] = float(min_val)
    validations['max'] = float(max_val)

    print(f"  ℹ️  Mean: {mean:.6f}")
    print(f"  ℹ️  Std:  {std:.6f}")
    print(f"  ℹ️  Min:  {min_val:.6f}")
    print(f"  ℹ️  Max:  {max_val:.6f}")

    # 6. Sparsity
    zero_threshold = 1e-6
    sparsity = np.sum(np.abs(z_id) < zero_threshold) / len(z_id)
    validations['sparsity'] = float(sparsity)
    print(f"  ℹ️  Sparsity: {sparsity*100:.2f}% (values < {zero_threshold})")

    print()
    return validations

def analyze_component_similarity(core, experience, methodology, drift):
    """Analyze cosine similarity between components."""
    print("🔍 Analyzing inter-component similarity...")

    # Pad methodology and drift to 384D for fair comparison
    methodology_padded = np.pad(methodology, (0, 384 - len(methodology)), mode='constant')
    drift_padded = np.pad(drift, (0, 384 - len(drift)), mode='constant')

    components = {
        'Core': core,
        'Experience': experience,
        'Methodology': methodology_padded,
        'Drift': drift_padded
    }

    similarities = {}

    names = list(components.keys())
    for i, name1 in enumerate(names):
        for j, name2 in enumerate(names):
            if i < j:  # Only upper triangle
                vec1 = components[name1]
                vec2 = components[name2]

                # Cosine similarity = 1 - cosine distance
                similarity = 1 - cosine(vec1, vec2)
                pair_key = f"{name1}-{name2}"
                similarities[pair_key] = float(similarity)

                print(f"  {name1:12} vs {name2:12}: {similarity:+.4f}")

    print()
    return similarities

def create_distribution_analysis(z_id):
    """Create distribution analysis of Z_ID values."""
    print("📊 Analyzing value distribution...")

    # Histogram bins
    hist, bin_edges = np.histogram(z_id, bins=20)

    distribution = {
        'histogram': hist.tolist(),
        'bin_edges': bin_edges.tolist()
    }

    # Percentiles
    percentiles = [0, 25, 50, 75, 100]
    percentile_values = np.percentile(z_id, percentiles)

    distribution['percentiles'] = {
        f'p{p}': float(v) for p, v in zip(percentiles, percentile_values)
    }

    print(f"  ℹ️  Percentiles:")
    for p, v in zip(percentiles, percentile_values):
        print(f"      P{p:3d}: {v:+.6f}")

    print()
    return distribution

def save_z_id_baseline(z_id, validations, similarities, distribution):
    """Save complete Z_ID baseline for future comparisons."""
    print("💾 Saving Z_ID baseline...")

    # Save Z_ID vector
    z_id_file = PROCESSED_DIR / "z_id_baseline_20251111.npy"
    np.save(z_id_file, z_id)
    print(f"  ✅ Z_ID vector saved: {z_id_file}")

    # Save validation report
    report = {
        "creation_date": datetime.now().isoformat(),
        "agent_id": "nexus",
        "version": "1.0.0",
        "z_id": {
            "dimensions": 1024,
            "components": {
                "core": {"start": 0, "end": 384, "size": 384},
                "experience": {"start": 384, "end": 768, "size": 384},
                "methodology": {"start": 768, "end": 896, "size": 128},
                "drift": {"start": 896, "end": 1024, "size": 128}
            }
        },
        "validations": validations,
        "component_similarities": similarities,
        "distribution": distribution
    }

    report_file = PROCESSED_DIR / "z_id_baseline_report_20251111.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  ✅ Validation report saved: {report_file}")

    print()

def main():
    print("=" * 60)
    print("PERSISTENCIA - Phase 1 Week 1 Day 3")
    print("Assembling and Validating Z_ID Complete (1024D)")
    print("=" * 60)
    print()

    # Load components
    core, experience, methodology, drift = load_components()

    # Assemble Z_ID
    z_id = assemble_z_id(core, experience, methodology, drift)

    # Validate
    validations = validate_z_id(z_id)

    # Analyze similarity
    similarities = analyze_component_similarity(core, experience, methodology, drift)

    # Distribution analysis
    distribution = create_distribution_analysis(z_id)

    # Save baseline
    save_z_id_baseline(z_id, validations, similarities, distribution)

    # Final summary
    print("=" * 60)
    print("✅ DAY 3 COMPLETE")
    print("=" * 60)
    print()
    print(f"📊 Z_ID BASELINE CREATED:")
    print(f"  • Dimensions: 1024D")
    print(f"  • Norm: {validations['norm']:.6f}")
    print(f"  • All validations: {'PASS' if all([validations['dimensionality'], validations['no_nan'], validations['no_inf']]) else 'FAIL'}")
    print()
    print("🎯 NEXT: Day 4 - Calculate baseline C_i (coherence score)")

if __name__ == "__main__":
    main()
