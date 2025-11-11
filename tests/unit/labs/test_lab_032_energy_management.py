"""
LAB_032: Energy Management - Unit Tests

Homeostasis: Mental energy tracking, ego depletion, compensatory control

Key Papers:
- Baumeister et al. (1998) - Ego depletion and self-control
- Hockey (2013) - Compensatory control model
- Muraven & Baumeister (2000) - Self-control as limited resource
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Social_Homeostasis.LAB_032_Energy_Management.energy_management_system import (
    EnergyManagementSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with full energy"""
        system = EnergyManagementSystem()
        assert system.current_energy == 1.0  # Full energy
        assert system.fatigue_level == 0.0

    def test_custom_initialization(self):
        """System accepts custom starting energy"""
        system = EnergyManagementSystem(starting_energy=0.5)
        assert system.current_energy == 0.5


class TestEnergyDepletion:
    """Test energy depletion mechanics"""

    def test_energy_depletes_with_cognitive_load(self):
        """Energy decreases with cognitive tasks"""
        system = EnergyManagementSystem()

        initial_energy = system.current_energy

        # Perform cognitive task
        result = system.deplete_energy(
            task_difficulty=0.7,
            duration=1.0
        )

        assert system.current_energy < initial_energy
        assert result["energy_depleted"] > 0

    def test_harder_tasks_deplete_more_energy(self):
        """Difficult tasks deplete more energy than easy tasks"""
        system1 = EnergyManagementSystem()
        system2 = EnergyManagementSystem()

        # Easy task
        system1.deplete_energy(task_difficulty=0.3, duration=1.0)

        # Hard task
        system2.deplete_energy(task_difficulty=0.9, duration=1.0)

        # Hard task should deplete more
        assert system2.current_energy < system1.current_energy

    def test_longer_tasks_deplete_more_energy(self):
        """Longer duration depletes more energy"""
        system1 = EnergyManagementSystem()
        system2 = EnergyManagementSystem()

        # Short task
        system1.deplete_energy(task_difficulty=0.5, duration=0.5)

        # Long task
        system2.deplete_energy(task_difficulty=0.5, duration=2.0)

        # Longer task should deplete more
        assert system2.current_energy < system1.current_energy

    def test_depletion_accelerates_at_low_energy(self):
        """Depletion accelerates when energy is low (fatigue effect)"""
        system = EnergyManagementSystem(starting_energy=0.3)

        depletion_low_energy = system.deplete_energy(
            task_difficulty=0.5,
            duration=0.5
        )["energy_depleted"]

        # Fresh system for comparison
        system_fresh = EnergyManagementSystem()
        depletion_high_energy = system_fresh.deplete_energy(
            task_difficulty=0.5,
            duration=0.5
        )["energy_depleted"]

        # Low energy should deplete faster
        assert depletion_low_energy > depletion_high_energy


class TestFatigue:
    """Test fatigue computation"""

    def test_fatigue_inverse_of_energy(self):
        """Fatigue = 1 - energy"""
        system = EnergyManagementSystem(starting_energy=0.7)

        fatigue = system.compute_fatigue_level()

        assert fatigue == pytest.approx(0.3, abs=0.01)

    def test_high_energy_low_fatigue(self):
        """High energy means low fatigue"""
        system = EnergyManagementSystem(starting_energy=0.9)

        assert system.compute_fatigue_level() < 0.2

    def test_low_energy_high_fatigue(self):
        """Low energy means high fatigue"""
        system = EnergyManagementSystem(starting_energy=0.2)

        assert system.compute_fatigue_level() > 0.7


class TestCompensatoryControl:
    """Test compensatory control under fatigue (Hockey 2013)"""

    def test_high_fatigue_increases_effort(self):
        """Under fatigue, effort increases to maintain performance"""
        system = EnergyManagementSystem(starting_energy=0.3)

        result = system.compensatory_effort(task_importance=0.8)

        # Should increase effort under fatigue
        assert result["effort_multiplier"] > 1.0

    def test_low_fatigue_normal_effort(self):
        """With high energy, effort is normal"""
        system = EnergyManagementSystem(starting_energy=0.9)

        result = system.compensatory_effort(task_importance=0.5)

        # Effort multiplier should be close to 1.0
        assert result["effort_multiplier"] == pytest.approx(1.0, abs=0.1)

    def test_important_tasks_get_more_effort(self):
        """Important tasks receive more compensatory effort"""
        system = EnergyManagementSystem(starting_energy=0.3)

        # Important task
        important = system.compensatory_effort(task_importance=0.9)

        # Unimportant task
        unimportant = system.compensatory_effort(task_importance=0.2)

        # Important task should get more effort
        assert important["effort_multiplier"] > unimportant["effort_multiplier"]

    def test_focus_narrowing_under_fatigue(self):
        """Fatigue causes focus narrowing (Hockey 2013)"""
        system = EnergyManagementSystem(starting_energy=0.2)

        result = system.compensatory_effort(task_importance=0.7)

        # Focus should narrow (< 1.0)
        assert result["focus_width"] < 1.0
        assert result["focus_width"] < 0.5  # Significant narrowing


