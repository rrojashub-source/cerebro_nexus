"""
LAB_016: Acetylcholine System - Test Suite

TDD (Test-Driven Development) approach:
1. RED: Write failing tests first
2. GREEN: Implement code to pass tests
3. REFACTOR: Optimize while keeping tests passing

Biological Inspiration:
- Basal forebrain cholinergic neurons
- Hasselmo (2006) - "The role of acetylcholine in learning and memory"

Core Functions:
- Attention amplification (enhances signal-to-noise)
- Encoding strength (high ACh → strong memory formation)
- Learning rate modulation (ACh gates plasticity)
- Stimulus selectivity (enhances relevant, suppresses irrelevant)

Test Phases:
- Phase 1: Core ACh Tests (basic functionality)
- Phase 2: Integration Tests (with other LABs)
- Phase 3: Edge Cases & Performance
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_016_Acetylcholine_System import AcetylcholineSystem


# ============================================================================
# PHASE 1: CORE ACETYLCHOLINE TESTS
# ============================================================================

class TestBasicACh:
    """Test 1: Basic ACh Level Management"""

    def test_ach_baseline(self):
        """ACh should start at baseline"""
        ach = AcetylcholineSystem(baseline_level=0.5)
        assert ach.current_level == pytest.approx(0.5)

    def test_attention_demand_increases_ach(self):
        """Attention demand should increase ACh"""
        ach = AcetylcholineSystem(baseline_level=0.5)
        initial = ach.current_level

        ach.update_level(attention_demand=0.8, learning_context=False)

        assert ach.current_level > initial

    def test_learning_context_activates_ach(self):
        """Learning context should strongly activate ACh"""
        ach = AcetylcholineSystem(baseline_level=0.5)
        initial = ach.current_level

        ach.update_level(attention_demand=0.5, learning_context=True)

        assert ach.current_level > initial

    def test_ach_level_bounds(self):
        """ACh should be clamped between 0 and 1"""
        ach = AcetylcholineSystem()

        # Test upper bound
        for _ in range(20):
            ach.update_level(attention_demand=1.0, learning_context=True)

        assert 0.0 <= ach.current_level <= 1.0


class TestAttentionAmplification:
    """Test 2: Attention Gain Modulation"""

    def test_high_ach_amplifies_attention(self):
        """High ACh should amplify attention signal"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set high ACh
        ach.current_level = 0.9

        attention_gain = ach.compute_attention_gain(stimulus_relevance=0.8)

        # High ACh + high relevance → strong amplification
        assert attention_gain > 1.5

    def test_low_ach_minimal_amplification(self):
        """Low ACh should give minimal amplification"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set low ACh
        ach.current_level = 0.2

        attention_gain = ach.compute_attention_gain(stimulus_relevance=0.5)

        # Low ACh → minimal amplification (close to 1.0)
        assert 1.0 <= attention_gain < 1.5

    def test_irrelevant_stimuli_suppressed(self):
        """Irrelevant stimuli should be suppressed"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set moderate ACh
        ach.current_level = 0.7

        # Low relevance should give low gain
        gain_low = ach.compute_attention_gain(stimulus_relevance=0.2)
        gain_high = ach.compute_attention_gain(stimulus_relevance=0.8)

        assert gain_low < gain_high


class TestEncodingStrength:
    """Test 3: Memory Encoding Enhancement"""

    def test_high_ach_boosts_encoding(self):
        """High ACh should boost memory encoding"""
        ach = AcetylcholineSystem(baseline_level=0.5, encoding_boost=1.5)

        # Set high ACh
        ach.current_level = 0.9

        base_strength = 0.5
        boosted_strength = ach.compute_encoding_strength(base_strength)

        assert boosted_strength > base_strength

    def test_low_ach_baseline_encoding(self):
        """Low ACh should give near-baseline encoding"""
        ach = AcetylcholineSystem(baseline_level=0.5, encoding_boost=1.5)

        # Set low ACh
        ach.current_level = 0.2

        base_strength = 0.5
        boosted_strength = ach.compute_encoding_strength(base_strength)

        # Should be close to base (minimal boost)
        assert base_strength <= boosted_strength < base_strength * 1.3

    def test_encoding_bounded(self):
        """Encoding strength should not exceed 1.0"""
        ach = AcetylcholineSystem(baseline_level=0.5, encoding_boost=2.0)

        # Set max ACh
        ach.current_level = 1.0

        base_strength = 0.9
        boosted_strength = ach.compute_encoding_strength(base_strength)

        assert boosted_strength <= 1.0


