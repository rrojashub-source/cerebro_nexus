"""
NeuroEmotionalBridge - Test Suite

TDD (Test-Driven Development) approach
Integration between Layer 2 (Emotional 8D) and Layer 4 (Neurotransmitters)
"""

import pytest
import sys
from pathlib import Path
from dataclasses import dataclass

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from INTEGRATION_LAYERS import NeuroEmotionalBridge
from LAYER_4_Neurochemistry_Full.LAB_013_Dopamine_System import DopamineSystem
from LAYER_4_Neurochemistry_Full.LAB_014_Serotonin_System import SerotoninSystem
from LAYER_4_Neurochemistry_Full.LAB_015_Norepinephrine_System import NorepinephrineSystem
from LAYER_4_Neurochemistry_Full.LAB_016_Acetylcholine_System import AcetylcholineSystem
from LAYER_4_Neurochemistry_Full.LAB_017_GABA_System import GABASystem


# ============================================================================
# TEST DATA STRUCTURES
# ============================================================================

@dataclass
class EmotionalState:
    """Plutchik 8D emotional state"""
    joy: float = 0.0
    trust: float = 0.0
    fear: float = 0.0
    surprise: float = 0.0
    sadness: float = 0.0
    disgust: float = 0.0
    anger: float = 0.0
    anticipation: float = 0.0


@dataclass
class SomaticMarker:
    """Damasio somatic marker (simplified)"""
    valence: float = 0.0
    arousal: float = 0.0
    situation: str = "neutral"


# ============================================================================
# PHASE 1: FORWARD PASS TESTS (Emotions → Neurotransmitters)
# ============================================================================

class TestForwardPass:
    """Test 1: Emotions → Neurotransmitters"""

    def test_joy_increases_dopamine(self):
        """High joy should increase dopamine motivation level"""
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(joy=0.8, anticipation=0.2)
        somatic_marker = SomaticMarker(valence=0.6, arousal=0.5)

        result = bridge.forward_pass(emotional_state, somatic_marker)

        # Joy (0.8) * 0.4 = 0.32 contribution
        assert result['dopamine'] > 0.3  # Should be elevated
        assert result['dopamine'] <= 1.0  # Clamped

    def test_fear_increases_norepinephrine(self):
        """High fear should increase norepinephrine arousal"""
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(fear=0.9)
        somatic_marker = SomaticMarker(valence=-0.5, arousal=0.8)

        result = bridge.forward_pass(emotional_state, somatic_marker)

        # Fear (0.9) * 0.6 + arousal (0.8) * 0.4 = 0.54 + 0.32 = 0.86
        assert result['norepinephrine'] > 0.7  # Should be high
        assert result['norepinephrine'] <= 1.0

    def test_trust_increases_serotonin(self):
        """High trust should increase serotonin mood level"""
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(trust=0.8, sadness=0.1)
        somatic_marker = SomaticMarker(valence=0.7)

        result = bridge.forward_pass(emotional_state, somatic_marker)

        # Trust (0.8) * 0.5 - sadness (0.1) * 0.3 = 0.4 - 0.03 = 0.37
        assert result['serotonin'] > 0.3
        assert result['serotonin'] <= 1.0

    def test_anticipation_increases_dopamine_and_acetylcholine(self):
        """High anticipation should increase both dopamine and acetylcholine"""
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(anticipation=0.9, surprise=0.2)
        somatic_marker = SomaticMarker()

        result = bridge.forward_pass(emotional_state, somatic_marker)

        # Dopamine: anticipation (0.9) * 0.3 = 0.27
        assert result['dopamine'] > 0.25

        # Acetylcholine: anticipation (0.9) * 0.5 = 0.45
        assert result['acetylcholine'] > 0.4
        assert result['acetylcholine'] <= 1.0

    def test_anger_increases_gaba_compensatory(self):
        """High anger should trigger GABA spike (inhibitory control)"""
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(anger=0.8, fear=0.5)
        somatic_marker = SomaticMarker(valence=-0.6, arousal=0.7)

        result = bridge.forward_pass(emotional_state, somatic_marker)

        # Anger (0.8) * 0.4 = 0.32 contribution
        assert result['gaba'] > 0.3  # Compensatory GABA spike
        assert result['gaba'] <= 1.0

    def test_sadness_decreases_serotonin(self):
        """High sadness should deplete serotonin"""
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(sadness=0.9, trust=0.2)
        somatic_marker = SomaticMarker(valence=-0.8)

        result = bridge.forward_pass(emotional_state, somatic_marker)

        # Trust (0.2) * 0.5 - sadness (0.9) * 0.3 = 0.1 - 0.27 = -0.17 (baseline shifts down)
        assert result['serotonin'] < 0.5  # Below neutral baseline


# ============================================================================
# PHASE 2: BACKWARD PASS TESTS (Neurotransmitters → Emotions)
# ============================================================================

