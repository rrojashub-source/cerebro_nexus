"""
LAB_033: Allostatic Load - Unit Tests

Homeostasis: Cumulative stress tracking, stress effects on cognition

Key Papers:
- McEwen (2000) - Allostasis and allostatic load
- Arnsten (2009) - Stress impairs prefrontal cortex
- Sapolsky (2004) - Why zebras don't get ulcers
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Social_Homeostasis.LAB_033_Allostatic_Load.allostatic_load_system import (
    AllostaticLoadSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with zero load"""
        system = AllostaticLoadSystem()
        assert system.current_load == 0.0

    def test_custom_initialization(self):
        """System accepts custom starting load"""
        system = AllostaticLoadSystem(starting_load=0.3)
        assert system.current_load == 0.3


class TestStressAccumulation:
    """Test stress accumulation mechanics"""

    def test_load_accumulates_with_stressors(self):
        """Allostatic load increases with stressors"""
        system = AllostaticLoadSystem()

        initial_load = system.current_load

        # Experience stressor
        system.accumulate_stress(stressor_intensity=0.7)

        assert system.current_load > initial_load

    def test_stronger_stressors_add_more_load(self):
        """Intense stressors add more load"""
        system1 = AllostaticLoadSystem()
        system2 = AllostaticLoadSystem()

        # Mild stressor
        system1.accumulate_stress(stressor_intensity=0.3)

        # Severe stressor
        system2.accumulate_stress(stressor_intensity=0.9)

        assert system2.current_load > system1.current_load

    def test_load_accumulates_over_multiple_stressors(self):
        """Multiple stressors accumulate load"""
        system = AllostaticLoadSystem()

        # Multiple stressors
        for _ in range(5):
            system.accumulate_stress(stressor_intensity=0.5)

        assert system.current_load > 0.2  # Significant accumulation


class TestStressDecay:
    """Test stress decay (chronic stress recovery)"""

    def test_load_decays_slowly_without_stressors(self):
        """Allostatic load decays slowly (chronic recovery)"""
        system = AllostaticLoadSystem(starting_load=0.8)

        initial_load = system.current_load

        # Time passes without stressors
        system.decay_stress(time_units=5)

        assert system.current_load < initial_load
        assert system.current_load > 0.4  # Decays slowly

    def test_decay_is_gradual_not_immediate(self):
        """Decay is gradual (chronic stress persists)"""
        system = AllostaticLoadSystem(starting_load=0.6)

        # Short time
        system.decay_stress(time_units=1)

        # Should still have significant load
        assert system.current_load > 0.5

    def test_prolonged_rest_reduces_load_significantly(self):
        """Prolonged rest significantly reduces load"""
        system = AllostaticLoadSystem(starting_load=0.7)

        # Long rest period
        system.decay_stress(time_units=20)

        assert system.current_load < 0.4


class TestPerformanceCurve:
    """Test inverted-U performance curve"""

    def test_optimal_load_best_performance(self):
        """Moderate load (0.3-0.6) produces best performance"""
        system = AllostaticLoadSystem(starting_load=0.45)

        result = system.compute_stress_effects()

        assert result["performance_multiplier"] > 0.9

    def test_low_load_underaroused(self):
        """Very low load = under-aroused, suboptimal performance"""
        system = AllostaticLoadSystem(starting_load=0.1)

        result = system.compute_stress_effects()

        assert result["performance_multiplier"] < 0.9

    def test_high_load_overaroused(self):
        """High load (>0.6) = over-aroused, impaired performance"""
        system = AllostaticLoadSystem(starting_load=0.8)

        result = system.compute_stress_effects()

        assert result["performance_multiplier"] < 0.7

    def test_extreme_load_severe_impairment(self):
        """Extreme load (>0.9) = severe impairment"""
        system = AllostaticLoadSystem(starting_load=0.95)

        result = system.compute_stress_effects()

        assert result["performance_multiplier"] < 0.5


class TestPFCImpairment:
    """Test prefrontal cortex impairment under stress"""

    def test_high_load_impairs_pfc(self):
        """Load > 0.65 impairs PFC functions (Arnsten 2009)"""
        system = AllostaticLoadSystem(starting_load=0.8)

        result = system.pfc_impairment()

        assert result["pfc_impaired"] == True
        assert result["impairment_level"] > 0.3  # At 0.8 load, expect > 0.3

    def test_low_load_no_pfc_impairment(self):
        """Load < 0.6 does not impair PFC"""
        system = AllostaticLoadSystem(starting_load=0.4)

        result = system.pfc_impairment()

        assert result["pfc_impaired"] == False

    def test_cognitive_control_impaired_under_stress(self):
        """High load impairs cognitive control (LAB_019 integration)"""
        system = AllostaticLoadSystem(starting_load=0.8)

        result = system.modulate_cognitive_function(
            function="cognitive_control",
            baseline=0.8
        )

        assert result["modulated_performance"] < 0.8

    def test_cognitive_flexibility_reduced_under_stress(self):
        """High load reduces cognitive flexibility (LAB_020 integration)"""
        system = AllostaticLoadSystem(starting_load=0.75)

        result = system.modulate_cognitive_function(
            function="cognitive_flexibility",
            baseline=0.8
        )

        assert result["modulated_performance"] < 0.8

    def test_error_monitoring_impaired(self):
        """High load impairs error monitoring (LAB_021 integration)"""
        system = AllostaticLoadSystem(starting_load=0.8)

        result = system.modulate_cognitive_function(
            function="error_monitoring",
            baseline=0.8
        )

        assert result["modulated_performance"] < 0.8


