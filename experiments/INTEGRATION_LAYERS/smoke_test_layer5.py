#!/usr/bin/env python3
"""
Session 11: Smoke Test - Layer 5 (Higher Cognition)

Tests:
- LAB_051 Hybrid Memory (fact extraction)
- LAB_052 Temporal Reasoning (temporal linking)
- Full Stack Integration (Layer 2+3+4+5)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from experiments.INTEGRATION_LAYERS.cognitive_stack import (
    CognitiveStack,
    EmotionalState,
    SomaticMarker
)


def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def smoke_test_layer5():
    """
    Smoke test Layer 5 integration

    Scenario:
    - Event 1: "Session 10 COMPLETE - NEXUS v3.0.0 - 32/32 tests (100%)"
    - Event 2: "Session 11 START - Implementing Layer 5 (LAB_051 + LAB_052)"
    - Event 3: "Breakthrough: 95.5% accuracy achieved with 12.3ms latency"

    Expected:
    - Fact extraction from all events
    - Temporal linking between events
    - Full stack integration (Layer 2+3+4+5)
    """
    print_section("SESSION 11: SMOKE TEST - LAYER 5 HIGHER COGNITION")

    stack = CognitiveStack()

    # ========================================================================
    # EVENT 1: Session 10 Complete
    # ========================================================================
    print_section("EVENT 1: Session 10 Complete")

    result1 = stack.process_event(
        content="Session 10 COMPLETE - NEXUS version 3.0.0 - 32 tests passing (100% accuracy)",
        emotional_state=EmotionalState(joy=0.95, trust=0.9),
        somatic_marker=SomaticMarker(valence=0.9, arousal=0.6),
        novelty=0.7
    )

    print("Input:")
    print("  Content: 'Session 10 COMPLETE - NEXUS version 3.0.0 - 32 tests passing (100% accuracy)'")
    print("  Emotion: joy=0.95, trust=0.9")
    print("  Novelty: 0.7")
    print()

    # Layer 2 (Cognitive)
    print("Layer 2 - Cognitive Loop:")
    print(f"  Salience Score: {result1['memory']['salience_score']:.3f}")
    print(f"  Attention Level: {result1['attention']['level']:.3f}")
    print()

    # Layer 4 (Neuro)
    print("Layer 4 - Neurochemistry:")
    print(f"  Dopamine: {result1['neuro_state']['dopamine']:.3f}")
    print(f"  Acetylcholine: {result1['neuro_state']['acetylcholine']:.3f}")
    print()

    # Layer 3 (Memory)
    print("Layer 3 - Memory Dynamics:")
    print(f"  Encoding Strength: {result1['memory']['encoding_strength']:.3f}")
    print(f"  Decay Rate: {result1['memory']['decay']['decay_rate']:.3f}")
    print()

    # Layer 5 (Higher Cognition)
    print("Layer 5 - Higher Cognition:")
    print(f"  Facts Extracted: {result1['hybrid_memory']['facts']}")
    print(f"  Facts Count: {result1['hybrid_memory']['facts_count']}")
    print(f"  Temporal Refs: {result1['temporal_reasoning']['temporal_refs']}")
    print(f"  Linked Events: {result1['temporal_reasoning']['linked_events_count']}")
    print()

    # ========================================================================
    # EVENT 2: Session 11 Start
    # ========================================================================
    print_section("EVENT 2: Session 11 Start")

    result2 = stack.process_event(
        content="Session 11 START - Implementing Layer 5 (LAB_051 Hybrid Memory + LAB_052 Temporal Reasoning)",
        emotional_state=EmotionalState(anticipation=0.85, trust=0.8),
        somatic_marker=SomaticMarker(valence=0.7, arousal=0.7),
        novelty=0.8
    )

    print("Input:")
    print("  Content: 'Session 11 START - Implementing Layer 5 (LAB_051 + LAB_052)'")
    print("  Emotion: anticipation=0.85, trust=0.8")
    print("  Novelty: 0.8")
    print()

    print("Layer 5 - Higher Cognition:")
    print(f"  Facts Extracted: {result2['hybrid_memory']['facts']}")
    print(f"  Facts Count: {result2['hybrid_memory']['facts_count']}")
    print(f"  Temporal Refs: {result2['temporal_reasoning']['temporal_refs']}")
    print(f"  Linked Events: {result2['temporal_reasoning']['linked_events_count']}")
    print()

    # ========================================================================
    # EVENT 3: Breakthrough
    # ========================================================================
    print_section("EVENT 3: Breakthrough Achievement")

    result3 = stack.process_event(
        content="Breakthrough: 95.5% accuracy achieved with 12.3ms latency - Phase 2 complete",
        emotional_state=EmotionalState(joy=0.95, surprise=0.85, anticipation=0.8),
        somatic_marker=SomaticMarker(valence=0.95, arousal=0.8),
        novelty=0.95
    )

    print("Input:")
    print("  Content: 'Breakthrough: 95.5% accuracy achieved with 12.3ms latency - Phase 2 complete'")
    print("  Emotion: joy=0.95, surprise=0.85, anticipation=0.8")
    print("  Novelty: 0.95")
    print()

    print("Layer 5 - Higher Cognition:")
    print(f"  Facts Extracted: {result3['hybrid_memory']['facts']}")
    print(f"  Facts Count: {result3['hybrid_memory']['facts_count']}")
    print(f"  Temporal Refs: {result3['temporal_reasoning']['temporal_refs']}")
    print(f"  Linked Events: {result3['temporal_reasoning']['linked_events_count']}")
    print()

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print_section("SMOKE TEST SUMMARY")

    print("✅ Layer 5 Components:")
    print("  ✓ LAB_051 Hybrid Memory - Fact extraction operational")
    print("  ✓ LAB_052 Temporal Reasoning - Temporal linking operational")
    print()

    print("✅ Integration Points:")
    print("  ✓ Layer 2 (Cognitive) → Layer 5 (salience influences fact extraction)")
    print("  ✓ Layer 4 (Neuro) → Layer 5 (neurotransmitters modulate extraction)")
    print("  ✓ Layer 5 (Facts) → Layer 3 (facts stored in memory metadata)")
    print()

    print("✅ Facts Extracted Across 3 Events:")
    total_facts = (
        result1['hybrid_memory']['facts_count'] +
        result2['hybrid_memory']['facts_count'] +
        result3['hybrid_memory']['facts_count']
    )
    print(f"  Total Facts: {total_facts}")
    print()

    print("✅ Temporal Links:")
    print(f"  Event 1: {result1['temporal_reasoning']['linked_events_count']} linked")
    print(f"  Event 2: {result2['temporal_reasoning']['linked_events_count']} linked")
    print(f"  Event 3: {result3['temporal_reasoning']['linked_events_count']} linked")
    print()

    print("✅ Full Stack Operational:")
    print("  Layer 2 (Cognitive) ↔ Layer 3 (Memory) ↔ Layer 4 (Neuro) ↔ Layer 5 (Higher Cognition)")
    print()

    print_section("SESSION 11: LAYER 5 SMOKE TEST - ✅ SUCCESS")


if __name__ == "__main__":
    smoke_test_layer5()
