"""
LAB_016: Acetylcholine System - Test Suite

TDD (Test-Driven Development) approach
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_016_Acetylcholine_System import AcetylcholineSystem


# ============================================================================
# PHASE 1: CORE FUNCTIONALITY TESTS
# ============================================================================

class TestAChUpdate:
    """Test 1: ACh Update Mechanism"""

    def test_novelty_increases_ach(self):
        """Novel stimuli should increase ACh"""
        ach = AcetylcholineSystem(baseline_ach=0.5)

        for _ in range(10):
            ach.update_ach(novelty=0.6, attention_demand=0.3)

        assert ach.ach_level > 0.5  # ACh increased

    def test_attention_demand_increases_ach(self):
        """High attention demand should increase ACh"""
        ach = AcetylcholineSystem(baseline_ach=0.5)

        for _ in range(15):
            ach.update_ach(novelty=0.2, attention_demand=0.8)

        assert ach.ach_level > 0.5  # ACh increased

    def test_ach_decays_toward_baseline(self):
        """ACh should decay back toward baseline over time"""
        ach = AcetylcholineSystem(baseline_ach=0.5, ach_decay=0.85)

        # Spike ACh high
        ach.update_ach(novelty=1.0, attention_demand=1.0)
        ach_after_spike = ach.ach_level

        # Let it decay (no novelty/attention)
        for _ in range(20):
            ach.update_ach(novelty=0.0, attention_demand=0.0)

        # Should have decayed toward baseline (0.5)
        assert ach.ach_level < ach_after_spike
        assert abs(ach.ach_level - 0.5) < abs(ach_after_spike - 0.5)


class TestAttentionAmplification:
    """Test 2: Attention Amplification"""

    def test_high_ach_amplifies_attention(self):
        """High ACh should amplify attention signal"""
        ach = AcetylcholineSystem(baseline_ach=0.9, amplification_gain=0.3)

        base_attention = 0.5
        amplified = ach.amplify_attention(base_attention)

        assert amplified > base_attention  # Amplified

    def test_low_ach_baseline_attention(self):
        """Low ACh should give baseline attention (minimal amplification)"""
        ach = AcetylcholineSystem(baseline_ach=0.1, amplification_gain=0.3)

        base_attention = 0.5
        amplified = ach.amplify_attention(base_attention)

        assert amplified < base_attention * 1.1  # Minimal amplification

    def test_amplification_clamped(self):
        """Amplification should not exceed 1.0"""
        ach = AcetylcholineSystem(baseline_ach=1.0, amplification_gain=0.5)

        base_attention = 0.9
        amplified = ach.amplify_attention(base_attention)

        assert amplified <= 1.0  # Clamped


class TestEncodingModulation:
    """Test 3: Encoding Modulation"""

    def test_encoding_mode_strong_encoding(self):
        """Encoding mode with high ACh should give strong encoding"""
        ach = AcetylcholineSystem(baseline_ach=0.8, encoding_threshold=0.6)
        ach.set_mode("encoding")

        result = ach.modulate_encoding(base_encoding_strength=0.5)

        assert result["is_strong_encoding"] is True
        assert result["encoding_strength"] > 0.5  # Boosted

    def test_recall_mode_weak_encoding(self):
        """Recall mode should reduce encoding (consolidation phase)"""
        ach = AcetylcholineSystem(baseline_ach=0.8)
        ach.set_mode("recall")

        result = ach.modulate_encoding(base_encoding_strength=0.5)

        assert result["is_strong_encoding"] is False
        assert result["encoding_strength"] < 0.5  # Reduced

    def test_low_ach_weak_encoding(self):
        """Low ACh should give weak encoding even in encoding mode"""
        ach = AcetylcholineSystem(baseline_ach=0.3, encoding_threshold=0.6)
        ach.set_mode("encoding")

        result = ach.modulate_encoding(base_encoding_strength=0.5)

        assert result["is_strong_encoding"] is False  # Below threshold


class TestLearningReadiness:
    """Test 4: Learning Readiness"""

    def test_high_ach_ready_to_learn(self):
        """High ACh should indicate readiness to learn"""
        ach = AcetylcholineSystem(baseline_ach=0.8, encoding_threshold=0.6)

        result = ach.compute_learning_readiness()

        assert result["is_ready_to_learn"] is True
        assert result["plasticity_gate"] > 0.6  # High plasticity

    def test_low_ach_not_ready(self):
        """Low ACh should indicate not ready to learn (consolidation)"""
        ach = AcetylcholineSystem(baseline_ach=0.3, encoding_threshold=0.6)

        result = ach.compute_learning_readiness()

        assert result["is_ready_to_learn"] is False
        assert result["plasticity_gate"] < 0.6  # Low plasticity


class TestModeSwitch:
    """Test 5: Mode Switching"""

    def test_set_encoding_mode(self):
        """Should be able to set encoding mode"""
        ach = AcetylcholineSystem()
        ach.set_mode("encoding")

        assert ach.mode == "encoding"

    def test_set_recall_mode(self):
        """Should be able to set recall mode"""
        ach = AcetylcholineSystem()
        ach.set_mode("recall")

        assert ach.mode == "recall"


class TestAChStability:
    """Test 6: ACh Stability"""

    def test_stable_ach_has_high_stability(self):
        """Consistent ACh should have high stability score"""
        ach = AcetylcholineSystem()

        # Many events with same intensity
        for _ in range(20):
            ach.update_ach(novelty=0.3, attention_demand=0.3)

        stability = ach.get_ach_stability()

        assert stability > 0.8  # High stability

    def test_volatile_ach_has_low_stability(self):
        """Volatile ACh should have low stability score"""
        ach = AcetylcholineSystem(ach_decay=0.5, novelty_sensitivity=1.0)

        # Alternating extreme novelty levels
        for i in range(50):
            novelty = 1.0 if i % 2 == 0 else 0.0
            attention = 1.0 if i % 2 == 0 else 0.0
            ach.update_ach(novelty=novelty, attention_demand=attention)

        stability = ach.get_ach_stability()

        assert stability < 0.99  # Lower than stable (which would be >0.99)


class TestFullProcessing:
    """Test 7: Full Stimulus Processing"""

    def test_process_stimulus_returns_complete_state(self):
        """process_stimulus should return all ACh outputs"""
        ach = AcetylcholineSystem()

        result = ach.process_stimulus(
            novelty=0.5,
            attention_demand=0.4,
            base_attention=0.5,
            base_encoding_strength=0.5
        )

        assert "ach_level" in result
        assert "amplified_attention" in result
        assert "encoding" in result
        assert "learning_readiness" in result
        assert "ach_stability" in result

    def test_ach_history_window_maintained(self):
        """ACh history should maintain fixed window size"""
        ach = AcetylcholineSystem(history_window=10)

        for i in range(25):
            ach.process_stimulus(novelty=0.3, attention_demand=0.3)

        assert len(ach.ach_history) == 10  # Window maintained

    def test_total_events_counter(self):
        """Should correctly count total events"""
        ach = AcetylcholineSystem()

        for i in range(15):
            ach.process_stimulus(novelty=0.2, attention_demand=0.2)

        assert ach.total_events == 15


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestNoveltyAttentionInteraction:
    """Test 8: Novelty + Attention Interaction"""

    def test_high_novelty_high_attention_strong_effect(self):
        """
        High novelty + high attention = strong ACh spike
        """
        ach = AcetylcholineSystem(baseline_ach=0.5)

        result = ach.process_stimulus(
            novelty=0.9,
            attention_demand=0.9,
            base_attention=0.5
        )

        # ACh should spike significantly
        assert result["ach_level"] > 0.7
        # Attention should be amplified
        assert result["amplified_attention"] > 0.5

    def test_encoding_recall_cycle(self):
        """
        Encoding mode (high ACh) → Recall mode (low ACh) cycle
        """
        ach = AcetylcholineSystem(baseline_ach=0.7, encoding_threshold=0.6)

        # Encoding mode
        ach.set_mode("encoding")
        result_encoding = ach.process_stimulus(novelty=0.5, attention_demand=0.5)

        assert result_encoding["encoding"]["is_strong_encoding"] is True

        # Switch to recall mode
        ach.set_mode("recall")
        result_recall = ach.process_stimulus(novelty=0.1, attention_demand=0.1)

        assert result_recall["encoding"]["is_strong_encoding"] is False


# ============================================================================
# PHASE 3: EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Test 9: Edge Cases"""

    def test_extreme_novelty_clamped(self):
        """Extreme novelty should not exceed ACh bounds"""
        ach = AcetylcholineSystem(baseline_ach=0.5)

        # Many extremely novel stimuli
        for _ in range(50):
            ach.update_ach(novelty=1.0, attention_demand=1.0)

        # ACh should not exceed 1.0
        assert ach.ach_level <= 1.0

    def test_extreme_decay_clamped(self):
        """Extreme decay should not go below ACh bounds"""
        ach = AcetylcholineSystem(baseline_ach=0.5)

        # Spike high first
        ach.update_ach(novelty=1.0, attention_demand=1.0)

        # Then many decay cycles
        for _ in range(100):
            ach.update_ach(novelty=0.0, attention_demand=0.0)

        # ACh should not go below 0.0
        assert ach.ach_level >= 0.0