class TestRecovery:
    """Test energy recovery dynamics"""

    def test_recovery_during_rest(self):
        """Energy recovers during rest"""
        system = EnergyManagementSystem(starting_energy=0.4)

        initial_energy = system.current_energy

        # Rest
        system.recover(duration=1.0)

        assert system.current_energy > initial_energy

    def test_recovery_exponential(self):
        """Recovery follows exponential curve (diminishing returns)"""
        system = EnergyManagementSystem(starting_energy=0.2)

        # First hour of rest
        system.recover(duration=1.0)
        energy_after_1hr = system.current_energy

        # Second hour of rest
        system.recover(duration=1.0)
        energy_after_2hr = system.current_energy

        # Gains diminish
        gain_first_hour = energy_after_1hr - 0.2
        gain_second_hour = energy_after_2hr - energy_after_1hr

        assert gain_second_hour < gain_first_hour

    def test_longer_rest_more_recovery(self):
        """Longer rest = more recovery"""
        system1 = EnergyManagementSystem(starting_energy=0.5)
        system2 = EnergyManagementSystem(starting_energy=0.5)

        system1.recover(duration=0.5)  # Short rest
        system2.recover(duration=2.0)  # Long rest

        assert system2.current_energy > system1.current_energy


class TestCognitiveImpairment:
    """Test cognitive function impairment under fatigue"""

    def test_low_energy_impairs_cognitive_control(self):
        """Fatigue impairs cognitive control (LAB_019 integration)"""
        system = EnergyManagementSystem(starting_energy=0.2)

        result = system.modulate_cognitive_functions(
            function="cognitive_control",
            baseline=0.8
        )

        # Should be impaired
        assert result["modulated_performance"] < 0.8

    def test_low_energy_reduces_cognitive_flexibility(self):
        """Fatigue reduces cognitive flexibility (LAB_020 integration)"""
        system = EnergyManagementSystem(starting_energy=0.3)

        result = system.modulate_cognitive_functions(
            function="cognitive_flexibility",
            baseline=0.8
        )

        # Should be reduced
        assert result["modulated_performance"] < 0.8

    def test_high_energy_maintains_cognitive_functions(self):
        """High energy maintains cognitive performance"""
        system = EnergyManagementSystem(starting_energy=0.9)

        result = system.modulate_cognitive_functions(
            function="cognitive_control",
            baseline=0.8
        )

        # Should be maintained or slightly enhanced
        assert result["modulated_performance"] >= 0.75


class TestCircadianIntegration:
    """Test integration with LAB_031 (Circadian Rhythm)"""

    def test_circadian_modulates_baseline_energy(self):
        """Low circadian alertness reduces baseline energy"""
        system = EnergyManagementSystem()

        # High circadian alertness (morning)
        result_morning = system.apply_circadian_modulation(
            circadian_alertness=0.8
        )

        # Low circadian alertness (night)
        result_night = system.apply_circadian_modulation(
            circadian_alertness=0.2
        )

        # Morning should have higher effective energy
        assert result_morning["effective_energy"] > result_night["effective_energy"]

    def test_circadian_affects_recovery_rate(self):
        """Recovery faster during high circadian periods"""
        system1 = EnergyManagementSystem(starting_energy=0.5)
        system2 = EnergyManagementSystem(starting_energy=0.5)

        # Recover with high circadian
        system1.recover(duration=1.0, circadian_alertness=0.8)

        # Recover with low circadian
        system2.recover(duration=1.0, circadian_alertness=0.2)

        # Higher circadian should recover more
        assert system1.current_energy > system2.current_energy


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_task_event(self):
        """Process cognitive task event"""
        system = EnergyManagementSystem()

        result = system.process_event(
            event_type="perform_task",
            task_difficulty=0.6,
            duration=1.0,
            importance=0.7
        )

        assert "energy_after" in result
        assert "fatigue_level" in result
        assert result["energy_after"] < 1.0

    def test_process_rest_event(self):
        """Process rest/recovery event"""
        system = EnergyManagementSystem(starting_energy=0.4)

        result = system.process_event(
            event_type="rest",
            duration=1.0
        )

        assert "energy_after" in result
        assert result["energy_after"] > 0.4

    def test_process_circadian_update(self):
        """Process circadian modulation event"""
        system = EnergyManagementSystem()

        result = system.process_event(
            event_type="circadian_update",
            circadian_alertness=0.7
        )

        assert "effective_energy" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_energy_metrics(self):
        """get_state returns complete energy state"""
        system = EnergyManagementSystem(starting_energy=0.6)

        state = system.get_state()

        assert "current_energy" in state
        assert "fatigue_level" in state
        assert "total_tasks_performed" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = EnergyManagementSystem()

        state = system.get_state()

        # Should be JSON serializable
        import json
        json_str = json.dumps(state)
        assert json_str is not None
