"""
LAB_008: Emotional Contagion - Quick Test

Validate emotional spreading logic works correctly.

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / 'implementation'))

from emotional_contagion import (
    EmotionalState,
    EmotionalContagionEngine
)


def test_emotional_spreading():
    """Test basic emotional contagion spreading"""

    print("=" * 70)
    print("LAB_008: Emotional Contagion - Quick Test")
    print("=" * 70)
    print()

    # Create engine
    engine = EmotionalContagionEngine(
        similarity_threshold=0.7,
        max_hops=2,
        intensity_threshold=0.6
    )

    # Create strong emotional state (breakthrough moment)
    strong_emotion = EmotionalState(
        joy=0.9,
        anticipation=0.85,
        trust=0.8,
        fear=0.2,
        sadness=0.1,
        disgust=0.1,
        anger=0.1,
        surprise=0.7
    )

    print(f"Source Emotion:")
    print(f"  Intensity: {strong_emotion.intensity:.2f}")
    print(f"  Valence:   {strong_emotion.valence:.2f} (positive)")
    print()

    # Create similarity graph (simple 5-episode network)
    similarity_graph = {
        'episode_001': [
            ('episode_002', 0.85),  # High similarity
            ('episode_003', 0.75),  # Medium similarity
        ],
        'episode_002': [
            ('episode_001', 0.85),
            ('episode_004', 0.80),
        ],
        'episode_003': [
            ('episode_001', 0.75),
            ('episode_005', 0.72),
        ],
        'episode_004': [
            ('episode_002', 0.80),
        ],
        'episode_005': [
            ('episode_003', 0.72),
        ]
    }

    # Propagate emotion from episode_001
    print("🧠 Propagating emotion from episode_001...")
    overlays = engine.on_episode_access(
        'episode_001',
        strong_emotion,
        similarity_graph
    )

    print(f"✅ Created {len(overlays)} contagion overlays")
    print()

    # Show overlays
    print("Contagion Overlays:")
    for overlay in overlays:
        emotion, intensity = overlay.get_effective_emotion()
        print(f"  {overlay.episode_id}:")
        print(f"    Intensity: {intensity:.3f}")
        print(f"    Valence:   {emotion.valence:.3f}")
        print(f"    Distance:  {overlay.semantic_distance} hop(s)")

    print()

    # Test retrieval bias
    print("🔍 Testing Retrieval Bias:")
    print()

    # Simulate query with similar positive emotion
    query_emotion = EmotionalState(
        joy=0.8,
        anticipation=0.7,
        trust=0.75,
        fear=0.3,
        sadness=0.2,
        disgust=0.2,
        anger=0.2,
        surprise=0.6
    )

    print(f"Query Emotion: Valence={query_emotion.valence:.2f} (positive)")
    print()

    # Simulate retrieval candidates
    candidates = [
        ('episode_001', 0.90),  # Source (high base score)
        ('episode_002', 0.70),  # Has contagion
        ('episode_003', 0.65),  # Has contagion
        ('episode_004', 0.60),  # Has contagion (2-hop)
        ('episode_999', 0.75),  # No contagion (control)
    ]

    print("Candidate Episodes (base scores):")
    for ep_id, score in candidates:
        print(f"  {ep_id}: {score:.2f}")

    print()

    # Adjust scores
    adjusted = engine.adjust_retrieval_scores(candidates, query_emotion)

    print("After Emotional Contagion Bias:")
    for ep_id, score in adjusted:
        original = next(s for e, s in candidates if e == ep_id)
        boost = ((score / original) - 1.0) * 100 if original > 0 else 0
        marker = "🔥" if boost > 5 else "  "
        print(f"  {marker} {ep_id}: {score:.2f} ({boost:+.1f}%)")

    print()

    # Stats
    stats = engine.get_stats()
    print("=" * 70)
    print("Statistics:")
    print(f"  Episodes affected: {stats['propagator']['episodes_affected']}")
    print(f"  Total overlays:    {stats['propagator']['total_overlays']}")
    print(f"  Avg intensity:     {stats['propagator']['avg_intensity']:.3f}")
    print()

    # Success criteria
    print("=" * 70)
    print("Success Criteria:")
    print()

    checks = [
        ("Overlays created", len(overlays) >= 3, len(overlays)),
        ("Episodes affected", stats['propagator']['episodes_affected'] >= 3, stats['propagator']['episodes_affected']),
        ("Avg intensity", stats['propagator']['avg_intensity'] >= 0.2, f"{stats['propagator']['avg_intensity']:.3f}"),
    ]

    all_pass = True
    for criterion, passed, value in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {criterion:<25} ({value})")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("🎉 ALL TESTS PASSED - Emotional contagion working!")
    else:
        print("⚠️  Some tests failed - Needs debugging")

    print()


if __name__ == "__main__":
    test_emotional_spreading()
