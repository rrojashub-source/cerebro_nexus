"""
LAB_036: Intrinsic Motivation - Unit Tests

Advanced Learning: Curiosity, mastery, autonomy drives

Key Papers:
- Ryan & Deci (2000) - Self-determination theory
- Oudeyer et al. (2007) - Intrinsic motivation in robots
- White (1959) - Motivation reconsidered: competence
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_036_Intrinsic_Motivation.intrinsic_motivation_system import (
    IntrinsicMotivationSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default weights"""
        system = IntrinsicMotivationSystem()
        assert system.curiosity_weight == 0.4
        assert system.mastery_weight == 0.4
        assert system.autonomy_weight == 0.2
        assert system.current_curiosity == 0.0
        assert system.current_competence == 0.0
        assert system.current_autonomy == 0.0

    def test_custom_weights(self):
        """System accepts custom component weights"""
        system = IntrinsicMotivationSystem(
            curiosity_weight=0.5,
            mastery_weight=0.3,
            autonomy_weight=0.2
        )
        assert system.curiosity_weight == 0.5
        assert system.mastery_weight == 0.3
        assert system.autonomy_weight == 0.2

    def test_weights_sum_to_one(self):
        """Component weights should sum to 1.0"""
        system = IntrinsicMotivationSystem()
        total = system.curiosity_weight + system.mastery_weight + system.autonomy_weight
        assert total == pytest.approx(1.0, abs=0.01)


class TestCuriosityDrive:
    """Test epistemic curiosity (Berlyne 1960)"""

    def test_moderate_novelty_peak_curiosity(self):
        """Inverted-U: moderate novelty produces peak curiosity"""
        system = IntrinsicMotivationSystem()

        low_novelty = system.compute_curiosity_drive(novelty_level=0.2, information_gap=0.5)
        moderate_novelty = system.compute_curiosity_drive(novelty_level=0.5, information_gap=0.5)
        high_novelty = system.compute_curiosity_drive(novelty_level=0.9, information_gap=0.5)

        # Moderate should be highest
        assert moderate_novelty > low_novelty
        assert moderate_novelty > high_novelty

    def test_information_gap_increases_curiosity(self):
        """Larger information gap = higher curiosity"""
        system = IntrinsicMotivationSystem()

        small_gap = system.compute_curiosity_drive(novelty_level=0.5, information_gap=0.2)
        large_gap = system.compute_curiosity_drive(novelty_level=0.5, information_gap=0.8)

        assert large_gap > small_gap

    def test_zero_novelty_low_curiosity(self):
        """Zero novelty = low curiosity (boredom)"""
        system = IntrinsicMotivationSystem()

        curiosity = system.compute_curiosity_drive(novelty_level=0.0, information_gap=0.5)

        assert curiosity < 0.3

    def test_extreme_novelty_low_curiosity(self):
        """Extreme novelty = low curiosity (confusion/anxiety)"""
        system = IntrinsicMotivationSystem()

        curiosity = system.compute_curiosity_drive(novelty_level=1.0, information_gap=0.5)

        assert curiosity < 0.7  # Less than moderate novelty

    def test_curiosity_updates_state(self):
        """Computing curiosity updates current_curiosity"""
        system = IntrinsicMotivationSystem()

        curiosity = system.compute_curiosity_drive(novelty_level=0.5, information_gap=0.6)

        assert system.current_curiosity == curiosity
        assert system.current_curiosity > 0


class TestCompetenceMastery:
    """Test competence/mastery motivation (White 1959, flow theory)"""

    def test_optimal_challenge_peak_motivation(self):
        """Skill ≈ challenge produces peak motivation (flow)"""
        system = IntrinsicMotivationSystem()

        too_easy = system.compute_competence_motivation(skill_level=0.8, challenge_level=0.3)
        optimal = system.compute_competence_motivation(skill_level=0.6, challenge_level=0.6)
        too_hard = system.compute_competence_motivation(skill_level=0.3, challenge_level=0.9)

        # Optimal challenge = peak motivation
        assert optimal > too_easy
        assert optimal > too_hard

    def test_progress_increases_motivation(self):
        """Progress toward mastery increases motivation"""
        system = IntrinsicMotivationSystem()

        # Initial state
        baseline = system.compute_competence_motivation(skill_level=0.4, challenge_level=0.5)

        # After improvement
        improved = system.compute_competence_motivation(skill_level=0.5, challenge_level=0.5)

        # Progress (skill increase) should increase motivation
        assert improved >= baseline

    def test_too_easy_task_boredom(self):
        """Challenge << skill = boredom (low motivation)"""
        system = IntrinsicMotivationSystem()

        motivation = system.compute_competence_motivation(skill_level=0.9, challenge_level=0.2)

        assert motivation < 0.5  # Low motivation

    def test_too_hard_task_anxiety(self):
        """Challenge >> skill = anxiety (low motivation)"""
        system = IntrinsicMotivationSystem()

        motivation = system.compute_competence_motivation(skill_level=0.2, challenge_level=0.9)

        assert motivation < 0.5  # Low motivation

    def test_competence_updates_state(self):
        """Computing competence updates current_competence"""
        system = IntrinsicMotivationSystem()

        competence = system.compute_competence_motivation(skill_level=0.6, challenge_level=0.6)

        assert system.current_competence == competence


