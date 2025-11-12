"""
LAB_035: Reward Prediction Error - Unit Tests

Homeostasis: "Learning what matters & motivation"

Key Papers:
- Schultz et al. (1997) - Dopamine neurons: reward prediction error
- Sutton & Barto (1998) - Reinforcement Learning
- Montague et al. (2004) - Computational psychiatry of RPE
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_035_Reward_Prediction_Error.reward_prediction_error_system import (
    RewardPredictionErrorSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default RPE parameters"""
        system = RewardPredictionErrorSystem()
        assert system.learning_rate == 0.3
        assert len(system.value_estimates) == 0

    def test_custom_learning_rate(self):
        """System accepts custom learning rate"""
        system = RewardPredictionErrorSystem(learning_rate=0.05)
        assert system.learning_rate == 0.05

    def test_custom_discount_factor(self):
        """System accepts custom discount factor (gamma)"""
        system = RewardPredictionErrorSystem(discount_factor=0.95)
        assert system.discount_factor == 0.95


class TestRewardPrediction:
    """Test reward prediction mechanism"""

    def test_initial_state_zero_prediction(self):
        """New state → zero value prediction"""
        system = RewardPredictionErrorSystem()

        prediction = system.predict_value(state="new_state")

        assert prediction == 0.0

    def test_experienced_state_returns_learned_value(self):
        """Previously seen state → returns learned value"""
        system = RewardPredictionErrorSystem()

        # Learn value
        system.value_estimates["state_A"] = 0.8

        prediction = system.predict_value(state="state_A")

        assert prediction == 0.8

    def test_prediction_stored_in_cache(self):
        """Predictions stored for fast lookup"""
        system = RewardPredictionErrorSystem()

        system.predict_value(state="state_X")

        assert "state_X" in system.value_estimates

    def test_prediction_bounded(self):
        """Value predictions bounded [0-1]"""
        system = RewardPredictionErrorSystem()
        system.value_estimates["state_B"] = 1.5  # Invalid

        # Should still return bounded value
        assert system.predict_value(state="state_B") <= 1.0


class TestPredictionError:
    """Test reward prediction error (RPE) computation"""

    def test_positive_rpe_better_than_expected(self):
        """Actual > Expected → Positive RPE (dopamine burst)"""
        system = RewardPredictionErrorSystem()

        # Expect low reward
        system.value_estimates["state_A"] = 0.3

        # Get high reward
        result = system.compute_prediction_error(
            state="state_A",
            actual_reward=0.8
        )

        assert result["prediction_error"] > 0
        assert result["dopamine_signal"] == "burst"

    def test_negative_rpe_worse_than_expected(self):
        """Actual < Expected → Negative RPE (dopamine dip)"""
        system = RewardPredictionErrorSystem()

        # Expect high reward
        system.value_estimates["state_B"] = 0.9

        # Get low reward
        result = system.compute_prediction_error(
            state="state_B",
            actual_reward=0.2
        )

        assert result["prediction_error"] < 0
        assert result["dopamine_signal"] == "dip"

    def test_zero_rpe_as_expected(self):
        """Actual = Expected → Zero RPE (dopamine baseline)"""
        system = RewardPredictionErrorSystem()

        system.value_estimates["state_C"] = 0.7

        result = system.compute_prediction_error(
            state="state_C",
            actual_reward=0.7
        )

        assert abs(result["prediction_error"]) < 0.01
        assert result["dopamine_signal"] == "baseline"

    def test_rpe_magnitude(self):
        """RPE magnitude = |actual - expected|"""
        system = RewardPredictionErrorSystem()

        system.value_estimates["state_D"] = 0.5

        result = system.compute_prediction_error(
            state="state_D",
            actual_reward=0.9
        )

        assert abs(result["prediction_error"] - 0.4) < 0.01


class TestValueUpdate:
    """Test value function update (TD learning)"""

    def test_positive_rpe_increases_value(self):
        """Positive RPE → Increase value estimate"""
        system = RewardPredictionErrorSystem()

        system.value_estimates["state_A"] = 0.3

        # Get positive RPE
        system.update_value(state="state_A", actual_reward=0.8)

        assert system.value_estimates["state_A"] > 0.3

    def test_negative_rpe_decreases_value(self):
        """Negative RPE → Decrease value estimate"""
        system = RewardPredictionErrorSystem()

        system.value_estimates["state_B"] = 0.9

        # Get negative RPE
        system.update_value(state="state_B", actual_reward=0.2)

        assert system.value_estimates["state_B"] < 0.9

    def test_learning_rate_controls_update_speed(self):
        """Higher learning rate → faster value updates"""
        system1 = RewardPredictionErrorSystem(learning_rate=0.01)
        system2 = RewardPredictionErrorSystem(learning_rate=0.5)

        system1.value_estimates["state_A"] = 0.5
        system2.value_estimates["state_A"] = 0.5

        system1.update_value(state="state_A", actual_reward=1.0)
        system2.update_value(state="state_A", actual_reward=1.0)

        assert abs(system2.value_estimates["state_A"] - 0.5) > abs(system1.value_estimates["state_A"] - 0.5)

    def test_td_learning_formula(self):
        """V(s) ← V(s) + α * [R - V(s)]"""
        system = RewardPredictionErrorSystem(learning_rate=0.1)

        system.value_estimates["state_A"] = 0.5

        # R = 0.8, V(s) = 0.5, α = 0.1
        # V_new = 0.5 + 0.1 * (0.8 - 0.5) = 0.5 + 0.03 = 0.53
        system.update_value(state="state_A", actual_reward=0.8)

        expected_value = 0.5 + 0.1 * (0.8 - 0.5)
        assert abs(system.value_estimates["state_A"] - expected_value) < 0.01


