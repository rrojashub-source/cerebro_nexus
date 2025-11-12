"""
LAB_034: Rest/Recovery Cycles - Unit Tests

Homeostasis: "Sleep & mental restoration"

Key Papers:
- Walker (2017) - Why We Sleep
- Xie et al. (2013) - Brain clears waste during sleep
- McEwen (2006) - Sleep deprivation increases stress
- Tononi & Cirelli (2014) - Synaptic homeostasis hypothesis
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_034_Rest_Recovery.rest_recovery_system import (
    RestRecoverySystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default rest/recovery parameters"""
        system = RestRecoverySystem()
        assert system.fatigue_threshold == 0.7
        assert system.mental_energy == 1.0
        assert system.adenosine_level == 0.0

    def test_custom_fatigue_threshold(self):
        """System accepts custom fatigue threshold"""
        system = RestRecoverySystem(fatigue_threshold=0.8)
        assert system.fatigue_threshold == 0.8

    def test_custom_initial_energy(self):
        """System accepts custom initial energy"""
        system = RestRecoverySystem(initial_energy=0.5)
        assert system.mental_energy == 0.5


class TestFatigueDetection:
    """Test fatigue accumulation and detection"""

    def test_cognitive_work_increases_fatigue(self):
        """Cognitive work → fatigue accumulation"""
        system = RestRecoverySystem()

        initial_energy = system.mental_energy

        # Perform cognitive work
        system.perform_cognitive_work(intensity=0.8, duration_minutes=60)

        assert system.mental_energy < initial_energy

    def test_fatigue_accumulates_with_work(self):
        """Repeated work → cumulative fatigue"""
        system = RestRecoverySystem()

        # Multiple work sessions
        for _ in range(5):
            system.perform_cognitive_work(intensity=0.7, duration_minutes=30)

        assert system.mental_energy < 0.5

    def test_high_intensity_work_faster_fatigue(self):
        """High intensity → faster fatigue"""
        system1 = RestRecoverySystem()
        system1.perform_cognitive_work(intensity=0.9, duration_minutes=30)

        system2 = RestRecoverySystem()
        system2.perform_cognitive_work(intensity=0.3, duration_minutes=30)

        assert system1.mental_energy < system2.mental_energy

    def test_rest_need_detected_at_threshold(self):
        """Fatigue reaches threshold → rest needed"""
        system = RestRecoverySystem(fatigue_threshold=0.7)

        # Work until fatigued
        for _ in range(10):
            system.perform_cognitive_work(intensity=0.5, duration_minutes=20)

        assert system.needs_rest() == True


class TestAdenosineAccumulation:
    """Test adenosine buildup (sleep pressure)"""

    def test_adenosine_increases_with_wakefulness(self):
        """Time awake → adenosine accumulation"""
        system = RestRecoverySystem()

        initial_adenosine = system.adenosine_level

        # Simulate wakefulness
        system.simulate_wakefulness(hours=8)

        assert system.adenosine_level > initial_adenosine

    def test_adenosine_cleared_during_sleep(self):
        """Sleep → adenosine clearance"""
        system = RestRecoverySystem()

        # Accumulate adenosine
        system.simulate_wakefulness(hours=12)
        high_adenosine = system.adenosine_level

        # Sleep clears adenosine
        system.rest(duration_hours=6)

        assert system.adenosine_level < high_adenosine

    def test_high_adenosine_increases_sleep_pressure(self):
        """High adenosine → strong rest need"""
        system = RestRecoverySystem()

        system.simulate_wakefulness(hours=16)

        assert system.get_sleep_pressure() > 0.7


class TestRestTriggering:
    """Test rest mode triggering"""

    def test_rest_triggered_when_fatigued(self):
        """High fatigue → rest mode activated"""
        system = RestRecoverySystem()

        # Induce fatigue
        for _ in range(15):
            system.perform_cognitive_work(intensity=0.6, duration_minutes=20)

        result = system.trigger_rest_if_needed()

        assert result["rest_triggered"] == True

    def test_rest_not_triggered_when_energized(self):
        """High energy → no rest needed"""
        system = RestRecoverySystem()

        result = system.trigger_rest_if_needed()

        assert result["rest_triggered"] == False

    def test_forced_rest_always_triggers(self):
        """Forced rest → always activates"""
        system = RestRecoverySystem()

        result = system.rest(duration_hours=2, forced=True)

        assert result["rest_occurred"] == True


