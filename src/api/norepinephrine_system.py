"""
LAB_015: Norepinephrine System - Arousal, Alertness & Stress Response

Implements noradrenergic signaling based on:
- Aston-Jones & Cohen (2005): Locus coeruleus and adaptive gain theory
- Sara (2009): Norepinephrine and behavioral flexibility
- Arnsten (2009): Stress and prefrontal cortex function

Core Functions:
1. Arousal/alertness regulation
2. Stress response (fight-or-flight)
3. Signal-to-noise ratio modulation
4. Behavioral flexibility (task switching)
5. Encoding enhancement (emotional memories)

Neuroscience Foundation:
- Locus Coeruleus (LC): Main norepinephrine source
- PFC: Executive function under stress
- Amygdala: Emotional memory consolidation
- Hippocampus: Stress-enhanced encoding

Inverted-U Function:
- Too low NE → drowsy, inattentive
- Optimal NE → alert, focused
- Too high NE → anxious, distractible
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class ArousalState(Enum):
    """Current arousal/alertness level"""
    DROWSY = "drowsy"          # Very low NE
    RELAXED = "relaxed"        # Low NE
    ALERT = "alert"            # Optimal NE
    VIGILANT = "vigilant"      # High NE
    STRESSED = "stressed"      # Very high NE (pathological)


class LCMode(Enum):
    """Locus Coeruleus firing modes (Aston-Jones & Cohen)"""
    TONIC = "tonic"      # Baseline, task-disengaged
    PHASIC = "phasic"    # Task-engaged, responsive to salient events


@dataclass
class NorepinephrineSignal:
    """NE release event"""
    timestamp: float
    level: float  # 0-1 normalized
    mode: LCMode
    source: str
    arousal_effect: float
    encoding_boost: float


@dataclass
class StressEvent:
    """Record of stressor and response"""
    timestamp: float
    stressor_type: str
    intensity: float  # 0-1
    duration: float  # seconds
    ne_response: float
    behavioral_response: str  # "freeze", "fight", "flight", "fawn"


@dataclass
class PerformanceMetrics:
    """Task performance under different NE levels"""
    timestamp: float
    ne_level: float
    task_difficulty: float
    performance_score: float
    reaction_time: float
    error_rate: float


class YerkesDodsonCurve:
    """
    Models the inverted-U relationship between arousal and performance.

    Low arousal → poor performance (drowsy)
    Optimal arousal → peak performance
    High arousal → degraded performance (anxiety)
    """

    def __init__(self, optimal_arousal: float = 0.6):
        self.optimal_arousal = optimal_arousal

    def compute_performance_multiplier(
        self,
        current_arousal: float,
        task_difficulty: float = 0.5
    ) -> float:
        """
        Compute performance multiplier based on arousal.

        Task difficulty shifts optimal arousal:
        - Easy tasks → higher optimal arousal
        - Hard tasks → lower optimal arousal
        """
        # Adjust optimal based on task difficulty
        # Harder tasks need lower arousal (Yerkes-Dodson)
        adjusted_optimal = self.optimal_arousal - (task_difficulty * 0.2)

        # Inverted-U curve using Gaussian
        distance_from_optimal = abs(current_arousal - adjusted_optimal)

        # Peak at optimal, drops off with distance
        multiplier = np.exp(-(distance_from_optimal ** 2) / 0.2)

        return multiplier

    def compute_cognitive_flexibility(self, arousal: float) -> float:
        """
        Moderate arousal → high flexibility
        Extreme arousal → rigid/perseverative
        """
        # Similar inverted-U, but optimal around 0.5
        distance_from_moderate = abs(arousal - 0.5)

        flexibility = np.exp(-(distance_from_moderate ** 2) / 0.15)

        return flexibility


class StressResponseSystem:
    """
    Manages acute and chronic stress responses.

    Acute stress → NE surge → enhanced performance (short-term)
    Chronic stress → NE dysregulation → impaired function
    """

    def __init__(self):
        self.stress_history: deque = deque(maxlen=1000)
        self.chronic_stress_level = 0.0
        self.last_stressor_time = time.time()

        # Allostatic load (cumulative stress burden)
        self.allostatic_load = 0.0

    def process_stressor(
        self,
        stressor_type: str,
        intensity: float,
        duration: float = 5.0
    ) -> Tuple[float, StressEvent]:
        """
        Process acute stressor and compute NE response.

        Returns NE surge magnitude and stress event record.
        """
        # NE response proportional to stressor intensity
        ne_surge = intensity * 0.8

        # Determine behavioral response based on intensity and type
        if intensity < 0.3:
            response = "freeze"  # Low threat, assess
        elif intensity < 0.6:
            response = "fight"   # Moderate, confront
        elif intensity < 0.8:
            response = "flight"  # High, escape
        else:
            response = "fawn"    # Overwhelming, appease

        # Create stress event
        event = StressEvent(
            timestamp=time.time(),
            stressor_type=stressor_type,
            intensity=intensity,
            duration=duration,
            ne_response=ne_surge,
            behavioral_response=response
        )

        self.stress_history.append(event)
        self.last_stressor_time = time.time()

        # Update chronic stress and allostatic load
        self._update_chronic_stress(intensity, duration)

        return ne_surge, event

    def _update_chronic_stress(self, intensity: float, duration: float):
        """Update chronic stress level and allostatic load"""
        # Add to allostatic load
        load_increment = intensity * (duration / 60.0)  # Normalize by minutes
        self.allostatic_load += load_increment

        # Decay allostatic load over time (recovery)
        time_since_last = time.time() - self.last_stressor_time
        recovery_rate = 0.1  # Per hour
        recovery = (time_since_last / 3600.0) * recovery_rate
        self.allostatic_load = max(0.0, self.allostatic_load - recovery)

        # Chronic stress is smoothed allostatic load
        self.chronic_stress_level = min(1.0, self.allostatic_load / 10.0)

    def get_stress_vulnerability(self) -> float:
        """
        Get current vulnerability to stress (0-1).

        High allostatic load → high vulnerability (less resilient)
        """
        return self.chronic_stress_level


class NorepinephrineSystem:
    """
    Main LAB_015 implementation.

    Manages noradrenergic signaling including:
    - Tonic vs phasic LC firing modes
    - Arousal/alertness regulation
    - Stress response
    - Performance modulation (Yerkes-Dodson)
    - Encoding enhancement for emotional/stressful events
    """

    def __init__(
        self,
        baseline_ne: float = 0.4,
        lc_gain: float = 1.5,
        stress_threshold: float = 0.7
    ):
        # Core parameters
        self.baseline_ne = baseline_ne  # Tonic level
        self.lc_gain = lc_gain  # Phasic response gain
        self.stress_threshold = stress_threshold

        # Current state
        self.current_ne = baseline_ne
        self.current_arousal = ArousalState.RELAXED
        self.lc_mode = LCMode.TONIC
        self.last_update_time = time.time()

        # Components
        self.yerkes_dodson = YerkesDodsonCurve(optimal_arousal=0.6)
        self.stress_system = StressResponseSystem()

        # History
        self.signal_history: deque = deque(maxlen=1000)
        self.performance_history: deque = deque(maxlen=500)

        # Statistics
        self.total_phasic_events = 0
        self.total_stress_events = 0

    def process_salient_event(
        self,
        salience: float,
        emotional_valence: float = 0.0,
        is_stressor: bool = False
    ) -> NorepinephrineSignal:
        """
        Process salient event (surprise, novelty, threat).

        High salience → phasic NE burst
        Negative valence + high salience → stress response
        """
        # Phasic NE response to salience
        phasic_ne = salience * self.lc_gain

        # Emotional content amplifies
        emotion_multiplier = 1.0 + abs(emotional_valence) * 0.5

        effective_ne = phasic_ne * emotion_multiplier

        # If stressor, engage stress system
        if is_stressor:
            stress_surge, stress_event = self.stress_system.process_stressor(
                stressor_type="salient_event",
                intensity=salience,
                duration=5.0
            )
            effective_ne += stress_surge
            self.total_stress_events += 1

        # Update NE level (bounded 0-1)
        self.current_ne = min(1.0, self.baseline_ne + effective_ne)

        # Update LC mode
        if effective_ne > 0.3:
            self.lc_mode = LCMode.PHASIC
            self.total_phasic_events += 1
        else:
            self.lc_mode = LCMode.TONIC

        # Update arousal state
        self._update_arousal()

        # Compute encoding boost (emotional memories)
        # High NE + emotional valence → strong encoding
        encoding_boost = self.current_ne * (0.5 + abs(emotional_valence) * 0.5)

        # Create signal
        signal = NorepinephrineSignal(
            timestamp=time.time(),
            level=self.current_ne,
            mode=self.lc_mode,
            source="salient_event",
            arousal_effect=effective_ne,
            encoding_boost=encoding_boost
        )

        self.signal_history.append(signal)
        self.last_update_time = time.time()

        return signal

    def _update_arousal(self):
        """Update arousal state based on current NE"""
        if self.current_ne < 0.2:
            self.current_arousal = ArousalState.DROWSY
        elif self.current_ne < 0.4:
            self.current_arousal = ArousalState.RELAXED
        elif self.current_ne < 0.7:
            self.current_arousal = ArousalState.ALERT
        elif self.current_ne < 0.85:
            self.current_arousal = ArousalState.VIGILANT
        else:
            self.current_arousal = ArousalState.STRESSED

    def get_current_ne(self) -> float:
        """
        Get current NE with decay applied.
        Phasic NE decays back to tonic baseline.
        """
        elapsed = time.time() - self.last_update_time

        # Fast decay (NE cleared quickly)
        decay_rate = 0.3  # Half-life ~2.3 seconds

        delta_from_baseline = self.current_ne - self.baseline_ne
        decayed_delta = delta_from_baseline * np.exp(-decay_rate * elapsed)

        current = self.baseline_ne + decayed_delta

        return current

    def compute_task_performance(
        self,
        task_difficulty: float,
        baseline_performance: float = 0.8
    ) -> PerformanceMetrics:
        """
        Compute task performance based on current NE (Yerkes-Dodson).

        Returns performance metrics.
        """
        current_ne = self.get_current_ne()

        # Performance multiplier from Yerkes-Dodson
        multiplier = self.yerkes_dodson.compute_performance_multiplier(
            current_arousal=current_ne,
            task_difficulty=task_difficulty
        )

        # Final performance
        performance = baseline_performance * multiplier

        # Reaction time: optimal NE → fastest
        # Too low or too high → slower
        base_rt = 500  # ms
        rt_multiplier = 2.0 - multiplier  # Inverse
        reaction_time = base_rt * rt_multiplier

        # Error rate: inversely related to performance
        error_rate = 1.0 - performance

        # Create metrics
        metrics = PerformanceMetrics(
            timestamp=time.time(),
            ne_level=current_ne,
            task_difficulty=task_difficulty,
            performance_score=performance,
            reaction_time=reaction_time,
            error_rate=error_rate
        )

        self.performance_history.append(metrics)

        return metrics

    def get_encoding_boost(self, emotional_intensity: float = 0.5) -> float:
        """
        Get current memory encoding boost.

        High NE + emotion → strong encoding (flashbulb memories)
        """
        current_ne = self.get_current_ne()

        # NE level + emotional intensity
        boost = current_ne * (0.5 + emotional_intensity * 0.5)

        # Cap at 2x baseline encoding
        boost = min(2.0, boost)

        return boost

    def get_cognitive_flexibility(self) -> float:
        """
        Get current cognitive flexibility (task switching).

        Moderate NE → flexible
        High/low NE → rigid
        """
        current_ne = self.get_current_ne()

        return self.yerkes_dodson.compute_cognitive_flexibility(current_ne)

    def get_signal_to_noise_ratio(self) -> float:
        """
        Get neural signal-to-noise ratio.

        Moderate NE → high SNR (focused)
        Low NE → low SNR (drowsy)
        High NE → low SNR (distractible)
        """
        # Similar to performance, inverted-U
        current_ne = self.get_current_ne()

        optimal_ne = 0.6
        distance = abs(current_ne - optimal_ne)

        snr = np.exp(-(distance ** 2) / 0.25)

        return snr

    def regulate_baseline(self, delta: float):
        """
        Adjust baseline NE (e.g., via sleep, exercise, chronic stress).
        """
        self.baseline_ne += delta
        self.baseline_ne = max(0.0, min(1.0, self.baseline_ne))

    def get_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        current_ne = self.get_current_ne()

        return {
            "baseline_ne": self.baseline_ne,
            "current_ne": current_ne,
            "arousal_state": self.current_arousal.value,
            "lc_mode": self.lc_mode.value,
            "total_phasic_events": self.total_phasic_events,
            "total_stress_events": self.total_stress_events,
            "chronic_stress_level": self.stress_system.chronic_stress_level,
            "allostatic_load": self.stress_system.allostatic_load,
            "cognitive_flexibility": self.get_cognitive_flexibility(),
            "signal_to_noise_ratio": self.get_signal_to_noise_ratio(),
            "encoding_boost": self.get_encoding_boost(),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_015: Norepinephrine System - Test")
    print("=" * 60)

    # Create NE system
    ne_system = NorepinephrineSystem(
        baseline_ne=0.4,
        lc_gain=1.5,
        stress_threshold=0.7
    )

    print("\n📊 Initial State:")
    stats = ne_system.get_statistics()
    print(f"  NE Level: {stats['current_ne']:.3f}")
    print(f"  Arousal: {stats['arousal_state']}")
    print(f"  LC Mode: {stats['lc_mode']}")

    # Scenario 1: Moderate salient event (optimal)
    print("\n⚡ Processing moderate salient event...")
    signal = ne_system.process_salient_event(salience=0.6, emotional_valence=0.3)
    print(f"  NE Level: {signal.level:.3f}")
    print(f"  Arousal: {ne_system.current_arousal.value}")
    print(f"  LC Mode: {signal.mode.value}")
    print(f"  Encoding Boost: {signal.encoding_boost:.3f}x")

    # Test performance at optimal arousal
    print("\n📈 Task Performance (optimal arousal):")
    metrics = ne_system.compute_task_performance(task_difficulty=0.5)
    print(f"  Performance: {metrics.performance_score:.3f}")
    print(f"  Reaction Time: {metrics.reaction_time:.0f}ms")
    print(f"  Error Rate: {metrics.error_rate:.3f}")

    # Scenario 2: High stress event
    print("\n😰 Processing high-stress event...")
    signal = ne_system.process_salient_event(
        salience=0.9,
        emotional_valence=-0.8,
        is_stressor=True
    )
    print(f"  NE Level: {signal.level:.3f} (surge)")
    print(f"  Arousal: {ne_system.current_arousal.value}")
    print(f"  Encoding Boost: {signal.encoding_boost:.3f}x (flashbulb memory)")

    # Test performance under stress
    print("\n📉 Task Performance (high arousal/stress):")
    metrics = ne_system.compute_task_performance(task_difficulty=0.5)
    print(f"  Performance: {metrics.performance_score:.3f} (degraded)")
    print(f"  Reaction Time: {metrics.reaction_time:.0f}ms (slower)")
    print(f"  Error Rate: {metrics.error_rate:.3f} (higher)")

    # Wait for NE to decay
    print("\n⏳ Waiting for NE decay...")
    time.sleep(2)
    current_ne = ne_system.get_current_ne()
    print(f"  NE Level: {current_ne:.3f} (decayed toward baseline)")

    # Show final statistics
    print("\n📊 Final Statistics:")
    stats = ne_system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_015 Test Complete!")