class TestDopamineSignal:
    """Test dopamine modulation"""

    def test_large_positive_rpe_strong_burst(self):
        """Large positive RPE → Strong dopamine burst"""
        system = RewardPredictionErrorSystem()

        system.value_estimates["state_A"] = 0.1

        result = system.compute_prediction_error(
            state="state_A",
            actual_reward=0.9
        )

        assert result["dopamine_magnitude"] > 0.5

    def test_small_rpe_weak_signal(self):
        """Small RPE → Weak dopamine signal"""
        system = RewardPredictionErrorSystem()

        system.value_estimates["state_B"] = 0.5

        result = system.compute_prediction_error(
            state="state_B",
            actual_reward=0.52
        )

        assert result["dopamine_magnitude"] < 0.1

    def test_dopamine_drives_learning(self):
        """Dopamine signal strength correlates with learning"""
        system = RewardPredictionErrorSystem()

        system.value_estimates["state_A"] = 0.5

        # Strong dopamine signal
        result = system.compute_prediction_error(
            state="state_A",
            actual_reward=1.0
        )

        assert result["dopamine_magnitude"] > 0.3
        assert result["learning_signal"] == "strong"


class TestTemporalDifference:
    """Test temporal difference learning"""

    def test_multi_step_learning(self):
        """TD learning across multiple timesteps"""
        system = RewardPredictionErrorSystem()

        # Timestep 1: Low reward
        system.update_value(state="state_A", actual_reward=0.2)

        # Timestep 2: Higher reward
        system.update_value(state="state_A", actual_reward=0.6)

        # Value should converge towards 0.6
        assert system.value_estimates["state_A"] > 0.2

    def test_discount_factor_affects_future_reward(self):
        """Discount factor (gamma) weights future rewards"""
        system = RewardPredictionErrorSystem(discount_factor=0.9)

        # With discounting, future rewards valued less
        result = system.update_value_td(
            state="state_A",
            reward=0.5,
            next_state="state_B",
            next_state_value=0.8
        )

        # TD target = reward + gamma * V(s')
        # TD target = 0.5 + 0.9 * 0.8 = 1.22 (capped at 1.0)
        assert result["td_target"] > 0.5

    def test_td_error_drives_update(self):
        """TD error = [R + γV(s')] - V(s)"""
        system = RewardPredictionErrorSystem(learning_rate=0.1, discount_factor=0.9)

        system.value_estimates["state_A"] = 0.3
        system.value_estimates["state_B"] = 0.7

        result = system.update_value_td(
            state="state_A",
            reward=0.5,
            next_state="state_B",
            next_state_value=0.7
        )

        # TD target = 0.5 + 0.9 * 0.7 = 1.13 (capped)
        # TD error = 1.0 - 0.3 = 0.7
        assert result["td_error"] > 0

    def test_convergence_with_consistent_rewards(self):
        """Consistent rewards → Value converges"""
        system = RewardPredictionErrorSystem(learning_rate=0.2)

        # Repeat same reward 10 times
        for _ in range(10):
            system.update_value(state="state_A", actual_reward=0.7)

        # Should converge close to 0.7
        assert abs(system.value_estimates["state_A"] - 0.7) < 0.1


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_habit_formation(self):
        """LAB_036: Strong positive RPE strengthens habits"""
        system = RewardPredictionErrorSystem()

        result = system.compute_prediction_error(
            state="habit_action",
            actual_reward=0.9
        )

        # Positive RPE signals habit reinforcement
        assert result["prediction_error"] > 0
        assert result.get("habit_signal", None) == "strengthen"

    def test_integration_with_skill_acquisition(self):
        """LAB_040: RPE guides skill learning"""
        system = RewardPredictionErrorSystem()

        # During skill practice
        result = system.compute_prediction_error(
            state="skill_practice",
            actual_reward=0.8
        )

        # Positive RPE indicates progress
        assert result["learning_signal"] in ["moderate", "strong"]

    def test_integration_with_motivation(self):
        """RPE drives motivation and exploration"""
        system = RewardPredictionErrorSystem()

        # Unexpected high reward
        result = system.compute_prediction_error(
            state="new_action",
            actual_reward=1.0
        )

        # Should signal high motivation
        assert result["dopamine_magnitude"] > 0.5


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_reward_event(self):
        """Process reward observation event"""
        system = RewardPredictionErrorSystem()

        result = system.process_event(
            event_type="reward_observation",
            state="state_A",
            reward=0.8
        )

        assert "prediction_error" in result

    def test_process_prediction_event(self):
        """Process value prediction event"""
        system = RewardPredictionErrorSystem()

        result = system.process_event(
            event_type="predict_value",
            state="state_B"
        )

        assert "predicted_value" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_rpe_metrics(self):
        """get_state returns RPE system metrics"""
        system = RewardPredictionErrorSystem()

        system.update_value(state="state_A", actual_reward=0.7)

        state = system.get_state()

        assert "total_states" in state
        assert "learning_rate" in state
        assert "average_value" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = RewardPredictionErrorSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
