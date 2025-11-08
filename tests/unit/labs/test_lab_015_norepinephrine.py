"""
LAB_015: Norepinephrine System - Test Suite

TDD (Test-Driven Development) approach:
1. RED: Write failing tests first
2. GREEN: Implement code to pass tests
3. REFACTOR: Optimize while keeping tests passing

Biological Inspiration:
- Locus coeruleus (noradrenergic neurons)
- Aston-Jones & Cohen (2005) - "An integrative theory of locus coeruleus-norepinephrine function"

Core Functions:
- Arousal modulation (inverted-U relationship)
- Stress response (fight-or-flight activation)
- Focus width (narrow vs broad attention)
- Exploit vs explore (optimal arousal → exploit)

Test Phases:
- Phase 1: Core NE Tests (basic functionality)
- Phase 2: Integration Tests (with other LABs)
- Phase 3: Edge Cases & Performance
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_015_Norepinephrine_System import NorepinephrineSystem


# ============================================================================
# PHASE 1: CORE NOREPINEPHRINE TESTS
# ============================================================================

class TestBasicArousal:
    """Test 1: Basic Arousal Level Management"""

    def test_baseline_arousal(self):
        """NE should start at baseline arousal"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)
        assert ne.current_arousal == pytest.approx(0.5)

    def test_arousal_increases_with_stress(self):
        """Stress should increase arousal"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)
        initial = ne.current_arousal

        ne.update_arousal(task_urgency=0.8, stress=0.7, novelty=0.5)

        assert ne.current_arousal > initial

    def test_arousal_increases_with_novelty(self):
        """Novelty should boost arousal"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)
        initial = ne.current_arousal

        ne.update_arousal(task_urgency=0.5, stress=0.3, novelty=0.9)

        assert ne.current_arousal > initial

    def test_arousal_bounds(self):
        """Arousal should be clamped between 0 and 1"""
        ne = NorepinephrineSystem()

        # Test upper bound
        for _ in range(10):
            ne.update_arousal(task_urgency=1.0, stress=1.0, novelty=1.0)

        assert 0.0 <= ne.current_arousal <= 1.0


class TestInvertedUCurve:
    """Test 2: Inverted-U Performance Curve"""

    def test_optimal_arousal_maximum_performance(self):
        """Optimal arousal should give maximum performance"""
        ne = NorepinephrineSystem(optimal_range=(0.5, 0.7))

        # Set arousal to optimal
        ne.current_arousal = 0.6
        performance_optimal = ne.compute_performance_multiplier()

        # Set arousal too low
        ne.current_arousal = 0.2
        performance_low = ne.compute_performance_multiplier()

        # Set arousal too high
        ne.current_arousal = 0.95
        performance_high = ne.compute_performance_multiplier()

        # Optimal should be highest
        assert performance_optimal > performance_low
        assert performance_optimal > performance_high

    def test_performance_symmetric_around_optimal(self):
        """Performance should decline symmetrically away from optimal"""
        ne = NorepinephrineSystem(optimal_range=(0.5, 0.7))

        # Slightly below optimal
        ne.current_arousal = 0.4
        perf_below = ne.compute_performance_multiplier()

        # Slightly above optimal
        ne.current_arousal = 0.8
        perf_above = ne.compute_performance_multiplier()

        # Should be similar (inverted-U symmetry)
        assert abs(perf_below - perf_above) < 0.2


class TestFocusWidth:
    """Test 3: Focus Width Modulation"""

    def test_high_arousal_narrows_focus(self):
        """High arousal should narrow focus"""
        ne = NorepinephrineSystem()

        ne.current_arousal = 0.9
        focus_width_high = ne.compute_focus_width()

        ne.current_arousal = 0.3
        focus_width_low = ne.compute_focus_width()

        # High arousal → narrow focus (low width)
        assert focus_width_high < focus_width_low

    def test_low_arousal_broadens_focus(self):
        """Low arousal should broaden focus"""
        ne = NorepinephrineSystem()

        ne.current_arousal = 0.2
        focus_width = ne.compute_focus_width()

        # Low arousal → broad focus (high width)
        assert focus_width > 0.5


