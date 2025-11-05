"""
LAB_015: Norepinephrine System - Test Suite

TDD (Test-Driven Development) approach
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_015_Norepinephrine_System import NorepinephrineSystem


# ============================================================================
# PHASE 1: CORE FUNCTIONALITY TESTS
# ============================================================================

class TestArousalUpdate:
    """Test 1: Arousal Update Mechanism"""

    def test_stress_increases_arousal(self):
        """Stress events should increase arousal"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)

        for _ in range(10):
            ne.update_arousal(stress_event=0.3)

        assert ne.arousal_level > 0.5  # Arousal increased

    def test_calming_decreases_arousal(self):
        """Calming events should decrease arousal"""
        ne = NorepinephrineSystem(baseline_arousal=0.7)

        for _ in range(10):
            ne.update_arousal(stress_event=-0.3)

        assert ne.arousal_level < 0.7  # Arousal decreased

    def test_arousal_decays_toward_baseline(self):
        """Arousal should decay back toward baseline over time"""
        ne = NorepinephrineSystem(baseline_arousal=0.5, arousal_decay=0.9)

        # Spike arousal high
        ne.update_arousal(stress_event=1.0)
        arousal_after_spike = ne.arousal_level

        # Let it decay (no stress events)
        for _ in range(20):
            ne.update_arousal(stress_event=0.0)

        # Should have decayed toward baseline (0.5)
        assert ne.arousal_level < arousal_after_spike
        assert abs(ne.arousal_level - 0.5) < abs(arousal_after_spike - 0.5)


class TestPerformanceCurve:
    """Test 2: Performance Curve (Yerkes-Dodson Law)"""

    def test_optimal_arousal_gives_best_performance(self):
        """Optimal arousal should give best performance"""
        ne = NorepinephrineSystem(baseline_arousal=0.6, optimal_arousal=0.6)

        result = ne.compute_performance()

        assert result["is_optimal"] is True
        assert result["performance_efficiency"] > 0.95  # Near peak

    def test_low_arousal_poor_performance(self):
        """Low arousal should give poor performance (under-stimulated)"""
        ne = NorepinephrineSystem(baseline_arousal=0.1, optimal_arousal=0.6)

        result = ne.compute_performance()

        assert result["is_optimal"] is False
        assert result["performance_efficiency"] < 0.5  # Poor performance

    def test_high_arousal_poor_performance(self):
        """High arousal should give poor performance (over-stimulated)"""
        ne = NorepinephrineSystem(baseline_arousal=0.95, optimal_arousal=0.6)

        result = ne.compute_performance()

        assert result["is_optimal"] is False
        assert result["performance_efficiency"] < 0.5  # Poor performance


