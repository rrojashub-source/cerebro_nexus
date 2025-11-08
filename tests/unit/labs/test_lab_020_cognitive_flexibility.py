"""
LAB_020: Cognitive Flexibility System - Unit Tests

Core Executive Function: Task switching and mental set shifting

Biological Foundation:
- Dorsolateral prefrontal cortex (dlPFC)
- Anterior cingulate cortex (ACC)
- Posterior parietal cortex

Neurochemistry:
- Dopamine (LAB_013): Facilitates set switching (D2 receptors)
- Norepinephrine (LAB_015): Arousal for attention shift
- Acetylcholine (LAB_016): Encoding new rules

Key Papers:
- Monsell (2003) - "Task switching"
- Kehagia et al. (2010) - "Neuropsychopharmacology of cognitive flexibility"
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Executive_Functions.LAB_020_Cognitive_Flexibility.cognitive_flexibility_system import (
    CognitiveFlexibilitySystem
)


class TestInitialization:
    """Test system initialization and default parameters"""

    def test_default_initialization(self):
        """System initializes with correct default parameters"""
        system = CognitiveFlexibilitySystem()

        assert system.baseline_flexibility == 0.5
        assert system.switch_cost_base == 150.0
        assert system.reconfiguration_speed == 0.8
        assert system.rule_encoding_strength == 0.7
        assert system.adaptation_rate == 0.15
        assert system.history_window == 20

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = CognitiveFlexibilitySystem()

        assert system.current_flexibility == 0.5
        assert system.current_task_set is None
        assert system.task_set_history == []
        assert system.switch_count == 0
        assert system.successful_switches == 0
        assert system.total_switch_cost == 0.0

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = CognitiveFlexibilitySystem(
            baseline_flexibility=0.7,
            switch_cost_base=120.0,
            reconfiguration_speed=0.9
        )

        assert system.baseline_flexibility == 0.7
        assert system.switch_cost_base == 120.0
        assert system.reconfiguration_speed == 0.9


class TestTaskSwitching:
    """Test task switching mechanism"""

    def test_first_task_sets_baseline(self):
        """First task establishes baseline (no switch cost)"""
        system = CognitiveFlexibilitySystem()

        success, cost = system.switch_task_set(new_task="A", preparation_time=0)

        assert success is True
        assert cost == 0.0  # No cost for first task
        assert system.current_task_set == "A"

    def test_switch_to_new_task_incurs_cost(self):
        """Switching to different task incurs switch cost"""
        system = CognitiveFlexibilitySystem()

        # Establish baseline
        system.switch_task_set(new_task="A", preparation_time=0)

        # Switch to B
        success, cost = system.switch_task_set(new_task="B", preparation_time=0)

        assert success is True
        assert cost > 0  # Should have switch cost
        assert system.current_task_set == "B"

    def test_repeat_task_no_cost(self):
        """Repeating same task has no switch cost"""
        system = CognitiveFlexibilitySystem()

        # Establish baseline
        system.switch_task_set(new_task="A", preparation_time=0)

        # Repeat A
        success, cost = system.switch_task_set(new_task="A", preparation_time=0)

        assert success is True
        assert cost == 0.0  # No cost for repeat
        assert system.current_task_set == "A"

    def test_preparation_time_reduces_cost(self):
        """Preparation time reduces switch cost"""
        system = CognitiveFlexibilitySystem()

        # Establish baseline
        system.switch_task_set(new_task="A", preparation_time=0)

        # Switch without preparation
        _, cost_unprepared = system.switch_task_set(new_task="B", preparation_time=0)

        # Switch back to A
        system.switch_task_set(new_task="A", preparation_time=0)

        # Switch with preparation
        _, cost_prepared = system.switch_task_set(new_task="B", preparation_time=500)

        assert cost_prepared < cost_unprepared

    def test_repeated_switches_improve_performance(self):
        """Practice with task switching improves flexibility"""
        system = CognitiveFlexibilitySystem()

        # Establish baseline with process_event (which updates flexibility)
        system.process_event(new_task="A", preparation_time=0)

        initial_flexibility = system.current_flexibility

        # Practice switching many times using process_event
        for i in range(20):
            task = "A" if i % 2 == 0 else "B"
            system.process_event(new_task=task, preparation_time=0)

        # Flexibility should improve with practice
        assert system.current_flexibility > initial_flexibility

    def test_switch_count_tracking(self):
        """System tracks switch count correctly"""
        system = CognitiveFlexibilitySystem()

        # Establish baseline
        system.switch_task_set(new_task="A", preparation_time=0)

        # Perform 5 actual switches
        for _ in range(5):
            system.switch_task_set(new_task="B", preparation_time=0)
            system.switch_task_set(new_task="A", preparation_time=0)

        # 10 switches total (5 to B, 5 to A)
        assert system.switch_count == 10


class TestSwitchCostComputation:
    """Test switch cost computation"""

    def test_base_cost_without_preparation(self):
        """Base cost applies without preparation"""
        system = CognitiveFlexibilitySystem(
            baseline_flexibility=0.5,
            switch_cost_base=150.0
        )

        # Zero preparedness
        cost = system.compute_switch_cost(preparedness=0.0)

        # Should be near base cost
        assert 140 <= cost <= 160

    def test_high_preparedness_reduces_cost(self):
        """High preparedness reduces switch cost"""
        system = CognitiveFlexibilitySystem(switch_cost_base=150.0)

        cost_low_prep = system.compute_switch_cost(preparedness=0.2)
        cost_high_prep = system.compute_switch_cost(preparedness=0.9)

        assert cost_high_prep < cost_low_prep

    def test_high_flexibility_reduces_cost(self):
        """High flexibility reduces switch cost"""
        system = CognitiveFlexibilitySystem(switch_cost_base=150.0)

        # Low flexibility
        system.current_flexibility = 0.3
        cost_low_flex = system.compute_switch_cost(preparedness=0.5)

        # High flexibility
        system.current_flexibility = 0.9
        cost_high_flex = system.compute_switch_cost(preparedness=0.5)

        assert cost_high_flex < cost_low_flex

    def test_cost_never_negative(self):
        """Switch cost is never negative"""
        system = CognitiveFlexibilitySystem()

        # Even with perfect preparation and flexibility
        system.current_flexibility = 1.0
        cost = system.compute_switch_cost(preparedness=1.0)

        assert cost >= 0.0


class TestFlexibilityUpdate:
    """Test flexibility update mechanism"""

    def test_practice_improves_flexibility(self):
        """Repeated successful switching improves flexibility"""
        system = CognitiveFlexibilitySystem(baseline_flexibility=0.5)

        initial_flex = system.current_flexibility

        # Simulate successful practice
        system.update_flexibility(switch_frequency=0.8, success_rate=0.9)

        assert system.current_flexibility > initial_flex

    def test_success_rate_affects_learning(self):
        """Higher success rate yields greater flexibility improvement"""
        system1 = CognitiveFlexibilitySystem(baseline_flexibility=0.5)
        system2 = CognitiveFlexibilitySystem(baseline_flexibility=0.5)

        # Low success
        system1.update_flexibility(switch_frequency=0.8, success_rate=0.5)

        # High success
        system2.update_flexibility(switch_frequency=0.8, success_rate=0.95)

        assert system2.current_flexibility > system1.current_flexibility

    def test_flexibility_bounded(self):
        """Flexibility stays within [0, 1]"""
        system = CognitiveFlexibilitySystem()

        # Extreme updates
        system.update_flexibility(switch_frequency=1.0, success_rate=1.0)
        assert 0.0 <= system.current_flexibility <= 1.0

        system.update_flexibility(switch_frequency=0.0, success_rate=0.0)
        assert 0.0 <= system.current_flexibility <= 1.0

    def test_low_success_degrades_flexibility(self):
        """Poor performance degrades flexibility"""
        system = CognitiveFlexibilitySystem(baseline_flexibility=0.7)

        initial_flex = system.current_flexibility

        # Simulate poor performance
        system.update_flexibility(switch_frequency=0.3, success_rate=0.2)

        assert system.current_flexibility < initial_flex

    def test_adaptation_rate_affects_speed(self):
        """Adaptation rate controls learning speed"""
        system_slow = CognitiveFlexibilitySystem(
            baseline_flexibility=0.5,
            adaptation_rate=0.05
        )
        system_fast = CognitiveFlexibilitySystem(
            baseline_flexibility=0.5,
            adaptation_rate=0.3
        )

        # Same training
        system_slow.update_flexibility(switch_frequency=0.8, success_rate=0.9)
        system_fast.update_flexibility(switch_frequency=0.8, success_rate=0.9)

        # Fast learner should change more
        delta_slow = abs(system_slow.current_flexibility - 0.5)
        delta_fast = abs(system_fast.current_flexibility - 0.5)

        assert delta_fast > delta_slow


class TestDopamineIntegration:
    """Test dopamine modulation of cognitive flexibility"""

    def test_optimal_dopamine_maximizes_flexibility(self):
        """Optimal dopamine level maximizes flexibility (inverted-U)"""
        system = CognitiveFlexibilitySystem(baseline_flexibility=0.5)

        # Test inverted-U curve
        flex_low = system.integrate_dopamine(dopamine_level=0.2)
        flex_optimal = system.integrate_dopamine(dopamine_level=0.6)
        flex_high = system.integrate_dopamine(dopamine_level=0.9)

        # Optimal should be highest
        assert flex_optimal > flex_low
        assert flex_optimal > flex_high

    def test_too_low_dopamine_impairs(self):
        """Low dopamine impairs flexibility"""
        system = CognitiveFlexibilitySystem(baseline_flexibility=0.6)

        modulated = system.integrate_dopamine(dopamine_level=0.1)

        assert modulated < system.baseline_flexibility

    def test_too_high_dopamine_impairs(self):
        """High dopamine impairs flexibility (distractibility)"""
        system = CognitiveFlexibilitySystem(baseline_flexibility=0.6)

        modulated = system.integrate_dopamine(dopamine_level=0.95)

        assert modulated < system.baseline_flexibility

    def test_integration_bounded(self):
        """Dopamine modulation keeps flexibility within [0, 1]"""
        system = CognitiveFlexibilitySystem(baseline_flexibility=0.9)

        # Extreme dopamine shouldn't push outside bounds
        modulated = system.integrate_dopamine(dopamine_level=0.0)
        assert 0.0 <= modulated <= 1.0

        modulated = system.integrate_dopamine(dopamine_level=1.0)
        assert 0.0 <= modulated <= 1.0


class TestAcetylcholineIntegration:
    """Test acetylcholine modulation of rule encoding"""

    def test_high_ach_speeds_encoding(self):
        """High acetylcholine speeds rule encoding"""
        system = CognitiveFlexibilitySystem(rule_encoding_strength=0.7)

        # High ACh should boost encoding
        boost = system.integrate_acetylcholine(ach_level=0.9)

        assert boost > system.rule_encoding_strength

    def test_low_ach_slows_encoding(self):
        """Low acetylcholine slows rule encoding"""
        system = CognitiveFlexibilitySystem(rule_encoding_strength=0.7)

        # Low ACh should reduce encoding
        boost = system.integrate_acetylcholine(ach_level=0.2)

        assert boost < system.rule_encoding_strength

    def test_encoding_boost_bounded(self):
        """Encoding boost stays within reasonable bounds"""
        system = CognitiveFlexibilitySystem()

        # Extreme ACh levels
        boost = system.integrate_acetylcholine(ach_level=0.0)
        assert 0.0 <= boost <= 2.0

        boost = system.integrate_acetylcholine(ach_level=1.0)
        assert 0.0 <= boost <= 2.0


class TestPerseverationDetection:
    """Test perseveration detection (stuck in old task set)"""

    def test_detects_perseveration(self):
        """Detects when stuck in same task (perseveration)"""
        system = CognitiveFlexibilitySystem(history_window=10)

        # Establish task A
        system.switch_task_set(new_task="A", preparation_time=0)

        # Repeat A many times (no switching)
        for _ in range(15):
            system.switch_task_set(new_task="A", preparation_time=0)

        perseveration = system.detect_perseveration()

        # Should detect perseveration (stuck in A)
        assert perseveration is True

    def test_no_perseveration_with_switching(self):
        """No perseveration detected with regular switching"""
        system = CognitiveFlexibilitySystem()

        # Alternate between tasks
        for i in range(10):
            task = "A" if i % 2 == 0 else "B"
            system.switch_task_set(new_task=task, preparation_time=0)

        perseveration = system.detect_perseveration()

        # Should NOT detect perseveration
        assert perseveration is False

    def test_perseveration_threshold_configurable(self):
        """Perseveration detection threshold is configurable"""
        system = CognitiveFlexibilitySystem(history_window=5)

        # Establish task A
        system.switch_task_set(new_task="A", preparation_time=0)

        # Repeat A (5 times = 100% of window)
        for _ in range(5):
            system.switch_task_set(new_task="A", preparation_time=0)

        # Shorter window = easier to detect perseveration
        perseveration = system.detect_perseveration()

        assert perseveration is True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete_cycle(self):
        """process_event executes complete processing cycle"""
        system = CognitiveFlexibilitySystem()

        result = system.process_event(new_task="A", preparation_time=0)

        # Should return all expected keys
        assert "flexibility" in result
        assert "switch_cost_ms" in result
        assert "switch_success" in result
        assert "perseveration_detected" in result

    def test_process_event_outputs_valid(self):
        """process_event returns valid output values"""
        system = CognitiveFlexibilitySystem()

        result = system.process_event(new_task="A", preparation_time=500)

        # All outputs should be valid ranges
        assert 0.0 <= result["flexibility"] <= 1.0
        assert result["switch_cost_ms"] >= 0.0
        assert isinstance(result["switch_success"], bool)
        assert isinstance(result["perseveration_detected"], bool)