class TestStatePersistence:
    """Test 10: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        ach = AcetylcholineSystem()

        # Generate some history
        for i in range(10):
            ach.process_stimulus(novelty=0.3, attention_demand=0.3)

        state = ach.get_state()

        # Verify all expected keys
        assert "ach_level" in state
        assert "ach_history" in state
        assert "ach_mean" in state
        assert "ach_stability" in state
        assert "mode" in state
        assert "learning_readiness" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        ach = AcetylcholineSystem()

        ach.process_stimulus(novelty=0.3, attention_demand=0.3)

        state1 = ach.get_state()
        state2 = ach.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["ach_level"] == state2["ach_level"]


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def fresh_acetylcholine():
    """Fixture: Fresh AcetylcholineSystem instance"""
    return AcetylcholineSystem(
        baseline_ach=0.5,
        amplification_gain=0.3,
        encoding_threshold=0.6,
        novelty_sensitivity=0.4,
        ach_decay=0.9,
        history_window=20
    )


@pytest.fixture
def acetylcholine_with_history():
    """Fixture: AcetylcholineSystem with ACh history"""
    ach = AcetylcholineSystem()

    # Generate 15 stimuli
    for _ in range(15):
        ach.process_stimulus(novelty=0.4, attention_demand=0.4)

    return ach


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
