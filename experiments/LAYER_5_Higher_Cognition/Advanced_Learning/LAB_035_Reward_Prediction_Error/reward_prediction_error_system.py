"""
LAB_035: Reward Prediction Error System

Homeostasis: "Learning what matters & motivation"

Key Mechanisms:
- Dopamine RPE: δ = R - V(s) (actual - expected reward)
- Temporal difference learning: V(s) ← V(s) + α * δ
- Positive RPE: Better than expected (dopamine burst)
- Negative RPE: Worse than expected (dopamine dip)
- Zero RPE: As expected (dopamine baseline)

Mathematical Model:
- Prediction error: δ = R - V(s)
- Value update: V(s) ← V(s) + α * δ
- TD error: δ = R + γV(s') - V(s)
- Dopamine signal: ∝ |δ|

Key Papers:
- Schultz et al. (1997): Dopamine neurons signal reward prediction error
- Sutton & Barto (1998): Reinforcement Learning
- Montague et al. (2004): Computational psychiatry of RPE
"""

import math
from typing import Dict, Optional


class RewardPredictionErrorSystem:
    """
    Reward Prediction Error: Learning what matters

    Core principle: Dopamine signals prediction errors, drives learning

    Implements:
    - Value prediction (expected reward)
    - Prediction error computation (δ = R - V)
    - Temporal difference learning (TD)
    - Dopamine signal modulation
    """

    def __init__(
        self,
        learning_rate: float = 0.3,
        discount_factor: float = 0.9
    ):
        """
        Initialize Reward Prediction Error System

        Args:
            learning_rate: Learning rate (alpha) [0-1]
            discount_factor: Discount factor (gamma) for future rewards [0-1]
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        # Value estimates: V(s) for each state
        self.value_estimates: Dict[str, float] = {}

        # RPE history (for analysis)
        self.rpe_history: list = []

    def predict_value(
        self,
        state: str
    ) -> float:
        """
        Predict expected reward for state

        Args:
            state: State identifier

        Returns:
            Expected value V(s) [0-1]
        """
        # Initialize unseen states to zero
        if state not in self.value_estimates:
            self.value_estimates[state] = 0.0

        return min(1.0, max(0.0, self.value_estimates[state]))

    def compute_prediction_error(
        self,
        state: str,
        actual_reward: float
    ) -> Dict:
        """
        Compute reward prediction error (RPE)

        Args:
            state: Current state
            actual_reward: Actual reward received [0-1]

        Returns:
            RPE result with dopamine signal
        """
        # Get predicted value
        predicted_value = self.predict_value(state)

        # Compute prediction error: δ = R - V(s)
        prediction_error = actual_reward - predicted_value

        # Determine dopamine signal
        if prediction_error > 0.1:
            dopamine_signal = "burst"
            learning_signal = "strong" if prediction_error > 0.3 else "moderate"
        elif prediction_error < -0.1:
            dopamine_signal = "dip"
            learning_signal = "strong" if prediction_error < -0.3 else "moderate"
        else:
            dopamine_signal = "baseline"
            learning_signal = "weak"

        # Dopamine magnitude (absolute prediction error)
        dopamine_magnitude = abs(prediction_error)

        # Habit signal integration (LAB_036)
        if prediction_error > 0.3:
            habit_signal = "strengthen"
        elif prediction_error < -0.3:
            habit_signal = "weaken"
        else:
            habit_signal = "maintain"

        return {
            "state": state,
            "predicted_value": float(predicted_value),
            "actual_reward": float(actual_reward),
            "prediction_error": float(prediction_error),
            "dopamine_signal": dopamine_signal,
            "dopamine_magnitude": float(dopamine_magnitude),
            "learning_signal": learning_signal,
            "habit_signal": habit_signal
        }

    def update_value(
        self,
        state: str,
        actual_reward: float
    ) -> Dict:
        """
        Update value estimate using prediction error

        Args:
            state: State identifier
            actual_reward: Actual reward received [0-1]

        Returns:
            Update result
        """
        # Get current value
        current_value = self.predict_value(state)

        # Compute prediction error
        prediction_error = actual_reward - current_value

        # TD learning: V(s) ← V(s) + α * δ
        new_value = current_value + self.learning_rate * prediction_error

        # Bound value [0, 1]
        new_value = min(1.0, max(0.0, new_value))

        # Update value estimate
        self.value_estimates[state] = new_value

        # Record RPE
        self.rpe_history.append({
            "state": state,
            "prediction_error": prediction_error,
            "old_value": current_value,
            "new_value": new_value
        })

        return {
            "state": state,
            "old_value": float(current_value),
            "new_value": float(new_value),
            "prediction_error": float(prediction_error)
        }

    def update_value_td(
        self,
        state: str,
        reward: float,
        next_state: str,
        next_state_value: float
    ) -> Dict:
        """
        Update value using temporal difference (TD) learning

        Args:
            state: Current state
            reward: Immediate reward
            next_state: Next state
            next_state_value: Value of next state V(s')

        Returns:
            TD update result
        """
        # Get current value
        current_value = self.predict_value(state)

        # TD target: R + γV(s')
        td_target = reward + self.discount_factor * next_state_value

        # Bound TD target
        td_target = min(1.0, max(0.0, td_target))

        # TD error: δ = [R + γV(s')] - V(s)
        td_error = td_target - current_value

        # Update: V(s) ← V(s) + α * δ
        new_value = current_value + self.learning_rate * td_error

        # Bound value
        new_value = min(1.0, max(0.0, new_value))

        # Update value estimate
        self.value_estimates[state] = new_value

        return {
            "state": state,
            "td_target": float(td_target),
            "td_error": float(td_error),
            "old_value": float(current_value),
            "new_value": float(new_value)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process RPE event

        Args:
            event_type: Type of event ("reward_observation", "predict_value", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "reward_observation":
            # Compute RPE and update value
            rpe_result = self.compute_prediction_error(
                state=kwargs["state"],
                actual_reward=kwargs["reward"]
            )

            # Update value
            self.update_value(
                state=kwargs["state"],
                actual_reward=kwargs["reward"]
            )

            return rpe_result

        elif event_type == "predict_value":
            predicted_value = self.predict_value(state=kwargs["state"])
            return {
                "predicted_value": float(predicted_value)
            }

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of RPE system

        Returns:
            System state with RPE metrics
        """
        if len(self.value_estimates) == 0:
            return {
                "total_states": 0,
                "learning_rate": self.learning_rate,
                "discount_factor": self.discount_factor,
                "average_value": 0.0,
                "rpe_history_length": 0
            }

        # Compute average value
        average_value = sum(self.value_estimates.values()) / len(self.value_estimates)

        # Recent RPE statistics
        recent_rpe = self.rpe_history[-10:] if len(self.rpe_history) > 0 else []
        if len(recent_rpe) > 0:
            avg_recent_rpe = sum(abs(r["prediction_error"]) for r in recent_rpe) / len(recent_rpe)
        else:
            avg_recent_rpe = 0.0

        return {
            "total_states": len(self.value_estimates),
            "learning_rate": self.learning_rate,
            "discount_factor": self.discount_factor,
            "average_value": float(average_value),
            "rpe_history_length": len(self.rpe_history),
            "avg_recent_rpe": float(avg_recent_rpe)
        }
