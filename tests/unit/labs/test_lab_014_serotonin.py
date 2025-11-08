"""
LAB_014: Serotonin System - Test Suite

TDD (Test-Driven Development) approach:
1. RED: Write failing tests first
2. GREEN: Implement code to pass tests
3. REFACTOR: Optimize while keeping tests passing

Biological Inspiration:
- Raphe nuclei (serotonergic neurons)
- Dayan & Huys (2009) - "Serotonin in Affective Control"

Core Functions:
- Mood stability (buffer against fluctuations)
- Impulse control (patience vs impulsivity)
- Temporal discounting (valuation of delayed rewards)
- Social sensitivity (social reward modulation)

Test Phases:
- Phase 1: Core Serotonin Tests (basic functionality)
- Phase 2: Integration Tests (with other LABs)
- Phase 3: Edge Cases & Performance
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_014_Serotonin_System import SerotoninSystem


# ============================================================================
# PHASE 1: CORE SEROTONIN TESTS
# ============================================================================

class TestBasicSerotoninLevel:
    """Test 1: Basic Serotonin Level Management"""

    def test_baseline_level(self):
        """Serotonin should start at baseline (neutral mood)"""
        serotonin = SerotoninSystem(baseline_level=0.5)
        assert serotonin.current_level == pytest.approx(0.5)

    def test_level_increases_with_positive_outcomes(self):
        """Positive outcomes should increase serotonin"""
        serotonin = SerotoninSystem(baseline_level=0.5)
        initial_level = serotonin.current_level

        serotonin.update_level(outcome=0.8, social_context=0.5)

        assert serotonin.current_level > initial_level

    def test_level_decreases_with_negative_outcomes(self):
        """Negative outcomes should decrease serotonin"""
        serotonin = SerotoninSystem(baseline_level=0.5)
        initial_level = serotonin.current_level

        serotonin.update_level(outcome=0.2, social_context=0.5)

        assert serotonin.current_level < initial_level

    def test_level_bounds(self):
        """Serotonin level should be clamped between 0 and 1"""
        serotonin = SerotoninSystem()

        # Test upper bound (many positive outcomes)
        for _ in range(20):
            serotonin.update_level(outcome=1.0, social_context=1.0)

        assert 0.0 <= serotonin.current_level <= 1.0

        # Reset and test lower bound
        serotonin = SerotoninSystem()
        for _ in range(20):
            serotonin.update_level(outcome=0.0, social_context=0.0)

        assert 0.0 <= serotonin.current_level <= 1.0


class TestMoodStabilization:
    """Test 2: Mood Stability & Buffering"""

    def test_high_serotonin_buffers_negative_mood(self):
        """High serotonin should buffer against negative mood swings"""
        serotonin = SerotoninSystem(baseline_level=0.8, stability_factor=0.8)

        # Apply negative event
        initial_mood = 0.7
        buffered_mood = serotonin.modulate_mood(
            current_mood=initial_mood,
            event_valence=-0.5
        )

        # Mood should decrease less due to high serotonin buffering
        # Without buffer: 0.7 + (-0.5) = 0.2
        # With buffer: should be > 0.2
        assert buffered_mood > 0.2
        assert buffered_mood < initial_mood  # But still decrease

    def test_low_serotonin_amplifies_mood_swings(self):
        """Low serotonin should allow larger mood fluctuations"""
        serotonin_high = SerotoninSystem(baseline_level=0.8, stability_factor=0.9)
        serotonin_low = SerotoninSystem(baseline_level=0.2, stability_factor=0.9)

        initial_mood = 0.5
        event_valence = -0.3

        mood_high_serotonin = serotonin_high.modulate_mood(initial_mood, event_valence)
        mood_low_serotonin = serotonin_low.modulate_mood(initial_mood, event_valence)

        # Low serotonin should produce larger mood change (less buffering)
        change_high = abs(mood_high_serotonin - initial_mood)
        change_low = abs(mood_low_serotonin - initial_mood)

        assert change_low > change_high

    def test_mood_stability_over_time(self):
        """Serotonin should create mood stability over multiple events"""
        serotonin = SerotoninSystem(baseline_level=0.7, stability_factor=0.8)

        mood = 0.6
        mood_changes = []

        # Apply alternating positive/negative events
        for i in range(10):
            event_valence = 0.3 if i % 2 == 0 else -0.3
            new_mood = serotonin.modulate_mood(mood, event_valence)
            mood_changes.append(abs(new_mood - mood))
            mood = new_mood

        # Mood changes should be smaller than raw event valence
        avg_change = sum(mood_changes) / len(mood_changes)
        assert avg_change < 0.3  # Buffered compared to raw ±0.3


class TestImpulseControl:
    """Test 3: Impulse Control & Patience"""

    def test_high_serotonin_increases_patience(self):
        """High serotonin should increase impulse control"""
        serotonin = SerotoninSystem(
            baseline_level=0.8,
            patience_multiplier=1.5
        )

        patience = serotonin.compute_impulse_control()

        # High serotonin → high patience
        assert patience > 0.7

    def test_low_serotonin_decreases_patience(self):
        """Low serotonin should decrease impulse control (impulsive)"""
        serotonin = SerotoninSystem(baseline_level=0.2)

        patience = serotonin.compute_impulse_control()

        # Low serotonin → low patience (impulsive)
        assert patience < 0.4

    def test_impulse_control_scaling(self):
        """Impulse control should scale with serotonin level"""
        serotonin_low = SerotoninSystem(baseline_level=0.3)
        serotonin_mid = SerotoninSystem(baseline_level=0.5)
        serotonin_high = SerotoninSystem(baseline_level=0.8)

        patience_low = serotonin_low.compute_impulse_control()
        patience_mid = serotonin_mid.compute_impulse_control()
        patience_high = serotonin_high.compute_impulse_control()

        assert patience_low < patience_mid < patience_high


class TestTemporalDiscounting:
    """Test 4: Temporal Discounting & Future Valuation"""

    def test_high_serotonin_values_future_more(self):
        """High serotonin should reduce temporal discounting (value future)"""
        serotonin = SerotoninSystem(baseline_level=0.8)

        # Discount rate for delayed reward
        discount_rate = serotonin.compute_temporal_discount(delay=10.0)

        # High serotonin → low discount rate (values future)
        assert discount_rate < 0.5

    def test_low_serotonin_devalues_future(self):
        """Low serotonin should increase temporal discounting (impulsive)"""
        serotonin = SerotoninSystem(baseline_level=0.2)

        discount_rate = serotonin.compute_temporal_discount(delay=10.0)

        # Low serotonin → high discount rate (devalues future)
        assert discount_rate > 0.6

    def test_discount_increases_with_delay(self):
        """Longer delays should increase discounting (standard hyperbolic)"""
        serotonin = SerotoninSystem(baseline_level=0.5)

        discount_short = serotonin.compute_temporal_discount(delay=1.0)
        discount_medium = serotonin.compute_temporal_discount(delay=10.0)
        discount_long = serotonin.compute_temporal_discount(delay=100.0)

        # Longer delay → higher discount
        assert discount_short < discount_medium < discount_long


class TestSocialContextModulation:
    """Test 5: Social Context Effects"""

    def test_positive_social_boosts_serotonin(self):
        """Positive social context should increase serotonin"""
        serotonin = SerotoninSystem(baseline_level=0.5)

        initial_level = serotonin.current_level

        # Positive social context
        serotonin.update_level(outcome=0.6, social_context=0.9)

        assert serotonin.current_level > initial_level

    def test_negative_social_lowers_serotonin(self):
        """Negative social context should decrease serotonin"""
        serotonin = SerotoninSystem(baseline_level=0.5)

        initial_level = serotonin.current_level

        # Negative social context (isolation, conflict)
        serotonin.update_level(outcome=0.6, social_context=0.1)

        # Should increase less than with positive social
        # (social context moderates outcome effect)
        serotonin_positive = SerotoninSystem(baseline_level=0.5)
        serotonin_positive.update_level(outcome=0.6, social_context=0.9)

        assert serotonin.current_level < serotonin_positive.current_level

    def test_social_sensitivity(self):
        """Serotonin should modulate social reward sensitivity"""
        serotonin = SerotoninSystem(baseline_level=0.5)

        # Social reward valuation should depend on serotonin
        social_sensitivity = serotonin.compute_social_sensitivity()

        assert 0.0 <= social_sensitivity <= 1.0


class TestFullEventProcessing:
    """Test 6: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all serotonin outputs"""
        serotonin = SerotoninSystem()

        result = serotonin.process_event(
            outcome=0.7,
            social_context=0.6
        )

        # Verify all expected keys
        assert "serotonin_level" in result
        assert "impulse_control" in result
        assert "mood_stability" in result
        assert "temporal_discount_rate" in result
        assert "social_sensitivity" in result

    def test_history_tracking(self):
        """Serotonin should maintain history window"""
        serotonin = SerotoninSystem(history_window=5)

        for i in range(10):
            serotonin.process_event(outcome=0.6, social_context=0.5)

        # History should be limited to window size
        assert len(serotonin.level_history) == 5

    def test_event_counter(self):
        """Should correctly count total events"""
        serotonin = SerotoninSystem()

        for i in range(7):
            serotonin.process_event(outcome=0.5, social_context=0.5)

        assert serotonin.total_events == 7


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestIntegrationWithDopamine:
    """Test 7: Integration with LAB_013 (Dopamine)"""

    def test_dopamine_serotonin_balance(self):
        """
        Test the critical dopamine-serotonin balance

        - High dopamine + low serotonin = impulsive reward-seeking
        - High serotonin + low dopamine = patient but unmotivated
        - Balanced = optimal (patient + motivated)
        """
        # Scenario 1: High dopamine, low serotonin (impulsive)
        serotonin_low = SerotoninSystem(baseline_level=0.2)
        patience_impulsive = serotonin_low.compute_impulse_control()

        # Scenario 2: Low dopamine, high serotonin (patient but sluggish)
        serotonin_high = SerotoninSystem(baseline_level=0.9)
        patience_high = serotonin_high.compute_impulse_control()

        # Scenario 3: Balanced
        serotonin_balanced = SerotoninSystem(baseline_level=0.6)
        patience_balanced = serotonin_balanced.compute_impulse_control()

        # High serotonin should have highest patience
        assert patience_high > patience_balanced > patience_impulsive

    def test_reward_timing_interaction(self):
        """
        Dopamine RPE + Serotonin temporal discount interaction

        Serotonin affects how much future rewards are valued
        """
        serotonin = SerotoninSystem(baseline_level=0.7)

        # High serotonin → patient → values delayed rewards more
        discount_rate = serotonin.compute_temporal_discount(delay=10.0)

        # Should be willing to wait (low discount)
        assert discount_rate < 0.6


class TestIntegrationWithNorepinephrine:
    """Test 8: Integration with LAB_015 (Norepinephrine - future)"""

    def test_stress_buffering(self):
        """
        High serotonin should buffer stress-induced arousal

        This simulates serotonin dampening NE stress response
        """
        serotonin_high = SerotoninSystem(baseline_level=0.8)
        serotonin_low = SerotoninSystem(baseline_level=0.3)

        # Apply stressful event
        stress_event = -0.6

        mood_high_serotonin = serotonin_high.modulate_mood(0.5, stress_event)
        mood_low_serotonin = serotonin_low.modulate_mood(0.5, stress_event)

        # High serotonin should buffer more (smaller mood drop)
        drop_high = abs(mood_high_serotonin - 0.5)
        drop_low = abs(mood_low_serotonin - 0.5)

        assert drop_high < drop_low


class TestIntegrationWithEmotionalSalience:
    """Test 9: Integration with LAB_001 (Emotional Salience)"""

    def test_mood_affects_salience_weighting(self):
        """
        Serotonin level should modulate emotional salience

        Low serotonin → negative bias (depressive)
        High serotonin → balanced emotional processing
        """
        serotonin_low = SerotoninSystem(baseline_level=0.2)
        serotonin_high = SerotoninSystem(baseline_level=0.8)

        # Low serotonin should show mood instability
        mood_low = serotonin_low.modulate_mood(0.5, -0.2)
        mood_high = serotonin_high.modulate_mood(0.5, -0.2)

        # High serotonin buffers better
        assert mood_high > mood_low


class TestIntegrationWithDecayModulation:
    """Test 10: Integration with LAB_002 (Decay Modulation)"""

    def test_mood_affects_memory_consolidation(self):
        """
        Serotonin mood state should affect memory importance

        Low serotonin → negative memories more salient
        High serotonin → balanced memory formation
        """
        serotonin = SerotoninSystem(baseline_level=0.6)

        # Get mood stability index
        result = serotonin.process_event(outcome=0.6, social_context=0.5)
        mood_stability = result["mood_stability"]

        # Stable mood should support balanced memory formation
        assert 0.0 <= mood_stability <= 1.0


# ============================================================================
# PHASE 3: EDGE CASES & PERFORMANCE
# ============================================================================

class TestEdgeCases:
    """Test 11: Edge Cases"""

    def test_extreme_outcomes(self):
        """System should handle extreme outcome values"""
        serotonin = SerotoninSystem()

        # Maximum positive outcome
        result_max = serotonin.process_event(outcome=1.0, social_context=1.0)
        assert 0.0 <= result_max["serotonin_level"] <= 1.0

        # Maximum negative outcome
        serotonin_negative = SerotoninSystem()
        result_min = serotonin_negative.process_event(outcome=0.0, social_context=0.0)
        assert 0.0 <= result_min["serotonin_level"] <= 1.0

    def test_rapid_fluctuations(self):
        """System should handle rapid outcome changes"""
        serotonin = SerotoninSystem()

        # Rapid alternating outcomes
        for i in range(20):
            outcome = 1.0 if i % 2 == 0 else 0.0
            result = serotonin.process_event(outcome, social_context=0.5)

        # Should remain stable (not crash or diverge)
        assert 0.0 <= serotonin.current_level <= 1.0

    def test_zero_stability_factor(self):
        """Zero stability factor should allow full mood swings"""
        serotonin = SerotoninSystem(
            baseline_level=0.5,
            stability_factor=0.0
        )

        # With zero buffering, mood should change drastically
        mood = serotonin.modulate_mood(0.5, -0.5)

        # Should allow large change (no buffering)
        assert abs(mood - 0.5) > 0.3

    def test_maximum_stability_factor(self):
        """Maximum stability factor should heavily buffer mood"""
        serotonin = SerotoninSystem(
            baseline_level=0.8,
            stability_factor=1.0
        )

        # With max buffering, mood should barely change
        mood = serotonin.modulate_mood(0.5, -0.5)

        # Should buffer significantly
        assert abs(mood - 0.5) < 0.3


class TestStatePersistence:
    """Test 12: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        serotonin = SerotoninSystem()

        # Generate some history
        for i in range(5):
            serotonin.process_event(outcome=0.6, social_context=0.5)

        state = serotonin.get_state()

        # Verify all expected keys
        assert "serotonin_level" in state
        assert "level_history" in state
        assert "level_mean" in state
        assert "impulse_control" in state
        assert "mood_stability_index" in state
        assert "temporal_discount_baseline" in state
        assert "social_sensitivity" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        serotonin = SerotoninSystem()

        serotonin.process_event(outcome=0.7, social_context=0.6)

        state1 = serotonin.get_state()
        state2 = serotonin.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["serotonin_level"] == state2["serotonin_level"]

    def test_history_window_management(self):
        """History window should maintain fixed size"""
        serotonin = SerotoninSystem(history_window=7)

        # Generate more events than window size
        for i in range(15):
            serotonin.process_event(outcome=0.5, social_context=0.5)

        # History should be capped at window size
        assert len(serotonin.level_history) == 7


