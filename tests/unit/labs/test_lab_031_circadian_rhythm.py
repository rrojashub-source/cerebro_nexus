"""
LAB_031: Circadian Rhythm Simulation - Unit Tests

Homeostasis: Time-of-day effects, alertness cycles, sleep pressure

Key Papers:
- Borbély (1982) - Two-process model of sleep regulation
- Dijk & Czeisler (1995) - Circadian and sleep-dependent control
- Schmidt et al. (2007) - Light entrainment
"""

import pytest
import math
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Social_Homeostasis.LAB_031_Circadian_Rhythm.circadian_rhythm_system import (
    CircadianRhythmSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = CircadianRhythmSystem()
        assert system.circadian_phase == 0.0  # Start at midnight
        assert system.time_awake == 0.0
        assert system.process_s == 0.0  # No sleep pressure at start

    def test_custom_initialization(self):
        """System accepts custom starting phase"""
        system = CircadianRhythmSystem(
            starting_phase=6.0,  # 6 AM
            initial_time_awake=2.0  # Already awake 2 hours
        )
        assert system.circadian_phase == 6.0
        assert system.time_awake == 2.0


class TestCircadianPhase:
    """Test circadian phase advancement"""

    def test_phase_advances_linearly(self):
        """Phase advances 1 hour per hour elapsed"""
        system = CircadianRhythmSystem()

        # Advance 5 hours
        system.update_circadian_phase(time_elapsed=5.0)

        assert system.circadian_phase == 5.0

    def test_phase_wraps_at_24_hours(self):
        """Phase wraps from 24 to 0 (24-hour cycle)"""
        system = CircadianRhythmSystem(starting_phase=22.0)

        # Advance 5 hours (should wrap to 3.0)
        system.update_circadian_phase(time_elapsed=5.0)

        assert system.circadian_phase == pytest.approx(3.0, abs=0.01)

    def test_light_entrainment_phase_shift(self):
        """Bright light causes phase shift"""
        system = CircadianRhythmSystem(starting_phase=2.0)  # 2 AM

        # Bright light at night delays phase
        system.update_circadian_phase(
            time_elapsed=1.0,
            light_exposure=0.9  # Bright light
        )

        # Phase should shift (delay at night)
        # Expected: phase delayed slightly
        assert system.circadian_phase < 3.0  # Less than normal advance


class TestProcessC:
    """Test Process C (Circadian alertness)"""

    def test_process_c_peaks_around_10am(self):
        """Process C has peak alertness ~10 AM"""
        system = CircadianRhythmSystem()

        # Morning peak (10 AM)
        process_c_10am = system.compute_process_c(phase=10.0)

        # Compare to night (2 AM)
        process_c_2am = system.compute_process_c(phase=2.0)

        assert process_c_10am > process_c_2am
        assert process_c_10am > 0.7  # High alertness in morning

    def test_process_c_has_evening_peak(self):
        """Process C has secondary peak ~9 PM"""
        system = CircadianRhythmSystem()

        # Evening peak (9 PM)
        process_c_9pm = system.compute_process_c(phase=21.0)

        # Compare to afternoon dip (3 PM)
        process_c_3pm = system.compute_process_c(phase=15.0)

        assert process_c_9pm > process_c_3pm

    def test_process_c_lowest_at_night(self):
        """Process C lowest at night (2-4 AM)"""
        system = CircadianRhythmSystem()

        process_c_3am = system.compute_process_c(phase=3.0)
        process_c_10am = system.compute_process_c(phase=10.0)

        assert process_c_3am < process_c_10am
        assert process_c_3am < 0.3  # Low alertness at night

    def test_process_c_sinusoidal(self):
        """Process C follows sinusoidal pattern"""
        system = CircadianRhythmSystem()

        # Sample at multiple times
        values = []
        for hour in [0, 6, 12, 18, 24]:
            values.append(system.compute_process_c(phase=hour % 24))

        # Should oscillate (not monotonic)
        assert not all(values[i] <= values[i+1] for i in range(len(values)-1))


class TestProcessS:
    """Test Process S (Homeostatic sleep pressure)"""

    def test_process_s_builds_during_wake(self):
        """Sleep pressure builds linearly during wake"""
        system = CircadianRhythmSystem()

        # Start awake
        system.time_awake = 0.0
        initial_s = system.compute_process_s()

        # After 8 hours awake
        system.time_awake = 8.0
        later_s = system.compute_process_s()

        assert later_s > initial_s
        assert later_s == pytest.approx(0.4, abs=0.05)  # ~5% per hour (0.05 rate)

    def test_process_s_caps_at_maximum(self):
        """Sleep pressure caps at 1.0"""
        system = CircadianRhythmSystem()

        # After 24 hours awake (extreme)
        system.time_awake = 24.0
        process_s = system.compute_process_s()

        assert process_s <= 1.0

    def test_sleep_resets_process_s(self):
        """Sleep resets homeostatic pressure"""
        system = CircadianRhythmSystem()

        # Build up sleep pressure
        system.time_awake = 16.0
        assert system.compute_process_s() > 0.1

        # Sleep
        system.sleep(duration=8.0)

        # Pressure should reset
        assert system.compute_process_s() == pytest.approx(0.0, abs=0.01)
        assert system.time_awake == 0.0


class TestAlertness:
    """Test alertness computation (C - S)"""

    def test_alertness_equals_c_minus_s(self):
        """Alertness = Process C - Process S"""
        system = CircadianRhythmSystem(starting_phase=10.0)  # Morning

        # Fresh (no sleep pressure)
        system.time_awake = 0.0
        process_c = system.compute_process_c()
        process_s = system.compute_process_s()
        alertness = system.compute_alertness()

        assert alertness == pytest.approx(process_c - process_s, abs=0.01)

    def test_alertness_high_in_morning_when_rested(self):
        """High alertness in morning after sleep"""
        system = CircadianRhythmSystem(starting_phase=8.0)  # 8 AM
        system.time_awake = 1.0  # Just woke up

        alertness = system.compute_alertness()
        assert alertness > 0.6  # High alertness

    def test_alertness_low_at_night_when_tired(self):
        """Low alertness at night after long wake"""
        system = CircadianRhythmSystem(starting_phase=23.0)  # 11 PM
        system.time_awake = 16.0  # Awake 16 hours

        alertness = system.compute_alertness()
        assert alertness < 0.3  # Low alertness

    def test_alertness_decreases_throughout_day(self):
        """Alertness decreases as day progresses (sleep pressure builds)"""
        system = CircadianRhythmSystem(starting_phase=8.0)

        # Morning
        system.time_awake = 1.0
        morning_alertness = system.compute_alertness()

        # Evening
        system.time_awake = 12.0
        system.circadian_phase = 20.0
        evening_alertness = system.compute_alertness()

        assert evening_alertness < morning_alertness


class TestTimeOfDayEffects:
    """Test cognitive performance modulation by alertness"""

    def test_high_alertness_enhances_performance(self):
        """High alertness improves cognitive performance"""
        system = CircadianRhythmSystem(starting_phase=10.0)
        system.time_awake = 2.0  # Fresh

        result = system.time_of_day_effects(
            cognitive_task="working_memory",
            baseline_performance=0.8
        )

        # Should enhance performance
        assert result["modulated_performance"] > 0.8

    def test_low_alertness_impairs_performance(self):
        """Low alertness impairs cognitive performance"""
        system = CircadianRhythmSystem(starting_phase=3.0)  # 3 AM
        system.time_awake = 18.0  # Very tired

        result = system.time_of_day_effects(
            cognitive_task="working_memory",
            baseline_performance=0.8
        )

        # Should impair performance
        assert result["modulated_performance"] < 0.8

    def test_different_tasks_affected_differently(self):
        """Some tasks more sensitive to circadian effects"""
        system = CircadianRhythmSystem(starting_phase=3.0)
        system.time_awake = 16.0

        # Working memory (sensitive)
        wm_result = system.time_of_day_effects(
            cognitive_task="working_memory",
            baseline_performance=0.8
        )

        # Simple motor (less sensitive)
        motor_result = system.time_of_day_effects(
            cognitive_task="simple_motor",
            baseline_performance=0.8
        )

        # Working memory should be more impaired
        assert wm_result["modulated_performance"] < motor_result["modulated_performance"]


class TestSleepConsolidationIntegration:
    """Test integration with LAB_003 (Sleep Consolidation)"""

    def test_high_sleep_pressure_triggers_consolidation(self):
        """High process S should trigger sleep consolidation"""
        system = CircadianRhythmSystem()

        # Build up sleep pressure
        system.time_awake = 16.0

        result = system.should_trigger_sleep_consolidation()

        assert result["should_consolidate"] == True
        assert result["sleep_pressure"] > 0.6

    def test_low_sleep_pressure_no_consolidation(self):
        """Low process S should not trigger consolidation"""
        system = CircadianRhythmSystem()

        # Just woke up
        system.time_awake = 2.0

        result = system.should_trigger_sleep_consolidation()

        assert result["should_consolidate"] == False


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_time_passage(self):
        """Process time passage event"""
        system = CircadianRhythmSystem(starting_phase=8.0)
        system.time_awake = 2.0

        result = system.process_event(
            event_type="time_passage",
            hours_elapsed=4.0
        )

        assert "new_phase" in result
        assert "alertness" in result
        assert result["new_phase"] == pytest.approx(12.0, abs=0.01)

    def test_process_sleep_event(self):
        """Process sleep event"""
        system = CircadianRhythmSystem()
        system.time_awake = 16.0

        result = system.process_event(
            event_type="sleep",
            duration=8.0
        )

        assert "sleep_quality" in result
        assert result["process_s_after"] == pytest.approx(0.0, abs=0.01)

    def test_process_wake_event(self):
        """Process wake event"""
        system = CircadianRhythmSystem()

        result = system.process_event(event_type="wake")

        assert "alertness" in result
        assert result["time_awake"] == 0.0


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_all_components(self):
        """get_state returns complete system state"""
        system = CircadianRhythmSystem(starting_phase=10.0)
        system.time_awake = 5.0

        state = system.get_state()

        assert "circadian_phase" in state
        assert "time_awake" in state
        assert "process_c" in state
        assert "process_s" in state
        assert "alertness" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = CircadianRhythmSystem()

        state = system.get_state()

        # Should be JSON serializable
        import json
        json_str = json.dumps(state)
        assert json_str is not None