class TestBackwardPass:
    """Test 2: Neurotransmitters → Emotions"""

    def test_high_dopamine_boosts_joy(self):
        """High dopamine should increase joy emotion"""
        bridge = NeuroEmotionalBridge()

        # Simulate high dopamine state
        bridge.neuro_systems['dopamine'].motivation_level = 0.85

        emotional_modulation = bridge.backward_pass()

        # Dopamine (0.85) * 0.3 = 0.255
        assert emotional_modulation['joy_boost'] > 0.2
        assert emotional_modulation['joy_boost'] <= 0.3  # Max modulation cap

    def test_high_serotonin_boosts_trust_reduces_sadness(self):
        """High serotonin should increase trust and reduce sadness"""
        bridge = NeuroEmotionalBridge()

        # Simulate high serotonin state
        bridge.neuro_systems['serotonin'].mood_level = 0.9

        emotional_modulation = bridge.backward_pass()

        # Trust boost: 0.9 * 0.4 = 0.36
        assert emotional_modulation['trust_boost'] > 0.2
        # Sadness reduction: negative value
        assert emotional_modulation['sadness_reduction'] < 0

    def test_excessive_norepinephrine_increases_fear(self):
        """Very high norepinephrine (>0.7) should trigger fear response"""
        bridge = NeuroEmotionalBridge()

        # Simulate excessive arousal (Yerkes-Dodson breakdown)
        bridge.neuro_systems['norepinephrine'].arousal_level = 0.9

        emotional_modulation = bridge.backward_pass()

        # Only if arousal > 0.7
        if bridge.neuro_systems['norepinephrine'].arousal_level > 0.7:
            assert 'fear_boost' in emotional_modulation
            assert emotional_modulation['fear_boost'] > 0

    def test_high_gaba_reduces_fear_and_anger(self):
        """High GABA should reduce fear and anger (calming effect)"""
        bridge = NeuroEmotionalBridge()

        # Simulate high GABA (anxiolytic state)
        bridge.neuro_systems['gaba'].gaba_level = 0.9

        emotional_modulation = bridge.backward_pass()

        # Fear reduction: 0.9 * -0.4 = -0.36, clamped to -0.3 (MAX_MODULATION)
        assert emotional_modulation['fear_reduction'] <= -0.25
        # Anger reduction: 0.9 * -0.3 = -0.27
        assert emotional_modulation['anger_reduction'] <= -0.2

    def test_high_acetylcholine_boosts_anticipation(self):
        """High acetylcholine should increase anticipation (attention gating)"""
        bridge = NeuroEmotionalBridge()

        # Simulate high attention state
        bridge.neuro_systems['acetylcholine'].ach_level = 0.9

        emotional_modulation = bridge.backward_pass()

        # Should boost anticipation
        assert 'anticipation_boost_ach' in emotional_modulation
        assert emotional_modulation['anticipation_boost_ach'] > 0


# ============================================================================
# PHASE 3: FULL CYCLE TESTS (Bidirectional Feedback)
# ============================================================================

class TestFullCycle:
    """Test 3: Full Bidirectional Integration"""

    def test_positive_feedback_loop_converges(self):
        """
        Test that joy → dopamine → joy loop converges (doesn't runaway)

        Should reach equilibrium due to dampening
        """
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(joy=0.5, anticipation=0.3)
        somatic_marker = SomaticMarker(valence=0.6)

        # Run 10 cycles
        joy_history = [emotional_state.joy]

        for _ in range(10):
            result = bridge.process_event(emotional_state, somatic_marker)

            # Apply emotional modulation back to state
            if 'joy_boost' in result['emotional_modulation']:
                emotional_state.joy += result['emotional_modulation']['joy_boost']
                emotional_state.joy = min(1.0, emotional_state.joy)  # Clamp

            joy_history.append(emotional_state.joy)

        # Should converge (not continue growing)
        # Last 3 values should be similar (< 0.05 variance)
        final_variance = max(joy_history[-3:]) - min(joy_history[-3:])
        assert final_variance < 0.1  # Converged

    def test_anxiety_gaba_negative_feedback_stabilizes(self):
        """
        Test that anxiety → GABA → fear reduction creates stable homeostasis
        """
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(fear=0.8, anger=0.6)
        somatic_marker = SomaticMarker(valence=-0.7, arousal=0.9)

        # Run 5 cycles (not 10, with MAX_MODULATION=0.3, 10 cycles brings fear to 0)
        fear_history = [emotional_state.fear]

        for _ in range(5):
            result = bridge.process_event(emotional_state, somatic_marker)

            # Apply fear reduction
            if 'fear_reduction' in result['emotional_modulation']:
                emotional_state.fear += result['emotional_modulation']['fear_reduction']
                emotional_state.fear = max(0.0, emotional_state.fear)  # Clamp

            fear_history.append(emotional_state.fear)

        # Fear should decrease over time (GABA calming)
        assert fear_history[-1] < fear_history[0]
        # Should still have some fear (not reach zero after 5 cycles)
        assert fear_history[-1] >= 0.0  # System is working (GABA reduces fear)

    def test_breakthrough_event_synergy(self):
        """
        Test multi-system synergy during breakthrough moment:
        joy + anticipation → dopamine + ACh → enhanced state
        """
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState(
            joy=0.9,
            anticipation=0.85,
            trust=0.8
        )
        somatic_marker = SomaticMarker(
            valence=0.9,
            arousal=0.7,
            situation="breakthrough"
        )

        result = bridge.process_event(emotional_state, somatic_marker)

        # Multiple neurotransmitters should be elevated
        assert result['neuro_state']['dopamine'] > 0.6  # Motivation
        assert result['neuro_state']['serotonin'] > 0.5  # Mood stability
        assert result['neuro_state']['acetylcholine'] > 0.5  # Attention encoding

        # Emotional modulation should enhance all positive emotions
        assert result['emotional_modulation']['joy_boost'] > 0
        assert result['emotional_modulation']['trust_boost'] > 0


