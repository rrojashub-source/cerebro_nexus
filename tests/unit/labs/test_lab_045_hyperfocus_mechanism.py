"""
LAB_045: Hyperfocus Mechanism - Unit Tests

Homeostasis: "Intense single-task concentration"

Key Papers:
- Ashinoff & Abu-Akel (2021) - Hyperfocus: the forgotten frontier of attention
- Carson (2011) - Hyperfocus in creativity and ADHD
- Brown (2005) - Attention & hyperfocus in ADHD
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_045_Hyperfocus_Mechanism.hyperfocus_system import (
    HyperfocusSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default hyperfocus parameters"""
        system = HyperfocusSystem()
        assert system.hyperfocus_threshold == 0.85
        assert system.in_hyperfocus == False

    def test_custom_hyperfocus_threshold(self):
        """System accepts custom hyperfocus threshold"""
        system = HyperfocusSystem(hyperfocus_threshold=0.85)
        assert system.hyperfocus_threshold == 0.85

    def test_custom_interruption_resistance(self):
        """System accepts custom interruption resistance"""
        system = HyperfocusSystem(interruption_resistance=0.8)
        assert system.interruption_resistance == 0.8


class TestIntenseFocus:
    """Test intense attention focus"""

    def test_narrow_attention_scope(self):
        """Hyperfocus → Narrow attention scope"""
        system = HyperfocusSystem()

        result = system.assess_attention_scope(
            task_count=1,
            attention_level=0.95
        )

        assert result["attention_scope"] == "narrow"
        assert result["hyperfocus_possible"] == True

    def test_multitasking_prevents_hyperfocus(self):
        """Multiple tasks → No hyperfocus"""
        system = HyperfocusSystem()

        result = system.assess_attention_scope(
            task_count=5,
            attention_level=0.9
        )

        assert result["attention_scope"] == "broad"
        assert result["hyperfocus_possible"] == False

    def test_intensity_increases_with_focus(self):
        """Longer single-task focus → Higher intensity"""
        system = HyperfocusSystem()

        result1 = system.measure_focus_intensity(duration_minutes=10)
        result2 = system.measure_focus_intensity(duration_minutes=120)

        assert result2["focus_intensity"] > result1["focus_intensity"]


class TestTimeBlindness:
    """Test time blindness (lose track of time)"""

    def test_hyperfocus_causes_time_blindness(self):
        """Hyperfocus → Time blindness"""
        system = HyperfocusSystem()
        system.in_hyperfocus = True

        result = system.assess_time_awareness(
            actual_minutes=120,
            perceived_minutes=30
        )

        assert result["time_blind"] == True

    def test_no_hyperfocus_accurate_time(self):
        """No hyperfocus → Accurate time awareness"""
        system = HyperfocusSystem()
        system.in_hyperfocus = False

        result = system.assess_time_awareness(
            actual_minutes=30,
            perceived_minutes=28
        )

        assert result["time_blind"] == False

    def test_extreme_distortion_indicates_hyperfocus(self):
        """Extreme time distortion → Hyperfocus indicator"""
        system = HyperfocusSystem()

        result = system.assess_time_awareness(
            actual_minutes=180,
            perceived_minutes=20
        )

        # 180/20 = 9.0 distortion ratio
        assert result["distortion_ratio"] > 5.0
        assert result["hyperfocus_indicator"] == True


class TestTaskImmersion:
    """Test task immersion"""

    def test_high_immersion_triggers_hyperfocus(self):
        """High task immersion → Hyperfocus"""
        system = HyperfocusSystem()

        result = system.detect_hyperfocus(
            attention_level=0.98,
            task_count=1,
            immersion_level=0.95,
            intrinsic_motivation=True
        )

        assert result["in_hyperfocus"] == True

    def test_low_immersion_no_hyperfocus(self):
        """Low immersion → No hyperfocus"""
        system = HyperfocusSystem()

        result = system.detect_hyperfocus(
            attention_level=0.95,
            task_count=1,
            immersion_level=0.3,
            intrinsic_motivation=False
        )

        assert result["in_hyperfocus"] == False

    def test_immersion_correlates_with_hyperfocus_strength(self):
        """Higher immersion → Stronger hyperfocus"""
        system = HyperfocusSystem()

        result = system.detect_hyperfocus(
            attention_level=0.98,
            task_count=1,
            immersion_level=0.98,
            intrinsic_motivation=True
        )

        assert result["hyperfocus_strength"] > 0.9


