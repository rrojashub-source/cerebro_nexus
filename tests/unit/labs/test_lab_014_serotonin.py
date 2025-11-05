"""
LAB_014: Serotonin System - Test Suite

TDD (Test-Driven Development) approach
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_014_Serotonin_System import SerotoninSystem


# ============================================================================
# PHASE 1: CORE FUNCTIONALITY TESTS
# ============================================================================

class TestMoodUpdate:
    """Test 1: Mood Update Mechanism"""

    def test_mood_increases_with_positive_events(self):
        """Positive emotional events should increase mood"""
        serotonin = SerotoninSystem(baseline_mood=0.5, mood_inertia=0.9)

        for _ in range(20):
            serotonin.update_mood(emotional_event=0.3)

        assert serotonin.mood_level > 0.5  # Mood increased

    def test_mood_decreases_with_negative_events(self):
        """Negative emotional events should decrease mood"""
        serotonin = SerotoninSystem(baseline_mood=0.7)

        for _ in range(10):
            serotonin.update_mood(emotional_event=-0.3)

        assert serotonin.mood_level < 0.7  # Mood decreased

    def test_mood_has_inertia(self):
        """Mood should change slowly (high inertia)"""
        serotonin = SerotoninSystem(baseline_mood=0.5, mood_inertia=0.95)

        # Single strong positive event
        mood_before = serotonin.mood_level
        serotonin.update_mood(emotional_event=1.0)
        mood_after = serotonin.mood_level

        # Change should be small due to inertia
        change = mood_after - mood_before
        assert change < 0.1  # Small change despite strong event


class TestImpulseControl:
    """Test 2: Impulse Control"""

    def test_high_mood_resists_temptation(self):
        """High mood (high serotonin) should resist temptation"""
        serotonin = SerotoninSystem(baseline_mood=0.9, impulse_threshold=0.7)

        temptation = 0.5
        result = serotonin.compute_impulse_control(temptation_strength=temptation)

        assert result["can_resist"] is True
        assert result["control_strength"] > temptation

    def test_low_mood_succumbs_to_temptation(self):
        """Low mood (low serotonin) should succumb to temptation"""
        serotonin = SerotoninSystem(baseline_mood=0.3, impulse_threshold=0.7)

        temptation = 0.5
        result = serotonin.compute_impulse_control(temptation_strength=temptation)

        assert result["can_resist"] is False
        assert result["control_strength"] < temptation

    def test_resistance_margin_correct(self):
        """Resistance margin should = control - temptation"""
        serotonin = SerotoninSystem(baseline_mood=0.8, impulse_threshold=0.7)

        temptation = 0.4
        result = serotonin.compute_impulse_control(temptation_strength=temptation)

        expected_control = 0.8 * 0.7
        expected_margin = expected_control - temptation

        assert result["resistance_margin"] == pytest.approx(expected_margin, abs=0.01)


class TestPatienceFactor:
    """Test 3: Patience Factor (Temporal Discounting)"""

    def test_high_mood_increases_patience(self):
        """High mood should increase patience (lower temporal discounting)"""
        serotonin = SerotoninSystem(baseline_mood=0.9, patience_factor=1.0)

        patience = serotonin.get_patience_factor()

        assert patience > 1.0  # More patient than baseline

    def test_low_mood_decreases_patience(self):
        """Low mood should decrease patience (higher temporal discounting)"""
        serotonin = SerotoninSystem(baseline_mood=0.3, patience_factor=1.0)

        patience = serotonin.get_patience_factor()

        assert patience < 1.0  # Less patient than baseline


class TestEmotionalReactivity:
    """Test 4: Emotional Reactivity Dampening"""

    def test_high_mood_dampens_reactivity(self):
        """High mood should dampen emotional reactivity"""
        serotonin = SerotoninSystem(baseline_mood=0.9, reactivity_dampening=0.5)

        reactivity = serotonin.modulate_reactivity(emotional_intensity=1.0)

        assert reactivity < 1.0  # Dampened

    def test_low_mood_preserves_reactivity(self):
        """Low mood should preserve emotional reactivity"""
        serotonin = SerotoninSystem(baseline_mood=0.2, reactivity_dampening=0.5)

        reactivity = serotonin.modulate_reactivity(emotional_intensity=1.0)

        assert reactivity > 0.8  # Less dampened


class TestMoodStability:
    """Test 5: Mood Stability"""

    def test_stable_mood_has_high_stability(self):
        """Consistent mood should have high stability score"""
        serotonin = SerotoninSystem()

        # Many events with same valence
        for _ in range(20):
            serotonin.update_mood(emotional_event=0.5)

        stability = serotonin.get_mood_stability()

        assert stability > 0.8  # High stability

    def test_volatile_mood_has_low_stability(self):
        """Volatile mood should have low stability score"""
        serotonin = SerotoninSystem(mood_inertia=0.5)  # Much lower inertia for volatility

        # Alternating positive/negative events
        for i in range(40):
            event = 1.0 if i % 2 == 0 else -1.0
            serotonin.update_mood(emotional_event=event)

        stability = serotonin.get_mood_stability()

        assert stability < 0.95  # Lower than stable mood (which is typically > 0.98)


class TestFullEventProcessing:
    """Test 6: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all serotonin outputs"""
        serotonin = SerotoninSystem()

        result = serotonin.process_event(
            emotional_event=0.3,
            temptation_strength=0.5
        )

        assert "mood_level" in result
        assert "impulse_control" in result
        assert "patience_factor" in result
        assert "emotional_reactivity" in result
        assert "mood_stability" in result

    def test_mood_history_window_maintained(self):
        """Mood history should maintain fixed window size"""
        serotonin = SerotoninSystem(history_window=10)

        for i in range(25):
            serotonin.process_event(emotional_event=0.2)

        assert len(serotonin.mood_history) == 10  # Window maintained

    def test_total_events_counter(self):
        """Should correctly count total events"""
        serotonin = SerotoninSystem()

        for i in range(15):
            serotonin.process_event(emotional_event=0.1)

        assert serotonin.total_events == 15


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestDopamineSerotoninInteraction:
    """Test 7: Integration with LAB_013 (Dopamine)"""

    def test_high_dopamine_low_serotonin_impulsive(self):
        """
        High dopamine (high RPE) + Low serotonin (low mood) = Impulsive behavior

        Simulates reward-seeking without patience
        """
        # Low serotonin (low mood)
        serotonin = SerotoninSystem(baseline_mood=0.3)

        # Strong temptation (simulating high dopamine RPE)
        result = serotonin.compute_impulse_control(temptation_strength=0.8)

        # Should NOT resist (impulsive)
        assert result["can_resist"] is False

    def test_balanced_dopamine_serotonin_optimal(self):
        """
        Balanced dopamine + serotonin = Optimal decision making

        Can pursue rewards but with patience
        """
        # Balanced serotonin
        serotonin = SerotoninSystem(baseline_mood=0.6)

        # Moderate temptation
        result = serotonin.compute_impulse_control(temptation_strength=0.3)

        # Should resist moderate temptation
        assert result["can_resist"] is True

        # Should have reasonable patience
        patience = serotonin.get_patience_factor()
        assert 0.5 < patience < 1.5


# ============================================================================
# PHASE 3: EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Test 8: Edge Cases"""

    def test_extreme_positive_events_clamped(self):
        """Extreme positive events should not exceed mood bounds"""
        serotonin = SerotoninSystem(baseline_mood=0.5)

        # Many extremely positive events
        for _ in range(100):
            serotonin.update_mood(emotional_event=1.0)

        # Mood should not exceed 1.0
        assert serotonin.mood_level <= 1.0

    def test_extreme_negative_events_clamped(self):
        """Extreme negative events should not go below mood bounds"""
        serotonin = SerotoninSystem(baseline_mood=0.5)

        # Many extremely negative events
        for _ in range(100):
            serotonin.update_mood(emotional_event=-1.0)

        # Mood should not go below 0.0
        assert serotonin.mood_level >= 0.0

    def test_zero_temptation_always_resists(self):
        """With zero temptation, should always resist"""
        serotonin = SerotoninSystem(baseline_mood=0.1)  # Very low mood

        result = serotonin.compute_impulse_control(temptation_strength=0.0)

        assert result["can_resist"] is True  # Even low mood resists zero temptation


class TestStatePersistence:
    """Test 9: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        serotonin = SerotoninSystem()

        # Generate some history
        for i in range(10):
            serotonin.process_event(emotional_event=0.2)

        state = serotonin.get_state()

        # Verify all expected keys
        assert "mood_level" in state
        assert "mood_history" in state
        assert "mood_mean" in state
        assert "mood_stability" in state
        assert "impulse_control_strength" in state
        assert "patience_factor" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        serotonin = SerotoninSystem()

        serotonin.process_event(emotional_event=0.3)

        state1 = serotonin.get_state()
        state2 = serotonin.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["mood_level"] == state2["mood_level"]


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def fresh_serotonin():
    """Fixture: Fresh SerotoninSystem instance"""
    return SerotoninSystem(
        baseline_mood=0.5,
        impulse_threshold=0.7,
        patience_factor=1.0,
        reactivity_dampening=0.5,
        mood_inertia=0.95,
        history_window=20
    )


@pytest.fixture
def serotonin_with_history():
    """Fixture: SerotoninSystem with mood history"""
    serotonin = SerotoninSystem()

    # Generate 15 positive events
    for _ in range(15):
        serotonin.process_event(emotional_event=0.3)

    return serotonin


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