class TestLearningRateModulation:
    """Test 4: Learning Rate Gating"""

    def test_high_ach_increases_learning_rate(self):
        """High ACh should gate plasticity (increase LR)"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set high ACh (learning mode)
        ach.current_level = 0.9

        base_lr = 0.1
        modulated_lr = ach.compute_learning_rate_modulation(base_lr)

        assert modulated_lr > base_lr

    def test_low_ach_reduces_learning_rate(self):
        """Low ACh should reduce plasticity"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set low ACh
        ach.current_level = 0.2

        base_lr = 0.1
        modulated_lr = ach.compute_learning_rate_modulation(base_lr)

        # Should be close to or below base
        assert modulated_lr <= base_lr * 1.2

    def test_learning_rate_bounded(self):
        """Learning rate should remain in reasonable bounds"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set max ACh
        ach.current_level = 1.0

        base_lr = 0.1
        modulated_lr = ach.compute_learning_rate_modulation(base_lr)

        # Should not explode (reasonable upper bound)
        assert modulated_lr < base_lr * 3.0


class TestSNREnhancement:
    """Test 5: Signal-to-Noise Ratio Enhancement"""

    def test_high_ach_improves_snr(self):
        """High ACh should improve signal-to-noise ratio"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set high ACh
        ach.current_level = 0.9

        snr_enhancement = ach.compute_snr_enhancement()

        # High ACh → strong SNR enhancement
        assert snr_enhancement > 0.7

    def test_low_ach_minimal_snr_enhancement(self):
        """Low ACh should give minimal SNR enhancement"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Set low ACh
        ach.current_level = 0.2

        snr_enhancement = ach.compute_snr_enhancement()

        # Low ACh → minimal SNR enhancement
        assert snr_enhancement < 0.5

    def test_snr_scales_with_ach(self):
        """SNR enhancement should scale with ACh level"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Test multiple ACh levels
        ach.current_level = 0.3
        snr_low = ach.compute_snr_enhancement()

        ach.current_level = 0.7
        snr_high = ach.compute_snr_enhancement()

        assert snr_high > snr_low