class TestExploitVsExplore:
    """Test 4: Exploit vs Explore Mode"""

    def test_optimal_arousal_exploits(self):
        """Optimal arousal should favor exploitation"""
        ne = NorepinephrineSystem(optimal_range=(0.5, 0.7))

        ne.current_arousal = 0.6  # Optimal
        explore_tendency = ne.get_exploit_vs_explore()

        # Low explore tendency = exploit mode
        assert explore_tendency < 0.5

    def test_extreme_arousal_explores(self):
        """Very low or high arousal should favor exploration"""
        ne = NorepinephrineSystem(optimal_range=(0.5, 0.7))

        # Very low arousal
        ne.current_arousal = 0.1
        explore_low = ne.get_exploit_vs_explore()

        # Very high arousal
        ne.current_arousal = 0.95
        explore_high = ne.get_exploit_vs_explore()

        # Both should explore more
        assert explore_low > 0.5
        assert explore_high > 0.5


class TestStressResponse:
    """Test 5: Stress Response"""

    def test_high_stress_activates_arousal(self):
        """High stress should trigger arousal spike"""
        ne = NorepinephrineSystem(baseline_arousal=0.5, stress_sensitivity=0.8)

        initial = ne.current_arousal

        stress_response = ne.compute_stress_response(stressor=0.9)

        # Should activate strongly
        assert stress_response > 0.7

    def test_low_stress_minimal_response(self):
        """Low stress should have minimal impact"""
        ne = NorepinephrineSystem(baseline_arousal=0.5, stress_sensitivity=0.8)

        stress_response = ne.compute_stress_response(stressor=0.1)

        # Should be minimal
        assert stress_response < 0.3


class TestFullEventProcessing:
    """Test 6: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all NE outputs"""
        ne = NorepinephrineSystem()

        result = ne.process_event(
            task_urgency=0.7,
            stress=0.5
        )

        # Verify all expected keys
        assert "arousal_level" in result
        assert "performance_multiplier" in result
        assert "focus_width" in result
        assert "explore_tendency" in result
        assert "stress_response" in result

    def test_history_tracking(self):
        """NE should maintain arousal history"""
        ne = NorepinephrineSystem(history_window=5)

        for i in range(10):
            ne.process_event(task_urgency=0.6, stress=0.4)

        # History should be limited to window size
        assert len(ne.arousal_history) == 5

    def test_event_counter(self):
        """Should correctly count total events"""
        ne = NorepinephrineSystem()

        for i in range(8):
            ne.process_event(task_urgency=0.5, stress=0.3)

        assert ne.total_events == 8


class TestArousalDecay:
    """Test 7: Arousal Decay Dynamics"""

    def test_arousal_decays_without_stimulation(self):
        """Arousal should decay toward baseline without input"""
        ne = NorepinephrineSystem(baseline_arousal=0.5, decay_rate=0.9)

        # Spike arousal high
        ne.current_arousal = 0.95

        # Apply neutral events (should decay)
        for _ in range(10):
            ne.update_arousal(task_urgency=0.5, stress=0.0, novelty=0.0)

        # Should decay toward baseline
        assert ne.current_arousal < 0.95
        assert ne.current_arousal > 0.45  # Not instant


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestIntegrationWithDopamine:
    """Test 8: Integration with LAB_013 (Dopamine)"""

    def test_arousal_amplifies_motivation(self):
        """
        High arousal + high dopamine = high drive/urgency

        Arousal amplifies motivational signals
        """
        ne_high = NorepinephrineSystem(baseline_arousal=0.8)
        ne_low = NorepinephrineSystem(baseline_arousal=0.3)

        # High arousal should amplify performance
        perf_high = ne_high.compute_performance_multiplier()
        perf_low = ne_low.compute_performance_multiplier()

        # Within optimal range, higher arousal = better performance
        if 0.5 <= ne_high.current_arousal <= 0.7:
            assert perf_high >= perf_low


class TestIntegrationWithAcetylcholine:
    """Test 9: Integration with LAB_016 (Acetylcholine - future)"""

    def test_arousal_affects_attention_selectivity(self):
        """
        High arousal + ACh = narrow focused attention
        Low arousal + ACh = broad distributed attention
        """
        ne = NorepinephrineSystem()

        # High arousal → narrow focus
        ne.current_arousal = 0.85
        focus_narrow = ne.compute_focus_width()

        # Low arousal → broad focus
        ne.current_arousal = 0.25
        focus_broad = ne.compute_focus_width()

        assert focus_narrow < focus_broad


