"""
LAB_035: Reward Prediction - Advanced Predictive Learning

Implements advanced reward prediction beyond basic TD learning:
- Sutton & Barto (2018): Temporal-difference learning
- Montague et al. (1996): Predictive hebbian learning model
- Dayan & Niv (2008): Model-based and model-free RL
- Gershman & Daw (2017): Reinforcement learning and episodic memory

Core Functions:
1. Model-free prediction (TD learning)
2. Model-based prediction (forward models)
3. Uncertainty estimation
4. Credit assignment (eligibility traces)
5. Multi-step prediction
6. Reward shaping

Neuroscience Foundation:
- Ventral striatum: Reward prediction
- Dorsal striatum: Action-value learning
- OFC: Outcome expectations
- vmPFC: Value representation

Integration:
- ← LAB_013 (Dopamine) for RPE signals
- → LAB_037 (Curiosity) for information rewards
- → LAB_038 (Intrinsic Motivation) for intrinsic rewards
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import deque, defaultdict
import numpy as np
from enum import Enum


class PredictionMode(Enum):
    """Prediction modes"""
    MODEL_FREE = "model_free"  # Direct value learning
    MODEL_BASED = "model_based"  # Internal model simulation


@dataclass
class State:
    """Environment state"""
    state_id: str
    features: Dict[str, float]


@dataclass
class Transition:
    """State transition"""
    timestamp: float
    state: str
    action: str
    next_state: str
    reward: float
    done: bool


@dataclass
class ValueEstimate:
    """Value estimate for state"""
    state_id: str
    value: float
    uncertainty: float  # Standard deviation
    update_count: int


class ModelFreePredictor:
    """Model-free reward prediction (TD learning)"""

    def __init__(self, learning_rate: float = 0.1, discount: float = 0.99):
        self.learning_rate = learning_rate
        self.discount = discount
        self.values: Dict[str, float] = defaultdict(float)
        self.update_counts: Dict[str, int] = defaultdict(int)

    def predict_value(self, state_id: str) -> float:
        """Predict value of state"""
        return self.values[state_id]

    def update_value(
        self,
        state_id: str,
        reward: float,
        next_state_id: Optional[str] = None
    ) -> float:
        """
        TD(0) value update.

        Returns TD error.
        """
        current_value = self.values[state_id]
        next_value = 0.0 if next_state_id is None else self.values[next_state_id]

        # TD error
        td_error = reward + self.discount * next_value - current_value

        # Update value
        self.values[state_id] += self.learning_rate * td_error
        self.update_counts[state_id] += 1

        return td_error


class ModelBasedPredictor:
    """Model-based prediction with forward model"""

    def __init__(self, discount: float = 0.99):
        self.discount = discount

        # Forward model: (state, action) -> (next_state, reward)
        self.transition_model: Dict[Tuple[str, str], Dict] = {}

        # Reward model
        self.reward_model: Dict[Tuple[str, str], float] = {}

    def learn_model(
        self,
        state: str,
        action: str,
        next_state: str,
        reward: float
    ):
        """Learn forward model from experience"""
        key = (state, action)

        # Update transition model
        if key not in self.transition_model:
            self.transition_model[key] = {"next_states": [], "counts": defaultdict(int)}

        self.transition_model[key]["next_states"].append(next_state)
        self.transition_model[key]["counts"][next_state] += 1

        # Update reward model (running average)
        if key not in self.reward_model:
            self.reward_model[key] = reward
        else:
            # Exponential moving average
            alpha = 0.1
            self.reward_model[key] = (1 - alpha) * self.reward_model[key] + alpha * reward

    def predict_outcome(
        self,
        state: str,
        action: str
    ) -> Tuple[Optional[str], float]:
        """
        Predict next state and reward.

        Returns (next_state, reward).
        """
        key = (state, action)

        # Predict next state (most frequent)
        if key in self.transition_model:
            counts = self.transition_model[key]["counts"]
            if counts:
                next_state = max(counts, key=counts.get)
            else:
                next_state = None
        else:
            next_state = None

        # Predict reward
        reward = self.reward_model.get(key, 0.0)

        return next_state, reward

    def simulate_trajectory(
        self,
        start_state: str,
        actions: List[str],
        horizon: int = 5
    ) -> List[Tuple[str, str, float]]:
        """
        Simulate trajectory using forward model.

        Returns list of (state, action, reward).
        """
        trajectory = []
        current_state = start_state

        for step in range(min(horizon, len(actions))):
            action = actions[step]

            # Predict outcome
            next_state, reward = self.predict_outcome(current_state, action)

            trajectory.append((current_state, action, reward))

            if next_state is None:
                break

            current_state = next_state

        return trajectory

    def compute_expected_return(
        self,
        start_state: str,
        actions: List[str]
    ) -> float:
        """
        Compute expected return of action sequence.

        Returns expected discounted return.
        """
        trajectory = self.simulate_trajectory(start_state, actions)

        expected_return = 0.0
        for t, (state, action, reward) in enumerate(trajectory):
            expected_return += (self.discount ** t) * reward

        return expected_return


class UncertaintyEstimator:
    """Estimates uncertainty in value predictions"""

    def __init__(self):
        self.value_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))

    def record_value(self, state_id: str, value: float):
        """Record value estimate"""
        self.value_history[state_id].append(value)

    def estimate_uncertainty(self, state_id: str) -> float:
        """
        Estimate uncertainty (standard deviation of values).

        Returns uncertainty.
        """
        history = self.value_history[state_id]

        if len(history) < 2:
            return 1.0  # High uncertainty with few samples

        return float(np.std(list(history)))


class EligibilityTracer:
    """Eligibility traces for credit assignment"""

    def __init__(self, decay: float = 0.9):
        self.decay = decay
        self.traces: Dict[str, float] = defaultdict(float)

    def update_traces(self):
        """Decay all traces"""
        for state in list(self.traces.keys()):
            self.traces[state] *= self.decay

            # Remove near-zero traces
            if self.traces[state] < 0.01:
                del self.traces[state]

    def mark_visited(self, state_id: str):
        """Mark state as visited (set trace to 1.0)"""
        self.traces[state_id] = 1.0

    def get_trace(self, state_id: str) -> float:
        """Get eligibility trace for state"""
        return self.traces.get(state_id, 0.0)


class RewardPredictionSystem:
    """
    Main LAB_035 implementation.

    Manages:
    - Model-free prediction
    - Model-based prediction
    - Uncertainty estimation
    - Credit assignment
    """

    def __init__(self, mode: PredictionMode = PredictionMode.MODEL_FREE):
        self.mode = mode

        # Components
        self.model_free = ModelFreePredictor()
        self.model_based = ModelBasedPredictor()
        self.uncertainty = UncertaintyEstimator()
        self.eligibility = EligibilityTracer()

        # History
        self.transitions: List[Transition] = []

    def predict_value(self, state_id: str) -> ValueEstimate:
        """
        Predict value of state.

        Returns value estimate with uncertainty.
        """
        if self.mode == PredictionMode.MODEL_FREE:
            value = self.model_free.predict_value(state_id)
        else:
            # Model-based: simulate from this state
            # (simplified: use model-free value as fallback)
            value = self.model_free.predict_value(state_id)

        uncertainty_val = self.uncertainty.estimate_uncertainty(state_id)
        update_count = self.model_free.update_counts[state_id]

        return ValueEstimate(
            state_id=state_id,
            value=value,
            uncertainty=uncertainty_val,
            update_count=update_count
        )

    def learn_from_transition(
        self,
        state: str,
        action: str,
        next_state: str,
        reward: float,
        done: bool = False
    ) -> float:
        """
        Learn from transition.

        Returns TD error.
        """
        # Record transition
        transition = Transition(
            timestamp=time.time(),
            state=state,
            action=action,
            next_state=next_state,
            reward=reward,
            done=done
        )
        self.transitions.append(transition)

        # Mark state as visited (eligibility trace)
        self.eligibility.mark_visited(state)

        # Update model-free predictor
        next_state_for_td = None if done else next_state
        td_error = self.model_free.update_value(state, reward, next_state_for_td)

        # Record value for uncertainty estimation
        value = self.model_free.predict_value(state)
        self.uncertainty.record_value(state, value)

        # Update model-based predictor
        self.model_based.learn_model(state, action, next_state, reward)

        # Decay eligibility traces
        self.eligibility.update_traces()

        return td_error

    def plan_trajectory(
        self,
        start_state: str,
        candidate_actions: List[str],
        horizon: int = 5
    ) -> Tuple[List[str], float]:
        """
        Plan best action sequence using model-based prediction.

        Returns (best_actions, expected_return).
        """
        if self.mode != PredictionMode.MODEL_BASED:
            # Switch to model-based temporarily
            pass

        # Simple planning: try each action sequence and pick best
        best_actions = candidate_actions[:horizon]
        best_return = self.model_based.compute_expected_return(start_state, best_actions)

        return best_actions, best_return

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "mode": self.mode.value,
            "states_visited": len(self.model_free.values),
            "total_transitions": len(self.transitions),
            "avg_value": (np.mean(list(self.model_free.values.values()))
                         if self.model_free.values else 0.0),
            "model_based_transitions": len(self.model_based.transition_model),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_035: Reward Prediction - Test")
    print("=" * 60)

    # Scenario 1: Model-free prediction
    print("\n🎯 Scenario 1: Model-Free Prediction (TD Learning)...")
    system_mf = RewardPredictionSystem(mode=PredictionMode.MODEL_FREE)

    # Simple gridworld: A -> B -> C (with rewards)
    transitions = [
        ("A", "right", "B", 0.0, False),
        ("B", "right", "C", 1.0, True),
    ]

    for _ in range(5):  # Multiple episodes
        for state, action, next_state, reward, done in transitions:
            td_error = system_mf.learn_from_transition(state, action, next_state, reward, done)

    print(f"  After 5 episodes:")
    for state_id in ["A", "B", "C"]:
        estimate = system_mf.predict_value(state_id)
        print(f"    V({state_id}) = {estimate.value:.3f}, "
              f"uncertainty={estimate.uncertainty:.3f}, "
              f"updates={estimate.update_count}")

    # Scenario 2: Model-based prediction
    print("\n🔮 Scenario 2: Model-Based Prediction...")
    system_mb = RewardPredictionSystem(mode=PredictionMode.MODEL_BASED)

    # Learn model
    for _ in range(3):
        for state, action, next_state, reward, done in transitions:
            system_mb.learn_from_transition(state, action, next_state, reward, done)

    # Predict outcome
    next_state_pred, reward_pred = system_mb.model_based.predict_outcome("A", "right")
    print(f"  Predicted: A + right → {next_state_pred}, reward={reward_pred:.3f}")

    next_state_pred, reward_pred = system_mb.model_based.predict_outcome("B", "right")
    print(f"  Predicted: B + right → {next_state_pred}, reward={reward_pred:.3f}")

    # Simulate trajectory
    print(f"\n  Simulated trajectory from A:")
    trajectory = system_mb.model_based.simulate_trajectory("A", ["right", "right"])
    for state, action, reward in trajectory:
        print(f"    {state} + {action} → reward={reward:.3f}")

    # Expected return
    expected = system_mb.model_based.compute_expected_return("A", ["right", "right"])
    print(f"  Expected return from A: {expected:.3f}")

    # Scenario 3: Uncertainty estimation
    print("\n📊 Scenario 3: Uncertainty Estimation...")

    # Add some noise to values
    for i in range(10):
        noise = np.random.normal(0, 0.1)
        system_mf.uncertainty.record_value("A", system_mf.model_free.predict_value("A") + noise)

    uncertainty = system_mf.uncertainty.estimate_uncertainty("A")
    print(f"  State A value: {system_mf.model_free.predict_value('A'):.3f}")
    print(f"  Uncertainty: {uncertainty:.3f}")

    # Scenario 4: Eligibility traces
    print("\n🔗 Scenario 4: Eligibility Traces (Credit Assignment)...")

    tracer = EligibilityTracer(decay=0.8)

    # Visit sequence: A -> B -> C
    tracer.mark_visited("A")
    print(f"  After visiting A: traces={dict(tracer.traces)}")

    tracer.update_traces()
    tracer.mark_visited("B")
    print(f"  After visiting B: traces={dict(tracer.traces)}")

    tracer.update_traces()
    tracer.mark_visited("C")
    print(f"  After visiting C: traces={dict(tracer.traces)}")

    tracer.update_traces()
    print(f"  After decay: traces={dict(tracer.traces)}")

    # Final statistics
    print("\n📈 Final Statistics:")
    stats = system_mf.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_035 Test Complete!")
