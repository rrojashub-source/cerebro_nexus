"""
LAB_046: Default Mode Network - Unit Tests

Homeostasis: "Self-referential processing & mind-wandering"

Key Papers:
- Raichle et al. (2001) - A default mode of brain function
- Buckner et al. (2008) - The brain's default network
- Andrews-Hanna et al. (2014) - The default network and self-generated thought
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_046_Default_Mode_Network.dmn_system import (
    DefaultModeNetworkSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default DMN parameters"""
        system = DefaultModeNetworkSystem()
        assert system.dmn_active == False
        assert system.mind_wandering_rate == 0.0

    def test_custom_baseline_activation(self):
        """System accepts custom baseline activation"""
        system = DefaultModeNetworkSystem(baseline_activation=0.6)
        assert system.baseline_activation == 0.6

    def test_custom_suppression_strength(self):
        """System accepts custom task suppression strength"""
        system = DefaultModeNetworkSystem(task_suppression_strength=0.9)
        assert system.task_suppression_strength == 0.9


class TestSelfReferentialProcessing:
    """Test self-referential processing"""

    def test_dmn_active_during_self_reflection(self):
        """Self-reflection → DMN activation"""
        system = DefaultModeNetworkSystem()

        result = system.engage_self_referential_processing(
            task_type="autobiographical_memory"
        )

        assert result["dmn_active"] == True

    def test_autobiographical_memory_activates_dmn(self):
        """Autobiographical memory retrieval → DMN"""
        system = DefaultModeNetworkSystem()

        result = system.engage_self_referential_processing(
            task_type="autobiographical_memory"
        )

        assert result["dmn_activation_level"] > 0.7

    def test_external_task_suppresses_dmn(self):
        """External task → DMN suppression"""
        system = DefaultModeNetworkSystem()

        result = system.suppress_dmn_for_task(
            task_difficulty=0.8
        )

        assert result["dmn_suppressed"] == True
        assert result["dmn_activation_level"] < 0.3

    def test_easy_task_allows_dmn_activity(self):
        """Easy task → DMN still partially active"""
        system = DefaultModeNetworkSystem()

        result = system.suppress_dmn_for_task(
            task_difficulty=0.2
        )

        assert result["dmn_activation_level"] > 0.5


class TestMindWandering:
    """Test mind-wandering (spontaneous thought)"""

    def test_rest_triggers_mind_wandering(self):
        """Rest/idle state → Mind-wandering"""
        system = DefaultModeNetworkSystem()

        result = system.trigger_mind_wandering(
            external_stimulation=0.1
        )

        assert result["mind_wandering"] == True

    def test_high_stimulation_prevents_wandering(self):
        """High external stimulation → No mind-wandering"""
        system = DefaultModeNetworkSystem()

        result = system.trigger_mind_wandering(
            external_stimulation=0.9
        )

        assert result["mind_wandering"] == False

    def test_wandering_rate_tracked(self):
        """Mind-wandering rate tracked over time"""
        system = DefaultModeNetworkSystem()

        system.trigger_mind_wandering(external_stimulation=0.1)
        system.trigger_mind_wandering(external_stimulation=0.1)

        assert system.mind_wandering_rate > 0


class TestSocialCognition:
    """Test social cognition (mentalizing)"""

    def test_mentalizing_activates_dmn(self):
        """Mentalizing (theory of mind) → DMN activation"""
        system = DefaultModeNetworkSystem()

        result = system.engage_social_cognition(
            task_type="mentalizing"
        )

        assert result["dmn_active"] == True

    def test_perspective_taking_dmn(self):
        """Perspective-taking → DMN involvement"""
        system = DefaultModeNetworkSystem()

        result = system.engage_social_cognition(
            task_type="perspective_taking"
        )

        assert result["dmn_activation_level"] > 0.6

    def test_social_tasks_overlap_with_self_referential(self):
        """Social cognition overlaps with self-referential processing"""
        system = DefaultModeNetworkSystem()

        result_social = system.engage_social_cognition(task_type="mentalizing")
        result_self = system.engage_self_referential_processing(task_type="self_reflection")

        # Both should activate DMN
        assert result_social["dmn_active"] == True
        assert result_self["dmn_active"] == True