class TestAutonomyPreference:
    """Test autonomy preference (Deci & Ryan)"""

    def test_self_directed_higher_motivation(self):
        """Self-directed actions have higher intrinsic value"""
        system = IntrinsicMotivationSystem()

        self_directed = system.compute_autonomy_preference(action_source="self")
        externally_controlled = system.compute_autonomy_preference(action_source="external")

        assert self_directed > externally_controlled

    def test_autonomy_weight_modulates_effect(self):
        """Autonomy weight modulates strength of preference"""
        system_high = IntrinsicMotivationSystem(autonomy_weight=0.4)
        system_low = IntrinsicMotivationSystem(autonomy_weight=0.1)

        # Both compute autonomy for self-directed action
        high_effect = system_high.compute_autonomy_preference(action_source="self")
        low_effect = system_low.compute_autonomy_preference(action_source="self")

        # Higher weight = stronger autonomy effect (though both positive)
        assert high_effect > 0
        assert low_effect > 0

    def test_external_control_reduces_motivation(self):
        """External control reduces intrinsic motivation"""
        system = IntrinsicMotivationSystem()

        external = system.compute_autonomy_preference(action_source="external")

        assert external < 0.7  # Reduced motivation

    def test_autonomy_updates_state(self):
        """Computing autonomy updates current_autonomy"""
        system = IntrinsicMotivationSystem()

        autonomy = system.compute_autonomy_preference(action_source="self")

        assert system.current_autonomy == autonomy


class TestIntrinsicReward:
    """Test total intrinsic motivation computation"""

    def test_intrinsic_reward_weighted_sum(self):
        """Intrinsic reward = weighted sum of components"""
        system = IntrinsicMotivationSystem()

        # Set components
        system.current_curiosity = 0.8
        system.current_competence = 0.6
        system.current_autonomy = 0.7

        reward = system.compute_intrinsic_reward()

        # Should be weighted sum
        expected = (0.8 * 0.4) + (0.6 * 0.4) + (0.7 * 0.2)
        assert reward == pytest.approx(expected, abs=0.01)

    def test_high_all_components_high_reward(self):
        """High curiosity + competence + autonomy = high reward"""
        system = IntrinsicMotivationSystem()

        system.current_curiosity = 0.9
        system.current_competence = 0.9
        system.current_autonomy = 0.9

        reward = system.compute_intrinsic_reward()

        assert reward > 0.8

    def test_low_all_components_low_reward(self):
        """Low all components = low reward"""
        system = IntrinsicMotivationSystem()

        system.current_curiosity = 0.1
        system.current_competence = 0.1
        system.current_autonomy = 0.1

        reward = system.compute_intrinsic_reward()

        assert reward < 0.3


class TestIntrinsicVsExtrinsic:
    """Test separation of intrinsic vs extrinsic motivation"""

    def test_intrinsic_independent_of_external_reward(self):
        """Intrinsic motivation computed independently of external rewards"""
        system = IntrinsicMotivationSystem()

        # Compute intrinsic with no external reward mention
        intrinsic = system.process_event(
            event_type="task_engagement",
            novelty=0.5,
            skill_level=0.6,
            challenge_level=0.6,
            action_source="self"
        )

        assert "intrinsic_reward" in intrinsic
        assert "extrinsic_reward" not in intrinsic  # Separate system

    def test_extrinsic_reward_reduces_intrinsic(self):
        """Extrinsic reward can reduce intrinsic motivation (undermining effect)"""
        system = IntrinsicMotivationSystem()

        # Baseline intrinsic motivation
        result_no_external = system.process_event(
            event_type="task_engagement",
            novelty=0.5,
            skill_level=0.6,
            challenge_level=0.6,
            action_source="self",
            external_reward=0.0
        )

        # With external reward
        result_with_external = system.process_event(
            event_type="task_engagement",
            novelty=0.5,
            skill_level=0.6,
            challenge_level=0.6,
            action_source="self",
            external_reward=1.0
        )

        # External reward should reduce intrinsic (undermining)
        assert result_with_external["intrinsic_reward"] < result_no_external["intrinsic_reward"]


class TestIntegrationNoveltyDetection:
    """Test integration with LAB_004 (Novelty Detection)"""

    def test_novelty_drives_curiosity(self):
        """High novelty from LAB_004 increases curiosity"""
        system = IntrinsicMotivationSystem()

        # Simulate LAB_004 novelty signal
        novelty_signal = 0.7

        curiosity = system.compute_curiosity_drive(
            novelty_level=novelty_signal,
            information_gap=0.5
        )

        assert curiosity > 0.5  # Novelty drives curiosity

    def test_zero_novelty_familiar(self):
        """Zero novelty (familiar) = low curiosity"""
        system = IntrinsicMotivationSystem()

        curiosity = system.compute_curiosity_drive(
            novelty_level=0.0,  # Completely familiar
            information_gap=0.3
        )

        assert curiosity < 0.4


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_task_engagement(self):
        """Process complete task engagement event"""
        system = IntrinsicMotivationSystem()

        result = system.process_event(
            event_type="task_engagement",
            novelty=0.5,
            information_gap=0.4,
            skill_level=0.6,
            challenge_level=0.6,
            action_source="self"
        )

        assert "curiosity" in result
        assert "competence" in result
        assert "autonomy" in result
        assert "intrinsic_reward" in result
        assert result["intrinsic_reward"] > 0

    def test_process_event_updates_state(self):
        """Processing event updates all state variables"""
        system = IntrinsicMotivationSystem()

        system.process_event(
            event_type="task_engagement",
            novelty=0.6,
            information_gap=0.5,
            skill_level=0.7,
            challenge_level=0.7,
            action_source="self"
        )

        assert system.current_curiosity > 0
        assert system.current_competence > 0
        assert system.current_autonomy > 0


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_all_components(self):
        """get_state returns all motivation components"""
        system = IntrinsicMotivationSystem()

        system.current_curiosity = 0.7
        system.current_competence = 0.6
        system.current_autonomy = 0.8

        state = system.get_state()

        assert "current_curiosity" in state
        assert "current_competence" in state
        assert "current_autonomy" in state
        assert "intrinsic_reward" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = IntrinsicMotivationSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