class TestAmygdalaReactivity:
    """Test amygdala reactivity enhancement under stress"""

    def test_high_load_enhances_amygdala_reactivity(self):
        """High stress enhances amygdala reactivity"""
        system = AllostaticLoadSystem(starting_load=0.8)

        result = system.amygdala_reactivity()

        assert result["reactivity_level"] > 1.2  # Enhanced

    def test_low_load_normal_amygdala(self):
        """Low stress = normal amygdala reactivity"""
        system = AllostaticLoadSystem(starting_load=0.3)

        result = system.amygdala_reactivity()

        assert 0.9 <= result["reactivity_level"] <= 1.1  # Normal range

    def test_emotional_salience_amplified(self):
        """Stress amplifies emotional salience (LAB_001 integration)"""
        system = AllostaticLoadSystem(starting_load=0.75)

        result = system.modulate_emotional_response(
            baseline_salience=0.6
        )

        # Should be amplified
        assert result["modulated_salience"] > 0.6


class TestWorkingMemoryReduction:
    """Test working memory capacity reduction under stress"""

    def test_high_load_reduces_working_memory(self):
        """Stress reduces working memory capacity (LAB_011 integration)"""
        system = AllostaticLoadSystem(starting_load=0.8)

        result = system.modulate_working_memory_capacity(
            baseline_capacity=7
        )

        assert result["modulated_capacity"] < 7

    def test_extreme_stress_severe_wm_reduction(self):
        """Extreme stress severely reduces WM capacity"""
        system = AllostaticLoadSystem(starting_load=0.95)

        result = system.modulate_working_memory_capacity(
            baseline_capacity=7
        )

        assert result["modulated_capacity"] <= 4  # Severe reduction


class TestNorepinephrineIntegration:
    """Test integration with LAB_015 (Norepinephrine)"""

    def test_acute_stress_triggers_norepinephrine(self):
        """Acute stressor triggers NE spike (LAB_015)"""
        system = AllostaticLoadSystem()

        result = system.accumulate_stress(
            stressor_intensity=0.8,
            stressor_type="acute"
        )

        assert "norepinephrine_spike" in result
        assert result["norepinephrine_spike"] == True

    def test_chronic_stress_no_ne_spike(self):
        """Chronic stress does not trigger acute NE spike"""
        system = AllostaticLoadSystem()

        result = system.accumulate_stress(
            stressor_intensity=0.3,
            stressor_type="chronic"
        )

        assert result.get("norepinephrine_spike", False) == False


class TestEnergyInteraction:
    """Test interaction with LAB_032 (Energy Management)"""

    def test_high_load_accelerates_energy_depletion(self):
        """High allostatic load accelerates energy depletion"""
        system = AllostaticLoadSystem(starting_load=0.7)

        result = system.compute_energy_depletion_modifier()

        # Should increase depletion rate
        assert result["depletion_multiplier"] > 1.0

    def test_low_load_normal_energy_depletion(self):
        """Low load = normal energy depletion"""
        system = AllostaticLoadSystem(starting_load=0.3)

        result = system.compute_energy_depletion_modifier()

        assert result["depletion_multiplier"] == pytest.approx(1.0, abs=0.1)


class TestRecoveryDynamics:
    """Test recovery from allostatic load"""

    def test_recovery_requires_prolonged_rest(self):
        """Recovery from chronic stress is slow"""
        system = AllostaticLoadSystem(starting_load=0.8)

        # Short rest
        system.decay_stress(time_units=2)

        # Should still be elevated
        assert system.current_load > 0.6

    def test_recovery_threshold(self):
        """Below threshold load (<0.3) = recovered"""
        system = AllostaticLoadSystem(starting_load=0.25)

        result = system.is_recovered()

        assert result["recovered"] == True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_stressor_event(self):
        """Process acute stressor event"""
        system = AllostaticLoadSystem()

        result = system.process_event(
            event_type="stressor",
            intensity=0.7,
            stressor_type="acute"
        )

        assert "load_after" in result
        assert result["load_after"] > 0.0

    def test_process_recovery_event(self):
        """Process recovery/rest event"""
        system = AllostaticLoadSystem(starting_load=0.6)

        result = system.process_event(
            event_type="recovery",
            duration=5
        )

        assert result["load_after"] < 0.6

    def test_process_cognitive_task_under_stress(self):
        """Process cognitive task with stress modulation"""
        system = AllostaticLoadSystem(starting_load=0.7)

        result = system.process_event(
            event_type="cognitive_task",
            function="cognitive_control",
            baseline=0.8
        )

        assert "modulated_performance" in result
        assert result["modulated_performance"] < 0.8


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_load_metrics(self):
        """get_state returns complete stress state"""
        system = AllostaticLoadSystem(starting_load=0.5)

        state = system.get_state()

        assert "current_load" in state
        assert "pfc_impaired" in state
        assert "performance_level" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = AllostaticLoadSystem()

        state = system.get_state()

        # Should be JSON serializable
        import json
        json_str = json.dumps(state)
        assert json_str is not None