class TestFuturePlanning:
    """Test future planning (prospection)"""

    def test_future_simulation_activates_dmn(self):
        """Future simulation → DMN activation"""
        system = DefaultModeNetworkSystem()

        result = system.engage_future_planning(
            planning_type="episodic_future_thinking"
        )

        assert result["dmn_active"] == True

    def test_prospection_high_dmn_activity(self):
        """Prospection (future thinking) → High DMN"""
        system = DefaultModeNetworkSystem()

        result = system.engage_future_planning(
            planning_type="goal_planning"
        )

        assert result["dmn_activation_level"] > 0.7

    def test_immediate_planning_lower_dmn(self):
        """Immediate/concrete planning → Lower DMN"""
        system = DefaultModeNetworkSystem()

        result = system.engage_future_planning(
            planning_type="immediate_action"
        )

        assert result["dmn_activation_level"] < 0.5


class TestTaskNegativeActivation:
    """Test task-negative activation"""

    def test_dmn_deactivates_during_focused_task(self):
        """Focused external task → DMN deactivation"""
        system = DefaultModeNetworkSystem()

        result = system.engage_external_task(
            task_type="focused_attention",
            difficulty=0.9
        )

        assert result["dmn_active"] == False

    def test_dmn_reactivates_post_task(self):
        """Task completion → DMN reactivation"""
        system = DefaultModeNetworkSystem()

        # Suppress during task
        system.suppress_dmn_for_task(task_difficulty=0.9)

        # Reactivate after task
        result = system.reactivate_dmn()

        assert result["dmn_reactivated"] == True
        assert result["dmn_activation_level"] > 0.5

    def test_anticorrelation_with_task_positive_network(self):
        """DMN anticorrelates with task-positive network"""
        system = DefaultModeNetworkSystem()

        result_task = system.engage_external_task(
            task_type="problem_solving",
            difficulty=0.8
        )

        # High task activation → Low DMN
        assert result_task["dmn_activation_level"] < 0.3

    def test_task_difficulty_modulates_suppression(self):
        """Harder task → Stronger DMN suppression"""
        system = DefaultModeNetworkSystem()

        result_easy = system.suppress_dmn_for_task(task_difficulty=0.2)
        result_hard = system.suppress_dmn_for_task(task_difficulty=0.9)

        assert result_hard["dmn_activation_level"] < result_easy["dmn_activation_level"]


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_rest(self):
        """LAB_034: Rest activates DMN"""
        system = DefaultModeNetworkSystem()

        result = system.activate_during_rest()

        assert result["dmn_active"] == True
        assert result["dmn_activation_level"] >= 0.7

    def test_integration_with_meditation(self):
        """LAB_044: Meditation modulates DMN"""
        system = DefaultModeNetworkSystem()

        result = system.modulate_by_meditation(
            meditation_active=True
        )

        assert result["dmn_modulated"] == True
        assert result["dmn_activation_level"] < 0.5

    def test_integration_with_flow(self):
        """LAB_043: Flow state suppresses DMN"""
        system = DefaultModeNetworkSystem()

        result = system.suppress_during_flow(
            flow_active=True
        )

        assert result["dmn_suppressed"] == True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_self_referential_event(self):
        """Process self-referential processing event"""
        system = DefaultModeNetworkSystem()

        result = system.process_event(
            event_type="self_referential",
            task_type="autobiographical_memory"
        )

        assert "dmn_active" in result

    def test_process_external_task_event(self):
        """Process external task event"""
        system = DefaultModeNetworkSystem()

        result = system.process_event(
            event_type="external_task",
            task_type="problem_solving",
            difficulty=0.8
        )

        assert "dmn_active" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_dmn_metrics(self):
        """get_state returns DMN metrics"""
        system = DefaultModeNetworkSystem()

        system.dmn_active = True

        state = system.get_state()

        assert "dmn_active" in state
        assert "dmn_activation_level" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = DefaultModeNetworkSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
