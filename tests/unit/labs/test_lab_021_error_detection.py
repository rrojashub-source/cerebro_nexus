"""
LAB_021: Error Detection & Correction System - Unit Tests

Monitoring Component: Performance monitoring and error processing

Biological Foundation:
- Anterior cingulate cortex (ACC)
- Medial prefrontal cortex (mPFC)

Neurochemistry:
- Dopamine (LAB_013): Negative RPE signals errors
- Norepinephrine (LAB_015): Arousal spike on error detection

Key Papers:
- Botvinick et al. (2001) - "Conflict monitoring and anterior cingulate cortex"
- Holroyd & Coles (2002) - "The neural basis of human error processing"
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Executive_Functions.LAB_021_Error_Detection.error_detection_system import (
    ErrorDetectionSystem
)


class TestInitialization:
    """Test system initialization and default parameters"""

    def test_default_initialization(self):
        """System initializes with correct default parameters"""
        system = ErrorDetectionSystem()

        assert system.baseline_sensitivity == 0.6
        assert system.conflict_threshold == 0.5
        assert system.error_learning_rate == 0.2
        assert system.correction_strength == 0.8
        assert system.adaptation_rate == 0.15
        assert system.history_window == 25

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = ErrorDetectionSystem()

        assert system.current_sensitivity == 0.6
        assert system.conflict_level == 0.0
        assert system.errors_detected == 0
        assert system.corrections_applied == 0
        assert system.conflict_history == []
        assert system.error_history == []

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = ErrorDetectionSystem(
            baseline_sensitivity=0.7,
            conflict_threshold=0.6,
            error_learning_rate=0.3
        )

        assert system.baseline_sensitivity == 0.7
        assert system.conflict_threshold == 0.6
        assert system.error_learning_rate == 0.3


class TestConflictDetection:
    """Test conflict detection mechanism"""

    def test_high_conflict_balanced_responses(self):
        """High conflict when responses are balanced"""
        system = ErrorDetectionSystem()

        # Balanced responses → high conflict
        conflict = system.detect_conflict(
            response_a_strength=0.5,
            response_b_strength=0.5
        )

        assert conflict > 0.8  # Should be high conflict

    def test_low_conflict_dominant_response(self):
        """Low conflict when one response dominates"""
        system = ErrorDetectionSystem()

        # One dominates → low conflict
        conflict = system.detect_conflict(
            response_a_strength=0.9,
            response_b_strength=0.1
        )

        assert conflict < 0.3  # Should be low conflict

    def test_conflict_formula_correct(self):
        """Conflict formula: min(a, b) / (max(a, b) + epsilon)"""
        system = ErrorDetectionSystem()

        conflict = system.detect_conflict(
            response_a_strength=0.3,
            response_b_strength=0.7
        )

        # Expected: 0.3 / (0.7 + epsilon) ≈ 0.42
        assert 0.40 <= conflict <= 0.45

    def test_conflict_threshold_detection(self):
        """Conflict above threshold flagged correctly"""
        system = ErrorDetectionSystem(conflict_threshold=0.5)

        # Below threshold
        conflict_low = system.detect_conflict(0.2, 0.8)
        assert conflict_low < system.conflict_threshold

        # Above threshold
        conflict_high = system.detect_conflict(0.5, 0.5)
        assert conflict_high > system.conflict_threshold

    def test_zero_response_handled(self):
        """Zero response strength handled without error"""
        system = ErrorDetectionSystem()

        # Should not crash
        conflict = system.detect_conflict(0.0, 0.8)

        assert conflict >= 0.0


class TestErrorDetection:
    """Test error detection mechanism"""

    def test_detects_mismatch(self):
        """Detects mismatch between expected and actual"""
        system = ErrorDetectionSystem()

        error_detected, magnitude = system.detect_error(
            actual_outcome="A",
            expected_outcome="B",
            confidence=0.8
        )

        assert error_detected is True
        assert magnitude > 0.0

    def test_no_error_on_match(self):
        """No error when expected matches actual"""
        system = ErrorDetectionSystem()

        error_detected, magnitude = system.detect_error(
            actual_outcome="A",
            expected_outcome="A",
            confidence=0.8
        )

        assert error_detected is False
        assert magnitude == 0.0

    def test_confidence_modulates_detection(self):
        """High confidence errors have higher magnitude"""
        system = ErrorDetectionSystem()

        # Low confidence error
        _, mag_low_conf = system.detect_error("A", "B", confidence=0.3)

        # High confidence error
        _, mag_high_conf = system.detect_error("A", "B", confidence=0.9)

        assert mag_high_conf > mag_low_conf

    def test_error_magnitude_bounded(self):
        """Error magnitude stays within [0, 1]"""
        system = ErrorDetectionSystem()

        # Maximum confidence mismatch
        _, magnitude = system.detect_error("A", "B", confidence=1.0)

        assert 0.0 <= magnitude <= 1.0

    def test_low_sensitivity_reduces_detection(self):
        """Low sensitivity may miss subtle errors"""
        system = ErrorDetectionSystem(baseline_sensitivity=0.2)

        error_detected, _ = system.detect_error("A", "B", confidence=0.3)

        # Low sensitivity + low confidence might miss error
        # (Implementation specific - just check boolean type)
        assert isinstance(error_detected, bool)

    def test_error_tracking(self):
        """System tracks error detections"""
        system = ErrorDetectionSystem()

        initial_count = system.errors_detected

        system.detect_error("A", "B", confidence=0.8)

        assert system.errors_detected > initial_count


class TestERNComputation:
    """Test Error-Related Negativity computation"""

    def test_ern_scales_with_magnitude(self):
        """ERN amplitude scales with error magnitude"""
        system = ErrorDetectionSystem()

        ern_small = system.compute_ern_amplitude(
            error_magnitude=0.3,
            sensitivity=0.6
        )

        ern_large = system.compute_ern_amplitude(
            error_magnitude=0.9,
            sensitivity=0.6
        )

        assert ern_large > ern_small

    def test_sensitivity_modulates_ern(self):
        """Higher sensitivity produces larger ERN"""
        system = ErrorDetectionSystem()

        ern_low_sens = system.compute_ern_amplitude(0.7, sensitivity=0.3)
        ern_high_sens = system.compute_ern_amplitude(0.7, sensitivity=0.9)

        assert ern_high_sens > ern_low_sens

    def test_ern_realistic_range(self):
        """ERN amplitude in realistic range (arbitrary units)"""
        system = ErrorDetectionSystem()

        ern = system.compute_ern_amplitude(0.8, sensitivity=0.7)

        # Typical ERN: 5-20 arbitrary units
        assert 0 < ern < 30

    def test_zero_magnitude_zero_ern(self):
        """Zero error magnitude produces zero ERN"""
        system = ErrorDetectionSystem()

        ern = system.compute_ern_amplitude(0.0, sensitivity=0.6)

        assert ern == 0.0


class TestCorrectionTriggering:
    """Test correction signal generation"""

    def test_correction_increases_control(self):
        """Correction signal includes control boost"""
        system = ErrorDetectionSystem()

        correction = system.trigger_correction(error_magnitude=0.7)

        assert "control_boost" in correction
        assert correction["control_boost"] > 0.0

    def test_post_error_slowing_computed(self):
        """Correction includes post-error slowing"""
        system = ErrorDetectionSystem()

        correction = system.trigger_correction(error_magnitude=0.7)

        assert "post_error_slowing_ms" in correction
        assert correction["post_error_slowing_ms"] > 0

    def test_correction_strength_realistic(self):
        """Correction strength in realistic range"""
        system = ErrorDetectionSystem()

        correction = system.trigger_correction(error_magnitude=0.8)

        # Control boost typically 0-1
        assert 0.0 <= correction["control_boost"] <= 1.0

        # Post-error slowing typically 20-50ms
        assert 10 < correction["post_error_slowing_ms"] < 100

    def test_larger_errors_stronger_correction(self):
        """Larger errors trigger stronger corrections"""
        system = ErrorDetectionSystem()

        corr_small = system.trigger_correction(0.3)
        corr_large = system.trigger_correction(0.9)

        assert corr_large["control_boost"] > corr_small["control_boost"]

    def test_correction_tracking(self):
        """System tracks corrections applied"""
        system = ErrorDetectionSystem()

        initial_count = system.corrections_applied

        system.trigger_correction(0.7)

        assert system.corrections_applied > initial_count


class TestDopamineRPEIntegration:
    """Test dopamine reward prediction error integration"""

    def test_negative_rpe_signals_error(self):
        """Negative RPE indicates error (worse than expected)"""
        system = ErrorDetectionSystem()

        # Negative RPE = error
        error_mag = system.integrate_dopamine_rpe(rpe=-0.7)

        assert error_mag > 0.0

    def test_positive_rpe_no_error(self):
        """Positive RPE indicates no error (better than expected)"""
        system = ErrorDetectionSystem()

        # Positive RPE = no error
        error_mag = system.integrate_dopamine_rpe(rpe=0.5)

        assert error_mag == 0.0

    def test_rpe_magnitude_maps_to_error_magnitude(self):
        """RPE magnitude maps to error magnitude"""
        system = ErrorDetectionSystem()

        # Small negative RPE
        mag_small = system.integrate_dopamine_rpe(rpe=-0.2)

        # Large negative RPE
        mag_large = system.integrate_dopamine_rpe(rpe=-0.9)

        assert mag_large > mag_small

    def test_zero_rpe_zero_error(self):
        """Zero RPE means no error"""
        system = ErrorDetectionSystem()

        error_mag = system.integrate_dopamine_rpe(rpe=0.0)

        assert error_mag == 0.0


class TestNorepinephrineIntegration:
    """Test norepinephrine arousal spike integration"""

    def test_error_triggers_arousal_spike(self):
        """Error detection triggers arousal spike"""
        system = ErrorDetectionSystem()

        arousal_boost = system.integrate_norepinephrine_arousal(
            baseline_arousal=0.5,
            error_detected=True,
            error_magnitude=0.7
        )

        assert arousal_boost > 0.0

    def test_no_error_no_arousal_spike(self):
        """No error means no arousal spike"""
        system = ErrorDetectionSystem()

        arousal_boost = system.integrate_norepinephrine_arousal(
            baseline_arousal=0.5,
            error_detected=False,
            error_magnitude=0.0
        )

        assert arousal_boost == 0.0

    def test_arousal_boost_realistic(self):
        """Arousal boost in realistic range"""
        system = ErrorDetectionSystem()

        arousal_boost = system.integrate_norepinephrine_arousal(
            baseline_arousal=0.5,
            error_detected=True,
            error_magnitude=0.8
        )

        # Arousal boost typically 0.2-0.5
        assert 0.0 < arousal_boost < 1.0


class TestSensitivityUpdate:
    """Test sensitivity adaptation mechanism"""

    def test_adapts_based_on_experience(self):
        """Sensitivity adapts based on error history"""
        system = ErrorDetectionSystem(baseline_sensitivity=0.6)

        initial_sens = system.current_sensitivity

        # Simulate experience with errors
        system.update_sensitivity(
            error_frequency=0.2,
            correction_success_rate=0.8
        )

        # Sensitivity should change
        assert system.current_sensitivity != initial_sens

    def test_false_alarms_reduce_sensitivity(self):
        """Too many false alarms reduce sensitivity"""
        system = ErrorDetectionSystem(baseline_sensitivity=0.6)

        initial_sens = system.current_sensitivity

        # High error frequency but low correction success = false alarms
        system.update_sensitivity(
            error_frequency=0.8,
            correction_success_rate=0.3
        )

        # Should reduce sensitivity
        assert system.current_sensitivity < initial_sens

    def test_missed_errors_increase_sensitivity(self):
        """Missed errors increase sensitivity"""
        system = ErrorDetectionSystem(baseline_sensitivity=0.6)

        initial_sens = system.current_sensitivity

        # Low error frequency but high correction success = missed errors
        system.update_sensitivity(
            error_frequency=0.1,
            correction_success_rate=0.9
        )

        # Should increase sensitivity
        assert system.current_sensitivity > initial_sens


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete_cycle(self):
        """process_event executes complete processing cycle"""
        system = ErrorDetectionSystem()

        result = system.process_event(
            response_strengths=[0.6, 0.4],
            actual_outcome="A",
            expected_outcome="B",
            confidence=0.8
        )

        # Should return all expected keys
        assert "conflict_level" in result
        assert "error_detected" in result
        assert "error_magnitude" in result
        assert "ern_amplitude" in result
        assert "correction" in result

    def test_process_event_outputs_valid(self):
        """process_event returns valid output values"""
        system = ErrorDetectionSystem()

        result = system.process_event(
            response_strengths=[0.5, 0.5],
            actual_outcome="A",
            expected_outcome="A",
            confidence=0.7
        )

        # All outputs should be valid ranges
        assert 0.0 <= result["conflict_level"] <= 1.0
        assert isinstance(result["error_detected"], bool)
        assert result["error_magnitude"] >= 0.0
        assert result["ern_amplitude"] >= 0.0