class TestIntegrationWithSerotonin:
    """Test 10: Integration with LAB_014 (Serotonin)"""

    def test_stress_buffering_interaction(self):
        """
        High serotonin should buffer stress-induced arousal

        Simulates serotonin dampening NE stress response
        """
        ne = NorepinephrineSystem(baseline_arousal=0.5)

        # High stress event
        stress_response = ne.compute_stress_response(stressor=0.9)

        # High stress should activate NE
        assert stress_response > 0.5


# ============================================================================
# PHASE 3: EDGE CASES & PERFORMANCE
# ============================================================================

class TestEdgeCases:
    """Test 11: Edge Cases"""

    def test_extreme_stress(self):
        """System should handle extreme stress"""
        ne = NorepinephrineSystem()

        result = ne.process_event(task_urgency=1.0, stress=1.0)

        # Should remain bounded
        assert 0.0 <= result["arousal_level"] <= 1.0

    def test_zero_stress(self):
        """System should handle zero stress"""
        ne = NorepinephrineSystem()

        result = ne.process_event(task_urgency=0.5, stress=0.0)

        # Should work normally
        assert 0.0 <= result["arousal_level"] <= 1.0

    def test_rapid_arousal_changes(self):
        """System should handle rapid fluctuations"""
        ne = NorepinephrineSystem()

        # Rapid alternating high/low
        for i in range(20):
            stress = 1.0 if i % 2 == 0 else 0.0
            ne.process_event(task_urgency=0.5, stress=stress)

        # Should remain stable
        assert 0.0 <= ne.current_arousal <= 1.0


class TestStatePersistence:
    """Test 12: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        ne = NorepinephrineSystem()

        # Generate some history
        for i in range(5):
            ne.process_event(task_urgency=0.6, stress=0.4)

        state = ne.get_state()

        # Verify all expected keys
        assert "arousal_level" in state
        assert "arousal_history" in state
        assert "arousal_mean" in state
        assert "performance_multiplier" in state
        assert "focus_width" in state
        assert "explore_tendency" in state
        assert "optimal_distance" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        ne = NorepinephrineSystem()

        ne.process_event(task_urgency=0.7, stress=0.5)

        state1 = ne.get_state()
        state2 = ne.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["arousal_level"] == state2["arousal_level"]


class TestLongTermDynamics:
    """Test 13: Long-term Dynamics"""

    def test_sustained_high_arousal_burnout(self):
        """Prolonged high arousal should model burnout"""
        ne = NorepinephrineSystem(baseline_arousal=0.5)

        # Sustained high stress
        for _ in range(20):
            ne.process_event(task_urgency=0.9, stress=0.9)

        # Arousal should be chronically high
        assert ne.current_arousal > 0.7

    def test_recovery_from_high_arousal(self):
        """Recovery from high arousal should be gradual"""
        ne = NorepinephrineSystem(baseline_arousal=0.5, decay_rate=0.92)

        # Create high arousal
        for _ in range(10):
            ne.process_event(task_urgency=0.9, stress=0.8)

        high_level = ne.current_arousal

        # Apply low-stress events
        for _ in range(10):
            ne.process_event(task_urgency=0.3, stress=0.1)

        # Should decrease but not instantly
        assert ne.current_arousal < high_level
        assert ne.current_arousal > 0.4  # Gradual recovery


# ============================================================================
# FIXTURES & UTILITIES
# ============================================================================

@pytest.fixture
def fresh_norepinephrine():
    """Fixture: Fresh NorepinephrineSystem instance"""
    return NorepinephrineSystem(
        baseline_arousal=0.5,
        optimal_range=(0.5, 0.7),
        stress_sensitivity=0.8,
        decay_rate=0.92,
        history_window=10
    )


@pytest.fixture
def ne_high_arousal():
    """Fixture: NorepinephrineSystem in high arousal state"""
    ne = NorepinephrineSystem(baseline_arousal=0.5)

    # Create high arousal
    for _ in range(10):
        ne.process_event(task_urgency=0.9, stress=0.8)

    return ne


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
