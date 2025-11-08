"""
LAB_019: Inhibitory Control System - Unit Tests

Core Executive Function: Suppression of prepotent responses

Biological Foundation:
- Right inferior frontal gyrus (rIFG)
- Pre-supplementary motor area (pre-SMA)
- Orbitofrontal cortex (OFC)

Neurochemistry:
- Serotonin (LAB_014): High 5-HT = strong control
- Norepinephrine (LAB_015): Optimal arousal enhances control
- GABA (LAB_017): Inhibitory neurotransmission

Key Papers:
- Aron et al. (2014) - "Frontosubthalamic circuits for stopping"
- Bari & Robbins (2013) - "Inhibition and impulsivity"
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Executive_Functions.LAB_019_Inhibitory_Control.inhibitory_control_system import (
    InhibitoryControlSystem
)


class TestInitialization:
    """Test system initialization and default parameters"""

    def test_default_initialization(self):
        """System initializes with correct default parameters"""
        system = InhibitoryControlSystem()

        assert system.baseline_control == 0.5
        assert system.control_gain == 2.0
        assert system.conflict_sensitivity == 0.8
        assert system.adaptation_rate == 0.1
        assert system.history_window == 15

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = InhibitoryControlSystem()

        assert system.current_control_strength == 0.5
        assert system.control_history == []
        assert system.total_inhibitions == 0
        assert system.successful_inhibitions == 0

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = InhibitoryControlSystem(
            baseline_control=0.7,
            control_gain=3.0,
            conflict_sensitivity=0.9
        )

        assert system.baseline_control == 0.7
        assert system.control_gain == 3.0
        assert system.conflict_sensitivity == 0.9


class TestControlStrengthUpdate:
    """Test control strength update mechanism"""

    def test_high_conflict_increases_control(self):
        """High response conflict increases control strength"""
        system = InhibitoryControlSystem(baseline_control=0.5)

        # High conflict should boost control
        initial_control = system.current_control_strength
        system.update_control_strength(response_conflict=0.8, prepotency=0.7)

        assert system.current_control_strength > initial_control

    def test_low_conflict_maintains_baseline(self):
        """Low conflict maintains control near baseline"""
        system = InhibitoryControlSystem(baseline_control=0.5)

        # Low conflict, should stay near baseline
        system.update_control_strength(response_conflict=0.1, prepotency=0.3)

        assert 0.4 <= system.current_control_strength <= 0.6

    def test_control_strength_bounded(self):
        """Control strength stays within [0, 1]"""
        system = InhibitoryControlSystem()

        # Extreme inputs
        system.update_control_strength(response_conflict=1.0, prepotency=1.0)
        assert 0.0 <= system.current_control_strength <= 1.0

        system.update_control_strength(response_conflict=0.0, prepotency=0.0)
        assert 0.0 <= system.current_control_strength <= 1.0

    def test_adaptation_over_time(self):
        """Control strength adapts with repeated high conflict"""
        system = InhibitoryControlSystem(baseline_control=0.5, adaptation_rate=0.2)

        initial_control = system.current_control_strength

        # Repeated high conflict should strengthen control
        for _ in range(10):
            system.update_control_strength(response_conflict=0.9, prepotency=0.8)

        assert system.current_control_strength > initial_control

    def test_history_tracking(self):
        """Control history tracks recent levels"""
        system = InhibitoryControlSystem(history_window=5)

        for i in range(7):
            system.update_control_strength(response_conflict=0.5, prepotency=0.5)

        # Should only keep last 5
        assert len(system.control_history) == 5


class TestInhibitionAttempt:
    """Test inhibition attempt mechanism"""

    def test_high_control_inhibits_strong_prepotency(self):
        """High control strength successfully inhibits strong prepotent response"""
        system = InhibitoryControlSystem(baseline_control=0.9)

        # High control should inhibit even strong prepotency
        success = system.attempt_inhibition(prepotency=0.8, control_available=0.9)
        assert success is True

    def test_low_control_fails_strong_prepotency(self):
        """Low control strength fails to inhibit strong prepotent response"""
        system = InhibitoryControlSystem(baseline_control=0.2)

        # Low control should fail against strong prepotency
        success = system.attempt_inhibition(prepotency=0.9, control_available=0.2)
        assert success is False

    def test_success_rate_tracking(self):
        """System tracks inhibition success rate"""
        system = InhibitoryControlSystem(baseline_control=0.7)

        # Perform multiple inhibition attempts
        for _ in range(10):
            system.attempt_inhibition(prepotency=0.5, control_available=0.7)

        assert system.total_inhibitions == 10
        assert system.successful_inhibitions > 0
        assert system.successful_inhibitions <= 10

    def test_failed_inhibition_doesnt_crash(self):
        """Failed inhibition doesn't cause errors"""
        system = InhibitoryControlSystem(baseline_control=0.1)

        # This should fail but not crash
        try:
            success = system.attempt_inhibition(prepotency=1.0, control_available=0.1)
            assert success is False
        except Exception as e:
            pytest.fail(f"Failed inhibition raised exception: {e}")

    def test_boundary_case_zero_prepotency(self):
        """Zero prepotency is always successfully inhibited"""
        system = InhibitoryControlSystem()

        success = system.attempt_inhibition(prepotency=0.0, control_available=0.5)
        assert success is True

    def test_boundary_case_max_prepotency(self):
        """Maximum prepotency requires very high control"""
        system = InhibitoryControlSystem()

        # Low control vs max prepotency
        success = system.attempt_inhibition(prepotency=1.0, control_available=0.3)
        assert success is False

        # High control vs max prepotency
        success = system.attempt_inhibition(prepotency=1.0, control_available=0.95)
        assert success is True


