"""
LAB_017: GABA System - Test Suite

TDD (Test-Driven Development) approach
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_017_GABA_System import GABASystem


# ============================================================================
# PHASE 1: CORE FUNCTIONALITY TESTS
# ============================================================================

class TestGABAUpdate:
    """Test 1: GABA Update Mechanism"""

    def test_anxiety_increases_gaba(self):
        """High anxiety should increase GABA"""
        gaba = GABASystem(baseline_gaba=0.5)

        for _ in range(15):
            gaba.update_gaba(anxiety=0.8, excitation=0.3)

        assert gaba.gaba_level > 0.5  # GABA increased

    def test_excitation_increases_gaba(self):
        """High excitation should increase GABA"""
        gaba = GABASystem(baseline_gaba=0.5)

        for _ in range(20):
            gaba.update_gaba(anxiety=0.2, excitation=0.9)

        assert gaba.gaba_level > 0.5  # GABA increased

    def test_gaba_decays_toward_baseline(self):
        """GABA should decay back toward baseline over time"""
        gaba = GABASystem(baseline_gaba=0.5, gaba_decay=0.85)

        # Spike GABA high
        gaba.update_gaba(anxiety=1.0, excitation=1.0)
        gaba_after_spike = gaba.gaba_level

        # Let it decay (no anxiety/excitation)
        for _ in range(20):
            gaba.update_gaba(anxiety=0.0, excitation=0.0)

        # Should have decayed toward baseline (0.5)
        assert gaba.gaba_level < gaba_after_spike
        assert abs(gaba.gaba_level - 0.5) < abs(gaba_after_spike - 0.5)


class TestEIBalance:
    """Test 2: Excitation/Inhibition Balance"""

    def test_high_excitation_low_gaba_overexcited(self):
        """High excitation with low GABA should be over_excited"""
        gaba = GABASystem(baseline_gaba=0.2)

        result = gaba.compute_ei_balance(excitation=0.9)

        assert result["balance_state"] == "over_excited"
        assert result["is_balanced"] is False
        assert result["ei_ratio"] > 1.5  # High ratio

    def test_balanced_ei_ratio(self):
        """Healthy E/I ratio should be balanced"""
        gaba = GABASystem(baseline_gaba=0.7, inhibition_strength=0.7)

        result = gaba.compute_ei_balance(excitation=0.6)

        assert result["is_balanced"] is True
        assert result["balance_state"] == "balanced"
        assert 1.0 <= result["ei_ratio"] <= 1.5

    def test_high_gaba_low_excitation_overinhibited(self):
        """High GABA with low excitation should be over_inhibited"""
        gaba = GABASystem(baseline_gaba=0.9)

        result = gaba.compute_ei_balance(excitation=0.3)

        assert result["balance_state"] == "over_inhibited"
        assert result["is_balanced"] is False
        assert result["ei_ratio"] < 1.0  # Low ratio


class TestAnxietyModulation:
    """Test 3: Anxiety Modulation"""

    def test_high_gaba_reduces_anxiety(self):
        """High GABA should reduce anxiety"""
        gaba = GABASystem(baseline_gaba=0.9)

        base_anxiety = 0.8
        result = gaba.modulate_anxiety(base_anxiety)

        assert result["modulated_anxiety"] < base_anxiety  # Reduced
        assert result["is_calm"] is True

    def test_low_gaba_high_anxiety(self):
        """Low GABA should result in high anxiety"""
        gaba = GABASystem(baseline_gaba=0.2, anxiety_threshold=0.6)

        base_anxiety = 0.5
        result = gaba.modulate_anxiety(base_anxiety)

        assert result["modulated_anxiety"] >= base_anxiety * 0.8  # Minimal reduction
        assert result["is_calm"] is False

    def test_gaba_above_threshold_calm(self):
        """GABA above threshold should indicate calm state"""
        gaba = GABASystem(baseline_gaba=0.8, anxiety_threshold=0.6)

        result = gaba.modulate_anxiety(base_anxiety=0.5)

        assert result["is_calm"] is True  # Above threshold


class TestInhibitoryControl:
    """Test 4: Inhibitory Control"""

    def test_high_gaba_suppresses_excitation(self):
        """High GABA should strongly suppress excitatory signals"""
        gaba = GABASystem(baseline_gaba=0.9, inhibition_strength=0.7)

        excitatory_signal = 0.8
        result = gaba.compute_inhibitory_control(excitatory_signal)

        assert result["net_signal"] < excitatory_signal  # Suppressed
        assert result["suppression_ratio"] > 0.5  # Strong suppression

    def test_low_gaba_weak_suppression(self):
        """Low GABA should give weak suppression"""
        gaba = GABASystem(baseline_gaba=0.2, inhibition_strength=0.7)

        excitatory_signal = 0.8
        result = gaba.compute_inhibitory_control(excitatory_signal)

        assert result["net_signal"] > excitatory_signal * 0.7  # Weak suppression
        assert result["suppression_ratio"] < 0.3  # Low suppression

    def test_net_signal_clamped(self):
        """Net signal should be clamped to [0, 1]"""
        gaba = GABASystem(baseline_gaba=1.0, inhibition_strength=1.0)

        # Very high inhibition
        result = gaba.compute_inhibitory_control(excitatory_signal=0.3)

        assert result["net_signal"] >= 0.0  # Not negative


class TestNetworkStability:
    """Test 5: Network Stability"""

    def test_stable_gaba_high_stability(self):
        """Consistent GABA should have high stability score"""
        gaba = GABASystem()

        # Many events with same intensity
        for _ in range(20):
            gaba.update_gaba(anxiety=0.3, excitation=0.3)

        stability = gaba.get_network_stability()

        assert stability > 0.8  # High stability

    def test_volatile_gaba_low_stability(self):
        """Volatile GABA should have low stability score"""
        gaba = GABASystem(gaba_decay=0.5, anxiety_sensitivity=0.8)

        # Alternating extreme anxiety levels
        for i in range(40):
            anxiety = 1.0 if i % 2 == 0 else 0.0
            excitation = 1.0 if i % 2 == 0 else 0.0
            gaba.update_gaba(anxiety=anxiety, excitation=excitation)

        stability = gaba.get_network_stability()

        assert stability < 0.99  # Lower than stable


class TestFullProcessing:
    """Test 6: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all GABA outputs"""
        gaba = GABASystem()

        result = gaba.process_event(
            anxiety=0.5,
            excitation=0.4,
            base_anxiety=0.5,
            excitatory_signal=0.5
        )

        assert "gaba_level" in result
        assert "ei_balance" in result
        assert "anxiety" in result
        assert "inhibitory_control" in result
        assert "network_stability" in result

    def test_gaba_history_window_maintained(self):
        """GABA history should maintain fixed window size"""
        gaba = GABASystem(history_window=10)

        for i in range(25):
            gaba.process_event(anxiety=0.3, excitation=0.3)

        assert len(gaba.gaba_history) == 10  # Window maintained

    def test_total_events_counter(self):
        """Should correctly count total events"""
        gaba = GABASystem()

        for i in range(15):
            gaba.process_event(anxiety=0.2, excitation=0.2)

        assert gaba.total_events == 15


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestAnxietyExcitationInteraction:
    """Test 7: Anxiety + Excitation Interaction"""

    def test_high_anxiety_high_excitation_strong_gaba(self):
        """
        High anxiety + high excitation = strong GABA spike
        """
        gaba = GABASystem(baseline_gaba=0.5)

        result = gaba.process_event(
            anxiety=0.9,
            excitation=0.9,
            base_anxiety=0.8
        )

        # GABA should spike significantly
        assert result["gaba_level"] > 0.6
        # Anxiety should be modulated down
        assert result["anxiety"]["modulated_anxiety"] < 0.8

    def test_ei_balance_cycle(self):
        """
        E/I balance should shift from over_excited → balanced → over_inhibited
        """
        gaba = GABASystem(baseline_gaba=0.3)

        # Start: over_excited (low GABA)
        result1 = gaba.process_event(anxiety=0.2, excitation=0.8)
        assert result1["ei_balance"]["balance_state"] == "over_excited"

        # Build up GABA
        for _ in range(10):
            gaba.process_event(anxiety=0.7, excitation=0.7)

        # End: more balanced or over_inhibited (high GABA)
        result2 = gaba.process_event(anxiety=0.2, excitation=0.3)
        assert result2["ei_balance"]["balance_state"] in ["balanced", "over_inhibited"]


# ============================================================================
# PHASE 3: EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Test 8: Edge Cases"""

    def test_extreme_anxiety_clamped(self):
        """Extreme anxiety should not exceed GABA bounds"""
        gaba = GABASystem(baseline_gaba=0.5)

        # Many extremely anxious events
        for _ in range(50):
            gaba.update_gaba(anxiety=1.0, excitation=1.0)

        # GABA should not exceed 1.0
        assert gaba.gaba_level <= 1.0

    def test_extreme_decay_clamped(self):
        """Extreme decay should not go below GABA bounds"""
        gaba = GABASystem(baseline_gaba=0.5)

        # Spike high first
        gaba.update_gaba(anxiety=1.0, excitation=1.0)

        # Then many decay cycles
        for _ in range(100):
            gaba.update_gaba(anxiety=0.0, excitation=0.0)

        # GABA should not go below 0.0
        assert gaba.gaba_level >= 0.0


class TestStatePersistence:
    """Test 9: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        gaba = GABASystem()

        # Generate some history
        for i in range(10):
            gaba.process_event(anxiety=0.3, excitation=0.3)

        state = gaba.get_state()

        # Verify all expected keys
        assert "gaba_level" in state
        assert "gaba_history" in state
        assert "gaba_mean" in state
        assert "network_stability" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        gaba = GABASystem()

        gaba.process_event(anxiety=0.3, excitation=0.3)

        state1 = gaba.get_state()
        state2 = gaba.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["gaba_level"] == state2["gaba_level"]


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def fresh_gaba():
    """Fixture: Fresh GABASystem instance"""
    return GABASystem(
        baseline_gaba=0.5,
        inhibition_strength=0.7,
        anxiety_threshold=0.6,
        anxiety_sensitivity=0.3,
        gaba_decay=0.9,
        history_window=20
    )


@pytest.fixture
def gaba_with_history():
    """Fixture: GABASystem with GABA history"""
    gaba = GABASystem()

    # Generate 15 events
    for _ in range(15):
        gaba.process_event(anxiety=0.4, excitation=0.4)

    return gaba


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
