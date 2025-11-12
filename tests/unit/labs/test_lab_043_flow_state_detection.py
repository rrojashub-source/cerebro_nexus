"""
LAB_043: Flow State Detection - Unit Tests

Homeostasis: "Optimal experience & performance"

Key Papers:
- Csikszentmihalyi (1990) - Flow: The Psychology of Optimal Experience
- Nakamura & Csikszentmihalyi (2002) - The concept of flow
- Ullén et al. (2010) - Proneness for psychological flow in everyday life
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_043_Flow_State_Detection.flow_state_system import (
    FlowStateSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default flow detection parameters"""
        system = FlowStateSystem()
        assert system.flow_threshold == 0.7
        assert system.in_flow == False

    def test_custom_flow_threshold(self):
        """System accepts custom flow threshold"""
        system = FlowStateSystem(flow_threshold=0.8)
        assert system.flow_threshold == 0.8

    def test_custom_skill_level(self):
        """System accepts custom initial skill level"""
        system = FlowStateSystem(initial_skill=0.6)
        assert system.skill_level == 0.6


class TestChallengeSkillBalance:
    """Test challenge-skill balance (core flow condition)"""

    def test_matched_challenge_skill_enables_flow(self):
        """Challenge ≈ Skill → Flow possible"""
        system = FlowStateSystem(initial_skill=0.7)

        result = system.assess_challenge_skill_balance(
            challenge=0.7,
            skill=0.7
        )

        assert result["balance"] > 0.8
        assert result["flow_possible"] == True

    def test_high_challenge_low_skill_anxiety(self):
        """Challenge >> Skill → Anxiety (no flow)"""
        system = FlowStateSystem(initial_skill=0.3)

        result = system.assess_challenge_skill_balance(
            challenge=0.9,
            skill=0.3
        )

        assert result["state"] == "anxiety"
        assert result["flow_possible"] == False

    def test_low_challenge_high_skill_boredom(self):
        """Challenge << Skill → Boredom (no flow)"""
        system = FlowStateSystem(initial_skill=0.9)

        result = system.assess_challenge_skill_balance(
            challenge=0.3,
            skill=0.9
        )

        assert result["state"] == "boredom"
        assert result["flow_possible"] == False

    def test_slight_mismatch_tolerable(self):
        """Slight mismatch (±0.1) → Flow still possible"""
        system = FlowStateSystem()

        result = system.assess_challenge_skill_balance(
            challenge=0.7,
            skill=0.6
        )

        assert result["flow_possible"] == True


class TestAttentionAbsorption:
    """Test attention absorption (focus depth)"""

    def test_high_absorption_indicates_flow(self):
        """High attention absorption → Flow indicator"""
        system = FlowStateSystem()

        result = system.measure_attention_absorption(
            focus_duration_minutes=60,
            distraction_count=1
        )

        assert result["absorption_level"] > 0.7

    def test_frequent_distractions_low_absorption(self):
        """Frequent distractions → Low absorption (no flow)"""
        system = FlowStateSystem()

        result = system.measure_attention_absorption(
            focus_duration_minutes=30,
            distraction_count=15
        )

        assert result["absorption_level"] < 0.3

    def test_longer_focus_higher_absorption(self):
        """Longer focus duration → Higher absorption"""
        system = FlowStateSystem()

        result_short = system.measure_attention_absorption(
            focus_duration_minutes=10,
            distraction_count=2
        )

        result_long = system.measure_attention_absorption(
            focus_duration_minutes=60,
            distraction_count=2
        )

        assert result_long["absorption_level"] > result_short["absorption_level"]


class TestTimeDistortion:
    """Test time distortion (subjective time perception)"""

    def test_flow_distorts_time_perception(self):
        """Flow → Time distortion (perceived ≠ actual)"""
        system = FlowStateSystem()
        system.in_flow = True

        result = system.measure_time_distortion(
            actual_minutes=60,
            perceived_minutes=30
        )

        assert result["distortion_ratio"] > 1.5
        assert result["flow_indicator"] == True

    def test_no_flow_accurate_time_perception(self):
        """No flow → Accurate time perception"""
        system = FlowStateSystem()
        system.in_flow = False

        result = system.measure_time_distortion(
            actual_minutes=60,
            perceived_minutes=58
        )

        assert result["distortion_ratio"] < 1.2
        assert result["flow_indicator"] == False

    def test_strong_distortion_strong_flow(self):
        """Stronger time distortion → Stronger flow"""
        system = FlowStateSystem()

        result = system.measure_time_distortion(
            actual_minutes=60,
            perceived_minutes=20
        )

        # 60/20 = 3.0 distortion ratio
        assert result["distortion_ratio"] == 3.0