class TestLongTermDynamics:
    """Test 13: Long-term System Dynamics"""

    def test_homeostatic_regulation(self):
        """Serotonin should regulate toward baseline over time"""
        serotonin = SerotoninSystem(baseline_level=0.5)

        # Spike serotonin high
        for _ in range(10):
            serotonin.process_event(outcome=1.0, social_context=1.0)

        serotonin_high = serotonin.current_level

        # Apply neutral events (should drift toward baseline)
        for _ in range(20):
            serotonin.process_event(outcome=0.5, social_context=0.5)

        # Should be closer to baseline than peak
        assert abs(serotonin.current_level - 0.5) < abs(serotonin_high - 0.5)

    def test_sustained_low_mood(self):
        """Prolonged negative outcomes should create sustained low serotonin"""
        serotonin = SerotoninSystem(baseline_level=0.5)

        # Sustained negative outcomes (depression model)
        for _ in range(15):
            serotonin.process_event(outcome=0.2, social_context=0.3)

        # Serotonin should be chronically low
        assert serotonin.current_level < 0.4

    def test_recovery_dynamics(self):
        """Recovery from low serotonin should be gradual"""
        serotonin = SerotoninSystem(baseline_level=0.5)

        # Create low serotonin state
        for _ in range(10):
            serotonin.process_event(outcome=0.1, social_context=0.2)

        low_level = serotonin.current_level

        # Apply single positive event
        serotonin.process_event(outcome=0.9, social_context=0.8)

        # Should improve, but not instantly recover
        assert serotonin.current_level > low_level
        assert serotonin.current_level < 0.7  # Gradual recovery


# ============================================================================
# FIXTURES & UTILITIES
# ============================================================================

@pytest.fixture
def fresh_serotonin():
    """Fixture: Fresh SerotoninSystem instance"""
    return SerotoninSystem(
        baseline_level=0.5,
        stability_factor=0.7,
        patience_multiplier=1.5,
        history_window=20
    )


@pytest.fixture
def serotonin_with_history():
    """Fixture: SerotoninSystem with some history"""
    serotonin = SerotoninSystem()

    # Generate 10 positive events
    for _ in range(10):
        serotonin.process_event(outcome=0.7, social_context=0.6)

    return serotonin


@pytest.fixture
def serotonin_depleted():
    """Fixture: SerotoninSystem in depleted state (depression model)"""
    serotonin = SerotoninSystem(baseline_level=0.5)

    # Create depletion via sustained negative outcomes
    for _ in range(15):
        serotonin.process_event(outcome=0.2, social_context=0.3)

    return serotonin


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