class TestSSRTComputation:
    """Test Stop-Signal Reaction Time computation"""

    def test_high_control_low_ssrt(self):
        """High control strength results in low SSRT (fast stopping)"""
        system = InhibitoryControlSystem(baseline_control=0.9)

        ssrt = system.compute_ssrt()

        # High control = fast stopping = low SSRT
        assert ssrt < 200  # milliseconds

    def test_low_control_high_ssrt(self):
        """Low control strength results in high SSRT (slow stopping)"""
        system = InhibitoryControlSystem(baseline_control=0.2)

        ssrt = system.compute_ssrt()

        # Low control = slow stopping = high SSRT
        assert ssrt > 300  # milliseconds

    def test_ssrt_formula_correct(self):
        """SSRT formula: base_rt * (1.0 - control_strength)"""
        system = InhibitoryControlSystem(baseline_control=0.5)
        system.base_rt = 400  # Set base reaction time

        ssrt = system.compute_ssrt()

        expected_ssrt = 400 * (1.0 - 0.5)
        assert abs(ssrt - expected_ssrt) < 1.0

    def test_ssrt_updates_with_control(self):
        """SSRT decreases as control strength increases"""
        system = InhibitoryControlSystem(baseline_control=0.3)

        ssrt_initial = system.compute_ssrt()

        # Increase control strength
        system.current_control_strength = 0.8

        ssrt_improved = system.compute_ssrt()

        assert ssrt_improved < ssrt_initial


class TestSerotoninIntegration:
    """Test serotonin modulation of inhibitory control"""

    def test_high_serotonin_amplifies_control(self):
        """High serotonin level amplifies control strength"""
        system = InhibitoryControlSystem(baseline_control=0.5)

        # High serotonin should boost control
        modulated_control = system.integrate_serotonin(serotonin_level=0.9)

        assert modulated_control > system.baseline_control

    def test_low_serotonin_weakens_control(self):
        """Low serotonin level weakens control strength"""
        system = InhibitoryControlSystem(baseline_control=0.5)

        # Low serotonin should reduce control
        modulated_control = system.integrate_serotonin(serotonin_level=0.2)

        assert modulated_control < system.baseline_control

    def test_integration_formula_realistic(self):
        """Serotonin integration uses realistic formula"""
        system = InhibitoryControlSystem(baseline_control=0.5, control_gain=2.0)

        # Should be multiplicative modulation
        modulated = system.integrate_serotonin(serotonin_level=0.8)

        # High serotonin should give strong boost
        assert 0.6 < modulated < 1.0

    def test_modulation_bounded(self):
        """Serotonin modulation keeps control within [0, 1]"""
        system = InhibitoryControlSystem(baseline_control=0.9)

        # Extreme serotonin shouldn't push above 1.0
        modulated = system.integrate_serotonin(serotonin_level=1.0)
        assert 0.0 <= modulated <= 1.0

        # Zero serotonin shouldn't push below 0.0
        modulated = system.integrate_serotonin(serotonin_level=0.0)
        assert 0.0 <= modulated <= 1.0


class TestImpulsivityComputation:
    """Test impulsivity computation (inverse of control)"""

    def test_impulsivity_inverse_of_control(self):
        """Impulsivity is inverse of control strength"""
        system = InhibitoryControlSystem(baseline_control=0.7)

        impulsivity = system.compute_impulsivity()

        # impulsivity = 1.0 - control_strength
        expected_impulsivity = 1.0 - 0.7
        assert abs(impulsivity - expected_impulsivity) < 0.01

    def test_high_control_low_impulsivity(self):
        """High control results in low impulsivity"""
        system = InhibitoryControlSystem(baseline_control=0.9)

        impulsivity = system.compute_impulsivity()

        assert impulsivity < 0.3

    def test_impulsivity_range_correct(self):
        """Impulsivity stays within [0, 1]"""
        system = InhibitoryControlSystem()

        # Test various control levels
        system.current_control_strength = 0.0
        assert 0.0 <= system.compute_impulsivity() <= 1.0

        system.current_control_strength = 0.5
        assert 0.0 <= system.compute_impulsivity() <= 1.0

        system.current_control_strength = 1.0
        assert 0.0 <= system.compute_impulsivity() <= 1.0


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete_cycle(self):
        """process_event executes complete processing cycle"""
        system = InhibitoryControlSystem(baseline_control=0.6)

        result = system.process_event(response_conflict=0.7, prepotency=0.6)

        # Should return all expected keys
        assert "control_strength" in result
        assert "ssrt" in result
        assert "impulsivity" in result
        assert "inhibition_success_rate" in result

    def test_process_event_outputs_valid(self):
        """process_event returns valid output values"""
        system = InhibitoryControlSystem()

        result = system.process_event(response_conflict=0.5, prepotency=0.5)

        # All outputs should be valid ranges
        assert 0.0 <= result["control_strength"] <= 1.0
        assert result["ssrt"] > 0
        assert 0.0 <= result["impulsivity"] <= 1.0
        assert 0.0 <= result["inhibition_success_rate"] <= 1.0

    def test_process_event_updates_state(self):
        """process_event updates internal state correctly"""
        system = InhibitoryControlSystem()

        initial_inhibitions = system.total_inhibitions

        system.process_event(response_conflict=0.6, prepotency=0.7)

        # State should be updated
        assert system.total_inhibitions > initial_inhibitions
        assert len(system.control_history) > 0