class TestFlowDetection:
    """Test flow state detection"""

    def test_multiple_conditions_trigger_flow(self):
        """Challenge-skill balance + absorption + clear goals → Flow"""
        system = FlowStateSystem(initial_skill=0.7)

        result = system.detect_flow(
            challenge=0.7,
            skill=0.7,
            attention_absorption=0.9,
            clear_goals=True,
            immediate_feedback=True
        )

        assert result["in_flow"] == True
        assert result["flow_strength"] > 0.7

    def test_single_condition_insufficient(self):
        """Only one condition met → No flow"""
        system = FlowStateSystem()

        result = system.detect_flow(
            challenge=0.7,
            skill=0.7,
            attention_absorption=0.2,  # Low
            clear_goals=False,
            immediate_feedback=False
        )

        assert result["in_flow"] == False

    def test_flow_strength_quantified(self):
        """Flow strength quantified [0-1]"""
        system = FlowStateSystem(initial_skill=0.8)

        result = system.detect_flow(
            challenge=0.8,
            skill=0.8,
            attention_absorption=0.95,
            clear_goals=True,
            immediate_feedback=True
        )

        assert 0 <= result["flow_strength"] <= 1

    def test_flow_state_persists(self):
        """Flow state persists until conditions break"""
        system = FlowStateSystem(initial_skill=0.7)

        # Enter flow
        system.detect_flow(
            challenge=0.7,
            skill=0.7,
            attention_absorption=0.9,
            clear_goals=True,
            immediate_feedback=True
        )

        assert system.in_flow == True

        # Conditions persist
        result = system.detect_flow(
            challenge=0.7,
            skill=0.7,
            attention_absorption=0.85,
            clear_goals=True,
            immediate_feedback=True
        )

        assert system.in_flow == True


class TestFlowMaintenance:
    """Test flow state maintenance"""

    def test_skill_growth_requires_challenge_increase(self):
        """Skill increases → Challenge must increase to maintain flow"""
        system = FlowStateSystem(initial_skill=0.5)

        # Initial flow
        system.detect_flow(
            challenge=0.5,
            skill=0.5,
            attention_absorption=0.9,
            clear_goals=True,
            immediate_feedback=True
        )

        assert system.in_flow == True

        # Skill grows
        system.skill_level = 0.7

        # Same challenge → Boredom (flow breaks)
        result = system.detect_flow(
            challenge=0.5,
            skill=0.7,
            attention_absorption=0.9,
            clear_goals=True,
            immediate_feedback=True
        )

        assert result["in_flow"] == False

    def test_flow_exit_tracked(self):
        """Flow exit conditions recorded"""
        system = FlowStateSystem(initial_skill=0.7)

        system.in_flow = True

        # Break flow with distraction
        result = system.detect_flow(
            challenge=0.7,
            skill=0.7,
            attention_absorption=0.2,  # Distracted
            clear_goals=True,
            immediate_feedback=True
        )

        assert result["in_flow"] == False
        assert result["exit_reason"] in ["low_absorption", "conditions_not_met"]

    def test_flow_duration_tracked(self):
        """Flow duration tracked"""
        system = FlowStateSystem()

        system.enter_flow()

        # Simulate 60 minutes in flow
        system.update_flow_duration(duration_minutes=60)

        assert system.get_flow_duration() == 60


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_hyperfocus(self):
        """LAB_045: Flow overlaps with hyperfocus"""
        system = FlowStateSystem(initial_skill=0.7)

        result = system.detect_flow(
            challenge=0.7,
            skill=0.7,
            attention_absorption=0.95,  # Hyperfocus level
            clear_goals=True,
            immediate_feedback=True
        )

        assert result["in_flow"] == True
        assert result.get("hyperfocus_active", False) == True

    def test_integration_with_skill_acquisition(self):
        """LAB_040: Flow accelerates skill learning"""
        system = FlowStateSystem(initial_skill=0.5)

        system.in_flow = True

        result = system.apply_to_skill_learning(practice_duration=60)

        assert result["learning_boost"] > 1.0

    def test_integration_with_motivation(self):
        """Flow enhances intrinsic motivation"""
        system = FlowStateSystem()

        system.enter_flow()

        result = system.get_motivation_level()

        assert result["motivation_type"] == "intrinsic"
        assert result["motivation_level"] > 0.8


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_flow_check_event(self):
        """Process flow detection event"""
        system = FlowStateSystem(initial_skill=0.7)

        result = system.process_event(
            event_type="flow_check",
            challenge=0.7,
            attention_absorption=0.9,
            clear_goals=True
        )

        assert "in_flow" in result

    def test_process_skill_update_event(self):
        """Process skill level update event"""
        system = FlowStateSystem()

        result = system.process_event(
            event_type="skill_update",
            new_skill_level=0.8
        )

        assert system.skill_level == 0.8


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_flow_metrics(self):
        """get_state returns flow state metrics"""
        system = FlowStateSystem()

        system.enter_flow()

        state = system.get_state()

        assert "in_flow" in state
        assert "flow_duration" in state
        assert "skill_level" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = FlowStateSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