class TestInterruptionResistance:
    """Test resistance to interruption"""

    def test_hyperfocus_resists_interruptions(self):
        """Hyperfocus → High interruption resistance"""
        system = HyperfocusSystem()
        system.in_hyperfocus = True

        result = system.attempt_interruption(interruption_strength=0.5)

        assert result["interrupted"] == False

    def test_strong_interruption_can_break_hyperfocus(self):
        """Strong interruption → Can break hyperfocus"""
        system = HyperfocusSystem(interruption_resistance=0.7)
        system.in_hyperfocus = True

        result = system.attempt_interruption(interruption_strength=0.9)

        assert result["interrupted"] == True

    def test_no_hyperfocus_easily_interrupted(self):
        """No hyperfocus → Easily interrupted"""
        system = HyperfocusSystem()
        system.in_hyperfocus = False

        result = system.attempt_interruption(interruption_strength=0.3)

        assert result["interrupted"] == True


class TestHyperfocusTriggers:
    """Test hyperfocus triggers"""

    def test_intrinsic_motivation_enables_hyperfocus(self):
        """Intrinsic motivation → Hyperfocus enabler"""
        system = HyperfocusSystem()

        result = system.detect_hyperfocus(
            attention_level=0.95,
            task_count=1,
            immersion_level=0.9,
            intrinsic_motivation=True
        )

        assert result["in_hyperfocus"] == True

    def test_extrinsic_motivation_weaker_hyperfocus(self):
        """Extrinsic motivation → Weaker hyperfocus"""
        system = HyperfocusSystem()

        result = system.detect_hyperfocus(
            attention_level=0.95,
            task_count=1,
            immersion_level=0.9,
            intrinsic_motivation=False
        )

        assert result["in_hyperfocus"] == False or result["hyperfocus_strength"] < 0.9

    def test_dopamine_surge_triggers_hyperfocus(self):
        """Dopamine surge (LAB_035) → Hyperfocus trigger"""
        system = HyperfocusSystem()

        result = system.trigger_from_dopamine(
            dopamine_level=0.9
        )

        assert result["hyperfocus_triggered"] == True


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_flow(self):
        """LAB_043: Hyperfocus overlaps with flow (but more intense)"""
        system = HyperfocusSystem()

        result = system.detect_hyperfocus(
            attention_level=0.98,
            task_count=1,
            immersion_level=0.95,
            intrinsic_motivation=True
        )

        assert result["in_hyperfocus"] == True
        assert result.get("flow_active", False) == True

    def test_integration_with_dopamine(self):
        """LAB_035: Dopamine drives hyperfocus intensity"""
        system = HyperfocusSystem()

        result = system.modulate_by_dopamine(
            base_intensity=0.8,
            dopamine_level=0.95
        )

        assert result["modulated_intensity"] > 0.8

    def test_integration_with_skill_acquisition(self):
        """LAB_040: Hyperfocus accelerates skill learning"""
        system = HyperfocusSystem()
        system.in_hyperfocus = True

        result = system.apply_to_skill_learning(practice_duration=60)

        assert result["learning_boost"] > 1.5


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_hyperfocus_check_event(self):
        """Process hyperfocus detection event"""
        system = HyperfocusSystem()

        result = system.process_event(
            event_type="hyperfocus_check",
            attention_level=0.98,
            task_count=1,
            immersion_level=0.95
        )

        assert "in_hyperfocus" in result

    def test_process_interruption_event(self):
        """Process interruption attempt event"""
        system = HyperfocusSystem()
        system.in_hyperfocus = True

        result = system.process_event(
            event_type="interruption",
            interruption_strength=0.5
        )

        assert "interrupted" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_hyperfocus_metrics(self):
        """get_state returns hyperfocus metrics"""
        system = HyperfocusSystem()

        system.in_hyperfocus = True

        state = system.get_state()

        assert "in_hyperfocus" in state
        assert "hyperfocus_threshold" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = HyperfocusSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