class TestFocusModulation:
    """Test 3: Focus Modulation"""

    def test_medium_arousal_high_focus(self):
        """Medium arousal should give high focus"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)

        focus = ne.modulate_focus()

        assert focus > 0.8  # High focus at medium arousal

    def test_extreme_arousal_low_focus(self):
        """Extreme arousal (low or high) should give lower focus"""
        ne_low = NorepinephrineSystem(baseline_arousal=0.1)
        ne_high = NorepinephrineSystem(baseline_arousal=0.95)

        focus_low = ne_low.modulate_focus()
        focus_high = ne_high.modulate_focus()

        assert focus_low < 0.5  # Low focus at low arousal
        assert focus_high < 0.5  # Low focus at high arousal


class TestAlertness:
    """Test 4: Alertness"""

    def test_high_arousal_high_alertness(self):
        """High arousal should give high alertness"""
        ne = NorepinephrineSystem(baseline_arousal=0.9)

        alertness = ne.get_alertness()

        assert alertness > 0.8  # High alertness

    def test_low_arousal_low_alertness(self):
        """Low arousal should give low alertness (drowsy)"""
        ne = NorepinephrineSystem(baseline_arousal=0.2)

        alertness = ne.get_alertness()

        assert alertness < 0.3  # Low alertness


class TestArousalStability:
    """Test 5: Arousal Stability"""

    def test_stable_arousal_has_high_stability(self):
        """Consistent arousal should have high stability score"""
        ne = NorepinephrineSystem()

        # Many events with same intensity
        for _ in range(20):
            ne.update_arousal(stress_event=0.1)

        stability = ne.get_arousal_stability()

        assert stability > 0.8  # High stability

    def test_volatile_arousal_has_low_stability(self):
        """Volatile arousal should have low stability score"""
        ne = NorepinephrineSystem(arousal_decay=0.8, stress_sensitivity=0.5)

        # Alternating stress/calm events
        for i in range(30):
            event = 1.0 if i % 2 == 0 else -1.0
            ne.update_arousal(stress_event=event)

        stability = ne.get_arousal_stability()

        assert stability < 0.95  # Lower than stable


class TestFullEventProcessing:
    """Test 6: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all norepinephrine outputs"""
        ne = NorepinephrineSystem()

        result = ne.process_event(stress_event=0.3)

        assert "arousal_level" in result
        assert "performance" in result
        assert "focus_strength" in result
        assert "alertness" in result
        assert "arousal_stability" in result

    def test_arousal_history_window_maintained(self):
        """Arousal history should maintain fixed window size"""
        ne = NorepinephrineSystem(history_window=10)

        for i in range(25):
            ne.process_event(stress_event=0.2)

        assert len(ne.arousal_history) == 10  # Window maintained

    def test_total_events_counter(self):
        """Should correctly count total events"""
        ne = NorepinephrineSystem()

        for i in range(15):
            ne.process_event(stress_event=0.1)

        assert ne.total_events == 15


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestStressSerotoninInteraction:
    """Test 7: Integration with LAB_014 (Serotonin)"""

    def test_high_stress_low_serotonin_poor_performance(self):
        """
        High stress (high arousal) + Low serotonin (low mood) = Poor performance

        Simulates anxious state with poor impulse control
        """
        # High stress (over-aroused)
        ne = NorepinephrineSystem(baseline_arousal=0.95, optimal_arousal=0.6)

        result = ne.process_event(stress_event=0.5)

        # Should have poor performance (too aroused)
        assert result["performance"]["performance_efficiency"] < 0.5
        assert result["performance"]["is_optimal"] is False

    def test_moderate_stress_balanced_optimal(self):
        """
        Moderate stress + balanced arousal = Optimal performance

        Ideal state for focused work
        """
        # Moderate arousal
        ne = NorepinephrineSystem(baseline_arousal=0.6, optimal_arousal=0.6)

        result = ne.process_event(stress_event=0.0)

        # Should have optimal performance
        assert result["performance"]["is_optimal"] is True
        assert result["focus_strength"] > 0.7


# ============================================================================
# PHASE 3: EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Test 8: Edge Cases"""

    def test_extreme_stress_clamped(self):
        """Extreme stress events should not exceed arousal bounds"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)

        # Many extremely stressful events
        for _ in range(50):
            ne.update_arousal(stress_event=1.0)

        # Arousal should not exceed 1.0
        assert ne.arousal_level <= 1.0

    def test_extreme_calming_clamped(self):
        """Extreme calming events should not go below arousal bounds"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)

        # Many extremely calming events
        for _ in range(50):
            ne.update_arousal(stress_event=-1.0)

        # Arousal should not go below 0.0
        assert ne.arousal_level >= 0.0

    def test_performance_curve_symmetry(self):
        """Performance should drop symmetrically from optimal"""
        ne_low = NorepinephrineSystem(baseline_arousal=0.3, optimal_arousal=0.6)
        ne_high = NorepinephrineSystem(baseline_arousal=0.9, optimal_arousal=0.6)

        perf_low = ne_low.compute_performance()
        perf_high = ne_high.compute_performance()

        # Both should have similar deviation and performance drop
        assert abs(perf_low["deviation_from_optimal"] - perf_high["deviation_from_optimal"]) < 0.05


class TestStatePersistence:
    """Test 9: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        ne = NorepinephrineSystem()

        # Generate some history
        for i in range(10):
            ne.process_event(stress_event=0.2)

        state = ne.get_state()

        # Verify all expected keys
        assert "arousal_level" in state
        assert "arousal_history" in state
        assert "arousal_mean" in state
        assert "arousal_stability" in state
        assert "performance_efficiency" in state
        assert "focus_strength" in state
        assert "alertness" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        ne = NorepinephrineSystem()

        ne.process_event(stress_event=0.3)

        state1 = ne.get_state()
        state2 = ne.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["arousal_level"] == state2["arousal_level"]


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def fresh_norepinephrine():
    """Fixture: Fresh NorepinephrineSystem instance"""
    return NorepinephrineSystem(
        baseline_arousal=0.5,
        stress_sensitivity=0.3,
        arousal_decay=0.95,
        optimal_arousal=0.6,
        focus_threshold=0.5,
        history_window=20
    )


@pytest.fixture
def norepinephrine_with_history():
    """Fixture: NorepinephrineSystem with arousal history"""
    ne = NorepinephrineSystem()

    # Generate 15 stress events
    for _ in range(15):
        ne.process_event(stress_event=0.3)

    return ne


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
