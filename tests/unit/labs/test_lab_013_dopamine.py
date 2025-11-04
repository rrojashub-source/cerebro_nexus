"""
LAB_013: Dopamine System - Test Suite

TDD (Test-Driven Development) approach:
1. RED: Write failing tests first
2. GREEN: Implement code to pass tests
3. REFACTOR: Optimize while keeping tests passing

Test Phases:
- Phase 1: Core RPE Tests (basic functionality)
- Phase 2: Integration Tests (with other LABs)
- Phase 3: Edge Cases & Performance
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_013_Dopamine_System import DopamineSystem


# ============================================================================
# PHASE 1: CORE RPE TESTS
# ============================================================================

class TestBasicRPEComputation:
    """Test 1: Basic RPE Computation"""

    def test_rpe_positive_surprise(self):
        """When actual > expected, RPE should be positive"""
        dopamine = DopamineSystem()
        rpe = dopamine.compute_rpe(expected=0.5, actual=0.8)
        assert rpe == pytest.approx(0.3)
        assert rpe > 0  # Positive surprise

    def test_rpe_negative_surprise(self):
        """When actual < expected, RPE should be negative"""
        dopamine = DopamineSystem()
        rpe = dopamine.compute_rpe(expected=0.7, actual=0.3)
        assert rpe == pytest.approx(-0.4)
        assert rpe < 0  # Negative surprise

    def test_rpe_no_surprise(self):
        """When actual == expected, RPE should be zero"""
        dopamine = DopamineSystem()
        rpe = dopamine.compute_rpe(expected=0.6, actual=0.6)
        assert rpe == 0.0


class TestLearningRateModulation:
    """Test 2: Learning Rate Modulation"""

    def test_lr_boost_on_positive_rpe(self):
        """Positive RPE should increase learning rate"""
        dopamine = DopamineSystem(baseline_lr=0.1, rpe_sensitivity=0.5)
        modulated_lr = dopamine.modulate_learning_rate(base_lr=0.1, rpe=0.4)
        assert modulated_lr > 0.1  # Boosted
        assert modulated_lr == pytest.approx(0.1 * (1.0 + 0.4 * 0.5))  # Formula

    def test_lr_reduction_on_negative_rpe(self):
        """Negative RPE should decrease learning rate"""
        dopamine = DopamineSystem(baseline_lr=0.1, rpe_sensitivity=0.5)
        modulated_lr = dopamine.modulate_learning_rate(base_lr=0.1, rpe=-0.6)
        assert modulated_lr < 0.1  # Reduced
        assert modulated_lr >= 0.01  # Clamped to minimum

    def test_lr_clipping(self):
        """Learning rate should be clamped between 0.01 and 1.0"""
        dopamine = DopamineSystem(baseline_lr=0.1, rpe_sensitivity=2.0)

        # Test upper bound
        modulated_lr_high = dopamine.modulate_learning_rate(base_lr=0.9, rpe=1.0)
        assert modulated_lr_high <= 1.0

        # Test lower bound
        modulated_lr_low = dopamine.modulate_learning_rate(base_lr=0.1, rpe=-1.0)
        assert modulated_lr_low >= 0.01


class TestMotivationTracking:
    """Test 3: Motivation Tracking"""

    def test_motivation_increases_with_positive_rpe(self):
        """Series of positive RPEs should increase motivation"""
        dopamine = DopamineSystem()

        initial_motivation = dopamine.motivation_level

        for _ in range(5):
            dopamine.update_motivation(rpe=0.3)

        assert dopamine.motivation_level > initial_motivation

    def test_motivation_decreases_with_negative_rpe(self):
        """Series of negative RPEs should decrease motivation"""
        dopamine = DopamineSystem()
        dopamine.motivation_level = 0.7  # Start high

        for _ in range(5):
            dopamine.update_motivation(rpe=-0.3)

        assert dopamine.motivation_level < 0.7

    def test_motivation_decay(self):
        """Motivation should decay toward baseline without RPE events"""
        dopamine = DopamineSystem(motivation_decay=0.9)
        dopamine.motivation_level = 0.9

        # Update with neutral RPE
        dopamine.update_motivation(rpe=0.0)

        # Motivation should decay
        assert dopamine.motivation_level < 0.9


class TestExplorationBonus:
    """Test 4: Exploration Bonus"""

    def test_exploration_bonus_increases_with_motivation(self):
        """Higher motivation should increase exploration"""
        dopamine = DopamineSystem()

        dopamine.motivation_level = 0.3
        low_exploration = dopamine.get_exploration_bonus()

        dopamine.motivation_level = 0.8
        high_exploration = dopamine.get_exploration_bonus()

        assert high_exploration > low_exploration

    def test_exploration_bonus_with_uncertainty(self):
        """Uncertainty should amplify exploration bonus"""
        dopamine = DopamineSystem()
        dopamine.motivation_level = 0.7

        low_uncertainty_explore = dopamine.get_exploration_bonus(uncertainty=0.2)
        high_uncertainty_explore = dopamine.get_exploration_bonus(uncertainty=0.9)

        assert high_uncertainty_explore > low_uncertainty_explore


class TestFullEventProcessing:
    """Test 5: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all dopamine outputs"""
        dopamine = DopamineSystem()

        result = dopamine.process_event(expected=0.5, actual=0.8)

        assert "rpe" in result
        assert "modulated_lr" in result
        assert "motivation_level" in result
        assert "exploration_bonus" in result
        assert result["rpe"] == pytest.approx(0.3)

    def test_rpe_history_window(self):
        """RPE history should maintain fixed window size"""
        dopamine = DopamineSystem(history_window=5)

        for i in range(10):
            dopamine.process_event(expected=0.5, actual=0.6)

        assert len(dopamine.rpe_history) == 5  # Window size maintained

    def test_total_events_counter(self):
        """Should correctly count total RPE events"""
        dopamine = DopamineSystem()

        for i in range(7):
            dopamine.process_event(expected=0.5, actual=0.6)

        assert dopamine.total_rpe_events == 7


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestIntegrationWithNoveltyDetection:
    """Test 6: Integration with LAB_004 (Novelty Detection)"""

    def test_high_novelty_lowers_expected_reward(self):
        """
        High novelty should bias expected reward lower (exploration)

        This simulates LAB_004 novelty signal affecting reward expectations
        """
        dopamine = DopamineSystem()

        # Novel situation: uncertain outcome, expect less
        expected_novel = 0.3
        actual_novel = 0.7
        result_novel = dopamine.process_event(expected=expected_novel, actual=actual_novel)

        # Familiar situation: certain outcome, expect more
        expected_familiar = 0.6
        actual_familiar = 0.7
        result_familiar = dopamine.process_event(expected=expected_familiar, actual=actual_familiar)

        # Novel situation should have higher RPE (positive surprise)
        assert result_novel["rpe"] > result_familiar["rpe"]
        # Novel situation should boost learning more
        assert result_novel["modulated_lr"] > result_familiar["modulated_lr"]


class TestIntegrationWithEmotionalSalience:
    """Test 7: Integration with LAB_001 (Emotional Salience)"""

    def test_high_rpe_boosts_salience(self):
        """
        High RPE should boost emotional salience

        This simulates LAB_001 salience scoring using RPE signal
        """
        dopamine = DopamineSystem()

        # High surprise event
        result_high_rpe = dopamine.process_event(expected=0.2, actual=0.9)
        high_rpe = abs(result_high_rpe["rpe"])

        # Low surprise event
        result_low_rpe = dopamine.process_event(expected=0.5, actual=0.6)
        low_rpe = abs(result_low_rpe["rpe"])

        # High RPE should be stronger signal
        assert high_rpe > low_rpe
        # Could be used to boost salience in LAB_001


class TestIntegrationWithDecayModulation:
    """Test 8: Integration with LAB_002 (Decay Modulation)"""

    def test_high_rpe_reduces_decay_rate(self):
        """
        High RPE memories should decay slower

        This simulates LAB_002 decay rate adjustment using RPE
        """
        dopamine = DopamineSystem()

        # Memorable event (high surprise)
        result_memorable = dopamine.process_event(expected=0.3, actual=0.9)
        rpe_memorable = abs(result_memorable["rpe"])

        # Mundane event (low surprise)
        result_mundane = dopamine.process_event(expected=0.5, actual=0.55)
        rpe_mundane = abs(result_mundane["rpe"])

        # High RPE should signal "important memory, decay slower"
        assert rpe_memorable > rpe_mundane
        # LAB_002 could use rpe_memorable to reduce decay rate


# ============================================================================
# PHASE 3: EDGE CASES & PERFORMANCE
# ============================================================================

class TestEdgeCases:
    """Test 9: Edge Cases"""

    def test_extreme_rpe_values(self):
        """System should handle extreme RPE values gracefully"""
        dopamine = DopamineSystem()

        # Maximum positive RPE
        rpe_max = dopamine.compute_rpe(expected=0.0, actual=1.0)
        assert rpe_max == 1.0

        # Maximum negative RPE
        rpe_min = dopamine.compute_rpe(expected=1.0, actual=0.0)
        assert rpe_min == -1.0

        # Should not crash on extreme modulation
        lr_extreme = dopamine.modulate_learning_rate(base_lr=0.1, rpe=1.0)
        assert 0.01 <= lr_extreme <= 1.0

    def test_zero_learning_rate(self):
        """System should handle zero base learning rate"""
        dopamine = DopamineSystem(baseline_lr=0.0)

        result = dopamine.process_event(expected=0.5, actual=0.8)

        # Should not crash, should clamp to minimum
        assert result["modulated_lr"] >= 0.01

    def test_boundary_values(self):
        """Test boundary conditions for all parameters"""
        dopamine = DopamineSystem()

        # Boundary: expected = actual (no surprise)
        result_zero = dopamine.process_event(expected=0.5, actual=0.5)
        assert result_zero["rpe"] == 0.0

        # Boundary: min values
        result_min = dopamine.process_event(expected=0.0, actual=0.0)
        assert result_min["rpe"] == 0.0

        # Boundary: max values
        result_max = dopamine.process_event(expected=1.0, actual=1.0)
        assert result_max["rpe"] == 0.0


class TestStatePersistence:
    """Test 10: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        dopamine = DopamineSystem()

        # Generate some history
        for i in range(5):
            dopamine.process_event(expected=0.5, actual=0.6)

        state = dopamine.get_state()

        # Verify all expected keys
        assert "rpe_current" in state
        assert "rpe_history" in state
        assert "rpe_mean" in state
        assert "motivation_level" in state
        assert "learning_rate_multiplier" in state
        assert "exploration_bonus" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        dopamine = DopamineSystem()

        dopamine.process_event(expected=0.5, actual=0.8)

        state1 = dopamine.get_state()
        state2 = dopamine.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["motivation_level"] == state2["motivation_level"]


# ============================================================================
# FIXTURES & UTILITIES
# ============================================================================

@pytest.fixture
def fresh_dopamine():
    """Fixture: Fresh DopamineSystem instance"""
    return DopamineSystem(
        baseline_lr=0.1,
        rpe_sensitivity=0.5,
        motivation_decay=0.95,
        history_window=10
    )


@pytest.fixture
def dopamine_with_history():
    """Fixture: DopamineSystem with some history"""
    dopamine = DopamineSystem()

    # Generate 5 positive events
    for _ in range(5):
        dopamine.process_event(expected=0.4, actual=0.7)

    return dopamine


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