class TestFullEventProcessing:
    """Test 6: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all ACh outputs"""
        ach = AcetylcholineSystem()

        result = ach.process_event(
            attention_demand=0.7,
            learning=True
        )

        # Verify all expected keys
        assert "ach_level" in result
        assert "attention_gain" in result
        assert "encoding_strength" in result
        assert "learning_rate_modulation" in result
        assert "snr_enhancement" in result

    def test_learning_mode_activates_ach(self):
        """Learning mode should strongly activate ACh"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # No learning
        result_no_learning = ach.process_event(attention_demand=0.5, learning=False)
        level_no_learning = result_no_learning["ach_level"]

        # With learning
        ach2 = AcetylcholineSystem(baseline_level=0.5)
        result_learning = ach2.process_event(attention_demand=0.5, learning=True)
        level_learning = result_learning["ach_level"]

        assert level_learning > level_no_learning

    def test_history_tracking(self):
        """ACh should maintain level history"""
        ach = AcetylcholineSystem(history_window=5)

        for i in range(10):
            ach.process_event(attention_demand=0.6, learning=(i % 2 == 0))

        # History should be limited to window size
        assert len(ach.level_history) == 5

    def test_event_counter(self):
        """Should correctly count total events"""
        ach = AcetylcholineSystem()

        for i in range(7):
            ach.process_event(attention_demand=0.5, learning=False)

        assert ach.total_events == 7


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestIntegrationWithNorepinephrine:
    """Test 7: Integration with LAB_015 (Norepinephrine)"""

    def test_ach_ne_attention_synergy(self):
        """
        ACh selectivity + NE arousal = focused attention

        High ACh enhances relevant stimuli
        NE arousal provides energy/focus
        Together = strong selective attention
        """
        ach = AcetylcholineSystem(baseline_level=0.7)

        # Simulate high ACh (attention amplification)
        attention_gain = ach.compute_attention_gain(stimulus_relevance=0.9)

        # High ACh should give strong amplification
        assert attention_gain > 1.5


class TestIntegrationWithDopamine:
    """Test 8: Integration with LAB_013 (Dopamine)"""

    def test_ach_dopamine_learning_synergy(self):
        """
        ACh gates plasticity + dopamine RPE = effective learning

        ACh opens learning gate (high LR)
        Dopamine provides learning signal (RPE)
        Together = strong learning
        """
        ach = AcetylcholineSystem(baseline_level=0.8)

        # Simulate learning mode (high ACh)
        base_lr = 0.1
        gated_lr = ach.compute_learning_rate_modulation(base_lr)

        # High ACh should increase learning rate
        assert gated_lr > base_lr * 1.3


class TestIntegrationWithNovelty:
    """Test 9: Integration with LAB_004 (Novelty Detection)"""

    def test_novelty_triggers_ach_spike(self):
        """
        Novel stimuli should trigger ACh spike (attention capture)

        Novelty detected → ACh spike → attention amplification + encoding boost
        """
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Simulate novelty event (high attention demand)
        result = ach.process_event(attention_demand=0.9, learning=False)

        # Should increase ACh
        assert result["ach_level"] > 0.5


# ============================================================================
# PHASE 3: EDGE CASES & PERFORMANCE
# ============================================================================

class TestEdgeCases:
    """Test 10: Edge Cases"""

    def test_extreme_attention_demand(self):
        """System should handle extreme attention demand"""
        ach = AcetylcholineSystem()

        result = ach.process_event(attention_demand=1.0, learning=True)

        # Should remain bounded
        assert 0.0 <= result["ach_level"] <= 1.0

    def test_zero_attention(self):
        """System should handle zero attention"""
        ach = AcetylcholineSystem()

        result = ach.process_event(attention_demand=0.0, learning=False)

        # Should work normally
        assert 0.0 <= result["ach_level"] <= 1.0

    def test_rapid_context_switches(self):
        """System should handle rapid learning/non-learning switches"""
        ach = AcetylcholineSystem()

        # Rapid alternating learning/non-learning
        for i in range(20):
            learning = (i % 2 == 0)
            ach.process_event(attention_demand=0.5, learning=learning)

        # Should remain stable
        assert 0.0 <= ach.current_level <= 1.0


class TestStatePersistence:
    """Test 11: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        ach = AcetylcholineSystem()

        # Generate some history
        for i in range(5):
            ach.process_event(attention_demand=0.6, learning=(i < 3))

        state = ach.get_state()

        # Verify all expected keys
        assert "ach_level" in state
        assert "level_history" in state
        assert "level_mean" in state
        assert "attention_gain" in state
        assert "encoding_strength" in state
        assert "learning_rate_modulation" in state
        assert "snr_enhancement" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        ach = AcetylcholineSystem()

        ach.process_event(attention_demand=0.7, learning=True)

        state1 = ach.get_state()
        state2 = ach.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["ach_level"] == state2["ach_level"]


class TestLongTermDynamics:
    """Test 12: Long-term Dynamics"""

    def test_sustained_learning_mode(self):
        """Prolonged learning should maintain high ACh"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Sustained learning
        for _ in range(15):
            ach.process_event(attention_demand=0.7, learning=True)

        # ACh should be elevated
        assert ach.current_level > 0.6

    def test_ach_decays_without_demand(self):
        """ACh should decay toward baseline without attention demand"""
        ach = AcetylcholineSystem(baseline_level=0.5)

        # Spike ACh high
        for _ in range(10):
            ach.process_event(attention_demand=0.9, learning=True)

        high_level = ach.current_level

        # Apply low-demand events
        for _ in range(10):
            ach.process_event(attention_demand=0.1, learning=False)

        # Should decrease
        assert ach.current_level < high_level


# ============================================================================
# FIXTURES & UTILITIES
# ============================================================================

@pytest.fixture
def fresh_acetylcholine():
    """Fixture: Fresh AcetylcholineSystem instance"""
    return AcetylcholineSystem(
        baseline_level=0.5,
        attention_gain=2.0,
        encoding_boost=1.5,
        selectivity_factor=0.8,
        history_window=10
    )


@pytest.fixture
def ach_learning_mode():
    """Fixture: AcetylcholineSystem in learning mode"""
    ach = AcetylcholineSystem(baseline_level=0.5)

    # Create learning mode (high ACh)
    for _ in range(10):
        ach.process_event(attention_demand=0.8, learning=True)

    return ach


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
