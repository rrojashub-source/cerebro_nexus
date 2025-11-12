"""
LAB_037: Curiosity Drive - Unit Tests

Advanced Learning: Information-seeking, exploration bonus

Key Papers:
- Kidd & Hayden (2015) - The psychology and neuroscience of curiosity
- Gottlieb et al. (2013) - Information-seeking, curiosity, and attention
- Schmidhuber (1991) - A possibility for implementing curiosity and boredom
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_037_Curiosity_Drive.curiosity_drive_system import (
    CuriosityDriveSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = CuriosityDriveSystem()
        assert system.exploration_bonus == 0.1
        assert system.uncertainty_threshold == 0.5
        assert system.current_curiosity == 0.0

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = CuriosityDriveSystem(
            exploration_bonus=0.2,
            uncertainty_threshold=0.6
        )
        assert system.exploration_bonus == 0.2
        assert system.uncertainty_threshold == 0.6


class TestInformationGapDetection:
    """Test information gap detection (Loewenstein 1994)"""

    def test_high_uncertainty_large_gap(self):
        """High uncertainty indicates large information gap"""
        system = CuriosityDriveSystem()

        gap = system.detect_information_gap(uncertainty=0.8, knowledge_level=0.3)

        assert gap > 0.6  # Large gap

    def test_low_uncertainty_small_gap(self):
        """Low uncertainty = small information gap"""
        system = CuriosityDriveSystem()

        gap = system.detect_information_gap(uncertainty=0.2, knowledge_level=0.7)

        assert gap < 0.4  # Small gap

    def test_prediction_error_as_gap_signal(self):
        """Prediction error indicates information gap"""
        system = CuriosityDriveSystem()

        # Large prediction error = large gap
        large_error = system.detect_information_gap(
            uncertainty=0.7,
            knowledge_level=0.4,
            prediction_error=0.8
        )

        # Small prediction error = small gap
        small_error = system.detect_information_gap(
            uncertainty=0.7,
            knowledge_level=0.4,
            prediction_error=0.2
        )

        assert large_error > small_error


class TestCuriosityComputation:
    """Test curiosity level computation"""

    def test_inverted_u_with_uncertainty(self):
        """Moderate uncertainty = peak curiosity (inverted-U)"""
        system = CuriosityDriveSystem()

        low = system.compute_curiosity_level(uncertainty=0.1, novelty=0.5)
        moderate = system.compute_curiosity_level(uncertainty=0.5, novelty=0.5)
        high = system.compute_curiosity_level(uncertainty=0.9, novelty=0.5)

        # Moderate should be highest
        assert moderate > low
        assert moderate > high

    def test_novelty_amplifies_curiosity(self):
        """High novelty (from LAB_004) amplifies curiosity"""
        system = CuriosityDriveSystem()

        low_novelty = system.compute_curiosity_level(uncertainty=0.5, novelty=0.2)
        high_novelty = system.compute_curiosity_level(uncertainty=0.5, novelty=0.8)

        assert high_novelty > low_novelty

    def test_zero_uncertainty_low_curiosity(self):
        """Zero uncertainty (certainty) = low curiosity"""
        system = CuriosityDriveSystem()

        curiosity = system.compute_curiosity_level(uncertainty=0.0, novelty=0.5)

        assert curiosity < 0.3

    def test_curiosity_updates_state(self):
        """Computing curiosity updates current_curiosity"""
        system = CuriosityDriveSystem()

        curiosity = system.compute_curiosity_level(uncertainty=0.5, novelty=0.6)

        assert system.current_curiosity == curiosity
        assert system.current_curiosity > 0


class TestExplorationBonus:
    """Test exploration bonus (intrinsic reward)"""

    def test_exploration_bonus_proportional_to_novelty(self):
        """Exploration bonus increases with action novelty"""
        system = CuriosityDriveSystem()

        low_novelty_bonus = system.compute_exploration_bonus(action_novelty=0.3)
        high_novelty_bonus = system.compute_exploration_bonus(action_novelty=0.8)

        assert high_novelty_bonus > low_novelty_bonus

    def test_bonus_parameter_modulates_strength(self):
        """exploration_bonus parameter modulates reward strength"""
        system_high = CuriosityDriveSystem(exploration_bonus=0.3)
        system_low = CuriosityDriveSystem(exploration_bonus=0.1)

        novelty = 0.7

        high_reward = system_high.compute_exploration_bonus(action_novelty=novelty)
        low_reward = system_low.compute_exploration_bonus(action_novelty=novelty)

        assert high_reward > low_reward

    def test_information_gain_as_intrinsic_reward(self):
        """Information gain provides intrinsic reward"""
        system = CuriosityDriveSystem()

        # Exploration that reduces uncertainty = reward
        reward = system.compute_exploration_bonus(
            action_novelty=0.6,
            information_gain=0.7
        )

        assert reward > system.exploration_bonus  # Base bonus amplified


class TestExploreExploitBalance:
    """Test exploration vs exploitation decision"""

    def test_high_curiosity_biases_exploration(self):
        """High curiosity → prefer exploration"""
        system = CuriosityDriveSystem()

        # High curiosity, low task value
        result = system.balance_explore_exploit(
            curiosity_level=0.8,
            task_value=0.3
        )

        assert result["action"] == "explore"
        assert result["explore_probability"] > 0.6

    def test_high_task_value_biases_exploitation(self):
        """High task value → prefer exploitation"""
        system = CuriosityDriveSystem()

        # Low curiosity, high task value
        result = system.balance_explore_exploit(
            curiosity_level=0.3,
            task_value=0.9
        )

        assert result["action"] == "exploit"
        assert result["exploit_probability"] > 0.6

    def test_balanced_state_mixed_strategy(self):
        """Balanced curiosity + task value = mixed strategy"""
        system = CuriosityDriveSystem()

        result = system.balance_explore_exploit(
            curiosity_level=0.5,
            task_value=0.5
        )

        # Should be close to 50/50
        assert 0.4 < result["explore_probability"] < 0.6


class TestIntegrationNoveltyDetection:
    """Test integration with LAB_004 (Novelty Detection)"""

    def test_novelty_increases_curiosity(self):
        """High novelty from LAB_004 increases curiosity"""
        system = CuriosityDriveSystem()

        # Simulate LAB_004 novelty signal
        novelty_signal = 0.8

        curiosity = system.compute_curiosity_level(
            uncertainty=0.5,
            novelty=novelty_signal
        )

        assert curiosity > 0.5

    def test_familiar_reduces_curiosity(self):
        """Familiar (zero novelty) reduces curiosity"""
        system = CuriosityDriveSystem()

        curiosity = system.compute_curiosity_level(
            uncertainty=0.5,
            novelty=0.0  # Completely familiar
        )

        assert curiosity < 0.4


class TestIntegrationDopamine:
    """Test integration with LAB_013 (Dopamine)"""

    def test_curiosity_as_intrinsic_reward_signal(self):
        """Curiosity generates intrinsic reward (dopamine signal)"""
        system = CuriosityDriveSystem()

        # High curiosity + information gain = reward
        result = system.process_event(
            event_type="exploration",
            uncertainty=0.6,
            novelty=0.7,
            information_gain=0.5
        )

        assert "intrinsic_reward" in result
        assert result["intrinsic_reward"] > 0.3  # Significant reward


class TestBidirectionalWithIntrinsicMotivation:
    """Test bidirectional integration with LAB_036"""

    def test_curiosity_component_of_intrinsic_motivation(self):
        """Curiosity is component of intrinsic motivation (LAB_036)"""
        system = CuriosityDriveSystem()

        curiosity = system.compute_curiosity_level(uncertainty=0.6, novelty=0.7)

        # This curiosity level feeds into LAB_036
        assert curiosity > 0  # Provides signal to LAB_036

    def test_intrinsic_motivation_modulates_curiosity(self):
        """Intrinsic motivation state modulates curiosity expression"""
        system = CuriosityDriveSystem()

        # High intrinsic motivation (from LAB_036) amplifies curiosity
        result_high_motivation = system.process_event(
            event_type="exploration",
            uncertainty=0.5,
            novelty=0.6,
            intrinsic_motivation_level=0.8  # From LAB_036
        )

        # Low intrinsic motivation
        result_low_motivation = system.process_event(
            event_type="exploration",
            uncertainty=0.5,
            novelty=0.6,
            intrinsic_motivation_level=0.2
        )

        # High motivation should amplify curiosity-driven exploration
        assert result_high_motivation["curiosity"] >= result_low_motivation["curiosity"]


class TestExplorationHistory:
    """Test exploration history tracking"""

    def test_exploration_history_tracked(self):
        """System tracks exploration actions"""
        system = CuriosityDriveSystem()

        system.process_event(
            event_type="exploration",
            uncertainty=0.6,
            novelty=0.7
        )

        assert len(system.exploration_history) > 0

    def test_repeated_exploration_reduces_novelty(self):
        """Repeated exploration of same target reduces novelty"""
        system = CuriosityDriveSystem()

        # First exploration
        first = system.process_event(
            event_type="exploration",
            uncertainty=0.6,
            novelty=0.8,
            target_id="target_A"
        )

        # Second exploration of same target
        second = system.process_event(
            event_type="exploration",
            uncertainty=0.6,
            novelty=0.8,  # Same novelty input
            target_id="target_A"
        )

        # Second should have reduced effective novelty (habituation)
        assert second["effective_novelty"] < first["effective_novelty"]


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_exploration_event(self):
        """Process exploration event computes curiosity + bonus"""
        system = CuriosityDriveSystem()

        result = system.process_event(
            event_type="exploration",
            uncertainty=0.6,
            novelty=0.7,
            information_gain=0.5
        )

        assert "curiosity" in result
        assert "exploration_bonus" in result
        assert "intrinsic_reward" in result

    def test_process_decision_event(self):
        """Process explore-exploit decision"""
        system = CuriosityDriveSystem()

        result = system.process_event(
            event_type="decision",
            curiosity_level=0.7,
            task_value=0.4
        )

        assert "action" in result
        assert result["action"] in ["explore", "exploit"]
        assert "explore_probability" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_curiosity_metrics(self):
        """get_state returns current curiosity state"""
        system = CuriosityDriveSystem()

        system.current_curiosity = 0.7

        state = system.get_state()

        assert "current_curiosity" in state
        assert state["current_curiosity"] == 0.7

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = CuriosityDriveSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