class TestRecoveryProcess:
    """Test recovery and resource restoration"""

    def test_rest_restores_mental_energy(self):
        """Rest → mental energy restoration"""
        system = RestRecoverySystem()

        # Deplete energy
        for _ in range(10):
            system.perform_cognitive_work(intensity=0.7, duration_minutes=30)

        low_energy = system.mental_energy

        # Rest restores
        system.rest(duration_hours=6)

        assert system.mental_energy > low_energy

    def test_longer_rest_more_recovery(self):
        """Longer rest → more recovery"""
        system1 = RestRecoverySystem(initial_energy=0.3)
        system1.rest(duration_hours=2)

        system2 = RestRecoverySystem(initial_energy=0.3)
        system2.rest(duration_hours=8)

        assert system2.mental_energy > system1.mental_energy

    def test_recovery_rate_depends_on_sleep_quality(self):
        """Sleep quality → recovery rate"""
        system1 = RestRecoverySystem(initial_energy=0.4)
        system1.rest(duration_hours=6, sleep_quality=0.9)

        system2 = RestRecoverySystem(initial_energy=0.4)
        system2.rest(duration_hours=6, sleep_quality=0.4)

        assert system1.mental_energy > system2.mental_energy

    def test_full_recovery_requires_adequate_rest(self):
        """Adequate rest → full recovery"""
        system = RestRecoverySystem(initial_energy=0.2)

        system.rest(duration_hours=8, sleep_quality=0.8)

        assert system.mental_energy > 0.9


class TestStressReduction:
    """Test stress reduction during rest"""

    def test_rest_reduces_stress(self):
        """Rest → stress reduction"""
        system = RestRecoverySystem()

        # Induce stress through overwork
        for _ in range(20):
            system.perform_cognitive_work(intensity=0.8, duration_minutes=30)

        stress_before = system.get_stress_level()

        # Rest reduces stress
        system.rest(duration_hours=6)

        stress_after = system.get_stress_level()

        assert stress_after < stress_before

    def test_chronic_stress_requires_more_rest(self):
        """High stress → longer recovery needed"""
        system = RestRecoverySystem()

        # Chronic stress
        for _ in range(30):
            system.perform_cognitive_work(intensity=0.9, duration_minutes=30)

        # Short rest insufficient
        system.rest(duration_hours=2)

        assert system.get_stress_level() > 0.5


class TestCircadianInfluence:
    """Test circadian rhythm integration (LAB_031)"""

    def test_circadian_aligned_sleep_more_restorative(self):
        """Sleep during circadian low → better recovery"""
        system = RestRecoverySystem(initial_energy=0.3)

        # Sleep aligned with circadian rhythm
        result = system.rest(duration_hours=6, circadian_alignment=True)

        assert result["recovery_rate"] > 0.1  # Enhanced recovery

    def test_circadian_misaligned_sleep_less_restorative(self):
        """Sleep misaligned → reduced recovery"""
        system = RestRecoverySystem(initial_energy=0.3)

        # Sleep against circadian rhythm
        result = system.rest(duration_hours=6, circadian_alignment=False)

        assert result["recovery_rate"] < 0.15  # Reduced recovery


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_dmn(self):
        """LAB_046: Rest activates Default Mode Network"""
        system = RestRecoverySystem()

        result = system.rest(duration_hours=2)

        assert result.get("dmn_active", False) == True

    def test_integration_with_allostatic_load(self):
        """LAB_033: Rest reduces allostatic load"""
        system = RestRecoverySystem()

        # High allostatic load
        for _ in range(20):
            system.perform_cognitive_work(intensity=0.8, duration_minutes=30)

        load_before = system.get_allostatic_load()

        # Rest reduces load
        system.rest(duration_hours=8)

        load_after = system.get_allostatic_load()

        assert load_after < load_before

    def test_integration_with_energy_management(self):
        """LAB_032: Energy management coordinates rest timing"""
        system = RestRecoverySystem()

        # Deplete energy
        for _ in range(15):
            system.perform_cognitive_work(intensity=0.7, duration_minutes=30)

        # Energy management signals rest need
        assert system.needs_rest() == True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_work_event(self):
        """Process cognitive work event"""
        system = RestRecoverySystem()

        result = system.process_event(
            event_type="cognitive_work",
            intensity=0.7,
            duration_minutes=60
        )

        assert "mental_energy" in result

    def test_process_rest_event(self):
        """Process rest event"""
        system = RestRecoverySystem()

        result = system.process_event(
            event_type="rest",
            duration_hours=6
        )

        assert "rest_occurred" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_metrics(self):
        """get_state returns rest/recovery metrics"""
        system = RestRecoverySystem()

        state = system.get_state()

        assert "mental_energy" in state
        assert "adenosine_level" in state
        assert "needs_rest" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = RestRecoverySystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
