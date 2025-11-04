"""
LAB_013: Dopamine System - Reward Prediction Error & Motivation

Implements biological dopaminergic signaling based on:
- Schultz et al. (1997): Dopamine neurons encode reward prediction errors
- Berridge & Robinson (2003): Wanting vs Liking dissociation
- Montague et al. (1996): Temporal difference learning in dopamine

Core Functions:
1. Reward Prediction Error (RPE) computation
2. Learning rate modulation based on RPE magnitude
3. Motivation/drive system (tonic dopamine baseline)
4. Phasic dopamine bursts for salient events
5. Integration with novelty detection (LAB_004)

Neuroscience Foundation:
- VTA (Ventral Tegmental Area): Reward prediction
- Substantia Nigra: Motor learning, habits
- Striatum: Action selection based on reward expectation
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class DopamineMode(Enum):
    """Dopamine release modes"""
    TONIC = "tonic"      # Baseline sustained release
    PHASIC = "phasic"    # Burst firing for salient events


@dataclass
class RewardExpectation:
    """Tracks expected reward for a context/state"""
    context_id: str
    expected_value: float
    confidence: float
    last_updated: float
    update_count: int = 0
    prediction_errors: List[float] = field(default_factory=list)


@dataclass
class DopamineSignal:
    """Dopamine release event"""
    timestamp: float
    mode: DopamineMode
    level: float  # Normalized 0-1
    rpe: Optional[float] = None  # Reward prediction error
    source: str = "unknown"
    context_id: Optional[str] = None


@dataclass
class MotivationalState:
    """Current motivational/drive state"""
    baseline_dopamine: float  # Tonic level (0-1)
    current_dopamine: float   # Current level including phasic
    motivation: float         # Drive to seek reward (0-1)
    learning_rate: float      # Modulated by RPE (0-1)
    curiosity_drive: float    # Exploration bonus (0-1)
    last_reward_time: float
    reward_deficit: float     # Time since last reward


class RewardPredictionEngine:
    """
    Implements temporal difference (TD) learning for reward prediction.
    Learns to predict future rewards from current state/context.
    """

    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95):
        self.base_learning_rate = learning_rate
        self.discount_factor = discount_factor  # γ in TD learning

        # Store value predictions for different contexts
        self.value_table: Dict[str, RewardExpectation] = {}

        # RPE history for analysis
        self.rpe_history: deque = deque(maxlen=1000)

    def get_expected_value(self, context_id: str) -> float:
        """Get expected reward value for a context"""
        if context_id not in self.value_table:
            return 0.0
        return self.value_table[context_id].expected_value

    def compute_rpe(
        self,
        context_id: str,
        actual_reward: float,
        next_context_id: Optional[str] = None
    ) -> float:
        """
        Compute Reward Prediction Error (RPE) using TD learning.

        RPE = r(t) + γ * V(s_{t+1}) - V(s_t)

        where:
        - r(t) = actual reward received
        - γ = discount factor
        - V(s_{t+1}) = expected value of next state
        - V(s_t) = expected value of current state
        """
        current_value = self.get_expected_value(context_id)

        # Get next state value (0 if terminal state)
        next_value = 0.0
        if next_context_id:
            next_value = self.get_expected_value(next_context_id)

        # TD error: δ = r + γV(s') - V(s)
        rpe = actual_reward + (self.discount_factor * next_value) - current_value

        # Store RPE in history
        self.rpe_history.append({
            "timestamp": time.time(),
            "context_id": context_id,
            "rpe": rpe,
            "actual_reward": actual_reward,
            "expected_value": current_value
        })

        return rpe

    def update_value(
        self,
        context_id: str,
        rpe: float,
        learning_rate: Optional[float] = None
    ):
        """
        Update value prediction using RPE.

        V(s) ← V(s) + α * RPE
        """
        lr = learning_rate if learning_rate is not None else self.base_learning_rate

        if context_id not in self.value_table:
            self.value_table[context_id] = RewardExpectation(
                context_id=context_id,
                expected_value=0.0,
                confidence=0.0,
                last_updated=time.time()
            )

        expectation = self.value_table[context_id]

        # Update value: V ← V + α * δ
        expectation.expected_value += lr * rpe

        # Update metadata
        expectation.last_updated = time.time()
        expectation.update_count += 1
        expectation.prediction_errors.append(rpe)

        # Keep only recent errors
        if len(expectation.prediction_errors) > 100:
            expectation.prediction_errors = expectation.prediction_errors[-100:]

        # Update confidence based on prediction stability
        if len(expectation.prediction_errors) >= 10:
            recent_errors = expectation.prediction_errors[-10:]
            error_variance = np.var(recent_errors)
            # High variance = low confidence
            expectation.confidence = 1.0 / (1.0 + error_variance)
        else:
            # Low confidence with few samples
            expectation.confidence = expectation.update_count / 10.0

    def get_prediction_stability(self, context_id: str) -> float:
        """Get how stable predictions are for this context (0-1)"""
        if context_id not in self.value_table:
            return 0.0

        expectation = self.value_table[context_id]
        return expectation.confidence


class DopamineSystem:
    """
    Main LAB_013 implementation.

    Manages dopaminergic signaling including:
    - Tonic baseline dopamine levels
    - Phasic dopamine bursts from RPE
    - Learning rate modulation
    - Motivation and drive
    """

    def __init__(
        self,
        baseline_dopamine: float = 0.5,
        rpe_gain: float = 2.0,
        decay_half_life: float = 5.0,
        novelty_bonus: float = 0.3
    ):
        # Core parameters
        self.baseline_dopamine = baseline_dopamine  # Tonic level
        self.rpe_gain = rpe_gain  # How much RPE affects phasic dopamine
        self.decay_half_life = decay_half_life  # Phasic dopamine decay (seconds)
        self.novelty_bonus = novelty_bonus  # Bonus from novel stimuli

        # Reward prediction engine
        self.predictor = RewardPredictionEngine()

        # Current state
        self.current_dopamine = baseline_dopamine
        self.last_update_time = time.time()
        self.last_reward_time = time.time()

        # Dopamine release history
        self.release_history: deque = deque(maxlen=1000)

        # Statistics
        self.total_rpe_events = 0
        self.positive_rpes = 0
        self.negative_rpes = 0

    def process_event(
        self,
        context_id: str,
        actual_reward: float,
        novelty_score: float = 0.0,
        next_context_id: Optional[str] = None
    ) -> Tuple[float, DopamineSignal]:
        """
        Process a reward/event and compute dopamine response.

        Returns:
            - RPE value
            - Dopamine signal generated
        """
        # Compute RPE
        rpe = self.predictor.compute_rpe(context_id, actual_reward, next_context_id)

        # Add novelty bonus to effective RPE (dopamine responds to novelty)
        effective_rpe = rpe + (novelty_score * self.novelty_bonus)

        # Compute dopamine release
        # Positive RPE → phasic burst
        # Negative RPE → dip below baseline
        phasic_delta = self.rpe_gain * effective_rpe

        # Dopamine cannot go below 0
        new_dopamine = max(0.0, min(1.0, self.baseline_dopamine + phasic_delta))

        # Create dopamine signal
        signal = DopamineSignal(
            timestamp=time.time(),
            mode=DopamineMode.PHASIC,
            level=new_dopamine,
            rpe=rpe,
            source="reward_event",
            context_id=context_id
        )

        # Update state
        self.current_dopamine = new_dopamine
        self.last_update_time = time.time()

        if actual_reward > 0:
            self.last_reward_time = time.time()

        # Record signal
        self.release_history.append(signal)

        # Update value prediction using modulated learning rate
        learning_rate = self.compute_learning_rate(abs(rpe))
        self.predictor.update_value(context_id, rpe, learning_rate)

        # Update statistics
        self.total_rpe_events += 1
        if rpe > 0:
            self.positive_rpes += 1
        elif rpe < 0:
            self.negative_rpes += 1

        return rpe, signal

    def compute_learning_rate(self, rpe_magnitude: float) -> float:
        """
        Modulate learning rate based on RPE magnitude.
        Larger errors → higher learning rate (faster adaptation)

        Based on: Pearce & Hall (1980) - Attention & associability
        """
        # Sigmoid mapping: large RPE → high learning rate
        # Small RPE → low learning rate (predictions are good)
        base_lr = self.predictor.base_learning_rate

        # Scale RPE magnitude to learning rate boost
        # α = α_base * (1 + tanh(|RPE|))
        boost = 1.0 + np.tanh(rpe_magnitude)

        return base_lr * boost

    def get_current_dopamine(self) -> float:
        """
        Get current dopamine level with decay applied.
        Phasic dopamine decays back to tonic baseline.
        """
        elapsed = time.time() - self.last_update_time

        # Exponential decay toward baseline
        # D(t) = D_baseline + (D_current - D_baseline) * exp(-λt)
        decay_rate = np.log(2) / self.decay_half_life

        delta_from_baseline = self.current_dopamine - self.baseline_dopamine
        decayed_delta = delta_from_baseline * np.exp(-decay_rate * elapsed)

        current = self.baseline_dopamine + decayed_delta

        return current

    def get_motivation_level(self) -> float:
        """
        Compute current motivation/drive level.

        High when:
        - Dopamine is elevated (recent reward)
        - It's been a while since last reward (deficit)
        - Recent positive RPEs (learning opportunities)
        """
        # Current dopamine contributes to motivation
        dopamine_factor = self.get_current_dopamine()

        # Time since last reward creates deficit/drive
        time_since_reward = time.time() - self.last_reward_time
        # Increases over time, saturates at ~60 seconds
        deficit_factor = min(1.0, time_since_reward / 60.0)

        # Recent positive RPEs indicate learning opportunities
        recent_rpes = [
            entry.rpe for entry in list(self.release_history)[-10:]
            if entry.rpe is not None
        ]

        if recent_rpes:
            avg_rpe = np.mean(recent_rpes)
            rpe_factor = max(0.0, avg_rpe)  # Only positive RPEs motivate
        else:
            rpe_factor = 0.0

        # Combine factors
        # motivation = dopamine * (1 + deficit) + rpe_bonus
        motivation = dopamine_factor * (1.0 + deficit_factor * 0.5) + rpe_factor * 0.3

        return min(1.0, motivation)

    def get_curiosity_drive(self, novelty_score: float) -> float:
        """
        Compute curiosity/exploration drive.

        Novelty + moderate dopamine → exploration
        Low dopamine → exploitation (seek known rewards)
        """
        dopamine = self.get_current_dopamine()

        # Sweet spot: moderate dopamine + novelty
        # Too low dopamine → need guaranteed reward (exploit)
        # High dopamine → already satisfied

        # Inverted U-curve for dopamine effect
        dopamine_modulation = 4 * dopamine * (1 - dopamine)

        curiosity = novelty_score * dopamine_modulation

        return curiosity

    def get_motivational_state(self) -> MotivationalState:
        """Get complete motivational state snapshot"""
        current_dopamine = self.get_current_dopamine()

        return MotivationalState(
            baseline_dopamine=self.baseline_dopamine,
            current_dopamine=current_dopamine,
            motivation=self.get_motivation_level(),
            learning_rate=self.compute_learning_rate(
                abs(self.predictor.rpe_history[-1]["rpe"])
                if self.predictor.rpe_history else 0.0
            ),
            curiosity_drive=self.get_curiosity_drive(0.5),  # Placeholder
            last_reward_time=self.last_reward_time,
            reward_deficit=time.time() - self.last_reward_time
        )

    def get_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        recent_rpes = [
            entry["rpe"] for entry in list(self.predictor.rpe_history)
            if entry["rpe"] is not None
        ]

        return {
            "total_rpe_events": self.total_rpe_events,
            "positive_rpes": self.positive_rpes,
            "negative_rpes": self.negative_rpes,
            "baseline_dopamine": self.baseline_dopamine,
            "current_dopamine": self.get_current_dopamine(),
            "motivation_level": self.get_motivation_level(),
            "contexts_learned": len(self.predictor.value_table),
            "avg_rpe": np.mean(recent_rpes) if recent_rpes else 0.0,
            "rpe_variance": np.var(recent_rpes) if recent_rpes else 0.0,
            "time_since_last_reward": time.time() - self.last_reward_time,
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_013: Dopamine System - Test")
    print("=" * 60)

    # Create dopamine system
    dopamine = DopamineSystem(
        baseline_dopamine=0.5,
        rpe_gain=2.0,
        decay_half_life=5.0
    )

    print("\n📊 Simulating reward learning scenario...")

    # Scenario: Learning to predict reward in context "task_complete"
    context = "task_complete"

    # Trial 1: Unexpected reward (positive RPE)
    print(f"\n🎯 Trial 1: Unexpected reward")
    rpe, signal = dopamine.process_event(
        context_id=context,
        actual_reward=1.0,
        novelty_score=0.8
    )
    print(f"  RPE: {rpe:+.3f}")
    print(f"  Dopamine: {signal.level:.3f}")
    print(f"  Motivation: {dopamine.get_motivation_level():.3f}")

    # Wait a bit
    time.sleep(1)

    # Trial 2: Expected reward (small RPE)
    print(f"\n🎯 Trial 2: Expected reward")
    rpe, signal = dopamine.process_event(
        context_id=context,
        actual_reward=1.0,
        novelty_score=0.2
    )
    print(f"  RPE: {rpe:+.3f} (should be smaller)")
    print(f"  Dopamine: {signal.level:.3f}")
    print(f"  Expected value learned: {dopamine.predictor.get_expected_value(context):.3f}")

    # Trial 3: Reward omission (negative RPE)
    print(f"\n🎯 Trial 3: Expected but no reward")
    rpe, signal = dopamine.process_event(
        context_id=context,
        actual_reward=0.0,
        novelty_score=0.0
    )
    print(f"  RPE: {rpe:+.3f} (negative)")
    print(f"  Dopamine: {signal.level:.3f} (dip below baseline)")

    # Show final statistics
    print(f"\n📈 Final Statistics:")
    stats = dopamine.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_013 Test Complete!")
