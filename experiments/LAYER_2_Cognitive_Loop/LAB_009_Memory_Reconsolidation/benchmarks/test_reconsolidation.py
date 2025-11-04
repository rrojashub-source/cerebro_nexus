"""
LAB_009: Memory Reconsolidation - Test Suite

Validate memory reconsolidation mechanics work correctly.

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

import sys
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent / 'implementation'))

from memory_reconsolidation import (
    Episode,
    IntegrationMode,
    MemoryReconsolidationEngine
)


def test_reconsolidation_system():
    """Test complete reconsolidation workflow"""

    print("=" * 70)
    print("LAB_009: Memory Reconsolidation - Test Suite")
    print("=" * 70)
    print()

    # Create engine
    engine = MemoryReconsolidationEngine(
        novelty_threshold=0.25,
        window_hours=6.0,
        default_integration_mode=IntegrationMode.ADDITIVE
    )

    # ========================================================================
    # TEST 1: Basic Reconsolidation Flow
    # ========================================================================

    print("TEST 1: Basic Reconsolidation Flow")
    print("-" * 70)

    # Create original episode
    original_episode = Episode(
        episode_id="episode_001",
        content="LAB_005 spreading activation - implemented, not tested",
        metadata={
            "project": "NEXUS_LABS",
            "status": "implemented",
            "tags": ["lab_005", "spreading_activation"]
        },
        embedding=np.array([0.5, 0.3, 0.8, 0.2, 0.6])
    )

    print(f"Original Episode:")
    print(f"  Content: {original_episode.content}")
    print(f"  Metadata: {original_episode.metadata}")
    print()

    # Mark as retrieved
    engine.on_episode_retrieval(original_episode)
    print("✓ Episode marked as retrieved")
    print()

    # New context (related but with new info)
    new_context = {
        "content": "LAB_005 tested with 75.7% accuracy, deployed with A/B testing",
        "metadata": {
            "status": "tested",
            "accuracy": 0.757,
            "deployment_status": "production"
        },
        "embedding": np.array([0.6, 0.4, 0.7, 0.3, 0.5])  # Similar but more different
    }

    print(f"New Context:")
    print(f"  Content: {new_context['content']}")
    print(f"  Metadata: {new_context['metadata']}")
    print()

    # Try reconsolidation
    success, updated_episode, reason = engine.try_reconsolidate(
        original_episode,
        new_context,
        IntegrationMode.ADDITIVE
    )

    print(f"Reconsolidation Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"  Reason: {reason}")

    if success and updated_episode:
        print()
        print(f"Updated Episode:")
        print(f"  Content: {updated_episode.content[:150]}...")
        print(f"  Metadata: {updated_episode.metadata}")
        print()

    # ========================================================================
    # TEST 2: Novelty Detection - Too Similar (Duplicate)
    # ========================================================================

    print()
    print("TEST 2: Novelty Detection - Too Similar (Duplicate)")
    print("-" * 70)

    duplicate_context = {
        "content": "LAB_005 spreading activation - implemented, not tested",  # Identical
        "metadata": {"status": "implemented"},
        "embedding": np.array([0.5, 0.3, 0.8, 0.2, 0.6])  # Identical embedding
    }

    success2, _, reason2 = engine.try_reconsolidate(
        original_episode,
        duplicate_context,
        IntegrationMode.ADDITIVE
    )

    print(f"Reconsolidation Result: {'✅ SUCCESS' if success2 else '❌ BLOCKED (expected)'}")
    print(f"  Reason: {reason2}")
    print()

    # ========================================================================
    # TEST 3: Novelty Detection - Too Different (Unrelated)
    # ========================================================================

    print()
    print("TEST 3: Novelty Detection - Too Different (Unrelated)")
    print("-" * 70)

    unrelated_context = {
        "content": "Making dinner - pasta with tomato sauce",  # Completely unrelated
        "metadata": {"meal": "dinner"},
        "embedding": np.array([0.1, 0.9, 0.1, 0.9, 0.1])  # Very different embedding
    }

    success3, _, reason3 = engine.try_reconsolidate(
        original_episode,
        unrelated_context,
        IntegrationMode.ADDITIVE
    )

    print(f"Reconsolidation Result: {'✅ SUCCESS' if success3 else '❌ BLOCKED (expected)'}")
    print(f"  Reason: {reason3}")
    print()

    # ========================================================================
    # TEST 4: Stability Window - Already Labile (Cooldown)
    # ========================================================================

    print()
    print("TEST 4: Stability Window - Already Labile (Cooldown)")
    print("-" * 70)

    # Try to reconsolidate again immediately (should be blocked - already labile)
    success4, _, reason4 = engine.try_reconsolidate(
        original_episode,
        new_context,
        IntegrationMode.ADDITIVE
    )

    print(f"Reconsolidation Result: {'✅ SUCCESS' if success4 else '❌ BLOCKED (expected - cooldown)'}")
    print(f"  Reason: {reason4}")
    print()

    # Check labile status
    is_labile = engine.stability_window.is_labile("episode_001")
    remaining = engine.stability_window.get_labile_time_remaining("episode_001")

    print(f"Episode Labile Status: {is_labile}")
    print(f"  Time Remaining: {remaining:.2f} hours" if remaining else "")
    print()

    # ========================================================================
    # TEST 5: Integration Modes - CORRECTIVE
    # ========================================================================

    print()
    print("TEST 5: Integration Modes - CORRECTIVE")
    print("-" * 70)

    # Create episode with incorrect info
    episode_incorrect = Episode(
        episode_id="episode_002",
        content="LAB_007 has 50% accuracy (poor performance)",
        metadata={
            "accuracy": 0.50,
            "status": "failed"
        },
        embedding=np.array([0.4, 0.6, 0.3, 0.7, 0.5])
    )

    engine.on_episode_retrieval(episode_incorrect)

    # Correction with accurate info
    correction_context = {
        "content": "LAB_007 actually has 75.7% accuracy (excellent performance)",
        "metadata": {
            "accuracy": 0.757,
            "status": "success"
        },
        "embedding": np.array([0.42, 0.58, 0.32, 0.68, 0.52])
    }

    success5, corrected_episode, reason5 = engine.try_reconsolidate(
        episode_incorrect,
        correction_context,
        IntegrationMode.CORRECTIVE
    )

    print(f"Reconsolidation Result: {'✅ SUCCESS' if success5 else '❌ FAILED'}")
    print(f"  Reason: {reason5}")

    if success5 and corrected_episode:
        print()
        print(f"Corrected Episode:")
        print(f"  Content: {corrected_episode.content}")
        print(f"  Metadata: {corrected_episode.metadata}")
        print()

    # ========================================================================
    # TEST 6: Integration Modes - ENRICHMENT
    # ========================================================================

    print()
    print("TEST 6: Integration Modes - ENRICHMENT")
    print("-" * 70)

    episode_minimal = Episode(
        episode_id="episode_003",
        content="LAB_008 emotional contagion implemented",
        metadata={
            "status": "implemented"
        },
        embedding=np.array([0.6, 0.4, 0.5, 0.5, 0.7])
    )

    engine.on_episode_retrieval(episode_minimal)

    enrichment_context = {
        "content": "LAB_008 tested with +17.5% retrieval boost for emotionally congruent memories",
        "metadata": {
            "retrieval_boost_percent": 17.5,
            "overlays_created": 4,
            "neuroscience_basis": "limbic_resonance",
            "tags": ["emotion", "contagion", "neuroscience"]
        },
        "embedding": np.array([0.55, 0.45, 0.45, 0.55, 0.65])
    }

    success6, enriched_episode, reason6 = engine.try_reconsolidate(
        episode_minimal,
        enrichment_context,
        IntegrationMode.ENRICHMENT
    )

    print(f"Reconsolidation Result: {'✅ SUCCESS' if success6 else '❌ FAILED'}")
    print(f"  Reason: {reason6}")

    if success6 and enriched_episode:
        print()
        print(f"Enriched Episode:")
        print(f"  Metadata Keys: {list(enriched_episode.metadata.keys())}")
        print(f"  Metadata: {enriched_episode.metadata}")
        print()

    # ========================================================================
    # Statistics
    # ========================================================================

    print()
    print("=" * 70)
    print("Statistics")
    print("=" * 70)

    stats = engine.get_stats()

    print(f"Stability Window:")
    print(f"  Labile Memories: {stats['stability_window']['labile_count']}")
    print(f"  Recent Retrievals: {stats['stability_window']['recent_retrievals']}")
    print(f"  Window Duration: {stats['stability_window']['window_hours']} hours")
    print()

    print(f"Reconsolidation Events:")
    print(f"  Total Events: {stats['reconsolidation_events']['total_events']}")
    print(f"  Avg Novelty Score: {stats['reconsolidation_events']['avg_novelty_score']:.3f}")
    print(f"  Unique Episodes Updated: {stats['reconsolidation_events']['unique_episodes_updated']}")
    print(f"  By Integration Mode: {stats['reconsolidation_events']['by_integration_mode']}")
    print()

    # ========================================================================
    # Success Criteria
    # ========================================================================

    print("=" * 70)
    print("Success Criteria")
    print("=" * 70)
    print()

    checks = [
        ("Basic reconsolidation works", success, True),
        ("Duplicate detection works", not success2, True),
        ("Unrelated detection works", not success3, True),
        ("Cooldown period works", not success4, True),
        ("CORRECTIVE mode works", success5, True),
        ("ENRICHMENT mode works", success6, True),
        ("Reconsolidation events logged", stats['reconsolidation_events']['total_events'] >= 2, True),
        ("Original content preserved",
         updated_episode and "LAB_005 spreading activation - implemented" in updated_episode.content if updated_episode else False,
         True),
    ]

    all_pass = True
    for criterion, result, expected in checks:
        passed = result == expected
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {criterion:<40} ({result})")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("🎉 ALL TESTS PASSED - Memory reconsolidation working!")
    else:
        print("⚠️  Some tests failed - Needs debugging")

    print()


if __name__ == "__main__":
    test_reconsolidation_system()
