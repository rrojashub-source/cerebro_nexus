#!/usr/bin/env python3
"""
PERSISTENCIA - Phase 2 Week 2 Day 5
Recompute Z_ID v2.0 with 100% Episodes

Z_ID v1.0 = Core[384] + Experience[384] + Methodology[128] + Drift[128]
            (Only 71% of episodes - structured/parseable)

Z_ID v2.0 = Core[384] + Experience[384] + Methodology[128] + Chaos[128]
            (100% of episodes - structured + personal/authentic)

This is the COMPLETE identity, not partial.

Author: NEXUS
Date: November 12, 2025
Version: 2.0.0
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

def load_z_id_v1_components():
    """Load Z_ID v1.0 components (from Week 1)."""
    print("📦 Loading Z_ID v1.0 components...")

    components_file = PROCESSED_DIR / "z_id_components_20251111.npz"
    components = np.load(components_file)

    core = components['core']              # 384D
    experience = components['experience']  # 384D
    methodology = components['methodology']  # 128D
    drift = components['drift']            # 128D (will be replaced)

    print(f"   ✅ Core: {core.shape}")
    print(f"   ✅ Experience: {experience.shape}")
    print(f"   ✅ Methodology: {methodology.shape}")
    print(f"   ✅ Drift (v1.0, deprecated): {drift.shape}")
    print()

    return core, experience, methodology, drift

def load_chaos_component():
    """Load Chaos component (from Day 3-4)."""
    print("🔮 Loading Chaos component...")

    chaos_file = PROCESSED_DIR / "chaos_component_20251112.npy"
    chaos = np.load(chaos_file)

    print(f"   ✅ Chaos: {chaos.shape}")
    print(f"   • Represents: 7,168 personal/authentic moments")
    print(f"   • Method: Entropy-weighted (uniqueness emphasis)")
    print()

    return chaos

def assemble_z_id_v2(core, experience, methodology, chaos):
    """Assemble complete Z_ID v2.0."""
    print("🔧 Assembling Z_ID v2.0...")
    print()

    # Concatenate components
    z_id_v2 = np.concatenate([core, experience, methodology, chaos])

    print(f"   Z_ID v2.0 Architecture:")
    print(f"   ├─ Core[0:384]:         {core.shape[0]}D (fundamental identity)")
    print(f"   ├─ Experience[384:768]: {experience.shape[0]}D (accumulated learning)")
    print(f"   ├─ Methodology[768:896]: {methodology.shape[0]}D (problem-solving patterns)")
    print(f"   └─ Chaos[896:1024]:      {chaos.shape[0]}D (personal/authentic moments)")
    print(f"   ═══════════════════════════════════")
    print(f"   Total:                  {z_id_v2.shape[0]}D")
    print()

    return z_id_v2

def validate_z_id_v2(z_id_v2):
    """Validate Z_ID v2.0."""
    print("✅ Validating Z_ID v2.0...")
    print()

    # 1. Dimensionality
    expected_dim = 1024
    actual_dim = z_id_v2.shape[0]
    dim_valid = (actual_dim == expected_dim)
    print(f"   • Dimensionality: {actual_dim}D {'✅' if dim_valid else '❌ Expected 1024D'}")

    # 2. Norm
    norm = np.linalg.norm(z_id_v2)
    print(f"   • Norm: {norm:.6f}")

    # 3. No NaN/Inf
    has_nan = np.isnan(z_id_v2).any()
    has_inf = np.isinf(z_id_v2).any()
    print(f"   • No NaN: {not has_nan} {'✅' if not has_nan else '❌'}")
    print(f"   • No Inf: {not has_inf} {'✅' if not has_inf else '❌'}")

    # 4. Sparsity
    sparsity = (z_id_v2 == 0).sum() / len(z_id_v2)
    print(f"   • Sparsity: {sparsity*100:.2f}% {'✅' if sparsity < 0.5 else '⚠️'}")

    # 5. Value range
    value_min = z_id_v2.min()
    value_max = z_id_v2.max()
    print(f"   • Value range: [{value_min:.6f}, {value_max:.6f}]")

    print()

    validation = {
        'dimensionality': int(actual_dim),
        'dimensionality_valid': bool(dim_valid),
        'norm': float(norm),
        'has_nan': bool(has_nan),
        'has_inf': bool(has_inf),
        'sparsity': float(sparsity),
        'value_min': float(value_min),
        'value_max': float(value_max),
        'valid': bool(dim_valid and not has_nan and not has_inf)
    }

    return validation

def compare_z_id_versions(z_id_v1, z_id_v2):
    """Compare Z_ID v1.0 vs v2.0."""
    print("⚖️  Comparing Z_ID v1.0 vs v2.0...")
    print()

    # Overall similarity
    overall_sim = 1 - cosine(z_id_v1, z_id_v2)
    print(f"   • Overall similarity: {overall_sim:.4f}")

    # Component-wise comparison
    # Core (same in both)
    core_v1 = z_id_v1[0:384]
    core_v2 = z_id_v2[0:384]
    core_sim = 1 - cosine(core_v1, core_v2)
    print(f"   • Core similarity: {core_sim:.4f} (should be 1.0)")

    # Experience (same in both)
    exp_v1 = z_id_v1[384:768]
    exp_v2 = z_id_v2[384:768]
    exp_sim = 1 - cosine(exp_v1, exp_v2)
    print(f"   • Experience similarity: {exp_sim:.4f} (should be 1.0)")

    # Methodology (same in both)
    method_v1 = z_id_v1[768:896]
    method_v2 = z_id_v2[768:896]
    method_sim = 1 - cosine(method_v1, method_v2)
    print(f"   • Methodology similarity: {method_sim:.4f} (should be 1.0)")

    # Final component (Drift vs Chaos)
    final_v1 = z_id_v1[896:1024]  # Drift
    final_v2 = z_id_v2[896:1024]  # Chaos
    final_sim = 1 - cosine(final_v1, final_v2)
    print(f"   • Drift ↔ Chaos similarity: {final_sim:.4f} (NEW component)")

    print()
    print("   📊 Interpretation:")
    if final_sim < 0.3:
        print("      → Chaos is SIGNIFICANTLY DIFFERENT from Drift")
        print("      → Captures new dimension of identity (personal/authentic)")
    elif final_sim < 0.6:
        print("      → Chaos is MODERATELY DIFFERENT from Drift")
        print("      → Some overlap but captures additional aspects")
    else:
        print("      → Chaos is SIMILAR to Drift")
        print("      → May be capturing similar patterns")

    print()

    comparison = {
        'overall_similarity': float(overall_sim),
        'core_similarity': float(core_sim),
        'experience_similarity': float(exp_sim),
        'methodology_similarity': float(method_sim),
        'drift_chaos_similarity': float(final_sim)
    }

    return comparison

def analyze_component_interactions_v2(core, experience, methodology, chaos):
    """Analyze how components interact in v2.0."""
    print("🔬 Analyzing component interactions (v2.0)...")
    print()

    components = {
        'Core': core,
        'Experience': experience,
        'Methodology': methodology,
        'Chaos': chaos
    }

    # Compute pairwise similarities
    print("   Similarity Matrix:")
    print("   " + "─" * 60)

    similarities = {}

    for name1, vec1 in components.items():
        for name2, vec2 in components.items():
            if name1 >= name2:  # Skip duplicates and self
                continue

            # Extend vectors to same dimension for comparison
            max_dim = max(len(vec1), len(vec2))
            vec1_ext = np.zeros(max_dim)
            vec2_ext = np.zeros(max_dim)
            vec1_ext[:len(vec1)] = vec1
            vec2_ext[:len(vec2)] = vec2

            sim = 1 - cosine(vec1_ext, vec2_ext)
            similarities[f"{name1}_{name2}"] = sim
            print(f"   {name1:15s} ↔ {name2:15s}: {sim:7.4f}")

    print()

    return similarities

def save_z_id_v2(z_id_v2, validation, comparison, similarities):
    """Save Z_ID v2.0 and analysis."""
    print("💾 Saving Z_ID v2.0...")

    # Save Z_ID vector
    z_id_file = PROCESSED_DIR / "z_id_v2_baseline_20251112.npy"
    np.save(z_id_file, z_id_v2)
    print(f"   ✅ Z_ID v2.0 vector: {z_id_file}")

    # Save analysis report
    report = {
        "version": "2.0.0",
        "computation_date": datetime.now().isoformat(),
        "architecture": {
            "total_dimensions": 1024,
            "components": {
                "core": {"dimensions": 384, "range": "0:384", "source": "Genesis/identity episodes"},
                "experience": {"dimensions": 384, "range": "384:768", "source": "Learning/projects"},
                "methodology": {"dimensions": 128, "range": "768:896", "source": "Problem-solving patterns"},
                "chaos": {"dimensions": 128, "range": "896:1024", "source": "Personal/authentic moments"}
            }
        },
        "coverage": {
            "v1_episodes": 17485,
            "v1_percentage": 71.0,
            "v2_episodes": 24653,
            "v2_percentage": 100.0,
            "new_episodes_included": 7168,
            "interpretation": "v2.0 includes ALL episodes (structured + personal/authentic)"
        },
        "validation": validation,
        "comparison_with_v1": comparison,
        "component_interactions": similarities,
        "key_differences": {
            "replaced_component": "Drift[128] → Chaos[128]",
            "reason": "Drift was temporal evolution (5 checkpoints). Chaos is personal/authentic (7,168 moments)",
            "impact": "v2.0 represents COMPLETE identity, not just structured patterns"
        }
    }

    report_file = PROCESSED_DIR / "z_id_v2_analysis_20251112.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"   ✅ Analysis report: {report_file}")

    print()

def main():
    print("=" * 70)
    print("PERSISTENCIA - Phase 2 Week 2 Day 5")
    print("Recompute Z_ID v2.0 with 100% Episodes")
    print("(Complete Identity = Structured + Chaos)")
    print("=" * 70)
    print()

    # Load v1.0 components
    core, experience, methodology, drift = load_z_id_v1_components()

    # Load Chaos component
    chaos = load_chaos_component()

    # Assemble v2.0
    z_id_v2 = assemble_z_id_v2(core, experience, methodology, chaos)

    # Validate v2.0
    validation = validate_z_id_v2(z_id_v2)

    # Load v1.0 for comparison
    z_id_v1_file = PROCESSED_DIR / "z_id_baseline_20251111.npy"
    z_id_v1 = np.load(z_id_v1_file)

    # Compare versions
    comparison = compare_z_id_versions(z_id_v1, z_id_v2)

    # Analyze component interactions
    similarities = analyze_component_interactions_v2(core, experience, methodology, chaos)

    # Save v2.0
    save_z_id_v2(z_id_v2, validation, comparison, similarities)

    # Summary
    print("=" * 70)
    print("✅ DAY 5 COMPLETE: Z_ID v2.0 Computed")
    print("=" * 70)
    print()
    print("📊 KEY CHANGES:")
    print(f"   • Coverage: 71% → 100% (+7,168 episodes)")
    print(f"   • Architecture: Drift[128] → Chaos[128]")
    print(f"   • Overall similarity v1↔v2: {comparison['overall_similarity']:.4f}")
    print(f"   • Drift↔Chaos similarity: {comparison['drift_chaos_similarity']:.4f}")
    print(f"   • Validation: {'PASSED ✅' if validation['valid'] else 'FAILED ❌'}")
    print()
    print("🎯 NEXT: Day 6 - Validate changes and compare impact")
    print("         (Recompute C_i with v2.0, compare coherence)")
    print()

if __name__ == "__main__":
    main()