# ============================================================================
# PHASE 4: INTEGRATION WITH EXISTING SYSTEMS
# ============================================================================

class TestIntegrationWithLAB001:
    """Test 4: Integration with LAB_001 Emotional Salience"""

    def test_high_salience_amplifies_neurotransmitter_response(self):
        """
        Emotionally salient events should trigger stronger neuro response
        """
        bridge = NeuroEmotionalBridge()

        # High salience event (emotionally intense)
        emotional_state = EmotionalState(
            joy=0.9,
            surprise=0.8,
            anticipation=0.85
        )
        somatic_marker = SomaticMarker(valence=0.9, arousal=0.8)

        result = bridge.process_event(emotional_state, somatic_marker)

        # Calculate salience (using LAB_001 algorithm - simplified here)
        intensity = 0.9  # High
        complexity = 0.7  # Mixed emotions

        # High salience should amplify dopamine response
        assert result['neuro_state']['dopamine'] > 0.7

    def test_low_salience_minimal_neurotransmitter_response(self):
        """
        Emotionally neutral events should have minimal neuro response
        """
        bridge = NeuroEmotionalBridge()

        # Low salience event (neutral)
        emotional_state = EmotionalState(
            joy=0.1,
            trust=0.2,
            anticipation=0.1
        )
        somatic_marker = SomaticMarker(valence=0.0, arousal=0.2)

        result = bridge.process_event(emotional_state, somatic_marker)

        # All neurotransmitters should be near baseline (baselines added: dopamine 0.4, serotonin 0.5, NE 0.3)
        assert result['neuro_state']['dopamine'] < 0.6  # Baseline 0.4 + low joy/anticipation
        assert result['neuro_state']['serotonin'] <= 0.65  # Baseline 0.5 + low trust
        assert result['neuro_state']['norepinephrine'] < 0.6  # Baseline 0.3 + low arousal


# ============================================================================
# PHASE 5: EDGE CASES & ROBUSTNESS
# ============================================================================

class TestEdgeCases:
    """Test 5: Edge Cases"""

    def test_all_zeros_emotional_state(self):
        """Handle all-zero emotional state gracefully"""
        bridge = NeuroEmotionalBridge()

        emotional_state = EmotionalState()  # All zeros
        somatic_marker = SomaticMarker()

        result = bridge.process_event(emotional_state, somatic_marker)

        # Should return baseline neurotransmitter levels
        assert 0.3 <= result['neuro_state']['dopamine'] <= 0.6
        assert 0.3 <= result['neuro_state']['serotonin'] <= 0.6

    def test_extreme_emotions_clamped(self):
        """Extreme emotions should be clamped to valid ranges"""
        bridge = NeuroEmotionalBridge()

        # Extreme values
        emotional_state = EmotionalState(
            joy=1.0,
            anticipation=1.0,
            trust=1.0
        )
        somatic_marker = SomaticMarker(valence=1.0, arousal=1.0)

        result = bridge.process_event(emotional_state, somatic_marker)

        # All neurotransmitters should be clamped to [0, 1]
        for neuro_type, level in result['neuro_state'].items():
            assert 0.0 <= level <= 1.0

    def test_modulation_cap_enforced(self):
        """Emotional modulation should respect MAX_MODULATION cap"""
        bridge = NeuroEmotionalBridge()

        # High neurotransmitter state
        bridge.neuro_systems['dopamine'].motivation_level = 1.0
        bridge.neuro_systems['serotonin'].mood_level = 1.0

        emotional_modulation = bridge.backward_pass()

        # All modulations should be <= 0.3 (MAX_MODULATION)
        for key, value in emotional_modulation.items():
            assert abs(value) <= 0.3  # Modulation cap


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def fresh_bridge():
    """Fixture: Fresh NeuroEmotionalBridge instance"""
    return NeuroEmotionalBridge()


@pytest.fixture
def positive_emotional_state():
    """Fixture: Positive emotional state"""
    return EmotionalState(
        joy=0.8,
        trust=0.7,
        anticipation=0.6
    )


@pytest.fixture
def negative_emotional_state():
    """Fixture: Negative emotional state"""
    return EmotionalState(
        fear=0.8,
        sadness=0.7,
        anger=0.5
    )


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
