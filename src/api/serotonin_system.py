"""
LAB_014: Serotonin System - Mood Regulation & Impulse Control

Implements serotonergic signaling based on:
- Cools et al. (2008): Serotonin and aversive processing
- Dayan & Huys (2009): Serotonin and time horizons
- Carver & Miller (2006): Serotonin and behavioral inhibition

Core Functions:
1. Mood state regulation (positive/negative affect)
2. Impulse control (delay gratification)
3. Aversive prediction (future threat/punishment)
4. Time horizon modulation (patience)
5. Social hierarchy processing

Neuroscience Foundation:
- Raphe nuclei: Serotonin production
- PFC: Impulse control, decision-making
- Amygdala: Aversive processing
- Striatum: Reward/punishment balance

Key Role: Balance optimism/pessimism, control impulsivity, manage time horizons
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class MoodState(Enum):
    """Current mood/affective state"""
    DEPRESSED = "depressed"      # Low serotonin
    NEUTRAL = "neutral"           # Baseline
    ELEVATED = "elevated"         # High serotonin
    MANIC = "manic"              # Excessive (pathological)


class ImpulseControl(Enum):
    """Level of behavioral inhibition"""
    IMPULSIVE = "impulsive"      # Low control
    MODERATE = "moderate"         # Normal
    RIGID = "rigid"              # Over-controlled


@dataclass
class SerotoninSignal:
    """Serotonin release/activity event"""
    timestamp: float
    level: float  # 0-1 normalized
    source: str
    mood_effect: float  # Impact on mood
    control_effect: float  # Impact on impulse control


@dataclass
class AversivePrediction:
    """Predicted future negative outcome"""
    context_id: str
    aversion_value: float  # Expected negativity (0-1)
    time_horizon: float  # When expected (seconds)
    confidence: float
    last_updated: float


@dataclass
class ImpulseEvent:
    """Record of an impulsive vs controlled decision"""
    timestamp: float
    context_id: str
    immediate_reward: float
    delayed_reward: float
    delay_duration: float
    choice: str  # "immediate" or "delayed"
    serotonin_level: float


class TimeHorizonManager:
    """
    Manages time horizons for planning and decision-making.
    Higher serotonin → longer time horizons → more patience
    Lower serotonin → shorter horizons → impulsivity
    """

    def __init__(self, base_horizon: float = 30.0):
        self.base_horizon = base_horizon  # Seconds

    def compute_effective_horizon(self, serotonin_level: float) -> float:
        """
        Compute effective planning horizon based on serotonin.

        Low serotonin → short horizon (impulsive)
        High serotonin → long horizon (patient)
        """
        # Serotonin (0-1) modulates horizon (0.5x to 2x base)
        multiplier = 0.5 + (serotonin_level * 1.5)

        return self.base_horizon * multiplier

    def discount_delayed_reward(
        self,
        reward_value: float,
        delay_seconds: float,
        serotonin_level: float
    ) -> float:
        """
        Compute subjective value of delayed reward.

        Hyperbolic discounting modulated by serotonin:
        V = R / (1 + k*D)

        where k (discount rate) is inversely related to serotonin
        """
        # Lower serotonin → higher k → steeper discounting (impatient)
        # Higher serotonin → lower k → shallower discounting (patient)
        k = 0.1 / (serotonin_level + 0.1)  # Discount rate

        discounted_value = reward_value / (1.0 + k * delay_seconds)

        return discounted_value


class AversiveProcessor:
    """
    Processes and predicts aversive/negative outcomes.
    High serotonin → less reactive to threat
    Low serotonin → hypervigilant to negative
    """

    def __init__(self):
        self.aversive_predictions: Dict[str, AversivePrediction] = {}
        self.recent_aversive_events: deque = deque(maxlen=100)

    def predict_aversion(
        self,
        context_id: str,
        features: Dict[str, float]
    ) -> float:
        """
        Predict aversive value for a context.

        Features might include:
        - uncertainty
        - social rejection risk
        - punishment history
        - threat signals
        """
        # Simple weighted combination for now
        aversion = 0.0

        if "uncertainty" in features:
            aversion += features["uncertainty"] * 0.3

        if "social_rejection_risk" in features:
            aversion += features["social_rejection_risk"] * 0.4

        if "punishment_history" in features:
            aversion += features["punishment_history"] * 0.3

        # Cap at 1.0
        aversion = min(1.0, aversion)

        return aversion

    def update_prediction(
        self,
        context_id: str,
        actual_aversion: float,
        predicted_aversion: float
    ):
        """Update aversive predictions based on outcomes"""
        prediction_error = actual_aversion - predicted_aversion

        # Store event
        self.recent_aversive_events.append({
            "timestamp": time.time(),
            "context_id": context_id,
            "actual": actual_aversion,
            "predicted": predicted_aversion,
            "error": prediction_error
        })

        # Update or create prediction
        if context_id in self.aversive_predictions:
            pred = self.aversive_predictions[context_id]
            # Adjust prediction based on error
            pred.aversion_value += 0.1 * prediction_error
            pred.aversion_value = max(0.0, min(1.0, pred.aversion_value))
            pred.last_updated = time.time()
        else:
            self.aversive_predictions[context_id] = AversivePrediction(
                context_id=context_id,
                aversion_value=actual_aversion,
                time_horizon=0.0,
                confidence=0.3,
                last_updated=time.time()
            )


class SerotoninSystem:
    """
    Main LAB_014 implementation.

    Manages serotonergic signaling including:
    - Mood state regulation
    - Impulse control / behavioral inhibition
    - Time horizon modulation
    - Aversive prediction and processing
    - Social hierarchy responses
    """

    def __init__(
        self,
        baseline_serotonin: float = 0.6,
        mood_sensitivity: float = 0.5,
        control_threshold: float = 0.5
    ):
        # Core parameters
        self.baseline_serotonin = baseline_serotonin
        self.mood_sensitivity = mood_sensitivity
        self.control_threshold = control_threshold

        # Current state
        self.current_serotonin = baseline_serotonin
        self.current_mood = MoodState.NEUTRAL
        self.last_update_time = time.time()

        # Components
        self.time_horizon_manager = TimeHorizonManager()
        self.aversive_processor = AversiveProcessor()

        # History
        self.signal_history: deque = deque(maxlen=1000)
        self.impulse_history: deque = deque(maxlen=500)

        # Statistics
        self.total_impulse_tests = 0
        self.controlled_choices = 0
        self.impulsive_choices = 0

    def process_reward_event(
        self,
        reward_value: float,
        social_context: bool = False
    ) -> SerotoninSignal:
        """
        Process reward event and adjust serotonin.

        Positive outcomes → serotonin increase
        Negative outcomes → serotonin decrease
        Social rewards → stronger effect
        """
        # Social context amplifies effect
        multiplier = 1.5 if social_context else 1.0

        # Reward affects serotonin (slow, gradual change)
        serotonin_delta = reward_value * 0.1 * multiplier

        # Update serotonin (bounded 0-1)
        self.current_serotonin += serotonin_delta
        self.current_serotonin = max(0.0, min(1.0, self.current_serotonin))

        # Update mood
        self._update_mood()

        # Create signal
        signal = SerotoninSignal(
            timestamp=time.time(),
            level=self.current_serotonin,
            source="reward_event",
            mood_effect=serotonin_delta * self.mood_sensitivity,
            control_effect=serotonin_delta * 0.5
        )

        self.signal_history.append(signal)
        self.last_update_time = time.time()

        return signal

    def process_aversive_event(
        self,
        aversion_value: float,
        social_context: bool = False
    ) -> SerotoninSignal:
        """
        Process aversive/negative event.

        Negative outcomes → serotonin decrease
        Social rejection → stronger effect
        """
        multiplier = 1.5 if social_context else 1.0

        # Aversive events decrease serotonin
        serotonin_delta = -aversion_value * 0.15 * multiplier

        self.current_serotonin += serotonin_delta
        self.current_serotonin = max(0.0, min(1.0, self.current_serotonin))

        self._update_mood()

        signal = SerotoninSignal(
            timestamp=time.time(),
            level=self.current_serotonin,
            source="aversive_event",
            mood_effect=serotonin_delta * self.mood_sensitivity,
            control_effect=serotonin_delta * 0.3
        )

        self.signal_history.append(signal)
        self.last_update_time = time.time()

        return signal

    def _update_mood(self):
        """Update mood state based on current serotonin"""
        if self.current_serotonin < 0.3:
            self.current_mood = MoodState.DEPRESSED
        elif self.current_serotonin < 0.5:
            self.current_mood = MoodState.NEUTRAL
        elif self.current_serotonin < 0.8:
            self.current_mood = MoodState.ELEVATED
        else:
            self.current_mood = MoodState.MANIC

    def impulse_control_test(
        self,
        context_id: str,
        immediate_reward: float,
        delayed_reward: float,
        delay_seconds: float
    ) -> Tuple[str, ImpulseEvent]:
        """
        Test impulse control: immediate vs delayed gratification.

        Returns choice ("immediate" or "delayed") and event record.
        """
        # Compute subjective value of delayed reward
        delayed_value = self.time_horizon_manager.discount_delayed_reward(
            delayed_reward,
            delay_seconds,
            self.current_serotonin
        )

        # Compare immediate vs discounted delayed
        if delayed_value > immediate_reward:
            choice = "delayed"
            self.controlled_choices += 1
        else:
            choice = "immediate"
            self.impulsive_choices += 1

        self.total_impulse_tests += 1

        # Record event
        event = ImpulseEvent(
            timestamp=time.time(),
            context_id=context_id,
            immediate_reward=immediate_reward,
            delayed_reward=delayed_reward,
            delay_duration=delay_seconds,
            choice=choice,
            serotonin_level=self.current_serotonin
        )

        self.impulse_history.append(event)

        return choice, event

    def get_impulse_control_level(self) -> str:
        """Get current impulse control classification"""
        if self.current_serotonin < 0.3:
            return ImpulseControl.IMPULSIVE.value
        elif self.current_serotonin < 0.7:
            return ImpulseControl.MODERATE.value
        else:
            return ImpulseControl.RIGID.value

    def get_mood_bias(self) -> float:
        """
        Get mood-related cognitive bias.

        Low serotonin → negative bias (pessimistic)
        High serotonin → positive bias (optimistic)

        Returns value from -1 (very negative) to +1 (very positive)
        """
        # Map serotonin (0-1) to bias (-1 to +1)
        bias = (self.current_serotonin - 0.5) * 2.0

        return bias

    def get_patience_level(self) -> float:
        """
        Get current patience/time horizon.

        Low serotonin → impatient
        High serotonin → patient
        """
        return self.current_serotonin

    def regulate_serotonin(self, target_delta: float):
        """
        Simulate serotonin regulation (e.g., via SSRIs, lifestyle).
        This would be called by homeostatic systems.
        """
        self.current_serotonin += target_delta
        self.current_serotonin = max(0.0, min(1.0, self.current_serotonin))
        self._update_mood()

    def get_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        return {
            "baseline_serotonin": self.baseline_serotonin,
            "current_serotonin": self.current_serotonin,
            "mood_state": self.current_mood.value,
            "impulse_control": self.get_impulse_control_level(),
            "mood_bias": self.get_mood_bias(),
            "patience_level": self.get_patience_level(),
            "total_impulse_tests": self.total_impulse_tests,
            "controlled_choices": self.controlled_choices,
            "impulsive_choices": self.impulsive_choices,
            "control_rate": (
                self.controlled_choices / self.total_impulse_tests
                if self.total_impulse_tests > 0 else 0.0
            ),
            "time_horizon_seconds": self.time_horizon_manager.compute_effective_horizon(
                self.current_serotonin
            ),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_014: Serotonin System - Test")
    print("=" * 60)

    # Create serotonin system
    serotonin = SerotoninSystem(
        baseline_serotonin=0.6,
        mood_sensitivity=0.5,
        control_threshold=0.5
    )

    print("\n📊 Initial State:")
    stats = serotonin.get_statistics()
    print(f"  Serotonin: {stats['current_serotonin']:.3f}")
    print(f"  Mood: {stats['mood_state']}")
    print(f"  Impulse Control: {stats['impulse_control']}")
    print(f"  Mood Bias: {stats['mood_bias']:+.3f}")

    # Scenario 1: Positive reward (social context)
    print("\n🎉 Processing positive social reward...")
    signal = serotonin.process_reward_event(reward_value=0.8, social_context=True)
    print(f"  Serotonin: {signal.level:.3f}")
    print(f"  Mood Effect: {signal.mood_effect:+.3f}")
    print(f"  New Mood: {serotonin.current_mood.value}")

    # Scenario 2: Impulse control test (with elevated serotonin)
    print("\n⏳ Impulse Control Test (elevated serotonin):")
    choice, event = serotonin.impulse_control_test(
        context_id="test_1",
        immediate_reward=1.0,
        delayed_reward=2.0,
        delay_seconds=10.0
    )
    print(f"  Choice: {choice}")
    print(f"  Patience: {serotonin.get_patience_level():.3f}")

    # Scenario 3: Series of negative events (simulate stress/rejection)
    print("\n😔 Processing negative events (social rejection)...")
    for i in range(3):
        signal = serotonin.process_aversive_event(aversion_value=0.6, social_context=True)
    print(f"  Serotonin: {signal.level:.3f}")
    print(f"  Mood: {serotonin.current_mood.value}")
    print(f"  Mood Bias: {serotonin.get_mood_bias():+.3f}")

    # Scenario 4: Impulse control test (with depleted serotonin)
    print("\n⚡ Impulse Control Test (depleted serotonin):")
    choice, event = serotonin.impulse_control_test(
        context_id="test_2",
        immediate_reward=1.0,
        delayed_reward=2.0,
        delay_seconds=10.0
    )
    print(f"  Choice: {choice} (likely impulsive)")
    print(f"  Patience: {serotonin.get_patience_level():.3f}")
    print(f"  Control: {serotonin.get_impulse_control_level()}")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = serotonin.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_014 Test Complete!")
